#!/bin/sh

# Проверка на доступность django
echo "Waiting for web server..."
while ! nc -z web 8000; do
  sleep 0.1
done
echo "Web server started"

# Запуск бота
python main.py
echo "Starting Bot"
# run the container CMD
exec "$@"
