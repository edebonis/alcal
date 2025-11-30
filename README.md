# Sistema ALCAL - Colegio Sagrado Corazón

Sistema de Administración de Legajos Escolares para el Colegio Sagrado Corazón de Alcalá.

## 📋 Descripción

ALCAL es un sistema de gestión escolar desarrollado en Django que permite administrar:
- Información de docentes y sus materias
- Datos de alumnos y sus familias
- Estructura académica (carreras, cursos, materias)
- Asistencias
- Calificaciones
- Observaciones

## 🏫 Estructura Académica

El colegio ofrece dos carreras:

1. **Bachillerato con orientación en Economía** (6 años)
   - Cursos: 1A, 2A, 3A, 4A, 5A, 6A

2. **Técnico en Programación** (7 años)
   - Cursos: 1B, 2B, 3B, 4B, 5B, 6B, 7B

## 📊 Estado Actual

**Base de datos actualizada al: 21/11/2025**

- ✅ 2 Carreras
- ✅ 13 Cursos
- ✅ 83 Docentes
- ✅ 159 Materias
- ✅ 396 Alumnos

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8+
- pip
- virtualenv (opcional pero recomendado)

### Instalación

```bash
# Clonar o acceder al directorio del proyecto
cd /home/esteban/Documentos/alcal

# Activar entorno virtual
source venv/bin/activate

# Instalar dependencias (si es necesario)
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario para el admin (opcional)
python manage.py createsuperuser
```

### Importar Datos

Para cargar los datos del colegio desde los archivos CSV:

```bash
# Opción 1: Recrear base de datos desde cero (recomendado)
rm -f db.sqlite3
python manage.py migrate
python scripts/import_data.py

# Opción 2: El script limpia automáticamente los datos existentes
python scripts/import_data.py
```

### Ejecutar el Servidor

```bash
python manage.py runserver 8008
```

Acceder a: http://localhost:8008

## 📁 Estructura del Proyecto

```
alcal/
├── alcal/              # Configuración principal del proyecto
├── alumnos/            # Aplicación de gestión de alumnos
├── asistencias/        # Aplicación de registro de asistencias
├── calificaciones/     # Aplicación de gestión de calificaciones
├── docentes/           # Aplicación de gestión de docentes
├── escuela/            # Aplicación de estructura académica
├── observaciones/      # Aplicación de observaciones
├── scripts/            # Scripts de importación y utilidades
│   └── import_data.py  # Script de importación de datos CSV
├── docs/               # Documentación
│   ├── MODELOS_DE_DATOS.md
│   └── database_erd_diagram.png
├── static/             # Archivos estáticos
├── templates/          # Templates HTML
├── db.sqlite3          # Base de datos SQLite
├── manage.py           # Script de gestión de Django
└── README.md           # Este archivo
```

## 📚 Documentación

- **[Modelos de Datos](docs/MODELOS_DE_DATOS.md)**: Documentación completa de los modelos de base de datos con diagramas ERD
- **Archivos CSV de origen**:
  - `Legajo Docente - Legajo.csv`
  - `Legajo Docente - DocenteMateria.csv`
  - `Legajo Estudiantes 2022 - LegajoGral.csv`

## 🔧 Aplicaciones Django

### Core
- **escuela**: Gestión de la estructura académica (carreras, cursos, materias, años)
- **docentes**: Gestión de información de docentes
- **alumnos**: Gestión de información de alumnos y familias

### Funcionalidades
- **asistencias**: Registro de asistencias de alumnos
- **calificaciones**: Gestión de notas y calificaciones
- **observaciones**: Registro de observaciones y comentarios

## 🗄️ Modelos Principales

### Escuela
- `Carrera`: Carreras ofrecidas
- `Anio`: Años lectivos
- `Curso`: Cursos (combinación de año y división)
- `Materia`: Asignaturas del plan de estudios

### Docentes
- `Docente`: Información de profesores

### Alumnos
- `Alumno`: Información de estudiantes
- `Padre`, `Madre`, `Tutor`: Información familiar

Ver [documentación completa de modelos](docs/MODELOS_DE_DATOS.md) para más detalles.

## 🔑 Relaciones Clave

```
Carrera (1) → Curso (N) → Materia (N) ← Docente (M)
                    ↓
                Alumno (N)
```

## 📝 Notas Importantes

- El campo `email` de docentes debe ser único
- Los alumnos se vinculan por email o DNI cuando están disponibles
- Las materias tienen 3 horas semanales por defecto
- La base de datos usa SQLite por defecto
- Los datos son del año lectivo 2022

## 🛠️ Comandos Útiles

```bash
# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Acceder a la shell de Django
python manage.py shell

# Crear superusuario
python manage.py createsuperuser

# Recolectar archivos estáticos
python manage.py collectstatic

# Ejecutar tests
python manage.py test
```

## 📞 Soporte

Para preguntas o problemas, contactar al administrador del sistema.

---

**Sistema ALCAL** - Colegio Sagrado Corazón de Alcalá  
Desarrollado con Django
