# Guía de Ejecución Local

Esta guía te ayudará a ejecutar el sistema de ML con Ray y microservicios localmente, sin necesidad de Docker ni AWS.

## Prerrequisitos

- **Python 3.8+** instalado
- **Node.js 16+** y npm instalados
- **Git** para clonar el repositorio

## Paso 1: Configurar el Entorno Python

### 1.1 Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 1.2 Instalar dependencias Python

```bash
# Instalar todas las dependencias
pip install -r requirements.txt
```

## Paso 2: Configurar Ray Cluster Local

### 2.1 Iniciar Ray Head Node

Abre una nueva terminal y ejecuta:

```bash
# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Iniciar Ray head node
ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0
```

Deberías ver algo como:
```
Local node IP: 192.168.1.100
Ray runtime started.
To connect to this Ray runtime, use ray.init(address='ray://localhost:10001')
```

### 2.2 Verificar Ray Dashboard

Abre tu navegador y ve a: `http://localhost:8265`

Deberías ver el dashboard de Ray con información del cluster.

## Paso 3: Ejecutar el Backend API

### 3.1 Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
# Crear archivo .env
echo "RAY_DISABLE_IMPORT_WARNING=1" > .env
echo "PYTHONPATH=." >> .env
```

### 3.2 Ejecutar la API

En una nueva terminal:

```bash
# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Navegar al directorio del proyecto
cd microservices/api

# Ejecutar la API
python main.py
```

La API estará disponible en: `http://localhost:8000`

### 3.3 Verificar la API

```bash
# Verificar que la API esté funcionando
curl http://localhost:8000/health

# Ver documentación de la API
# Abre en tu navegador: http://localhost:8000/docs
```

## Paso 4: Configurar el Frontend

### 4.1 Instalar dependencias Node.js

```bash
# Navegar al directorio frontend
cd frontend

# Instalar dependencias
npm install
```

### 4.2 Configurar URL de la API

Edita el archivo `frontend/src/components/Dashboard.js` para asegurarte de que apunte a la API local:

```javascript
// Cambiar la URL de la API si es necesario
const API_BASE_URL = 'http://localhost:8000';
```

### 4.3 Ejecutar el Frontend

```bash
# En el directorio frontend
npm start
```

El frontend estará disponible en: `http://localhost:3000`

## Paso 5: Verificar Todo el Sistema

### 5.1 Verificar todos los servicios

1. **Ray Dashboard**: `http://localhost:8265`
2. **API Backend**: `http://localhost:8000`
3. **Frontend**: `http://localhost:3000`

### 5.2 Probar funcionalidades

1. Abre `http://localhost:3000` en tu navegador
2. Ve a la pestaña "Training" y ejecuta un entrenamiento
3. Ve a "Prediction" y prueba hacer predicciones
4. Ve a "Benchmark" para ver comparaciones de rendimiento

## Paso 6: Scripts de Automatización

### 6.1 Script para Windows (start_local.bat)

Crea un archivo `start_local.bat` en la raíz:

```batch
@echo off
echo Iniciando sistema ML local...

echo 1. Activando entorno virtual...
call venv\Scripts\activate

echo 2. Iniciando Ray head node...
start "Ray Head" cmd /k "venv\Scripts\activate && ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0"

echo 3. Esperando que Ray inicie...
timeout /t 5

echo 4. Iniciando API backend...
start "API Backend" cmd /k "venv\Scripts\activate && cd microservices\api && python main.py"

echo 5. Esperando que API inicie...
timeout /t 5

echo 6. Iniciando Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo Sistema iniciado! Abre http://localhost:3000 en tu navegador
pause
```

### 6.2 Script para macOS/Linux (start_local.sh)

Crea un archivo `start_local.sh` en la raíz:

```bash
#!/bin/bash
echo "Iniciando sistema ML local..."

echo "1. Activando entorno virtual..."
source venv/bin/activate

echo "2. Iniciando Ray head node..."
ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0 &
RAY_PID=$!

echo "3. Esperando que Ray inicie..."
sleep 5

echo "4. Iniciando API backend..."
cd microservices/api
python main.py &
API_PID=$!

echo "5. Esperando que API inicie..."
sleep 5

echo "6. Iniciando Frontend..."
cd ../../frontend
npm start &
FRONTEND_PID=$!

echo "Sistema iniciado! Abre http://localhost:3000 en tu navegador"
echo "Para detener: kill $RAY_PID $API_PID $FRONTEND_PID"

# Mantener script ejecutándose
wait
```

Hacer ejecutable:
```bash
chmod +x start_local.sh
```

## Paso 7: Solución de Problemas

### 7.1 Problemas comunes

**Error: Ray no puede conectarse**
```bash
# Verificar que Ray esté ejecutándose
ray status

# Reiniciar Ray si es necesario
ray stop
ray start --head --port=6379 --dashboard-port=8265 --dashboard-host=0.0.0.0
```

**Error: Puerto ocupado**
```bash
# Verificar puertos en uso
# En Windows:
netstat -ano | findstr :8000
netstat -ano | findstr :3000
netstat -ano | findstr :6379

# En macOS/Linux:
lsof -i :8000
lsof -i :3000
lsof -i :6379
```

**Error: Módulos no encontrados**
```bash
# Verificar que estés en el entorno virtual
which python
# Debería mostrar: .../venv/bin/python

# Reinstalar dependencias
pip install -r requirements.txt
```

### 7.2 Logs útiles

```bash
# Ver logs de Ray
ray logs

# Ver logs de la API (en la terminal donde ejecutas main.py)
# Los logs aparecen directamente en la consola

# Ver logs del frontend (en la terminal donde ejecutas npm start)
# Los logs aparecen directamente en la consola
```

## Paso 8: Detener el Sistema

### 8.1 Detener todos los servicios

```bash
# Detener Ray
ray stop

# Detener API (Ctrl+C en la terminal donde está ejecutándose)
# Detener Frontend (Ctrl+C en la terminal donde está ejecutándose)
```

### 8.2 Script de parada

Crea `stop_local.bat` (Windows):
```batch
@echo off
echo Deteniendo sistema ML local...
ray stop
taskkill /f /im node.exe
taskkill /f /im python.exe
echo Sistema detenido
pause
```

Crea `stop_local.sh` (macOS/Linux):
```bash
#!/bin/bash
echo "Deteniendo sistema ML local..."
ray stop
pkill -f "python main.py"
pkill -f "npm start"
echo "Sistema detenido"
```

## Paso 9: Desarrollo

### 9.1 Estructura de archivos importantes

```
indra_proyecto/
├── microservices/api/main.py          # API principal
├── ray_parallelization/ml_pipeline.py # Pipeline de ML
├── frontend/src/                      # Código React
├── requirements.txt                   # Dependencias Python
└── frontend/package.json             # Dependencias Node.js
```

### 9.2 Modificar el código

- **API**: Edita `microservices/api/main.py`
- **ML Pipeline**: Edita `ray_parallelization/ml_pipeline.py`
- **Frontend**: Edita archivos en `frontend/src/`

Los cambios se reflejan automáticamente al guardar (hot reload).

## Paso 10: Próximos Pasos

Una vez que tengas todo funcionando localmente:

1. **Explora la API**: Ve a `http://localhost:8000/docs`
2. **Prueba el frontend**: Ve a `http://localhost:3000`
3. **Monitorea Ray**: Ve a `http://localhost:8265`
4. **Experimenta**: Modifica parámetros y ve cómo afectan el rendimiento

¡Disfruta desarrollando tu sistema de ML con Ray! 