from email.mime.multipart import MIMEMultipart
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


# def prepare_email_data(body, queue_name):
#     email_subject = ""
#     email_message = ""
#     match queue_name:
#         case "task_created":
#             email_subject = "Задача создана"
#             email_message = f"Новая задача создана с ID {body['id']}.\n Имя задачи: {body['title']}\n Приоритет: {body['priority']}\n Пользователь: {body['user_id']}"
#         case "user_registered":
#             email_subject = "Регистрация пользователя"
#             email_message = f"Пользователь {body['id']} успешно зарегистрирован.\nEmail: {body['email']}\nNickname: {body['nickname']}\n Имя: {body['first_name']}\nФамилия: {body['last_name']}"
#         case "comment_created":
#             email_subject = "Новый комментарий к задаче"
#             email_message = f"Пользователь {body['user_id']} оставил комментарий к задаче {body['task_id']}\nТекст комментария: {body['text']}"
#     return email_subject, email_message


class QueueConsumer(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        task_created_queue = Queue(
            "task_created",
            exchange=Exchange("tasks"),
            routing_key="task.created",
            channel=channel,
        )
        user_registered_queue = Queue(
            "user_registered",
            exchange=Exchange("registered"),
            routing_key="user.registered",
            channel=channel,
        )
        comment_created_queue = Queue(
            "comment_created",
            exchange=Exchange("comments"),
            routing_key="comment.created",
            channel=channel,
        )

        return [
            Consumer(task_created_queue, callbacks=[self.process_task_created]),
            Consumer(user_registered_queue, callbacks=[self.process_user_registered]),
            Consumer(comment_created_queue, callbacks=[self.process_comment_created]),
        ]

    def process_task_created(self, body, message):
        task_id = body.get("id")
        title = body.get("title")
        priority = body.get("priority")
        user_id = body.get("user_id")
        email = body.get("email")

        receiver_email = email
        email_subject = "Задача создана"
        email_message = f"Создана новая задача с ID {task_id}. Имя задачи: {title}. Приоритет: {priority}. Пользователь: {user_id}"
        self.send_email(receiver_email, email_subject, email_message)

        message.ack()

    def process_user_registered(self, body, message):
        user_id = body.get("id")
        email = body.get("email")
        nickname = body.get("nickname")
        first_name = body.get("first_name")
        last_name = body.get("last_name")

        receiver_email = email
        email_subject = "Регистрация пользователя"
        email_message = f"Пользователь {user_id} успешно зарегистрирован. Email: {email}. Nickname: {nickname}. Имя: {first_name}. Фамилия: {last_name}"
        self.send_email(receiver_email, email_subject, email_message)

        message.ack()

    def process_comment_created(self, body, message):
        user_id = body.get("user_id")
        task_id = body.get("task_id")
        comment_text = body.get("text")
        email = body.get("email")

        receiver_email = email
        email_subject = "Новый комментарий к задаче"
        email_message = f"Пользователь {user_id} оставил комментарий к задаче {task_id}. Текст комментария: {comment_text}."
        self.send_email(receiver_email, email_subject, email_message)

        message.ack()

    def send_email(self, receiver_email, email_subject, email_message):
        msg = MIMEMultipart()
        msg["Subject"] = email_subject
        msg["From"] = cfg.smtp_user
        msg["To"] = receiver_email
        msg.attach(MIMEText(email_message, "plain", "utf-8"))

        with smtplib.SMTP(cfg.smtp_host, cfg.smtp_port) as server:
            server.starttls()
            server.login(cfg.smtp_user, cfg.smtp_pass)
            server.sendmail(
                from_addr=cfg.smtp_user, to_addrs=receiver_email, msg=msg.as_string()
            )
            logger.info(f"Email sent to {receiver_email}")
            server.quit()


def monitor_queues():
    with Connection(cfg.rabbitmq.unicode_string()) as connection:
        consumer = QueueConsumer(connection)
        consumer.run()


def start_monitoring():
    monitor_queues()


process = multiprocessing.Process(target=start_monitoring)
process.start()
