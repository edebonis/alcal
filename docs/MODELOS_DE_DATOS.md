# Documentación de Modelos de Datos - Sistema ALCAL

## Sagrado Corazón ALCAL - Sistema de Gestión Escolar

**Fecha:** 21 de Noviembre, 2025  
**Versión:** 1.0  
**Estado:** Implementado con datos reales importados

---

## Índice
1. [Diagrama de Entidad-Relación](#diagrama-de-entidad-relación)
2. [Resumen Ejecutivo](#resumen-ejecutivo)
3. [Modelos del Sistema](#modelos-del-sistema)
4. [Relaciones entre Modelos](#relaciones-entre-modelos)
5. [Datos Importados](#datos-importados)

---

## Diagrama de Entidad-Relación

![Diagrama ERD del Sistema ALCAL](../database_erd_diagram.png)

---

## Resumen Ejecutivo

El sistema ALCAL (Administración de Legajos Escolares del Sagrado Corazón ALCAL) gestiona la información académica de una institución educativa con dos carreras principales:

- **Bachillerato con orientación en Economía** (6 años - Cursos A)
- **Técnico en Programación** (7 años - Cursos B)

### Datos Actuales del Sistema
- **2** Carreras registradas
- **13** Cursos activos (1A-6A, 1B-7B)
- **83** Docentes
- **159** Materias
- **396** Alumnos
- **1** Año lectivo (2022)

---

## Modelos del Sistema

### 1. Módulo Escuela (`escuela.models`)

#### 1.1 Carrera
Representa las carreras o planes de estudio ofrecidos por la institución.

```python
class Carrera(models.Model):
    nombre = models.CharField(max_length=50)
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `nombre`: Nombre de la carrera

**Ejemplos:**
- "Bachillerato con orientación en Economía"
- "Técnico en Programación"

---

#### 1.2 Anio
Representa el año o ciclo lectivo.

```python
class Anio(models.Model):
    ciclo_lectivo = models.IntegerField()
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `ciclo_lectivo`: Año del ciclo lectivo (ej: 2022, 2023)

---

#### 1.3 Curso
Representa un curso específico (combinación de año y división).

```python
class Curso(models.Model):
    curso = models.CharField(max_length=5)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `curso`: Identificador del curso (ej: "1A", "2B", "7B")
- `carrera`: Relación con Carrera (FK)

**Relaciones:**
- `carrera` → `Carrera` (Many-to-One)

**Cursos Actuales:**
- División A: 1A, 2A, 3A, 4A, 5A, 6A (Economía)
- División B: 1B, 2B, 3B, 4B, 5B, 6B, 7B (Técnica en Programación)

---

#### 1.4 Materia
Representa una asignatura o materia del plan de estudios.

```python
class Materia(models.Model):
    nombre = models.CharField(max_length=50)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    horas = models.IntegerField()
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `nombre`: Nombre de la materia
- `curso`: Relación con Curso (FK)
- `horas`: Cantidad de horas semanales

**Relaciones:**
- `curso` → `Curso` (Many-to-One)
- ← `Docente` (Many-to-Many)

---

### 2. Módulo Docentes (`docentes.models`)

#### 2.1 Docente
Representa a los profesores de la institución.

```python
class Docente(models.Model):
    legajo = models.IntegerField()
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20)
    nacionalidad = models.CharField(max_length=20)
    materia = models.ManyToManyField(Materia)
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `legajo`: Número de legajo del docente
- `nombre`: Nombre del docente
- `apellido`: Apellido del docente
- `dni`: Documento Nacional de Identidad (opcional)
- `email`: Correo electrónico (único, opcional)
- `direccion`: Dirección física (opcional)
- `telefono`: Número de teléfono
- `nacionalidad`: Nacionalidad del docente
- `materia`: Materias que imparte (Many-to-Many)

**Relaciones:**
- `materia` → `Materia` (Many-to-Many)

**Nota:** El campo `email` se utiliza como identificador único al importar datos.

---

### 3. Módulo Alumnos (`alumnos.models`)

#### 3.1 Padre
Información del padre del alumno.

```python
class Padre(models.Model):
    nombre_padre = models.CharField(max_length=50)
    apellido_padre = models.CharField(max_length=50)
    dni_padre = models.IntegerField(null=True, blank=True)
    direccion_padre = models.CharField(max_length=100, null=True, blank=True)
    telefono_padre = models.CharField(max_length=20)
    nacionalidad_padre = models.CharField(max_length=20)
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `nombre_padre`: Nombre del padre
- `apellido_padre`: Apellido del padre
- `dni_padre`: DNI del padre (opcional)
- `direccion_padre`: Dirección (opcional)
- `telefono_padre`: Teléfono de contacto
- `nacionalidad_padre`: Nacionalidad

---

#### 3.2 Madre
Información de la madre del alumno.

```python
class Madre(models.Model):
    nombre_madre = models.CharField(max_length=50)
    apellido_madre = models.CharField(max_length=50)
    dni_madre = models.IntegerField(null=True, blank=True)
    direccion_madre = models.CharField(max_length=100, null=True, blank=True)
    telefono_madre = models.CharField(max_length=20)
    nacionalidad_madre = models.CharField(max_length=20)
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `nombre_madre`: Nombre de la madre
- `apellido_madre`: Apellido de la madre
- `dni_madre`: DNI de la madre (opcional)
- `direccion_madre`: Dirección (opcional)
- `telefono_madre`: Teléfono de contacto
- `nacionalidad_madre`: Nacionalidad

---

#### 3.3 Tutor
Información del tutor o responsable legal del alumno.

```python
class Tutor(models.Model):
    nombre_tutor = models.CharField(max_length=50)
    apellido_tutor = models.CharField(max_length=50)
    dni_tutor = models.IntegerField(null=True, blank=True)
    direccion_tutor = models.CharField(max_length=100, null=True, blank=True)
    telefono_tutor = models.CharField(max_length=20)
    nacionalidad_tutor = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Tutores"
```

**Campos:**
- `id`: Clave primaria (auto-generada)
- `nombre_tutor`: Nombre del tutor
- `apellido_tutor`: Apellido del tutor
- `dni_tutor`: DNI del tutor (opcional)
- `direccion_tutor`: Dirección (opcional)
- `telefono_tutor`: Teléfono de contacto
- `nacionalidad_tutor`: Nacionalidad

---

#### 3.4 Alumno
Representa a los estudiantes de la institución.

```python
class Alumno(models.Model):
    legajo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.IntegerField(null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    direccion = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    nacionalidad = models.CharField(max_length=20, null=True, blank=True)
    padre = models.ForeignKey(Padre, null=True, blank=True, on_delete=models.CASCADE)
    madre = models.ForeignKey(Madre, null=True, blank=True, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    libre = models.BooleanField(default=False)
    condicional = models.BooleanField(default=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
```

**Campos:**
- `legajo`: Número de legajo (PK, auto-generado)
- `nombre`: Nombre del alumno
- `apellido`: Apellido del alumno
- `dni`: Documento Nacional de Identidad (opcional)
- `email`: Correo electrónico (opcional)
- `direccion`: Dirección física (opcional)
- `telefono`: Número de teléfono (opcional)
- `nacionalidad`: Nacionalidad (opcional)
- `padre`: Referencia al padre (FK, opcional)
- `madre`: Referencia a la madre (FK, opcional)
- `tutor`: Referencia al tutor (FK, opcional)
- `activo`: Indica si el alumno está activo (por defecto: True)
- `libre`: Indica si el alumno está libre (por defecto: False)
- `condicional`: Indica si el alumno está condicional (por defecto: False)
- `curso`: Curso al que pertenece (FK, requerido)

**Relaciones:**
- `curso` → `Curso` (Many-to-One, requerido)
- `padre` → `Padre` (Many-to-One, opcional)
- `madre` → `Madre` (Many-to-One, opcional)
- `tutor` → `Tutor` (Many-to-One, opcional)

---

## Relaciones entre Modelos

### Jerarquía Académica

```
Carrera (1) ──┐
              ↓
           Curso (N) ──┐
                       ↓
                   Materia (N) ←──── (M:N) ───→ Docente (M)
                       ↑
                       │
                   Alumno (N)
```

### Relaciones Familiares

```
Alumno (1) ──→ Padre (0..1)
          ├──→ Madre (0..1)
          └──→ Tutor (0..1)
```

### Descripción de Relaciones

| Desde     | Relación | Hacia    | Tipo        | Descripción                                    |
|-----------|----------|----------|-------------|------------------------------------------------|
| Curso     | →        | Carrera  | Many-to-One | Cada curso pertenece a una carrera             |
| Materia   | →        | Curso    | Many-to-One | Cada materia se dicta en un curso específico   |
| Docente   | ↔        | Materia  | Many-to-Many| Un docente puede dictar varias materias        |
| Alumno    | →        | Curso    | Many-to-One | Cada alumno pertenece a un curso               |
| Alumno    | →        | Padre    | Many-to-One | Relación opcional con información del padre    |
| Alumno    | →        | Madre    | Many-to-One | Relación opcional con información de la madre  |
| Alumno    | →        | Tutor    | Many-to-One | Relación opcional con información del tutor    |

---

## Datos Importados

### Proceso de Importación (21/11/2025)

**Base de datos recreada desde cero:**
- Se eliminó la base de datos existente (`db.sqlite3`)
- Se ejecutaron todas las migraciones para crear el esquema limpio
- Se importaron los datos desde los archivos CSV

Los datos fueron importados exitosamente desde los siguientes archivos CSV:

1. **Legajo Docente - Legajo.csv** → Tabla `Docente`
   - 83 docentes importados

2. **Legajo Docente - DocenteMateria.csv** → Tablas `Materia` y relación `Docente-Materia`
   - 159 materias creadas
   - Relaciones docente-materia establecidas

3. **Legajo Estudiantes 2022 - LegajoGral.csv** → Tabla `Alumno`
   - 396 alumnos importados (año lectivo 2022)
   - Algunos alumnos no se importaron por tener cursos no estándar en el CSV

### Estructura Creada

#### Carreras
1. Bachillerato con orientación en Economía
2. Técnico en Programación

#### Cursos por División

**División A (Economía):**
- 1A, 2A, 3A, 4A, 5A, 6A

**División B (Técnica en Programación):**
- 1B, 2B, 3B, 4B, 5B, 6B, 7B

---

## Script de Importación

El script de importación se encuentra en: `/scripts/import_data.py`

### Ejecución del Script

```bash
# Opción 1: Recrear base de datos desde cero (recomendado)
rm -f db.sqlite3
source venv/bin/activate
python manage.py migrate
python scripts/import_data.py

# Opción 2: El script limpia automáticamente los datos existentes
source venv/bin/activate
python scripts/import_data.py
```

### Funciones del Script

0. **`limpiar_datos()`**: Elimina todos los datos existentes de la base de datos
   - Se ejecuta automáticamente al inicio
   - Muestra un resumen de los registros que se eliminarán
   - Respeta las dependencias de claves foráneas para evitar errores

1. **`crear_estructura_base()`**: Crea carreras, años y cursos
   - Crea las 2 carreras principales
   - Crea el año lectivo 2022
   - Crea los 13 cursos (1A-6A, 1B-7B)

2. **`importar_docentes()`**: Importa información de docentes
   - Lee el archivo CSV de docentes
   - Usa el email como identificador único

3. **`importar_materias()`**: Importa materias y asigna docentes
   - Crea las materias con 3 horas semanales por defecto
   - Establece la relación Many-to-Many entre docentes y materias

4. **`importar_alumnos()`**: Importa información de alumnos
   - Identifica alumnos por email o DNI cuando están disponibles
   - Asigna cada alumno a su curso correspondiente

### Notas Importantes

- Los docentes se identifican por su **email único**
- Los alumnos se vinculan por **email** o **DNI** cuando están disponibles
- Las materias se crean con **3 horas semanales** por defecto
- Algunos alumnos no se importaron debido a cursos inexistentes en el CSV

---

## Notas Técnicas

### Migraciones Aplicadas

Se crearon las siguientes migraciones para agregar el campo `email`:

- `alumnos/migrations/0002_alumno_email.py`
- `docentes/migrations/0002_docente_email.py`

### Base de Datos

- Motor: SQLite (por defecto en Django)
- Ubicación: `db.sqlite3`

### Dependencias

- Django
- django-smart-selects (para campos encadenados)

---

## Próximos Pasos Sugeridos

1. ✅ Importar datos de padres/madres/tutores (actualmente opcional)
2. ✅ Completar información de horas cátedra por materia
3. ✅ Implementar módulos de:
   - Asistencias
   - Calificaciones
   - Observaciones
4. ✅ Crear reportes y estadísticas
5. ✅ Implementar sistema de autenticación y permisos

---

**Documento generado automáticamente**  
**Sistema ALCAL - Sagrado Corazón ALCAL**
