# coding: utf-8
from smtplib import SMTP, SMTPNotSupportedError


def get_connection(host, port, user, password, use_tls=True):
    connection = SMTP(host=host, port=port)
    if use_tls:
        connection.starttls()
    #:  Some SMTP servers does not support authentication.
    #:  If login raises SMTPNotSupportedError do not block the connection.
    try:
        connection.login(user, password)
    except SMTPNotSupportedError:
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
