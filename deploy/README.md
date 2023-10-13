# В данной директории все необходимое для развертывания СУБД и сервисов

# Сборка образа PostgreSQL

---

docker build -t postgres-image .

---

# Запуск

---

docker-compose -p deploy up -d

---

# Проверка статусов сервисов

---

docker ps --all --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

---

# Остановка

---

docker-compose stop

---

# tasks-service доступен по адресу

---

http://127.0.0.1:5000/docs

---

# comment-service доступен по адресу

---

http://127.0.0.1:4000/docs

---
