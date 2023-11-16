# В данной директории все необходимое для развертывания СУБД и сервисов

**Содержание**

- [Запуск](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#запуск)
- [Остановка](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#остановка)
- [Проверка статусов сервисов](httpPostgreSQLQ/EvoFP/tree/developer/deploy#проверка-статусов-сервисов)
- [PostgreSQL](https://github.com/maaaaQ/EvoFP/tree/developer/deploy#postgresql)

## Запуск

---

docker-compose -p deploy up -d

---

# Остановка

---

docker-compose stop

---

# Проверка статусов сервисов

---

docker ps --all --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

---

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
