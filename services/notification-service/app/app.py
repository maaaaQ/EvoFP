from kombu import Connection, Exchange, Producer, Queue
from .message_processing import process_message
from .config import Config
from kombu.utils import retry


rabbitmq_url = "amqp://guest:guest@localhost:5672//"
exchange_name = "notifications"
queue_name = "notifications"

with Connection(rabbitmq_url) as connection:
    channel = connection.channel()
    queue = channel.queue(queue_name)
    exchange = Exchange(exchange_name, type="direct")
    exchange.declare()
    producer = Producer(channel, exchange=exchange, routing_key=queue_name)

    def send_notification(body, email_to, message_properties):
        email_subject = "Уведомление"
        email_body = body.decode("utf-8")

        # Отправка письма через SMTP
        from smtplib import SMTP
        from email.mime.text import MIMEText
        from email.header import Header

        message = MIMEText(email_body, "plain", "utf-8")
        message["Subject"] = Header(email_subject, "utf-8")
        message["From"] = Config.smtp_user
        message["To"] = email_to

        with SMTP(Config.smtp_host, Config.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(Config.smtp_user, Config.smtp_pass)
            smtp.sendmail(Config.smtp_user, email_to, message.as_string())

    def process_message(body, message):
        send_notification(body, message.properties)
        message.ack()

    with connection.Consumer(queue, callbacks=[process_message]) as consumer:
        while True:
            try:
                connection.drain_events(timeout=2)
            except retry.OperationalError:
                continue
