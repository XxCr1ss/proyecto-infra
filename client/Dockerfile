# Dockerfile para el servicio del Cliente
FROM python:3.10-slim

# Instalar netcat para el script de espera
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# El comando para ejecutar el cliente se proporcionará en docker-compose.yml
# Será algo como: python client.py