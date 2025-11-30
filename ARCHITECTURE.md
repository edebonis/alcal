# ALCAL - Arquitectura del Sistema

**Última actualización**: 2025-11-30

---

## 📋 Visión General

ALCAL es un sistema de gestión académica desarrollado en Django 4.2 para instituciones educativas. Gestiona asistencias, calificaciones, observaciones de alumnos y administración de datos escolares.

### Tecnologías Principales

- **Backend**: Django 4.2 (Python)
- **Base de datos**: SQLite (desarrollo), PostgreSQL (producción recomendado)
- **Frontend**: Bootstrap 5.3.2 + ALCAL Premium Design System
- **Template Engine**: Django Template Language
- **Admin UI**: Grappelli + Django Admin

---

## 🏗️ Estructura del Proyecto

```
alcal/
├── alcal/                      # Proyecto Django principal
│   ├── settings.py            # Configuración global
│   ├── urls.py                # URLs principales (punto de entrada)
│   ├── views.py               # Vistas principales (selectores, home)
│   ├── wsgi.py / asgi.py     # Servidores de aplicación
│   └── api_urls.py            # Rutas de API REST
│
├── asistencias/               # App: Gestión de asistencias
│   ├── models.py              # Asistencia, Turno, CodigoAsistencia, CierreDiario
│   ├── views.py               # Vistas de toma y consulta de asistencias
│   ├── templates/             # Templates propios de asistencias
│   └── urls.py                # (No usado, las URLs están en alcal/urls.py)
│
├── administracion/            # App: CRUD de entidades escolares
│   ├── models.py              # (Usa modelos de otras apps)
│   ├── views.py               # Vistas CRUD para carreras, cursos, materias, etc.
│   ├── forms.py               # Formularios ModelForm
│   ├── urls.py                # URLs con namespace 'administracion:'
│   └── templates/             # Templates de gestión CRUD
│
├── alumnos/                   # App: Modelo Alumno
│   ├── models.py              # Alumno (legajo, datos personales, curso)
│   └── admin.py               # Configuración del admin
│
├── escuela/                   # App: Estructura escolar
│   ├── models.py              # Carrera, Curso, Anio (año lectivo)
│   └── admin.py
│
├── calificaciones/            # App: Gestión de notas
│   ├── models.py              # Calificacion, TipoEvaluacion
│   ├── views.py               # Vistas de ingreso y consulta de notas
│   └── templates/
│
├── templates/                 # Templates globales
│   ├── base_modern.html       # **Template base principal** (sidebar, estilos)
│   ├── home.html              # Página de inicio
│   ├── asistencia_selector.html
│   ├── calificaciones_selector.html
│   ├── consultas_selector.html
│   ├── ingresar_selector.html
│   └── observaciones.html
│
├── static/                    # Archivos estáticos
│   ├── css/
│   │   └── alcal-premium.css  # Sistema de diseño ALCAL
│   ├── js/
│   └── images/
│       └── logo-alcal.png
│
├── .agent/                    # Documentación y workflows del agente
│   ├── project_rules.md       # Reglas y convenciones del proyecto
│   └── workflows/             # Workflows definidos
│
├── docs/                      # Documentación del proyecto
│   ├── adr/                   # Architecture Decision Records
│   └── REPORTE_*.md           # Reportes de desarrollo
│
├── venv/                      # Entorno virtual Python
├── manage.py                  # CLI de Django
├── requirements.txt           # Dependencias Python
└── check_templates.py         # Script de validación de templates

```

---

## 📦 Apps y Responsabilidades

### 1. `alcal/` (Proyecto principal)
- **Responsabilidad**: Configuración global, URLs principales, vistas de selectores
- **URLs**: `/`, `/consultas/`, `/ingresar/`, `/asistencia/`, `/calificaciones/`
- **Vistas clave**: 
  - `home()`: Dashboard principal
  - `consultas_selector()`: Selector de consultas
  - `ingresar_selector()`: Selector de ingreso
  - `asistencia_selector()`: Selector de asistencias
  - `calificaciones_selector()`: Selector de calificaciones

### 2. `asistencias/`
- **Responsabilidad**: Gestión completa de asistencias (toma, consulta, cierre diario)
- **Modelos**: 
  - `Asistencia`: Registro de asistencia de un alumno en una fecha/turno
  - `Turno`: Turnos del día (Mañana, Tarde, Noche)
  - `CodigoAsistencia`: Códigos (P=Presente, F=Falta, T=Tardanza, J=Justificado)
  - `CierreDiario`: Cierre diario de asistencias
  - `DetalleCierreCurso`: Detalle del cierre por curso
