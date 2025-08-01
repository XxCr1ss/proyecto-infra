# Configuración Local del Proyecto ML

Este documento explica cómo ejecutar el proyecto de Machine Learning localmente sin necesidad de AWS o Docker.

## Prerrequisitos

- Python 3.8+ (recomendado 3.11+)
- Node.js 16+ y npm
- Git

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd proyecto-infra
```

### 2. Instalar dependencias de Python

```bash
pip install -r requirements_simple.txt
```

### 3. Instalar dependencias del Frontend

```bash
cd frontend
npm install
cd ..
```

## Ejecución

### Opción 1: Usando scripts automáticos (Recomendado)

#### Iniciar el proyecto:

```bash
start_local.bat
```

#### Detener el proyecto:

```bash
stop_local.bat
```

### Opción 2: Ejecución manual

#### Paso 1: Iniciar la API

```bash
python api_simple.py
```

La API estará disponible en: http://localhost:8001

#### Paso 2: Iniciar el Frontend (en otra terminal)

```bash
cd frontend
npm start
```

El frontend estará disponible en: http://localhost:3000

## Servicios Disponibles

### API Backend (Puerto 8001)

- **Health Check**: `GET http://localhost:8001/health`
- **Documentación**: `GET http://localhost:8001/docs`
- **Entrenar modelo**: `POST http://localhost:8001/train`
- **Realizar predicciones**: `POST http://localhost:8001/predict`
- **Estado del entrenamiento**: `GET http://localhost:8001/training-status`
- **Datos de ejemplo**: `GET http://localhost:8001/sample-data`

### Frontend (Puerto 3000)

- **Interfaz principal**: http://localhost:3000
- **Dashboard**: http://localhost:3000/dashboard
- **Entrenamiento**: http://localhost:3000/training
- **Predicciones**: http://localhost:3000/prediction

## Uso del Sistema

### 1. Entrenar Modelos

1. Ve a http://localhost:3000/training
2. Configura los parámetros de entrenamiento
3. Haz clic en "Iniciar Entrenamiento"
4. Monitorea el progreso en tiempo real

### 2. Realizar Predicciones

1. Ve a http://localhost:3000/prediction
2. Ingresa los datos de entrada
3. Haz clic en "Predecir"
4. Visualiza los resultados

### 3. Ver Métricas

1. Ve a http://localhost:3000/dashboard
2. Revisa las métricas de rendimiento
3. Analiza los resultados del entrenamiento

## Estructura del Proyecto

```
proyecto-infra/
├── api_simple.py              # API simplificada sin Ray
├── requirements_simple.txt    # Dependencias Python simplificadas
├── start_local.bat           # Script para iniciar servicios
├── stop_local.bat            # Script para detener servicios
├── frontend/                 # Aplicación React
│   ├── src/
│   ├── package.json
│   └── ...
└── ...
```

## Solución de Problemas

### Error: Puerto 8001 en uso

```bash
# Cambiar puerto en api_simple.py línea 157
uvicorn.run(app, host="0.0.0.0", port=8002)
```

### Error: Puerto 3000 en uso

El frontend automáticamente sugerirá usar otro puerto.

### Error: Módulos no encontrados

```bash
pip install -r requirements_simple.txt
```

### Error: Dependencias de Node.js

```bash
cd frontend
npm install
```

## Diferencias con la Versión Completa

Esta versión simplificada:

- ✅ No requiere Ray (paralelización)
- ✅ No requiere Docker
- ✅ No requiere AWS
- ✅ Funciona completamente en local
- ❌ No tiene paralelización distribuida
- ❌ No tiene escalabilidad automática

## Próximos Pasos

Para usar la versión completa con Ray y Docker:

1. Instalar Docker Desktop
2. Ejecutar `docker-compose up --build`
3. Ver documentación en `README.md`

## Soporte

Si encuentras problemas:

1. Verifica que todos los prerrequisitos estén instalados
2. Revisa los logs de error en las terminales
3. Asegúrate de que los puertos no estén en uso
4. Reinicia los servicios usando los scripts
