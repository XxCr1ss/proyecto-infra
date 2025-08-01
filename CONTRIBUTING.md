# Guía de Contribución

¡Gracias por tu interés en contribuir a nuestro proyecto de Machine Learning con Ray y Microservicios! Esta guía te ayudará a entender el proceso de contribución.

## Proceso de Contribución

1. **Fork del Repositorio**
   - Haz un fork del repositorio a tu cuenta personal

2. **Clona el Repositorio**
   ```bash
   git clone https://github.com/XxCr1ss/proyecto-infra
   cd proyecto-infra
   ```

3. **Crea una Rama**
   ```bash
   git checkout -b feature/nombre-de-tu-feature
   ```
   Usa prefijos como `feature/`, `bugfix/`, `docs/` según corresponda.

4. **Instala las Dependencias**
   ```bash
   pip install -r requirements.txt
   cd frontend && npm install && cd ..
   ```

5. **Realiza tus Cambios**
   - Escribe código limpio y mantenible
   - Sigue las convenciones de estilo del proyecto
   - Añade comentarios donde sea necesario

6. **Prueba tus Cambios**
   - Asegúrate de que tu código funciona correctamente
   - Ejecuta las pruebas existentes y añade nuevas si es necesario
   ```bash
   python test_system.py
   ```

7. **Commit tus Cambios**
   ```bash
   git add .
   git commit -m "Descripción clara del cambio"
   ```

8. **Push a tu Fork**
   ```bash
   git push origin feature/nombre-de-tu-feature
   ```

9. **Crea un Pull Request**
   - Ve a la página del repositorio original
   - Haz clic en "New Pull Request"
   - Selecciona tu rama y describe los cambios realizados

## Estándares de Código

### Python
- Sigue la guía de estilo PEP 8
- Usa docstrings para documentar funciones y clases
- Mantén las funciones pequeñas y con un solo propósito

### JavaScript/React
- Usa ES6+ y componentes funcionales
- Sigue las convenciones de nombres de React
- Mantén los componentes pequeños y reutilizables

## Estructura del Proyecto

Familiarízate con la estructura del proyecto antes de contribuir:

- `microservices/`: APIs y servicios backend
- `ray_parallelization/`: Código relacionado con Ray
- `frontend/`: Aplicación React
- `api_simple.py`: Versión simplificada de la API

## Reportar Bugs

Si encuentras un bug, por favor crea un issue con la siguiente información:

- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs. comportamiento actual
- Capturas de pantalla si aplica
- Entorno (sistema operativo, versión de Python, etc.)

## Proponer Mejoras

Si tienes ideas para mejorar el proyecto:

1. Verifica que no exista ya un issue similar
2. Crea un nuevo issue describiendo tu propuesta
3. Discute la idea con los mantenedores antes de implementarla

## Preguntas

Si tienes preguntas sobre el proyecto, puedes:

- Crear un issue con la etiqueta "question"
- Contactar a los mantenedores directamente

¡Gracias por contribuir a nuestro proyecto!