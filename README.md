# Sistema de Machine Learning con Ray y Microservicios

## 📋 Descripción del Proyecto

Este proyecto implementa un sistema completo de Machine Learning distribuido que combina:

- **Ray Framework** para paralelización y distribución de tareas de cómputo
- **Arquitectura de Microservicios** con APIs REST
- **Frontend interactivo** para visualización y control
- **Containerización con Docker** para despliegue simplificado

El sistema permite entrenar modelos de regresión en paralelo, realizar predicciones, ejecutar benchmarks de rendimiento y visualizar métricas en tiempo real.

## 🏗️ Estructura del Proyecto

```
proyecto-infra/
├── microservices/          # Microservicios y APIs con Ray
├── ray_parallelization/    # Módulos de paralelización con Ray
├── frontend/              # Cliente React
├── api_simple.py          # Versión simplificada de la API (sin Ray)
├── docker-compose.yml     # Configuración Docker con Ray
├── docker-compose.simple.yml # Configuración Docker simplificada
├── requirements.txt       # Dependencias completas
├── requirements_simple.txt # Dependencias simplificadas
└── scripts de inicio/parada # Para ejecución local y Docker
```

## 🚀 Características Principales

- **Paralelización de Entrenamiento**: Entrena múltiples modelos en paralelo usando Ray
- **Ensemble de Modelos**: Combina predicciones de múltiples modelos para mayor precisión
- **Benchmarking**: Compara rendimiento secuencial vs paralelo
- **Visualización en Tiempo Real**: Dashboard interactivo con métricas y gráficos
- **API REST**: Endpoints para todas las funcionalidades del sistema
- **Dos Modos de Ejecución**: Completo (con Ray) y Simplificado (sin Ray)

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Ray, FastAPI, scikit-learn
- **Frontend**: React, Bootstrap, Recharts
- **Infraestructura**: Docker, Docker Compose
- **ML**: Pandas, NumPy, scikit-learn

## ⚙️ Instalación y Configuración

### Prerrequisitos

- Python 3.8+ (recomendado 3.11+)
- Docker y Docker Compose (para modo containerizado)
- Node.js 16+ y npm (para desarrollo frontend)

### Opción 1: Ejecución Local Simplificada (Sin Ray)

1. **Instalar dependencias:**

```bash
pip install -r requirements_simple.txt
cd frontend && npm install && cd ..
```

2. **Iniciar servicios:**

```bash
# Windows
start_local.bat

# Linux/Mac
./start_local.sh
```

3. **Acceder a la aplicación:**
   - Frontend: http://localhost:3000
   - API: http://localhost:8001
   - Documentación API: http://localhost:8001/docs

### Opción 2: Ejecución con Docker (Recomendado)

1. **Versión simplificada (sin Ray):**

```bash
# Windows
start_docker.bat

# Linux/Mac
docker-compose -f docker-compose.simple.yml up --build
```

2. **Versión completa (con Ray):**

```bash
docker-compose up --build
```

## 📊 Funcionalidades Principales

### 1. Dashboard

- Visualización del estado del sistema
- Métricas de rendimiento
- Acceso rápido a todas las funcionalidades

### 2. Entrenamiento de Modelos

- Configuración de parámetros de entrenamiento
- Monitoreo en tiempo real del progreso
- Visualización de métricas de rendimiento

### 3. Predicciones

- Interfaz para ingresar datos de entrada
- Visualización de resultados de predicción
- Opción para usar datos de ejemplo

### 4. Benchmark

- Comparación de rendimiento secuencial vs paralelo
- Cálculo de speedup y eficiencia
- Visualización gráfica de resultados

### 5. Métricas Detalladas

- Estado del cluster Ray
- Recursos disponibles y utilizados
- Métricas de entrenamiento

## 🔌 APIs Disponibles

- `GET /health`: Estado del servicio
- `GET /metrics`: Métricas del sistema
- `POST /predict`: Realizar predicciones
- `POST /train`: Iniciar entrenamiento
- `GET /training-status`: Estado del entrenamiento
- `POST /benchmark`: Ejecutar benchmark
- `GET /sample-data`: Obtener datos de ejemplo

## 📚 Documentación Adicional

- **SETUP_LOCAL.md**: Instrucciones detalladas para configuración local
- **PORTS_CONFIG.md**: Configuración de puertos del sistema
- **CHANGES_SUMMARY.md**: Historial de cambios importantes

## 🤝 Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add some amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
