from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from . import config

cfg: config.Config = config.load_config()


class SendEmail:
    def __init__(self, smtp_user, smtp_pass, smtp_host, smtp_port):
        self.smtp_user = smtp_user
        self.smtp_pass = smtp_pass
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port

        self.server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        self.server.login(smtp_user, smtp_pass)

    def send_message(self, subject, message, receiver_email):
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = self.smtp_user
        msg["To"] = receiver_email

        msg.attach(MIMEText(message, "plain"))
        self.server.sendmail(self.smtp_user, receiver_email, msg.as_string())
