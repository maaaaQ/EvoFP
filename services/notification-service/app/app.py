from kombu import Connection, Exchange, Producer, Queue
from .config import Config
from smtplib import SMTP
from email.mime.text import MIMEText
from kombu.mixins import ConsumerMixin


def send_email(email_to, subject, message):
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = Config.smtp_user
    msg["To"] = email_to

    with SMTP(Config.smtp_host, Config.smtp_port) as server:
        server.starttls()
        server.login(Config.smtp_user, Config.smtp_pass)
        server.sendmail(Config.smtp_user, email_to, msg.as_string())


class QueueConsumer(ConsumerMixin):
    def __init__(self, connection, queue_name):
        self.connection = connection
        self.queue_name = queue_name

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.queue_name, callbacks=[self.process_message])]

    def process_message(self, body, message):
        if self.queue_name == "task_created":
            email_subject = "Задача создана"
            email_message = f"Новая задача создана с ID {body['id']}.\n Имя задачи: {body['title']}\n Приоритет: {body['prioriry']}\n Пользователь: {body['user_id']}"
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
    with Connection("amqp://guest:guest@127.0.0.1:15672/#/") as connection:
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


monitor_queues()
