# API сервиса отправки email о создании пользователя/задачи/комментария к задаче

<ins>Сервис использует SSL протокол доставки сообщений, для обеспечения защищенной передачи данных в сети Интернет.
Для использования нужно указать данные в </ins>[.env файле](https://github.com/maaaaQ/EvoFP/blob/developer/services/notification-service/.env)<ins> внутри сервиса и в </ins>[.env файле](https://github.com/maaaaQ/EvoFP/blob/developer/deploy/.env)<ins> внутри deploy. </ins>

```
SMTP_HOST = "параметр, который определяет адрес сервера SMTP для отправки электронной почты"
SMTP_PORT = "параметр, который определяет порт сервера SMTP. Для SSL стандартный порт 465"
SMTP_USER = "параметр, который указывает имя пользователя (username) для аутентификации при подключении к серверу SMTP"
SMTP_PASS = "параметр, который указывает пароль, который используется для аутентификации при отправке электронных писем через сервер SMTP"
```

# Зависимости

Перед запуском сервиса необходимо установить зависимости из файла requirements.txt

```
pip install -r requirements.txt
```

# Путь до исполняемого файла

EvoFP/services/notification-service

# Запуск

```
uvicorn app:app --reload
```

# Сборка образа

```
docker build -t notification-service:notif .
```

# Документация

После запуска доступна документация: http://127.0.0.1:8000/docs
