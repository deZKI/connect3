# Базовый образ
FROM python:3.12-alpine

# устанавливаем netcat
RUN echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/main" > /etc/apk/repositories && \
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.19/community" >> /etc/apk/repositories && \
    apk add --no-cache netcat-openbsd build-base libffi-dev


# Установка рабочей директории в контейнере
WORKDIR /app

# Копирование файлов зависимостей
COPY . /app

# Установка poetry и зависимостей проекта
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

# Делаем entrypoint скрипт исполняемым
RUN chmod +x entrypoint.sh

# Установка entrypoint
ENTRYPOINT ["sh", "entrypoint.sh"]
