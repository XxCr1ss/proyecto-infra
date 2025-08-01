# Preguntas Frecuentes (FAQ)

## Preguntas Generales

### ¿Qué es este proyecto?

Este proyecto es un sistema distribuido de Machine Learning que utiliza Ray para la paralelización, una arquitectura de microservicios con FastAPI, y un frontend en React. Está diseñado para demostrar cómo se puede implementar un pipeline de ML escalable y eficiente.

### ¿Qué tecnologías utiliza?

- **Backend**: Python, Ray, FastAPI, scikit-learn, pandas, numpy
- **Frontend**: React, Bootstrap, Recharts
- **Despliegue**: Docker, Docker Compose, AWS EC2

### ¿Puedo usar este proyecto en producción?

Este proyecto está diseñado principalmente con fines educativos y de demostración. Para un entorno de producción, se recomienda implementar características adicionales como autenticación, autorización, cifrado, pruebas exhaustivas y monitorización avanzada.

## Instalación y Configuración

### ¿Cómo instalo el proyecto localmente?

Existen dos formas principales:

1. **Modo Simplificado** (sin Ray ni Docker):
   ```bash
   pip install -r requirements_simple.txt
   cd frontend && npm install && cd ..
   python api_simple.py
   # En otra terminal
   cd frontend && npm start
   ```

2. **Modo Completo** (con Docker):
   ```bash
   docker-compose up --build
   ```

Consulta el archivo README.md para instrucciones detalladas.

### ¿Qué puertos utiliza el proyecto?

- **API Backend**: 8001
- **Frontend**: 3000
- **Ray Redis**: 6379
- **Ray Dashboard**: 8265
- **Ray Client**: 10001

Consulta el archivo PORTS_CONFIG.md para más detalles.

### ¿Cómo cambio los puertos?

Para cambiar los puertos, necesitas modificar varios archivos:

1. Para el backend: `docker-compose.yml`, `Dockerfile.api`, `main.py`
2. Para el frontend: `docker-compose.yml`, `frontend/package.json`, `frontend/src/config.js`
3. Para Ray: `docker-compose.yml`, `Dockerfile.ray`

Consulta PORTS_CONFIG.md para instrucciones detalladas.

## Uso del Sistema

### ¿Cómo entreno un modelo?

1. Navega a la sección de Entrenamiento en el frontend
2. Configura los parámetros del modelo
3. Haz clic en "Entrenar Modelo"
4. Espera a que el entrenamiento se complete
5. Revisa los resultados en la sección de métricas

### ¿Cómo realizo predicciones?

1. Navega a la sección de Predicciones
2. Introduce los valores para las características
3. Haz clic en "Predecir"
4. Revisa el resultado de la predicción

### ¿Cómo ejecuto un benchmark?

1. Navega a la sección de Benchmark
2. Configura el tamaño de datos y el número de workers
3. Haz clic en "Ejecutar Benchmark"
4. Revisa los resultados de rendimiento

## Solución de Problemas

### El frontend no puede conectarse al backend

1. Verifica que el backend esté en ejecución
2. Comprueba que los puertos configurados sean correctos
3. Asegúrate de que no haya firewalls bloqueando la conexión
4. Verifica la URL de la API en `frontend/src/config.js`

### Error al iniciar el cluster Ray

1. Verifica que los puertos 6379, 8265 y 10001 estén disponibles
2. Comprueba los logs de Docker para errores específicos
3. Asegúrate de que las variables de entorno estén configuradas correctamente

### El entrenamiento del modelo falla

1. Verifica que el cluster Ray esté funcionando correctamente
2. Comprueba los logs del backend para errores específicos
3. Asegúrate de que los datos de entrada sean válidos
4. Verifica que haya suficiente memoria disponible

### Docker Compose no puede construir las imágenes

1. Asegúrate de tener Docker y Docker Compose instalados correctamente
2. Verifica que tengas permisos suficientes
3. Comprueba que los Dockerfiles no contengan errores
4. Intenta ejecutar `docker system prune` para limpiar recursos no utilizados

## Despliegue

### ¿Cómo despliego el proyecto en AWS?

1. Configura instancias EC2 con suficientes recursos
2. Instala Docker y Docker Compose en las instancias
3. Clona el repositorio
4. Configura las variables de entorno necesarias
5. Ejecuta `docker-compose up --build`

Consulta `deployment/README.md` para instrucciones detalladas.

### ¿Puedo desplegar solo algunos componentes?

Sí, puedes modificar el archivo `docker-compose.yml` para incluir solo los servicios que necesites. Por ejemplo, puedes desplegar solo el backend y el frontend sin el cluster Ray para un entorno de desarrollo.

## Desarrollo y Contribución

### ¿Cómo puedo contribuir al proyecto?

1. Haz un fork del repositorio
2. Crea una rama para tu característica o corrección
3. Implementa tus cambios
4. Envía un pull request

Consulta CONTRIBUTING.md para más detalles.

### ¿Cómo añado un nuevo modelo al sistema?

1. Añade la implementación del modelo en `ray_parallelization/ml_pipeline.py`
2. Actualiza la API en `microservices/api/main.py` para exponer el nuevo modelo
3. Actualiza el frontend para permitir la selección y configuración del nuevo modelo

### ¿Cómo modifico el frontend?

1. Navega al directorio `frontend`
2. Modifica los archivos necesarios
3. Ejecuta `npm start` para ver los cambios en desarrollo
4. Construye la aplicación con `npm run build` para producción

## Rendimiento y Escalabilidad

### ¿Cómo puedo mejorar el rendimiento?

1. Aumenta el número de workers de Ray
2. Optimiza los algoritmos de ML en `ray_parallelization/ml_pipeline.py`
3. Considera utilizar instancias con más recursos (CPU, RAM, GPU)
4. Ajusta los parámetros de configuración de Ray

### ¿Cómo escalo el sistema para manejar más datos?

1. Aumenta el número de workers de Ray en `docker-compose.yml`
2. Considera implementar técnicas de procesamiento por lotes
3. Optimiza el almacenamiento y recuperación de datos
4. Considera utilizar un cluster Ray más grande en un entorno de producción

## Contacto y Soporte

### ¿Dónde puedo obtener ayuda adicional?

Si tienes preguntas o problemas que no están cubiertos en esta FAQ, puedes:

1. Crear un issue en el repositorio
2. Contactar a los mantenedores del proyecto
3. Consultar la documentación adicional en el directorio `docs`