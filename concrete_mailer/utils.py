# coding: utf-8
import sys
from smtplib import SMTP, SMTPException


def get_connection(host, port, user, password, use_tls=True):
    connection = SMTP(host=host, port=port)
    if use_tls:
        connection.starttls()
    #:  Some SMTP servers does not support authentication.
    #:  If login raises SMTPException do not block the connection.
    try:
        connection.login(user, password)
    except SMTPException as e:
        if sys.version_info.major == 3:
            mro = [c.__name__ for c in e.__class__.mro()]
            if 'SMTPNotSupportedError' not in mro:
                raise e
        pass
    return connection


class EmailToSend:
    def __init__(self, connection, email, *args, **kwargs):
        self.connection = connection
        self.email = email

    def send(self):
        if self.connection is None:
            return False
        self.connection.sendmail(
            from_addr=self.email['From'],
            to_addrs=self.email['To'],
            msg=self.email.as_string(),
        )
        self.connection.quit()
        return True
