# Guía Rápida

Esta guía te ayudará a poner en marcha el sistema de Machine Learning distribuido rápidamente.

## Inicio Rápido

### Opción 1: Modo Simplificado (Sin Docker)

Para una configuración rápida sin Ray ni Docker:

```bash
# Instalar dependencias de Python
pip install -r requirements_simple.txt

# Instalar dependencias del frontend
cd frontend && npm install && cd ..

# Iniciar el backend
python api_simple.py

# En otra terminal, iniciar el frontend
cd frontend && npm start
```

Accede a la aplicación en: http://localhost:3000

### Opción 2: Modo Completo (Con Docker)

Para una experiencia completa con Ray y Docker:

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build
```

Accede a la aplicación en: http://localhost:3000

## Funcionalidades Principales

### 1. Dashboard

- **Ruta**: `/dashboard`
- **Descripción**: Visualiza métricas del sistema y estado del cluster Ray
- **Uso**: Navega a esta sección para monitorear el rendimiento y estado del sistema

### 2. Entrenamiento de Modelos

- **Ruta**: `/training`
- **Descripción**: Configura y ejecuta entrenamientos de modelos
- **Uso**: 
  1. Selecciona los parámetros del modelo
  2. Haz clic en "Entrenar Modelo"
  3. Espera a que el entrenamiento se complete
  4. Revisa los resultados

### 3. Predicciones

- **Ruta**: `/predict`
- **Descripción**: Realiza predicciones con modelos entrenados
- **Uso**:
  1. Introduce los valores para las características
  2. Haz clic en "Predecir"
  3. Revisa el resultado de la predicción

### 4. Benchmark

- **Ruta**: `/benchmark`
- **Descripción**: Evalúa el rendimiento del sistema paralelo
- **Uso**:
  1. Configura el tamaño de datos y el número de workers
  2. Haz clic en "Ejecutar Benchmark"
  3. Analiza los resultados de rendimiento

## Endpoints de la API

### Principales Endpoints

- **Salud**: `GET /health`
- **Documentación**: `GET /docs`
- **Entrenamiento**: `POST /train`
- **Predicción**: `POST /predict`
- **Métricas**: `GET /metrics`
- **Benchmark**: `POST /benchmark`

Todos los endpoints están disponibles en: http://localhost:8001

## Verificación del Sistema

Para verificar que todo funciona correctamente:

1. Comprueba que la API responde: http://localhost:8001/health
2. Verifica que el frontend carga: http://localhost:3000
3. Para el modo completo, verifica el dashboard de Ray: http://localhost:8265

## Flujo de Trabajo Típico

1. **Entrenar un modelo**:
   - Navega a `/training`
   - Configura y ejecuta el entrenamiento

2. **Monitorear el progreso**:
   - Revisa el estado en `/dashboard`

3. **Realizar predicciones**:
   - Una vez entrenado el modelo, ve a `/predict`
   - Introduce datos y obtén predicciones

4. **Evaluar rendimiento**:
   - Ejecuta benchmarks en `/benchmark`
   - Analiza los resultados

## Comandos Útiles

### Docker

```bash
# Ver logs de contenedores
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener todos los servicios
docker-compose down
```

### Desarrollo Local

```bash
# Iniciar modo simplificado (Windows)
start_local.bat

# Iniciar modo simplificado (Linux/Mac)
./start_local.sh

# Detener modo simplificado (Windows)
stop_local.bat

# Detener modo simplificado (Linux/Mac)
./stop_local.sh
```

## Solución Rápida de Problemas

- **El frontend no se conecta al backend**: Verifica que la API esté en ejecución y que la URL configurada sea correcta
- **Error al iniciar Ray**: Asegúrate de que los puertos necesarios estén disponibles
- **Problemas con Docker**: Intenta `docker-compose down` seguido de `docker-compose up --build`

## Siguientes Pasos

- Explora la documentación completa en el directorio `docs/`
- Revisa el código fuente para entender la implementación
- Consulta `CONTRIBUTING.md` si deseas contribuir al proyecto

## Recursos Adicionales

- **README.md**: Información general del proyecto
- **SETUP_LOCAL.md**: Instrucciones detalladas para configuración local
- **PORTS_CONFIG.md**: Configuración de puertos
- **FAQ.md**: Preguntas frecuentes
- **ARQUITECTURA.md**: Detalles técnicos de la arquitectura