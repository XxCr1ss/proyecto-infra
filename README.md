# Proyecto: Infraestructuras Paralelas y Distribuidas con Ray y Microservicios

## Descripción del Proyecto

Este proyecto implementa una aplicación de Machine Learning distribuida que combina:

- **Ray Framework** para paralelización y distribución de tareas de cómputo
- **Arquitectura de Microservicios** desplegada en AWS EC2
- **APIs REST** construidas con FastAPI
- **Cliente Frontend** para interacción con las APIs

## Estructura del Proyecto

```
indra_proyecto/
├── ray_parallelization/     # Paralelización con Ray
├── microservices/          # Microservicios y APIs
├── frontend/              # Cliente frontend
├── deployment/            # Scripts de despliegue
├── docs/                  # Documentación
└── docker-compose.yml     # Orquestación de contenedores
```

## Tecnologías Utilizadas

- **Ray**: Framework para paralelización y distribución
- **FastAPI**: Framework para APIs REST
- **Docker**: Containerización
- **AWS EC2**: Infraestructura en la nube
- **React**: Frontend
- **Scikit-learn**: Machine Learning
- **Pandas/NumPy**: Procesamiento de datos

## Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- Docker y Docker Compose
- AWS CLI configurado
- Node.js 16+ (para el frontend)

### Instalación Local

1. **Clonar el repositorio:**

```bash
git clone <repository-url>
cd indra_proyecto
```

2. **Instalar dependencias de Python:**

```bash
pip install -r requirements.txt
```

3. **Instalar dependencias del frontend:**

```bash
cd frontend
npm install
```

4. **Ejecutar con Docker Compose:**

```bash
docker-compose up --build
```

## Uso

### Desarrollo Local

1. **Iniciar Ray cluster:**

```bash
cd ray_parallelization
ray start --head
```

2. **Ejecutar paralelización:**

```bash
python ml_pipeline.py
```

3. **Iniciar microservicios:**

```bash
cd microservices
uvicorn api.main:app --reload
```

4. **Iniciar frontend:**

```bash
cd frontend
npm start
```

### Despliegue en AWS

Ver sección de despliegue en `deployment/README.md`

## APIs Disponibles

- `POST /predict`: Realizar predicciones con el modelo ML
- `GET /health`: Estado del servicio
- `GET /metrics`: Métricas de rendimiento

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
