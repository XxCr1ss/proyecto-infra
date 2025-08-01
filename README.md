# Pipeline de ML con Ray y Docker Compose

Este proyecto demuestra un pipeline de machine learning paralelizado con Ray y desplegado como un conjunto de microservicios orquestados con Docker Compose.

## Arquitectura

La aplicación consta de los siguientes servicios:

- `ray-head`: El nodo principal del clúster de Ray.
- `ray-worker`: Un nodo trabajador para el clúster de Ray.
- `api`: una aplicación FastAPI que expone un endpoint de predicción.
- `trainer`: Un servicio que ejecuta el pipeline de entrenamiento de ML.
- `client`: Un cliente simple que consume la API.

## Cómo Ejecutar

1.  **Construir y ejecutar los servicios:**

    ```bash
    docker-compose up -d --build
    ```

2.  **Ver los logs para ver la salida:**

    ```bash
    docker-compose logs -f
    ```

Deberías ver la salida del pipeline de entrenamiento del servicio `trainer` y luego la salida del servicio `client` haciendo una predicción.

3.  **Acceder al Dashboard de Ray:**

    Abre tu navegador y navega a [http://localhost:8265](http://localhost:8265) para ver el Dashboard de Ray.

4.  **Acceder a la documentación de la API:**

    Abre tu navegador y navega a [http://localhost:8000/docs](http://localhost:8000/docs) para ver la documentación de FastAPI.

5.  **Detener los servicios:**

    ```bash
    docker-compose down
    ```