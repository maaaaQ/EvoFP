**[ToDoist API](https://github.com/maaaaQ/EvoFP)**

**Структура репозитория**

- [services](https://github.com/maaaaQ/EvoFP/tree/developer/services) - содержит исходные коды сервисов системы
  - [tasks-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/tasks-service) - сервис управления задачами
  - [comment-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/comment-service) - сервис управления комментариями к задачам
  - [user-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/user-service) - пользовательский сервис
  - [notification-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/notification-service) - сервис отправки уведомлений о важных действиях
  - [policy-enforcement-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/policy-enforcement-service) - сервис проверки полномочий
- [deploy](https://github.com/maaaaQ/EvoFP/tree/developer/deploy) - содержит все необходимое для развертывания СУБД и сервисов

**Концепция**

Концепция основана на предоставлении пользователям возможности взаимодействия с функциональностью и данными, связанными с планированием, управлением задачами и комментариями.
API Todoist предоставляет набор методов и эндпоинтов, которые позволяют пользователям создавать, изменять, удалять и получать информацию о задачах, комментариях.

API Todoist предлагает следующие возможности:

- Управление задачами: пользователи могут создавать новые задачи, изменять существующие задачи (например, изменять статус задачи, приоритет) и удалять задачи по их идентификаторам.
- Управление комментариями: пользователи могут создавать новые комментарии и просматривать имеющиеся комментарии к задачам.
- Поиск задач по статусу и приоритету: пользователи могут выполнять поиск задач по статусу и приоритету.

**Состав сервисов системы**

- Сервис проверки полномочий (Policy Enforcement Service) - Является точкой входа в приложение, принимает все входящие запросы, проверяет права доступа к запрашиваемому ресурсу и маршрутизирует на него
- Пользовательский сервис (User Service) - Предоставляет API для регистрации и авторизации пользователей, для управления полномочиями пользователей
- Сервис управления задачами (Tasks Service) - Предоставляет API для создания/изменения/удаления/просмотра задач в системе
- Сервис управления комментариями (Comments Service) - Предоставляет API для создания/изменения/удаления/просмотра комментариев к задачам в системе
- Сервис управления уведомлениями (Notification Service) - Предоставляет API для создания и отправки уведомлений на email пользователю о важных событиях

**Система хранения данных**

- [PostgreSQL](https://www.postgresql.org/)

**Брокер обмена сообщениями**

- [RabbitMQ](https://www.rabbitmq.com/)

**Архитектура проекта**

![Архитектура](https://github.com/maaaaQ/EvoFP/blob/developer/architecture.png)

**Поиск уязвимостей в исходном коде производится с помощью библиотеки [Bandit](https://github.com/PyCQA/bandit)**

- Необходимо перейти в корневой каталог (EvoFP)
- Запустить проверку уязвимостей командой

```
bandit -r .
```

**Поиск уязвимостей в docker образах производится с помощью [Trivy](https://github.com/aquasecurity/trivy)**

- Необходимо перейти в каталог (EvoFP/deploy)
- Для поиска уязвимостей в docker образе tasks-service выполнить команду:

```
docker run -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image deploy-tasks-service
```
