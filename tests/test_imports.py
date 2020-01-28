# coding: utf-8
from unittest import TestCase


class TestImports(TestCase):
    def test_imports(self):
        from concrete_mailer.client import EmailSenderClient
        from concrete_mailer.preparers import prepare_email
        from concrete_mailer.utils import (
            EmailToSend,
            EmailToConsole,
            get_connection,
        )
