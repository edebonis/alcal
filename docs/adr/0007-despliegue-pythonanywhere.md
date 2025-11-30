# 7. Estrategia de Despliegue en PythonAnywhere

**Fecha**: 2025-11-30
**Estado**: Aceptado

## Contexto

El proyecto ALCAL necesita ser desplegado en un entorno accesible públicamente para demostraciones y uso inicial. Se requiere una solución gratuita o de bajo costo que soporte Django y persistencia de datos.

## Decisión

Se ha decidido utilizar **PythonAnywhere** como plataforma de despliegue inicial.

### Detalles de Implementación

1.  **Servidor Web**: Se utiliza la infraestructura WSGI nativa de PythonAnywhere.
2.  **Archivos Estáticos**: Se utiliza la librería `Whitenoise` para servir archivos estáticos directamente desde la aplicación Django, eliminando la necesidad de configurar un servidor web externo para estáticos en la capa gratuita.
3.  **Base de Datos**: Se mantiene `SQLite` por su simplicidad y persistencia garantizada en el sistema de archivos de PythonAnywhere (a diferencia de plataformas como Heroku o Render en sus capas gratuitas).
4.  **Datos de Prueba**: Se implementa un script `populate_fake_data.py` basado en `Faker` para poblar la base de datos con información ficticia, permitiendo demos públicas sin exponer datos reales de alumnos.

## Consecuencias

### Positivas
- **Costo Cero**: La capa gratuita de PythonAnywhere es suficiente para el MVP.
- **Persistencia**: Los datos no se pierden al reiniciar la aplicación.
- **Simplicidad**: No requiere configuración compleja de Docker o servicios externos.

### Negativas
- **Rendimiento**: SQLite no es ideal para alta concurrencia, aunque suficiente para el alcance actual.
- **Escalabilidad**: Migrar a un entorno más robusto requerirá cambiar la base de datos a PostgreSQL y configurar un servidor de estáticos dedicado (S3 o Nginx).

## Referencias
- [PythonAnywhere Django Guide](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Whitenoise Documentation](https://whitenoise.readthedocs.io/)
