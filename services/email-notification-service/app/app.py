from fastapi import FastAPI
from pydantic import EmailStr
from .config import Config
from kombu import Connection, Exchange, Queue
from email_templates import handle_email_notification

app = FastAPI()


def send_email_notification(subject: str, body: str, email_to: EmailStr):
    with Connection(Config.rabbitmq) as conn:
        email_exchange = Exchange("email", type="direct")
        email_queue = Queue("email_queue", exchange=email_exchange, routing_key="email")

        with conn.Producer() as producer:
            producer.publish(
                {"subject": subject, "body": body, "email_to": email_to},
                exchange=email_exchange,
                routing_key="email",
            )


if __name__ == "__main__":
    handle_email_notification()
