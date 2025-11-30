# Changelog

Todas las modificaciones notables a este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Agregado
- Script `scripts/populate_fake_data.py` para generar datos de prueba (alumnos, docentes, cursos, materias) sin necesidad de archivos CSV reales.
- Configuración de `Whitenoise` para servir archivos estáticos en producción.
- Archivo `Procfile` para despliegue.

### Cambiado
- Limpieza masiva de `requirements.txt` para eliminar dependencias innecesarias y facilitar el despliegue.
- Actualización de `settings.py` para soportar configuración de entorno mediante `django-environ` y `Whitenoise`.
- Eliminación de referencias a `grappelli` en `urls.py` ya que la librería no se estaba utilizando.

### Seguridad
- Eliminación de archivos sensibles (CSVs con datos reales, PDFs) del historial de Git.
- Configuración de variables de entorno para secretos en producción.

## [1.0.0] - 2025-11-21

### Agregado
- Funcionalidad completa de Asistencias (toma, consulta, cierre diario).
- Funcionalidad completa de Calificaciones.
- Gestión de Alumnos, Docentes y Estructura Académica.
- API REST documentada con Swagger/OpenAPI.
- Sistema de diseño ALCAL Premium (Bootstrap 5).
- Reportes PDF para fichas de inscripción y constancias.
