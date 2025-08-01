# Dockerfile para el servicio de la API
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# El comando para ejecutar la API se proporcionará en docker-compose.yml
# Será algo como: uvicorn main:app --host 0.0.0.0 --port 8000