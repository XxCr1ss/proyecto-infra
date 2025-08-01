# Guía de Despliegue en AWS EC2

Esta guía describe cómo desplegar el sistema de ML con Ray y microservicios en AWS EC2.

## Prerrequisitos

- Cuenta de AWS con acceso a EC2
- AWS CLI configurado
- Docker y Docker Compose instalados en la instancia EC2
- Clave SSH para conectarse a la instancia

## Paso 1: Crear Instancia EC2

### 1.1 Configuración de la Instancia

```bash
# Crear instancia EC2 (recomendado: t3.large o superior)
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --count 1 \
  --instance-type t3.large \
  --key-name tu-clave-ssh \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=ML-Ray-System}]'
```

### 1.2 Configurar Security Groups

Asegúrate de que el security group permita el tráfico en los siguientes puertos:

- **22**: SSH
- **80**: HTTP
- **443**: HTTPS
- **3000**: Frontend React
- **8000**: API FastAPI
- **6379**: Ray Redis
- **8265**: Ray Dashboard

## Paso 2: Configurar la Instancia

### 2.1 Conectarse a la Instancia

```bash
ssh -i tu-clave.pem ubuntu@tu-ip-instancia
```

### 2.2 Instalar Dependencias

```bash
# Actualizar sistema
sudo apt-get update && sudo apt-get upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Instalar Git
sudo apt-get install git -y

# Reiniciar para aplicar cambios de Docker
sudo reboot
```

### 2.3 Clonar el Repositorio

```bash
git clone <tu-repositorio>
cd indra_proyecto
```

## Paso 3: Desplegar la Aplicación

### 3.1 Configurar Variables de Entorno

```bash
# Crear archivo .env
cat > .env << EOF
RAY_DISABLE_IMPORT_WARNING=1
PYTHONPATH=/app
REACT_APP_API_URL=http://tu-ip-instancia:8000
EOF
```

### 3.2 Ejecutar con Docker Compose

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build -d

# Verificar que todos los servicios estén ejecutándose
docker-compose ps

# Ver logs
docker-compose logs -f
```

### 3.3 Verificar el Despliegue

```bash
# Verificar API
curl http://localhost:8000/health

# Verificar Frontend
curl http://localhost:3000

# Verificar Ray Dashboard
curl http://localhost:8265
```

## Paso 4: Configurar Nginx (Opcional)

Para un despliegue en producción, es recomendable usar Nginx como proxy reverso:

### 4.1 Instalar Nginx

```bash
sudo apt-get install nginx -y
```

### 4.2 Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/ml-system
```

```nginx
server {
    listen 80;
    server_name tu-dominio.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # API
    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Ray Dashboard
    location /ray/ {
        proxy_pass http://localhost:8265/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

### 4.3 Habilitar Configuración

```bash
sudo ln -s /etc/nginx/sites-available/ml-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Paso 5: Monitoreo y Mantenimiento

### 5.1 Comandos Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f api

# Reiniciar un servicio
docker-compose restart api

# Escalar servicios
docker-compose up -d --scale ray-worker=4

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes
docker-compose down -v
```

### 5.2 Backup y Restauración

```bash
# Backup de datos
docker-compose exec api tar -czf /tmp/backup-$(date +%Y%m%d).tar.gz /app/data

# Restaurar datos
docker-compose exec api tar -xzf /tmp/backup-20231201.tar.gz -C /
```

### 5.3 Actualización de la Aplicación

```bash
# Obtener cambios del repositorio
git pull origin main

# Reconstruir y reiniciar servicios
docker-compose down
docker-compose up --build -d
```

## Paso 6: Configuración de SSL (Opcional)

Para HTTPS en producción:

```bash
# Instalar Certbot
sudo apt-get install certbot python3-certbot-nginx -y

# Obtener certificado SSL
sudo certbot --nginx -d tu-dominio.com

# Configurar renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Troubleshooting

### Problemas Comunes

1. **Puertos ocupados**: Verificar que los puertos 3000, 8000, 6379, 8265 estén libres
2. **Memoria insuficiente**: Aumentar el tamaño de la instancia EC2
3. **Problemas de red**: Verificar security groups y firewall
4. **Ray no inicia**: Verificar logs con `docker-compose logs ray-head`

### Logs de Debug

```bash
# Ver logs detallados
docker-compose logs --tail=100 -f

# Verificar estado de contenedores
docker-compose ps

# Verificar recursos del sistema
docker stats
```

## Costos Estimados

- **t3.large**: ~$30-40/mes
- **t3.xlarge**: ~$60-80/mes
- **Transferencia de datos**: Variable según uso

## Seguridad

- Usar security groups restrictivos
- Configurar firewall
- Mantener actualizaciones de seguridad
- Usar HTTPS en producción
- Implementar autenticación si es necesario
