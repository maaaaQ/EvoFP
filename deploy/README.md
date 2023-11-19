# В данной директории все необходимое для развертывания СУБД и сервисов

**Содержание**

- [Запуск](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#запуск)
- [Остановка](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#остановка)
- [Проверка статусов сервисов](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0-%D1%81%D1%82%D0%B0%D1%82%D1%83%D1%81%D0%BE%D0%B2-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%BE%D0%B2)
- [PostgreSQL](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#postgresql)
- [Внесение данных о SSL подключении для отправки уведомлений пользователю](https://github.com/maaaaQ/EvoFP/blob/developer/services/notification-service/README.md#api-%D1%81%D0%B5%D1%80%D0%B2%D0%B8%D1%81%D0%B0-%D0%BE%D1%82%D0%BF%D1%80%D0%B0%D0%B2%D0%BA%D0%B8-email-%D0%BE-%D1%81%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%B8%D0%B8-%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8F%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8%D0%BA%D0%BE%D0%BC%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D1%80%D0%B8%D1%8F-%D0%BA-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B5)

# Запуск

```
docker-compose -p deploy up -d
```

# Остановка

```
docker-compose stop
```

# Проверка статусов сервисов

```
docker ps --all --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

# PostgreSQL

За развертывание PostgreSQL отвечает следующая часть docker-compose файла:

```
volumes:
  postgresql-data:
    driver: local
    driver_opts:
      o: bind
      type: none
      device: ./postgresql/data
services:
	postgresql:
    image: postgres:15.5
    restart: always
    volumes:
      - postgresql-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: postgresql7
      POSTGRES_USER: postgres
      POSTGRES_DB: postgres
      PGDATA: /var/lib/postgresql/data/db-files/
    ports:
      - 5432:5432

```

В нем:

- Создается диск (volume) с названием postgresql-data, для хранения данных используется директория ./postgresql/data. Рекомендуется добавить директорию в gitignore:

```
deploy/postgresql/data/*
!deploy/postgresql/data/.gitkeep
```

- Создается контейнер **postgresql** на базе образа postgres:15.5
- К контейнеру монтируется volume **postgresql-data**
- Пробрасываются порты, PostreSQL будет доступен по {MACHINE_IP}:5432, например: **127.0.0.1:5432**
- Через переменные окружения задается пользователь, название первичной базы данных и директория хранения данных внутри контейнера:

```
POSTGRES_PASSWORD: postgresql7
POSTGRES_USER: postgres
POSTGRES_DB: postgres
PGDATA: /var/lib/postgresql/data/db-files/
```

Для тестирования подключения можно использовать утилиту psql или какой-либо GUI-клиент

**[Образ на Docker-Hub](https://hub.docker.com/_/postgres)**
