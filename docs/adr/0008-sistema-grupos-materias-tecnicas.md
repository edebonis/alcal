# 8. Sistema de Grupos para Materias Técnico-Específicas

**Fecha**: 2025-11-30
**Estado**: Aceptado

## Contexto

El Sagrado Corazón ALCAL ofrece dos carreras:
- **Bachillerato en Economía** (6 años, cursos "A")
- **Técnico en Programación** (7 años, cursos "B")

En la carrera técnica existen **materias técnico-específicas** que requieren dividir el curso en dos grupos (Grupo 1 y Grupo 2) para talleres prácticos. Estas materias pueden tener:
- Dos docentes diferentes (uno por grupo)
- Horarios diferentes por grupo
- Asistencias independientes por grupo

## Decisión

Se implementa un sistema de grupos con las siguientes características:

### 1. Modelo `Materia`
- Se agrega campo `es_tecnico_especifica` (Boolean)
- Indica si la materia divide el curso en grupos

### 2. Modelo Intermedio `DocenteMateria`
- Reemplaza la relación ManyToMany directa entre `Docente` y `Materia`
- Incluye campo `grupo` con opciones:
  - `'ambos'`: Para materias normales (valor por defecto)
  - `'1'`: Grupo 1 (solo para materias técnico-específicas)
  - `'2'`: Grupo 2 (solo para materias técnico-específicas)

### 3. Modelo `Alumno`
- Ya cuenta con campo `grupo` (valores: 'unico', '1', '2')
- Los alumnos de carreras técnicas se asignan a un grupo específico

### 4. Importación de Datos
- La columna 7 del CSV `Legajo Docente - DocenteMateria.csv` indica si es técnico-específica
- El script de importación lee este campo y configura las materias correctamente

## Consecuencias

### Positivas
- **Flexibilidad**: Permite asignar diferentes docentes a cada grupo
- **Trazabilidad**: Las asistencias y calificaciones se pueden filtrar por grupo
- **Escalabilidad**: El modelo intermedio permite agregar más campos en el futuro (ej: horarios)

### Negativas
- **Complejidad**: La relación Docente-Materia es más compleja que un ManyToMany simple
- **Migración**: Requiere migración de datos existentes
- **UI**: Las vistas de asistencias y calificaciones deben considerar grupos

### Neutral
- **Admin**: Se usa `TabularInline` para gestionar asignaciones docente-materia
- **Validación**: El modelo `DocenteMateria` valida que solo materias técnico-específicas tengan grupos 1 o 2

## Implementación

### Cambios en Modelos
```python
# escuela/models.py
class Materia(models.Model):
    es_tecnico_especifica = models.BooleanField(default=False)

# docentes/models.py
class DocenteMateria(models.Model):
    docente = models.ForeignKey(Docente)
    materia = models.ForeignKey(Materia)
    grupo = models.CharField(choices=[...])
```

### Cambios en Vistas
- Las vistas de asistencias deben filtrar alumnos por grupo cuando la materia es técnico-específica
- Las vistas de calificaciones deben mostrar solo los alumnos del grupo correspondiente

## Referencias
- CSV: `Legajo Docente - DocenteMateria.csv` (columna 7)
- Modelo Alumno: campo `grupo`
- Carreras técnicas: cursos con 7 años de duración (cursos "B")
