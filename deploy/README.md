# В данной директории все необходимое для развертывания СУБД и сервисов

# Запуск

---

docker-compose -p home-automation up -d

---

# Проверка статусов сервисов

---

docker ps --all --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

---

# Остановка

---

docker-compose stop

---