- **URLs clave**:
  - `/tomar_asistencia_curso/`: Tomar asistencia por curso (multi-turno)
  - `/lista_alumnos_curso/`: AJAX - Cargar lista de alumnos
  - `/guardar_asistencia_curso/`: Guardar asistencias
  - `/consultar_asistencia_curso/`: Consultar asistencias
  - `/ing_asistencia_alumno/`: Tomar asistencia individual
  - `/cierre_diario/`: Cierre diario de asistencias
- **Características especiales**:
  - Soporte multi-turno: permite tomar asistencia para varios turnos simultáneamente
  - Cierre parcial: permite cerrar solo algunos cursos
  - Actualización de cierres existentes

### 3. `administracion/`
- **Responsabilidad**: CRUD de entidades escolares (solo superusers)
- **Namespace**: `administracion:`
- **Entidades gestionadas**:
  - Carreras (`/gestion/carreras/`)
  - Cursos (`/gestion/cursos/`)
  - Materias (`/gestion/materias/`)
  - Docentes (`/gestion/docentes/`)
  - Alumnos (`/gestion/alumnos/`)
  - Turnos (`/gestion/turnos/`)
  - Códigos de Asistencia (`/gestion/codigos/`)
- **URLs**: `/gestion/*`
- **Templates**: Sistema consistente con `list.html`, `form.html`, `detail.html`, `delete.html`

### 4. `alumnos/`
- **Responsabilidad**: Modelo de datos de alumnos
- **Modelo principal**: `Alumno`
  - Campos: legajo, nombre, apellido, curso, grupo, datos de contacto, estado (activo, libre, condicional)
- **Relaciones**: 
  - `ForeignKey` a `Curso`
  - `OneToMany` desde `Asistencia`
  - `OneToMany` desde `Calificacion`

### 5. `escuela/`
- **Responsabilidad**: Estructura organizativa de la escuela
- **Modelos**:
  - `Carrera`: Carreras ofrecidas (ej: Técnico en Programación)
  - `Curso`: Cursos específicos (año + carrera + grupo)
  - `Anio`: Año lectivo
- **Relaciones**: `Carrera` ← `Curso` ← `Alumno`

### 6. `calificaciones/`
- **Responsabilidad**: Gestión de notas y evaluaciones
- **Modelos**:
  - `Calificacion`: Nota de un alumno en una materia
  - `TipoEvaluacion`: Trimestre, Parcial, Final, etc.
- **URLs**: `/ing_calificaciones/`, `/cons_calificaciones/`, etc.

---

## 🎨 Sistema de Diseño

### Base Template: `base_modern.html`

**Todos los templates del sistema deben heredar de este archivo.**

**Estructura**:
```html
<!DOCTYPE html>
<html>
  <head>
    <!-- Bootstrap 5, Bootstrap Icons, FontAwesome, ALCAL Premium CSS -->
    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <div class="app-container">
      <aside class="sidebar">
        <!-- Navegación con RBAC -->
      </aside>
      <main class="main-content">
        {% block content %}{% endblock %}
      </main>
    </div>
    <!-- Bootstrap JS -->
    {% block extra_js %}{% endblock %}
  </body>
</html>
```

**Bloques disponibles**:
- `{% block title %}`: Título de la página
- `{% block content %}`: Contenido principal
- `{% block extra_css %}`: CSS adicional
- `{% block extra_js %}`: JavaScript adicional

### ALCAL Premium Design System

- **Archivo**: `static/css/alcal-premium.css`
- **Clases principales**:
  - `.btn-alcal-primary`: Botón primario
  - `.text-alcal-primary`: Texto color primario
  - `.bg-alcal-primary`: Fondo color primario
  - `.card-premium`: Card con estilo premium
  - `.sidebar`, `.sidebar-nav`, `.nav-item`: Componentes de sidebar

### Componentes Bootstrap 5 Utilizados

- **Cards**: `.card`, `.card-header`, `.card-body`, `.card-footer`
- **Tables**: `.table`, `.table-hover`, `.table-responsive`, `.align-middle`
- **Buttons**: `.btn`, `.btn-primary`, `.btn-outline-*`, `.btn-sm`, `.btn-lg`
- **Forms**: `.form-control`, `.form-select`, `.form-label`, `.form-check`
- **Alerts**: `.alert`, `.alert-success`, `.alert-danger`, `.alert-info`, `.alert-warning`
- **Badges**: `.badge`, `.bg-success`, `.bg-danger`

---

## 🛣️ Routing y URLs

### Estrategia de Routing

**Centralizado**: Todas las URLs principales están en `alcal/urls.py`. Solo `administracion` tiene su propio `urls.py` con namespace.

### Convenciones de Nombres

