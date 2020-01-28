# coding: utf-8
from __future__ import unicode_literals, absolute_import, print_function
import os
import sys
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import premailer
from io import StringIO
from bs4 import BeautifulSoup
import uuid
import requests
from smtplib import SMTPException
from jinja2.sandbox import SandboxedEnvironment
from concrete_mailer.utils import get_connection, EmailToSend, EmailToConsole

if sys.version_info.major == 3:  # python3
    unicode_type = str
elif sys.version_info.major == 2:  # python2
    unicode_type = unicode  # pylint: disable=undefined-variable

EMAIL_HTML_SQUELETON = """
<html>
    <head>
        <meta charset="utf-8">
        <title>{title}</title>
        <style type="text/css">
        {css}
        </style>
    </head>
    <body>
        {body}
    </body>
</html>
"""
logger = logging.getLogger('concrete-mailer')


def prepare_email_body(context, css, template, title):

    #:  Before template is rendered, we verify that its content is secure
    env = SandboxedEnvironment()
    body = env.from_string(template).render(context)

    mylog = StringIO()
    myhandler = logging.StreamHandler(mylog)
    html_message = EMAIL_HTML_SQUELETON.format(title=title, css=css, body=body)

    p = premailer.Premailer(
        html=html_message,
        cssutils_logging_handler=myhandler,
        cssutils_logging_level=logging.INFO,
    )

    return p.transform()


def _process_html_to_embed_image_in_email_header(
    email, message_html, equivalences_key_path={}
):

    if not isinstance(equivalences_key_path, dict):
        raise ValueError("equivalences_key_path should be a dict")

    soup = BeautifulSoup(message_html, "lxml")
    tags = soup.find_all('img')

    for tag in tags:
        if tag['src'].startswith('cid:'):
            # key will be override by uuid
            key = tag['src'].replace('cid:', '')
            if key not in equivalences_key_path.keys():
                raise ValueError(
                    '"{key}" not found in "equivalences_key_path" keys'.format(
                        key=key
                    )
                )
            path = equivalences_key_path.get(key)
        else:
            path = tag['src']

        uid = uuid.uuid4().hex
        tag['src'] = 'cid:{}'.format(uid)

        if path.startswith('http'):
            resp = requests.get(path, stream=True)
            if resp.status_code != 200:
                logger.info(
                    'Fail to open url {}: {}, continue...'.format(
                        path, resp.content
                    ),
                    exc_info=True,
                )
                continue
            image_content = resp.content

        else:
            if os.path.isfile(path):
                with open(path, 'rb') as fp:
                    image_content = fp.read()
            else:
                logger.info('{} is not a file, continue...'.format(path))
                continue

        mime_image = MIMEImage(image_content)
        mime_image.add_header('Content-ID', '<{}>'.format(uid))
        mime_image.add_header(
            'Content-Disposition', 'inline', filename=os.path.basename(path)
        )
        email.attach(mime_image)

    return unicode_type(soup)


def prepare_email(
    context,
    css,
    html,
    title,
    sender,
    recipients,
    reply_to=None,
    equivalences_key_path=None,
    smtp_connection=None,
    attachments=None,
    debug=False,
    email_host=None,
    email_port=None,
    email_host_user=None,
    email_host_password=None,
):
    if equivalences_key_path is None:
        equivalences_key_path = {}
    if reply_to is None:
        reply_to = sender

    EmailBackendClass = EmailToConsole if debug else EmailToSend

    if smtp_connection is None and debug is False:
        try:
            smtp_connection = get_connection(
                host=email_host,
                port=email_port,
                sender_email=email_host_user,
                sender_password=email_host_password,
            )
        except SMTPException as e:
            logger.info('Failed to establish connection: {}'.format(e))
            raise

    message = prepare_email_body(
        context=context, css=css, template=html, title=title
    )

    # Prepare mails
    email = MIMEMultipart()
    email['From'] = sender
    email['To'] = ", ".join(recipients)
    email['Subject'] = title
    email['reply-to'] = reply_to

    # detect image in html and attach in header of email
    message = _process_html_to_embed_image_in_email_header(
        email=email,
        message_html=message,
        equivalences_key_path=equivalences_key_path,
    )

    email.attach(MIMEText(message, 'html'))

    if attachments is None:
        return EmailBackendClass(
            connection=smtp_connection, email=email, message=message
        )
    if isinstance(attachments, (list, tuple)) is False:
        raise ValueError("Attachements should be a list or a tuple")
    for attachment in attachments:
        if os.path.isfile(attachment) is False:
            logger.info("No such file {}. Skipping ...".format(attachment))
            continue
        file = MIMEBase('application', "octet-stream")
        with open(attachment, 'rb') as fd:
            file.set_payload(fd.read())
        encoders.encode_base64(file)
        filename = os.path.basename(attachment)
        file.add_header(
            'Content-Disposition', 'attachment; filename="{}"'.format(filename)
        )

        email.attach(file)

    return EmailBackendClass(
        connection=smtp_connection,
        email=email,
        message=message,
        attachments=attachments,
    )
