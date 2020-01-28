# coding: utf-8
import smtplib
import sys


def get_connection(host, port, sender_email, sender_password):
    s = smtplib.SMTP(host=host, port=port)
    s.starttls()
    s.login(sender_email, sender_password)
    return s


class EmailToConsole:
    def __init__(self, email, message, attachments=[], *args, **kwargs):
        self.email = email
        self.message = message
        self.attachments = attachments

    def send(self):
        sys.stdout.write("=" * 90)
        sys.stdout.write("\n")
        for key, value in self.email.items():
            sys.stdout.write('{key}: {value}\n'.format(key=key, value=value))
        sys.stdout.write("\n" * 3)
        if self.email.get('Subject'):
            sys.stdout.write("[{}]\n".format(self.email.get('Subject')))
            sys.stdout.write("\n")
        sys.stdout.write("{}\n".format(self.message))
        sys.stdout.write("=" * 90)
        sys.stdout.write("\n")
        return True


class EmailToSend:
    def __init__(self, connection, email, *args, **kwargs):
        self.connection = connection
        self.email = email

    def send(self):
        if self.connection is None:
            return False
        self.connection.sendmail(
            from_addr=self.connection.user,
            to_addrs=self.email['To'],
            msg=self.email.as_string(),
        )
        self.connection.quit()
        return True
