# Dockerfile para el servicio de Ray (puede ser usado para head y workers)
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y curl && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# El comando para iniciar el nodo de Ray se proporcionará en docker-compose.yml
# Este Dockerfile es genérico tanto para los nodos head como para los worker.