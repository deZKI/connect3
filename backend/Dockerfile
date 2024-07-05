# Базовый образ
FROM python:3.11.9-alpine3.19

# устанавливаем netcat
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/main" > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories && \
    apk add --no-cache netcat-openbsd build-base libffi-dev


# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов зависимостей
COPY . /app

# Установка poetry и зависимостей проекта
RUN pip install -r requirements.txt

# Делаем entrypoint скрипт исполняемым
RUN chmod +x entrypoint.sh

# Установка entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
