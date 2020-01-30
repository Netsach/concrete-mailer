# coding: utf-8
from unittest import TestCase


class TestImports(TestCase):
    def test_imports(self):
        from concrete_mailer.client import EmailSenderClient
        from concrete_mailer.preparers import prepare_email
        from concrete_mailer.utils import (
            EmailToSend,
            get_connection,
        )
        self.assertEqual(EmailSenderClient.__name__, 'EmailSenderClient')
        self.assertEqual(prepare_email.__name__, 'prepare_email')
        self.assertEqual(EmailToSend.__name__, 'EmailToSend')
        self.assertEqual(get_connection.__name__, 'get_connection')
