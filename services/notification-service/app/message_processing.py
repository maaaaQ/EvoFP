from .config import Config
import smtplib
from kombu import Connection, Exchange, Queue


def send_email(to, subject, body):
    smtp_connection = smtplib.SMTP(Config.smtp_host, Config.smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(Config.smtp_user, Config.smtp_pass)

    message = f"Subject: {subject},{body}"
    smtp_connection.sendmail(Config.smtp_user, to, message)

    smtp_connection.quit()


def process_message(body, message):
    to = body["to"]
    subject = body["subject"]
    body = body["body"]

    send_email(to, subject, body)

    message.ack()


connection = Connection("amqp://guest:guest@localhost:5672/")


exchange = Exchange("my_exchange", type="direct")
queue = Queue("my_queue", exchange, routing_key="my_key")


queue.maybe_bind(connection)
queue.declare()

with connection.channel() as channel:
    queue.consume(process_message)

    while True:
        connection.drain_events()


connection.release()
