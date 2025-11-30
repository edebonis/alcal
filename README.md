# Sistema ALCAL - Sagrado Corazón ALCAL

Sistema de Administración de Legajos Escolares para el Sagrado Corazón ALCAL.

## 📋 Descripción

ALCAL es un sistema de gestión escolar desarrollado en Django que permite administrar:
- Información de docentes y sus materias
- Datos de alumnos y sus familias
- Estructura académica (carreras, cursos, materias)
- **Sistema de grupos** para materias técnico-específicas
- Asistencias (con soporte multi-turno)
- Calificaciones
- Observaciones
- Generación de reportes PDF

## 🏫 Estructura Académica

El colegio ofrece dos carreras:

1. **Bachillerato con orientación en Economía** (6 años)
   - Cursos: 1A, 2A, 3A, 4A, 5A, 6A

2. **Técnico en Programación** (7 años)
   - Cursos: 1B, 2B, 3B, 4B, 5B, 6B, 7B
   - **Materias técnico-específicas**: Algunas materias dividen el curso en Grupo 1 y Grupo 2
   - Cada grupo puede tener un docente diferente y horarios distintos

## 📊 Estado Actual

## 📊 Estado Actual

**Base de datos actualizada al: 30/11/2025**

- ✅ 2 Carreras
- ✅ 13 Cursos
- ✅ Gestión completa de Docentes y Alumnos
- ✅ Sistema de Asistencias y Calificaciones funcional
- ✅ Despliegue en PythonAnywhere configurado

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.10+
- pip
- virtualenv (opcional pero recomendado)

### Instalación

#### 🐧 Linux / macOS

```bash
# 1. Clonar el repositorio
git clone https://github.com/edebonis/alcal.git
cd alcal

# 2. Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser
```

#### 🪟 Windows

```powershell
# 1. Clonar el repositorio
git clone https://github.com/edebonis/alcal.git
cd alcal

# 2. Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar base de datos
python manage.py migrate

# 5. Crear superusuario (opcional)
python manage.py createsuperuser
```

### Datos de Prueba (Demo)

Para probar el sistema sin necesidad de los archivos CSV reales, puedes generar datos ficticios:

```bash
# Genera alumnos, docentes, cursos y materias con datos falsos
python scripts/populate_fake_data.py
```

### Importar Datos Reales (Legacy)

Si cuentas con los archivos CSV originales (`Legajo Docente - Legajo.csv`, etc.):

```bash
python scripts/import_data.py
```

### Ejecutar el Servidor

```bash
python manage.py runserver 8008
```

Acceder a: http://localhost:8008

## ☁️ Despliegue (PythonAnywhere)

Este proyecto está configurado para desplegarse fácilmente en [PythonAnywhere](https://www.pythonanywhere.com/).

1. **Configuración**: Usa `Whitenoise` para estáticos.
2. **WSGI**: Configurar el archivo WSGI apuntando a `alcal.settings`.
3. **Base de Datos**: SQLite es persistente y soportada por defecto.

Ver `ARCHITECTURE.md` para más detalles de despliegue.

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

**Sistema ALCAL** - Sagrado Corazón ALCAL  
Desarrollado con Django