| Tipo | Convención | Ejemplo |
|------|-----------|---------|
| Selectores | `*_selector` | `asistencia_selector`, `consultas_selector` |
| Acciones de ingreso | `tomar_*`, `ingresar_*` | `tomar_asistencia_curso`, `ingresar_calificaciones` |
| Acciones de consulta | `consultar_*`, `cons_*` | `consultar_asistencia_curso`, `cons_calificaciones` |
| Guardado | `guardar_*` | `guardar_asistencia_curso` |
| CRUD admin | `administracion:*_list`, `administracion:*_create`, etc. | `administracion:curso_list` |
| AJAX endpoints | Mismo nombre que vista | `lista_alumnos_curso` |

### Mapa de URLs Principal

Ver [project_rules.md - URLs principales](/.agent/project_rules.md#urls-principales-memorizar)

---

## 🔐 Seguridad y Control de Acceso

### Modelo de Roles

| Rol | Capacidades |
|-----|-------------|
| **Superuser** | Acceso total (CRUD, admin Django, configuración) |
| **Staff** | Ingreso y consulta de asistencias, calificaciones, observaciones |
| **Usuario regular** | Solo consulta de calificaciones propias (estudiantes/padres) |

### RBAC en Sidebar (`base_modern.html`)

```django
<!-- Todos los usuarios autenticados -->
Dashboard, Asistencias, Calificaciones

<!-- Solo Staff o Superuser -->
{% if user.is_staff or user.is_superuser %}
  Observaciones, Cierre Diario
{% endif %}

<!-- Solo Superuser -->
{% if user.is_superuser %}
  Gestión (CRUD), Admin Django
{% endif %}
```

### Decoradores de Vista

- **Todas las vistas** (excepto home/login): `@login_required`
- **Vistas de modificación**: Validación adicional de `user.is_staff` si aplica

---

## 💾 Modelo de Datos

### Diagrama de Relaciones Principal

```
Carrera
  |
  ├── 1:N → Curso
  |           |
  |           ├── 1:N → Alumno
  |           |           |
  |           |           ├── 1:N → Asistencia
  |           |           └── 1:N → Calificacion
  |           |
  |           └── 1:N → Asistencia
  |
  └── 1:N → Materia
              |
              └── 1:N → Calificacion

Turno
  |
  └── 1:N → Asistencia

CodigoAsistencia
  |
  └── 1:N → Asistencia

Anio (año lectivo)
  |
  └── 1:N → Asistencia, Calificacion, Curso
```

### Modelos Críticos

#### `Alumno` (app: `alumnos`)
- Datos personales y de contacto
- Relación con `Curso` (año + carrera + grupo)
- Estados: activo, libre, condicional

#### `Asistencia` (app: `asistencias`)
- Registro diario de presencia
- Claves: alumno, curso, fecha, turno
- `codigo`: ForeignKey a `CodigoAsistencia`

#### `Curso` (app: `escuela`)
- Representa un curso específico (ej: "1° A - Técnico en Programación")
- Campos: curso (año), carrera, grupo, anio_lectivo

#### `CierreDiario` (app: `asistencias`)
- Cierre diario de asistencias
- Permite cierre parcial (solo algunos cursos)
- Permite actualización de cierres existentes

---

## 🔄 Flujos Principales

### 1. Toma de Asistencia por Curso

```
Usuario → /tomar_asistencia_curso/
  ↓
Selecciona: fecha, curso, turnos (múltiple)
  ↓
JavaScript AJAX → /lista_alumnos_curso/?curso_id=X&fecha=Y&turno_id=1,2
  ↓
Vista devuelve HTML con lista de alumnos y botones de código
  ↓
Usuario marca asistencias (P, F, T, J)
  ↓
Submit → /guardar_asistencia_curso/
  ↓
Vista crea/actualiza Asistencia para cada alumno × cada turno
  ↓
Mensaje de éxito + Redirect a /tomar_asistencia_curso/
```

### 2. Cierre Diario

```
Usuario Staff → /cierre_diario/
  ↓
Selecciona: fecha
  ↓
Sistema carga cursos y turnos disponibles
  ↓
Usuario selecciona: turnos, cursos/grupos a cerrar (parcial OK)
  ↓
Submit → /procesar_cierre_diario/
  ↓
Vista verifica si existe cierre para esa fecha
  ↓
Si existe: actualiza con update_or_create + mensaje de advertencia
Si no existe: crea nuevo cierre
  ↓
Mensaje de éxito
```

### 3. CRUD de Administración

```
Superuser → /gestion/
  ↓
Dashboard con tarjetas de cada entidad
  ↓
Selecciona entidad (ej: /gestion/cursos/)
  ↓
Lista con búsqueda, paginación, filtros
  ↓
CRUD: Create, Read, Update, Delete
  ↓
Formularios con validación
  ↓
Mensajes de feedback
```

---

## 🧪 Testing y Validación

### Scripts Disponibles

- **`check_templates.py`**: Valida sintaxis de todas las plantillas del proyecto.
- **`scripts/populate_fake_data.py`**: Genera datos de prueba (alumnos, docentes, cursos) usando `Faker`. Ideal para entornos de demo.
- **`scripts/import_data.py`**: Importa datos reales desde CSVs (requiere archivos originales).

### Comandos de Gestión

```bash
python manage.py check           # Verificar configuración
python manage.py migrate         # Aplicar migraciones
python manage.py test            # Ejecutar tests
python check_templates.py        # Validar templates
python scripts/populate_fake_data.py # Cargar datos demo
```

---

## ☁️ Despliegue y Producción

### PythonAnywhere

El proyecto está optimizado para despliegue en PythonAnywhere:

1. **Archivos Estáticos**: Se utiliza `Whitenoise` con `CompressedManifestStaticFilesStorage` para servir CSS/JS eficientemente sin necesidad de Nginx/Apache adicional.
2. **Base de Datos**: SQLite se mantiene como base de datos por defecto para facilitar el despliegue gratuito, aunque se recomienda PostgreSQL para alta concurrencia.
3. **Dependencias**: `requirements.txt` ha sido optimizado para incluir solo lo necesario.

### Configuración de Entorno

- **DEBUG**: Debe estar en `False` en producción.
- **SECRET_KEY**: Debe configurarse vía variable de entorno o `.env`.
- **ALLOWED_HOSTS**: Debe incluir el dominio de PythonAnywhere (ej: `usuario.pythonanywhere.com`).

---

## 📂 Dónde Poner Cada Cosa

| Elemento | Ubicación | Razón |
|----------|-----------|-------|
| **Nueva vista de asistencia** | `asistencias/views.py` | Responsabilidad de la app |
| **Nueva vista de calificación** | `calificaciones/views.py` | Responsabilidad de la app |
| **Nueva vista CRUD** | `administracion/views.py` | Centralización CRUD |
| **Selector de módulo** | `alcal/views.py` | Vista transversal |
| **URL principal** | `alcal/urls.py` | Centralización (excepto admin) |
| **URL de admin** | `administracion/urls.py` | Namespace `administracion:` |
| **Template global** | `templates/` | Compartido entre apps |
| **Template específico** | `{app}/templates/{app}/` | Específico de una app |
| **CSS/JS global** | `static/css/`, `static/js/` | Compartido |
| **Modelo de alumno** | `alumnos/models.py` | Responsabilidad única |
| **Modelo de asistencia** | `asistencias/models.py` | Responsabilidad única |
| **Modelo de estructura** | `escuela/models.py` | Carrera, Curso, Anio |
| **Documentación arquitectónica** | `docs/`, `ARCHITECTURE.md` | Root del proyecto |
| **ADR** | `docs/adr/` | Decisiones documentadas |
| **Reglas de proyecto** | `.agent/project_rules.md` | Configuración del agente |
| **Workflows** | `.agent/workflows/` | Procesos repetibles |

---

## 🚀 Decisiones Arquitectónicas Importantes

Ver archivos ADR en `docs/adr/` para detalles:

1. **Uso de Django Template Language** (vs Jinja2)
2. **Centralización de URLs** en `alcal/urls.py`
3. **Bootstrap 5 como framework CSS**
4. **Sistema de diseño ALCAL Premium**
5. **RBAC en sidebar** mediante `user.is_staff` / `user.is_superuser`
6. **Multi-turno en asistencias** (parámetro `turno_id` como CSV)
7. **Cierre parcial de asistencias** (no obligatorio cerrar todos los cursos)

---

## 📈 Escalabilidad y Mejoras Futuras

### Optimizaciones Recomendadas

- **Base de datos**: Migrar a PostgreSQL en producción
- **Caché**: Implementar Redis para sesiones y queries repetitivas
- **API REST**: Expandir `api_urls.py` para integración móvil
- **Tests**: Aumentar cobertura de tests unitarios y de integración
- **CI/CD**: Implementar pipeline automático de deploy
- **Logging**: Configurar logging estructurado (JSON) para monitoreo

### Extensiones Posibles

- Módulo de mensajería interna
- Generación de reportes PDF
- Integración con sistemas de pago
- App móvil (usando Django REST Framework)
- Dashboard analítico con gráficos interactivos

---

**Mantenido por**: Equipo de desarrollo ALCAL  
**Para consultas**: Ver `.agent/project_rules.md` y `docs/adr/`
