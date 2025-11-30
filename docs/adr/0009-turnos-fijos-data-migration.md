# 9. Turnos Fijos en el Sistema

**Fecha**: 2025-11-30
**Estado**: Aceptado

## Contexto

El sistema de asistencias del Sagrado Corazón ALCAL requiere registrar la presencia de alumnos en diferentes turnos del día. Los turnos son parte de la estructura organizativa del colegio y no cambian frecuentemente.

## Decisión

Los turnos se definen como **datos fijos** en la base de datos mediante una migración de datos (data migration), en lugar de gestionarse mediante CRUD.

### Turnos Definidos

1. **Mañana**
2. **Tarde**
3. **Educación Física**

Los horarios específicos no se almacenan en la base de datos ya que no son necesarios para el funcionamiento del sistema de asistencias.

### Implementación

- **Migración de datos**: `asistencias/migrations/0003_crear_turnos_fijos.py`
- Los turnos se crean automáticamente al ejecutar `python manage.py migrate`
- Usa `get_or_create` para evitar duplicados si se ejecuta múltiples veces

## Consecuencias

### Positivas
- **Simplicidad**: No hay CRUD de turnos que pueda generar inconsistencias
- **Integridad**: Los turnos siempre existen en la base de datos
- **Predecibilidad**: El sistema siempre tiene los mismos tres turnos disponibles

### Negativas
- **Flexibilidad limitada**: Cambiar horarios requiere una nueva migración
- **Mantenimiento**: Modificar turnos requiere intervención técnica (no se puede hacer desde el admin)

### Neutral
- Si en el futuro se necesita cambiar los turnos, se creará una nueva migración de datos
- Los turnos existentes en la base de datos no se eliminan, solo se actualizan

## Alternativas Consideradas

### Opción 1: CRUD completo de turnos
- **Rechazada**: Permite a usuarios crear/eliminar turnos, lo que podría romper la lógica del sistema
- Los turnos son parte de la estructura institucional, no datos variables

### Opción 2: Hardcodear en el código
- **Rechazada**: Dificulta cambios futuros y no permite personalización por instalación

### Opción 3: Turnos fijos con migración (ELEGIDA)
- **Aceptada**: Balance entre flexibilidad técnica y simplicidad de uso

## Modificaciones Futuras

Si se necesita agregar información adicional a los turnos (ej: horarios, descripción extendida):

```python
# Nueva migración: 0005_agregar_campo_a_turno.py
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='turno',
            name='descripcion',
            field=models.TextField(blank=True),
        ),
    ]
```

## Referencias
- Modelo: `asistencias/models.py` - `Turno`
- Migración: `asistencias/migrations/0003_crear_turnos_fijos.py`
- Uso: Asistencias, Cierre Diario, Detalle de Cierre por Curso
