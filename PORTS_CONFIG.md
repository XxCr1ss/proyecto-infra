# Configuración de Puertos del Proyecto ML

## Resumen de Puertos

### Backend API
- **Puerto Principal**: `8001`
- **Archivos afectados**:
  - `microservices/api/main.py` - API completa con Ray
  - `api_simple.py` - API simplificada sin Ray
  - `docker-compose.yml` - Mapeo de puertos para Docker
  - `docker-compose.simple.yml` - Mapeo de puertos para Docker simple

### Frontend
- **Puerto**: `3000`
- **Configuración**: 
  - `frontend/package.json` - Proxy para desarrollo
  - `frontend/src/config.js` - Configuración centralizada de endpoints

### Ray Cluster (solo en modo completo)
- **Redis**: `6379`
- **Dashboard**: `8265`
- **Client Port**: `10001`

## Configuración por Entorno

### Desarrollo Local
```bash
# API Backend (puerto 8001)
python api_simple.py                    # API simple
python microservices/api/main.py        # API completa

# Frontend (puerto 3000)
cd frontend && npm start
```

### Docker
```bash
# Modo completo con Ray
docker-compose up

# Modo simple sin Ray
docker-compose -f docker-compose.simple.yml up
```

## Variables de Entorno

### Frontend
- `REACT_APP_API_URL`: URL base de la API (por defecto: `http://localhost:8001`)

### Backend
- `PYTHONPATH`: Ruta de Python para imports
- `RAY_DISABLE_IMPORT_WARNING`: Deshabilitar warnings de Ray
- `RAY_HEAD_SERVICE_HOST`: Host del nodo Ray head
- `RAY_HEAD_SERVICE_PORT`: Puerto del nodo Ray head

## Endpoints de la API

Todos los endpoints están disponibles en `http://localhost:8001`:

- `GET /` - Información del servicio
- `GET /health` - Estado de salud
- `GET /metrics` - Métricas del sistema
- `POST /predict` - Realizar predicciones
- `POST /train` - Entrenar modelos
- `GET /training-status` - Estado del entrenamiento
- `POST /benchmark` - Ejecutar benchmarks
- `GET /sample-data` - Obtener datos de ejemplo

## Solución de Problemas

### Error de Conexión
1. Verificar que la API esté ejecutándose en el puerto 8001
2. Verificar que el frontend esté configurado para conectarse al puerto correcto
3. Revisar logs de Docker si se usa contenedores

### Cambio de Puertos
Para cambiar los puertos, modificar:
1. El puerto en los archivos de la API (`main.py`, `api_simple.py`)
2. El mapeo de puertos en `docker-compose.yml`
3. La configuración del frontend en `config.js`
4. El proxy en `package.json` 