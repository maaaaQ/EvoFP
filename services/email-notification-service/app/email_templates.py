from email.message import EmailMessage
from kombu import Connection, Exchange, Queue
from kombu.mixins import ConsumerMixin
from kombu.utils.url import parse_url
from smtplib import SMTP_SSL
from .config import Config
from pydantic import EmailStr


class EmailNotificationConsumer(ConsumerMixin):
    def __init__(self, connection: Connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        email_exchange = Exchange("email", type="direct")
        email_queue = Queue("email_queue", exchange=email_exchange, routing_key="email")

        return [Consumer(email_queue, callbacks=[self.on_email_notification])]

    def on_email_notification(self, body, message):
        subject = body["subject"]
        body = body["body"]
        email_to = body["email_to"]

        send_email(subject, body, email_to)

        message.ack()

    def handle_email_notification():
        with Connection(Config.rabbitmq) as conn:
            consumer = EmailNotificationConsumer(conn)
            consumer.run()


def send_email(subject: str, body: str, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = Config.smtp_user
    email["To"] = email_to

    email.set_content(body, subtype="html")

    with SMTP_SSL(Config.smtp_host, Config.smtp_port) as smtp:
        smtp.login(Config.smtp_user, Config.smtp_pass)
        smtp.send_message(email)
