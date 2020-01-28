# README

## Code Quality

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Netsach/concrete-mailer/Check%20Bandit?label=security)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Netsach/concrete-mailer/Check%20Black?label=black)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Netsach/concrete-mailer/Lint?label=lint)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/Netsach/concrete-mailer/Tests?label=tests)
![Codecov](https://img.shields.io/codecov/c/github/Netsach/concrete-mailer?logo=coedcov)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Python](https://img.shields.io/badge/python-2.7-3473A7?logo=python&logoColor=FED646)
![Python](https://img.shields.io/badge/python-3.6-3473A7?logo=python&logoColor=FED646)

## Description

:email: `concrete-mailer` is a python package for sending rich e-mails.

- It automatically embeds the linked image in email inline attachments.
- It avoids emails to end up in SPAM (applying best practices, with no guarantee)
- It automatically converts rich e-mails in plain-text format for receivers who have not enabled HTML format
- It allows sending e-mails with attachements
- It inlines CSS (no header in HTML e-mails)

:warning: It requires an SMTP server.

## Setup the environment

```shell
pip install concrete-mailer
```

## User Guide

`concrete-mailer` can be used in two ways:

### 1- Email Client (client.py)

```python
from concrete_mailer.client import EmailSenderClient
import os

#:  Define the smtp connexion variables in:
#:  SMTP_HOST_NAME, SMTP_HOST_PORT, SMTP_HOST_USER, SMTP_HOST_PASSWORD
client = EmailSenderClient(
    email_host=os.getenv('SMTP_HOST_NAME'),  #: smtp hostname
    email_port=os.getenv('SMTP_HOST_PORT'),  #: smtp host port
    email_host_user=os.getenv('SMTP_HOST_USER'),  #: smtp host username
    email_host_password=os.getenv('SMTP_HOST_PASSWORD'),  #: smtp host password
)

for name, email in (('John', 'john@mail.ext'), ('Jane', 'jane@mail.ext')):
    client.send(
        context={'name': name},
        template='''
            <h1>Concrete Mailer</h1>
            <p>Hello {{name}}. Welcome to README</p>
            <img src="/path/to/image1.jpg">
        ''',
        title='README',
        dests=[email, 'cc@netsach.org'],
        sender_name='Netsach',
        sender_email='sender@netsach.org',
        reply_to='contact@netsach.org',
        attachments=['/path/to/file.zip', '/path/to/image2.png'],
    )
```

`send` method returns:

- `True` if the email is successfully sent.
- `False` if a problem has occured.

### 2- Email preparers (preparer.py)
```python
from concrete_mailer.utils.preparers import prepare_email
import os

#:  Define the smtp connexion variables in:
#:  SMTP_HOST_NAME, SMTP_HOST_PORT, SMTP_HOST_USER, SMTP_HOST_PASSWORD
for name, email in (('John', 'john@mail.ext'), ('Jane', 'jane@mail.ext')):
    email = prepare_email(
        context={'name': name},
        html='''
            <h1>Concrete Mailer</h1>
            <p>Hello {{name}}. Welcome to README</p>
            <img src="/path/to/image1.jpg">
        ''',
        title='README',
        css='',  #: extra css
        sender='Netsach <sender@netsach.org>',
        reply_to='contact@netsach.org',
        recipients=[email, 'cc@netsach.org'],
        attachments=['/path/to/file.zip', '/path/to/image2.png'],
        email_host=os.getenv('SMTP_HOST_NAME'),  #: smtp hostname
        email_port=os.getenv('SMTP_HOST_PORT'),  #: smtp host port
        email_host_user=os.getenv('SMTP_HOST_USER'),  #: smtp host username
        email_host_password=os.getenv('SMTP_HOST_PASSWORD'),  #: smtp host password
    )
    email.send()
```

`send` method returns:

- `True` if the email is successfully sent.
- `False` if a problem has occured.

### Debug

An additionnal `debug` kwargs (`False` by default) can be added with the following behaviour:

-  if `debug` is `False` (*default*), then the client will try to establish an smtp connection and send the email with the given options.
-  if `debug` is `True`, the email body will be displayed in console instead of being sent to destinations. No stmp connection will be established (dry-run)

