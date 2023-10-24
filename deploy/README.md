# В данной директории все необходимое для развертывания СУБД и сервисов

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

http://127.0.0.1:5001/docs

---

# comment-service доступен по адресу

---

http://127.0.0.1:5002/docs

---

# user-service доступен по адресу

---

http://127.0.0.1:5003/docs

---

# policy-enforcement-service доступен по адресу

---

http://127.0.0.1:5000/docs

---
