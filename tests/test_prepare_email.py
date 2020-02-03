# coding: utf-8
from mock import patch
from unittest import TestCase
from concrete_mailer.preparers import prepare_email
from concrete_mailer.utils import EmailToSend, get_connection
from smtplib import SMTPException


class FakeSmtpConnection:
    def __init__(self, *args, **kwargs):
        self.user = ''

    def quit(self):
        pass

    def sendmail(self, *args, **kwargs):
        pass


class TestSendEmail(TestCase):
    def tearDown(self):
        patch.stopall()

    def test_success_send_mail(self):
        context = {'name': 'John Doe'}
        html = '<h1>Hello {{name}}</h1><p>Welcome to Concrete Mailer</p>'
        title = 'Hello Email'
        sender = 'test@netsach.org'
        recipients = ['email1.netsach.org', 'email2.netsach.org']
        reply_to = 'support@netsach.org'
        patch(
            'concrete_mailer.preparers.get_connection', new=FakeSmtpConnection
        ).start()
        email = prepare_email(
            context, '', html, title, sender, recipients, reply_to
        )
        self.assertTrue(email.send())

    def test_failure_send_mail(self):
        context = {'name': 'John Doe'}
        html = '<h1>Hello {{name}}</h1><p>Welcome to Concrete Mailer</p>'
        title = 'Hello Email'
        sender = 'test@netsach.org'
        recipients = ['email1.netsach.org', 'email2.netsach.org']
        patch(
            'concrete_mailer.preparers.get_connection',
            side_effect=SMTPException,
        ).start()

        with self.assertRaises(SMTPException):
            prepare_email(context, '', html, title, sender, recipients)

    def test_failure_instanciate_mail(self):
        email = EmailToSend(
            connection=None,
            email=None
        )
        self.assertFalse(email.send())

    def test_get_connection(self):
        patch(
            'concrete_mailer.utils.SMTP',
        ).start()
        self.assertIsNotNone(
            get_connection(
                host=None,
                port=None,
                user=None,
                password=None
            )
        )
