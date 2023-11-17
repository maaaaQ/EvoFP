from kombu import Connection, Exchange, Producer, Queue
from . import config, send_email

from kombu.mixins import ConsumerMixin
import logging
from fastapi.logger import logger
from fastapi import FastAPI

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


cfg: config.Config = config.load_config()

# Загрузка конфигурации
logger.info(
    "Notification Service configuration loaded:\n"
    + f"{cfg.model_dump_json(by_alias=True, indent=4)}"
)
send_email = send_email.SendEmail(
    smtp_user=cfg.smtp_user,
    smtp_pass=cfg.smtp_pass,
    smtp_host=cfg.smtp_host,
    smtp_port=cfg.smtp_port,
)


class QueueConsumer(ConsumerMixin):
    def __init__(self, connection, send_email):
        self.connection = connection
        self.send_email = send_email

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
            Consumer(task_created_queue, callbacks=[self.process_task_created_wrapper]),
            Consumer(
                user_registered_queue, callbacks=[self.process_user_registered_wrapper]
            ),
            Consumer(
                comment_created_queue, callbacks=[self.process_comment_created_wrapper]
            ),
        ]

    def process_task_created_wrapper(self, body, message):
        self.process_task_created(body, message)

    def process_user_registered_wrapper(self, body, message):
        self.process_user_registered(body, message)

    def process_comment_created_wrapper(self, body, message):
        self.process_comment_created(body, message)

    def process_task_created(self, body, message):
        task_id = body.get("id")
        title = body.get("title")
        priority = body.get("priority")
        user_id = body.get("user_id")
        email = body.get("email")

        receiver_email = email
        subject = "Задача создана"
        messages = f"Создана новая задача с ID {task_id}. Имя задачи: {title}. Приоритет: {priority}. Пользователь: {user_id}"
        self.send_email.send_message(subject, messages, receiver_email)
        message.ack()

    def process_user_registered(self, body, message):
        email = body.get("email")
        nickname = body.get("nickname")
        first_name = body.get("first_name")
        last_name = body.get("last_name")

        receiver_email = email
        subject = "Регистрация пользователя"
        messages = f"Пользователь {email} успешно зарегистрирован. Nickname: {nickname}. Имя: {first_name}. Фамилия: {last_name}"
        self.send_email.send_message(subject, messages, receiver_email)
        message.ack()

    def process_comment_created(self, body, message):
        user_id = body.get("user_id")
        task_id = body.get("tasks_id")
        comment_text = body.get("text")
        email = body.get("email")

        receiver_email = email
        subject = "Новый комментарий к задаче"
        messages = f"Пользователь {user_id} оставил комментарий к задаче {task_id}. Текст комментария: {comment_text}."
        self.send_email.send_message(subject, messages, receiver_email)
        message.ack()


def monitor_queues(send_email):
    with Connection(cfg.rabbitmq.unicode_string()) as connection:
        consumer = QueueConsumer(connection, send_email)
        consumer.run()


def start_monitoring():
    monitor_queues(send_email)


start_monitoring()
