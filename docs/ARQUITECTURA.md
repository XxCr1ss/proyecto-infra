# Arquitectura del Sistema

## Visión General

Este proyecto implementa un sistema distribuido de Machine Learning utilizando Ray para la paralelización, una arquitectura de microservicios con FastAPI, y un frontend en React. La arquitectura está diseñada para ser escalable, mantenible y eficiente en el procesamiento de datos y entrenamiento de modelos.

## Diagrama de Componentes

```
+-------------------+      +-------------------+      +-------------------+
|                   |      |                   |      |                   |
|  Frontend (React) | <--> |  API (FastAPI)    | <--> |  Ray Cluster      |
|                   |      |                   |      |  (Head + Workers) |
+-------------------+      +-------------------+      +-------------------+
                                    ^
                                    |
                                    v
                           +-------------------+
                           |                   |
                           |  ML Pipeline      |
                           |  (Scikit-learn)   |
                           |                   |
                           +-------------------+
```

## Componentes Principales

### 1. Frontend (React)

El frontend está desarrollado en React y proporciona una interfaz de usuario intuitiva para interactuar con el sistema. Incluye:

- **Dashboard**: Visualización de métricas del sistema y estado del cluster Ray
- **Entrenamiento**: Interfaz para configurar y ejecutar entrenamientos de modelos
- **Predicciones**: Formulario para realizar predicciones con modelos entrenados
- **Benchmark**: Herramienta para evaluar el rendimiento del sistema paralelo

El frontend se comunica con el backend a través de la API REST proporcionada por FastAPI.

### 2. API Backend (FastAPI)

El backend está implementado como un servicio REST utilizando FastAPI, que proporciona:

- Endpoints para entrenamiento de modelos
- Endpoints para realizar predicciones
- Endpoints para obtener métricas del sistema
- Endpoints para ejecutar benchmarks

La API actúa como intermediario entre el frontend y el sistema de procesamiento distribuido Ray.

### 3. Ray Cluster

Ray proporciona el framework para la computación distribuida y paralela:

- **Ray Head**: Nodo principal que coordina el cluster
- **Ray Workers**: Nodos trabajadores que ejecutan tareas en paralelo

El cluster Ray se encarga de distribuir las tareas de procesamiento y entrenamiento entre los nodos disponibles.

### 4. ML Pipeline

El pipeline de Machine Learning utiliza scikit-learn y está diseñado para ser ejecutado de forma paralela:

- Preprocesamiento de datos
- Entrenamiento de modelos
- Evaluación y validación
- Ensamblaje de modelos
- Predicciones

## Flujo de Datos

1. El usuario interactúa con el frontend para configurar y ejecutar tareas
2. El frontend envía solicitudes a la API
3. La API procesa las solicitudes y las envía al cluster Ray
4. Ray distribuye las tareas entre los nodos disponibles
5. Los resultados se devuelven a través de la API al frontend
6. El frontend muestra los resultados al usuario

## Despliegue

El sistema está diseñado para ser desplegado de varias formas:

### Modo Local Simplificado

Para desarrollo y pruebas, sin Ray ni Docker:

- API simple ejecutada directamente con Python
- Frontend ejecutado con npm

### Modo Docker Completo

Para entornos de producción, utilizando Docker Compose:

- Contenedor para la API
- Contenedor para el frontend
- Contenedores para el cluster Ray (head y workers)

### Despliegue en AWS

Para escalar en la nube:

- Instancias EC2 para cada componente
- Configuración de red y seguridad

## Comunicación entre Componentes

### Frontend → API

- Comunicación HTTP/REST
- Configurado a través de la variable de entorno `REACT_APP_API_URL`

### API → Ray

- Comunicación a través del cliente Ray
- Configurado mediante variables de entorno como `RAY_HEAD_SERVICE_HOST` y `RAY_HEAD_SERVICE_PORT`

## Escalabilidad

El sistema puede escalar horizontalmente añadiendo más nodos trabajadores al cluster Ray. Esto se puede hacer:

- En Docker: Añadiendo más servicios de worker en el docker-compose.yml
- En AWS: Lanzando más instancias EC2 y conectándolas al cluster

## Consideraciones de Seguridad

- La API no implementa autenticación en esta versión, lo que sería necesario para un entorno de producción
- Las comunicaciones entre contenedores están aisladas en una red Docker
- Para despliegues en la nube, se recomienda implementar grupos de seguridad y VPC

## Monitorización

- El dashboard de Ray proporciona información sobre el estado del cluster
- La API expone endpoints de métricas que son consumidos por el frontend
- Para entornos de producción, se recomienda integrar con sistemas de monitorización como Prometheus y Grafana

## Conclusión

Esta arquitectura proporciona un sistema flexible y escalable para el procesamiento distribuido de tareas de Machine Learning, permitiendo aprovechar los recursos disponibles de manera eficiente y adaptarse a diferentes entornos de despliegue.