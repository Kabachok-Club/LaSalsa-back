# Используем легковесный образ Python 3.13
FROM python:3.13-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения в контейнер
COPY ./app ./app

# Команда для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
