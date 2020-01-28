# coding: utf-8
from mock import patch
from unittest import TestCase
from concrete_mailer.client import EmailSenderClient
from smtplib import SMTPException


def fake_smtp_connection(with_exc_on_send=False):
    class FakeSmtpConnection:
        def __init__(self, *args, **kwargs):
            self.user = ''

        def quit(self):
            pass

        def sendmail(self, *args, **kwargs):
            if with_exc_on_send:
                raise SMTPException()
            pass

    return FakeSmtpConnection


class TestEmailClient(TestCase):
    def tearDown(self):
        patch.stopall()

    def test_success_send_mail(self):
        patch(
            'concrete_mailer.client.get_connection', new=fake_smtp_connection()
        ).start()
        client = EmailSenderClient()

        context = {'name': 'John Doe'}
        html = '<h1>Hello {{name}}</h1><p>Welcome to Concrete Mailer</p>'
        title = 'Hello Email'
        sender = 'test@netsach.org'
        recipients = ['email1.netsach.org', 'email2.netsach.org']
        email_sent = client.send(
            context,
            html,
            title,
            dests=recipients,
            sender_name='Netsach',
            sender_email=sender,
        )
        self.assertTrue(email_sent)

    def test_failure_send_mail(self):
        patch(
            'concrete_mailer.client.get_connection',
            new=fake_smtp_connection(with_exc_on_send=True),
        ).start()
        client = EmailSenderClient()

        context = {'name': 'John Doe'}
        html = '<h1>Hello {{name}}</h1><p>Welcome to Concrete Mailer</p>'
        title = 'Hello Email'
        sender = 'test@netsach.org'
        recipients = ['email1.netsach.org', 'email2.netsach.org']

        email_sent = client.send(
            context,
            html,
            title,
            dests=recipients,
            sender_name='Netsach',
            sender_email=sender,
        )
        self.assertFalse(email_sent)
