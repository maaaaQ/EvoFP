**[ToDoist API](https://github.com/maaaaQ/EvoFP)**

♦ **[Структура репозитория](https://github.com/maaaaQ/EvoFP#структура-репозитория)**

- services - содержит исходные коды сервисов системы
  - [tasks-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/tasks-service) - сервис управления задачами
  - [comment-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/comment-service) - сервис комментариями к задачам
  - [user-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/user-service) - пользовательский сервис
  - [notification-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/notification-service) - сервис отправки уведомлений о важных действиях
  - [policy-enforcement-service](https://github.com/maaaaQ/EvoFP/tree/developer/services/policy-enforcement-service) - сервис проверки полномочий

**[Концепция](https://github.com/maaaaQ/EvoFP#концепция)**

Концепция основана на предоставлении пользователям возможности взаимодействия с функциональностью и данными, связанными с планированием, управлением задачами и комментариями.
API Todoist предоставляет набор методов и эндпоинтов, которые позволяют пользователям создавать, изменять, удалять и получать информацию о задачах, комментариях.

♦ API Todoist предлагает следующие возможности:

- Управление задачами: пользователи могут создавать новые задачи, изменять существующие задачи (например, изменять статус задачи, приоритеты) и удалять задачи по их идентификаторам.
- Управление комментариями: пользователи могут создавать новые комментарии и просматривать имеющиеся комментарии к задачам.
- Поиск задач по статусу и приоритету: пользователи могут выполнять поиск задач по статусу и приоритету задач.

**[Состав сервисов системы](https://github.com/maaaaQ/EvoFP#состав-сервисов-системы)**

- Сервис проверки полномочий (Policy Enforcement Service) - Является точкой входа в приложение, принимает все входящие запросы, проверяет права доступа к запрашиваемому ресурсу и маршрутизирует на него
- Пользовательский сервис (User Service) - Предоставляет API для регистрации и авторизации пользователей, для управления полномочиями пользователей
- Сервис управления задачами (Tasks Service) - Предоставляет API для создания/изменения/удаления/просмотра задач в системе
- Сервис управления комментариями (Comments Service) - Предоставляет API для создания/изменения/удаления/просмотра комментариев к задачам в системе
- Сервис управления уведомлениями (Notification Service) - Предоставляет API для создания и отправки уведомлений на email пользователю о важных событиях

**[Система хранения данных](https://github.com/maaaaQ/EvoFP#система-хранения-данных)**

- [PostgreSQL](https://www.postgresql.org/)

♦ **[Брокер обмена сообщениями](https://github.com/maaaaQ/EvoFP#брокер-обмена-сообщениями)**

- [RabbitMQ](https://www.rabbitmq.com/)

**[Архитектура](https://github.com/maaaaQ/EvoFP#архитектура)**

- ![Архитектура](https://github.com/maaaaQ/EvoFP/blob/developer/architecture.png)

**[Развертывание](https://github.com/maaaaQ/EvoFP/tree/developer/deploy)**
