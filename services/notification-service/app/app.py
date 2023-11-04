from kombu import Connection, Exchange, Producer, Queue
from . import config
import smtplib
from email.mime.text import MIMEText
from kombu.mixins import ConsumerMixin
import logging
from fastapi.logger import logger
from fastapi import FastAPI
import multiprocessing

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


cfg: config.Config = config.load_config()

# Загрузка конфигурации
logger.info(
    "Notification Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)


def send_email(receiver_email, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = cfg.smtp_user
    msg["To"] = receiver_email

    with smtplib.SMTP_SSL(cfg.smtp_host, cfg.smtp_port) as server:
        server.login(cfg.smtp_user, cfg.smtp_pass)
        server.sendmail(cfg.smtp_user, receiver_email, msg.as_string())
        server.quit()


class QueueConsumer(ConsumerMixin):
    def __init__(self, connection, queue_name):
        self.connection = connection
        self.queue_name = queue_name

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queue_name, callbacks=[self.process_message])]

    def process_message(self, body, message):
        if self.queue_name == "task_created":
            email_subject = "Задача создана"
            email_message = f"Новая задача создана с ID {body['id']}.\n Имя задачи: {body['title']}\n Приоритет: {body['priority']}\n Пользователь: {body['user_id']}"
            send_email(
                receiver_email=body["email"],
                subject=email_subject,
                message=email_message,
            )
        elif self.queue_name == "user_registered":
            email_subject = "Регистрация пользователя"
            email_message = f"Пользователь {body['id']} успешно зарегистрирован.\nEmail: {body['email']}\nNickname: {body['nickname']}\n Имя: {body['first_name']}\nФамилия: {body['last_name']}"
            send_email(
                receiver_email=body["email"],
                subject=email_subject,
                message=email_message,
            )
        elif self.queue_name == "comment_created":
            email_subject = "Добавлен комментарий"
            email_message = f"Пользователь {body['user_id']} добавил комментарий к вашей задаче {body['task_id']}.\n Текст комментария: {body['text']}.\n Номер комментария: {body['id']}"
            send_email(
                receiver_email=body["email"],
                subject=email_subject,
                message=email_message,
            )

        message.ack()


def monitor_queues():
    with Connection(cfg.rabbitmq) as connection:
        with connection.channel() as channel:
            task_created_queue = Queue(
                "task_created", Exchange("tasks"), routing_key="task.created"
            )
            user_registered_queue = Queue(
                "user_registered", Exchange("registered"), routing_key="user.registered"
            )
            comment_created_queue = Queue(
                "comment_created", Exchange("comments"), routing_key="comment.created"
            )

            task_created_consumer = QueueConsumer(connection, task_created_queue)
            user_registered_consumer = QueueConsumer(connection, user_registered_queue)
            comment_created_consumer = QueueConsumer(connection, comment_created_queue)

            task_created_consumer.run()
            user_registered_consumer.run()
            comment_created_consumer.run()


def start_monitoring():
    monitor_queues()


if __name__ == "__main__":
    process = multiprocessing.Process(target=start_monitoring)
    process.start()
