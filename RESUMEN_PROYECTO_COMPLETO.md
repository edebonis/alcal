# 📚 Resumen Completo del Proyecto ALCAL

**Fecha de análisis:** 2025-01-XX  
**Sistema:** ALCAL - Administración de Legajos Escolares del Colegio Sagrado Corazón

---

## 🎯 Visión General

ALCAL es un sistema de gestión académica desarrollado en **Django 4.2** para gestionar:
- ✅ Asistencias de alumnos (multi-turno)
- ✅ Calificaciones (trimestrales y parciales)
- ✅ Observaciones
- ✅ Gestión de alumnos, docentes, cursos y materias
- ✅ Cierre diario de asistencias con reglas complejas

---

## 🏗️ Arquitectura del Sistema

### Estructura de Aplicaciones Django

```
alcal/                    # Proyecto principal
├── alcal/                # Configuración global
│   ├── settings.py       # Configuración (SQLite, DEBUG=True, ALLOWED_HOSTS=['*'])
│   ├── urls.py           # URLs centralizadas
│   ├── views.py          # Vistas de selectores y home
│   └── models.py         # PerfilUsuario (roles)
│
├── escuela/              # Estructura académica
│   └── models.py         # Carrera, Anio, Curso, Materia
│
├── docentes/             # Gestión de docentes
│   └── models.py         # Docente (con ManyToMany a Materia)
│
├── alumnos/              # Gestión de alumnos
│   └── models.py         # Alumno, Padre, Madre, Tutor
│
├── asistencias/          # Sistema de asistencias
│   ├── models.py         # Asistencia, Turno, CodigoAsistencia, CierreDiario, ReglaAsistencia
│   ├── views.py          # Toma y consulta de asistencias
│   └── services.py       # Lógica de negocio
│
├── calificaciones/       # Sistema de calificaciones
│   └── models.py         # CalificacionTrimestral, CalificacionParcial, Instancia
│
├── observaciones/        # Observaciones de alumnos
│   └── models.py         # Observacion, TipoObservacion
│
└── administracion/       # Panel CRUD personalizado
    ├── views.py          # Vistas CRUD para todas las entidades
    └── urls.py           # URLs con namespace 'administracion:'
```

---

## 📊 Modelos de Datos Principales

### 1. Estructura Académica (`escuela/`)

#### Carrera
- `nombre`: Nombre de la carrera
- Ejemplos: "Bachillerato con orientación en Economía", "Técnico en Programación"

#### Anio
- `ciclo_lectivo`: Año del ciclo (ej: 2022, 2025)

#### Curso
- `curso`: Identificador (ej: "1A", "2B", "7B")
- `carrera`: ForeignKey a Carrera

#### Materia
- `nombre`: Nombre de la materia
- `curso`: ForeignKey a Curso
- `horas`: Horas semanales

---

### 2. Docentes (`docentes/`)

#### Docente
**Campos principales:**
- `legajo_numero`: Número de legajo (CharField)
- `nombre`, `apellido`: Datos personales
- `dni`, `email` (único), `telefono`, `celular`
- `sexo`: M/F
- `fecha_nacimiento`, `nacionalidad`
- `fecha_alta`, `fecha_baja`
- `activo`: Boolean
- `cargo`: DOCENTE, DIRECTOR, VICEDIRECTOR, PRECEPTOR, etc.
- `modalidad`: TECNICA, ECONOMIA, AMBAS
- `anios_antiguedad`, `meses_antiguedad`
- `horas_totales`, `horas_extension`
- `es_titular`, `es_suplente`
- `materia`: ManyToManyField a Materia

**Relación:** Un docente puede dictar múltiples materias, una materia puede tener múltiples docentes.

---

### 3. Alumnos (`alumnos/`)

#### Alumno
**Campos principales:**
- `legajo`: AutoField (PK)
- `nombre`, `apellido`, `dni`
- `documento_tipo`: DNI, etc.
- `sexo`: M/F
- `fecha_nacimiento`, `lugar_nacimiento`, `nacionalidad`
- `email`, `direccion`, `localidad`, `telefono`, `celular_alumno`
- `padre`, `madre`, `tutor`: ForeignKeys opcionales
- `curso`: ForeignKey a Curso (requerido)
- `grupo`: 'unico', '1', '2'
- `fecha_ingreso`, `colegio_procedencia`
- `activo`, `libre`, `condicional`
- `fecha_baja`
- `dispensa`, `motivo_dispensa`
- `porcentaje_beca`
- `observaciones_admin`

#### Padre, Madre, Tutor
- Campos similares: nombre, apellido, dni, direccion, telefono, celular, email, profesion, nacionalidad
- Tutor tiene adicional: `vinculo_tutor`

---

### 4. Asistencias (`asistencias/`)

#### CodigoAsistencia
- `codigo`: P, t, T, A, r, R
- `descripcion`: Texto descriptivo
- `cantidad_falta`: Float (0.0, 0.5, 1.0)

#### Turno
- `nombre`: 'mañana', 'tarde', 'educacion_fisica'
- `hora_inicio`, `hora_fin`: TimeField

#### Asistencia
- `ciclo_lectivo`: ForeignKey a Anio
- `curso`: ForeignKey a Curso
- `alumno`: ChainedForeignKey a Alumno (filtrado por curso)
- `codigo`: ForeignKey a CodigoAsistencia
- `turno`: ForeignKey a Turno
- `fecha`: DateField
- `observaciones`: TextField
- `valor_falta_calculado`: Float (calculado en cierre)
- `procesado`: Boolean
- **Unique together:** `['alumno', 'fecha', 'turno']`

#### ReglaAsistencia
**Matriz de reglas para calcular faltas finales:**
- `codigo_manana`, `codigo_tarde`, `codigo_ed_fisica`: Códigos por turno
- `valor_falta`: Valor numérico resultante
- `observacion`: Texto explicativo
- **Unique together:** `['codigo_manana', 'codigo_tarde', 'codigo_ed_fisica']`

#### CierreDiario
- `fecha`: DateField (único)
- `fecha_cierre`: DateTimeField (auto)
- `usuario_cierre`: ForeignKey a User
- `total_asistencias_procesadas`: Integer
- `total_alumnos_procesados`: Integer
- `observaciones_cierre`: TextField

#### DetalleCierreCurso
**Configuración de qué turnos se dictaron por curso/grupo:**
- `cierre`: ForeignKey a CierreDiario
- `curso`: ForeignKey a Curso
- `grupo`: 'unico', '1', '2'
- `hubo_turno_manana`, `hubo_turno_tarde`, `hubo_turno_ed_fisica`: Boolean
- **Unique together:** `['cierre', 'curso', 'grupo']`

#### ResumenDiarioAlumno
**Resumen calculado después del cierre:**
- `cierre_diario`: ForeignKey a CierreDiario
- `alumno`: ForeignKey a Alumno
- `fecha`: DateField
- `codigo_manana`, `codigo_tarde`, `codigo_ed_fisica`: CharField
- `valor_falta_final`: Float (calculado desde ReglaAsistencia)
- `observacion_calculada`: CharField
- **Unique together:** `['alumno', 'fecha']`

---

### 5. Calificaciones (`calificaciones/`)

#### Instancia
- `instancia`: "1º Trimestre", "2º Trimestre", etc.

#### CalificacionTrimestral
- `nota`: Integer (1-10)
- `instancia`: ForeignKey a Instancia
- `curso`: ForeignKey a Curso
- `materia`: ChainedForeignKey a Materia
- `alumno`: ChainedForeignKey a Alumno
- `ciclo_lectivo`: ForeignKey a Anio
- `fecha`: DateField (auto_now_add)
- **Unique together:** `['alumno', 'materia', 'instancia', 'ciclo_lectivo']`

#### CalificacionParcial
- `nota`: Integer (1-10)
- `fecha`: DateField
- `curso`: ForeignKey a Curso
- `alumno`: ChainedForeignKey a Alumno
- `materia`: ChainedForeignKey a Materia
- `ciclo_lectivo`: ForeignKey a Anio

---

## 🛣️ URLs y Routing

### URLs Principales (`alcal/urls.py`)

#### Home y Admin
- `/` → `home()` - Dashboard principal
- `/admin/` → Django Admin
- `/grappelli/` → Grappelli admin

#### Selectores
- `/consultas/` → Selector de consultas
- `/ingresar/` → Selector de ingreso
- `/asistencia/` → Selector de asistencias
- `/calificaciones/` → Selector de calificaciones

#### Asistencias
- `/tomar_asistencia_curso/` → Toma de asistencia por curso (multi-turno)
- `/lista_alumnos_curso/` → AJAX - Lista de alumnos
- `/guardar_asistencia_curso/` → Guardar asistencias
- `/consultar_asistencia_curso/` → Consultar asistencias por curso
- `/ing_asistencia_alumno/` → Toma de asistencia individual
- `/cons_asistencia_alumno/` → Consulta de asistencia individual
- `/cierre_diario/` → Cierre diario de asistencias
- `/procesar_cierre_diario/` → Procesar cierre

#### Calificaciones
- `/ing_calificaciones/` → Ingreso de calificaciones
- `/ingresar_calificaciones_curso/` → Ingreso masivo por curso
- `/ing_calificaciones_alumno/` → Ingreso individual
- `/cons_calificaciones/` → Consulta de calificaciones
- `/consultar_calificaciones_curso/` → Consulta por curso
- `/cons_calificaciones_alumno/` → Consulta individual

#### Observaciones
- `/observaciones/` → Observaciones
- `/ing_observaciones/` → Ingreso de observaciones
- `/cons_observaciones/` → Consulta de observaciones

#### Administración (`/gestion/`)
- `/gestion/` → Dashboard de administración
- `/gestion/carreras/` → CRUD de carreras
- `/gestion/cursos/` → CRUD de cursos
- `/gestion/materias/` → CRUD de materias
- `/gestion/docentes/` → CRUD de docentes
- `/gestion/alumnos/` → CRUD de alumnos
- `/gestion/turnos/` → Lista de turnos
- `/gestion/codigos-asistencia/` → CRUD de códigos

#### API REST
- `/api/v1/` → API REST (ver `alcal/api_urls.py`)

---

## 🔐 Sistema de Autenticación y Roles

### Modelo de Usuario
- Usa `django.contrib.auth.models.User`
- Extendido con `PerfilUsuario` (app `alcal`)
- Roles: alumno, docente, preceptor, director, administrador, familiar

### Control de Acceso
- **Superuser**: Acceso total (CRUD, admin Django)
- **Staff**: Ingreso y consulta de asistencias, calificaciones, observaciones
- **Usuario regular**: Solo consulta de información propia

### Middleware
- `UserProfileMiddleware`: Gestiona perfiles de usuario
- `RoleBasedAccessMiddleware`: Control de acceso por roles

---

## 📁 Archivos CSV de Datos

### 1. Legajo Docente - Legajo.csv
- **Total registros:** 484 (incluyendo encabezado)
- **Docentes activos:** 63
- **Columnas principales:**
  - Nº de Registro, ACTIVX, APELLIDOS, NOMBRES, DOCUMENTO, EMAIL, etc.

### 2. Legajo Docente - DocenteMateria.csv
- **Total registros:** 1,500 (sin encabezado)
- **Estructura:** ID, Año, Curso, Materia, Docente, Email, ...
- **Explicación:** Cada fila es una relación única curso-materia-docente
  - La misma materia puede estar en varios cursos
  - Diferentes docentes pueden dar la misma materia
  - Un docente puede dar varias materias

### 3. Legajo Estudiantes 2022 - LegajoGral.csv
- **Total registros:** 783 (incluyendo encabezado)
- **Estudiantes activos:** 437
- **Columnas principales:**
  - ID, ACTIVX, CURSO, APELLIDO, NOMBRES, NUMERO (DNI), EMAIL, etc.

---

## 🛠️ Comandos de Gestión Disponibles

### Comandos de Setup de Datos

1. **`setup_datos_muestra`** - Carga muestra pequeña (10 docentes, 119 alumnos, 66 materias)
2. **`setup_datos_csv`** - Carga desde CSV (versión original)
3. **`setup_datos_csv_corregido`** - Carga desde CSV (versión corregida)
4. **`setup_datos_completos`** - Carga todos los datos reales
5. **`setup_datos_eficiente`** - Carga eficiente de datos
6. **`setup_datos_prueba`** - Datos de prueba simples
7. **`setup_datos_reales`** - Datos reales con lista completa
8. **`setup_simple`** - Setup simple con datos básicos
9. **`setup_sistema`** - Setup completo del sistema

### Comandos de Asistencias

1. **`setup_asistencias`** - Configura códigos y turnos
2. **`importar_reglas_asistencia`** - Importa reglas desde CSV

### Otros Comandos

1. **`crear_usuarios_demo`** - Crea usuarios de demostración

---

## 🎨 Frontend y Templates

### Template Base
- **`base_modern.html`**: Template base principal con sidebar y estilos ALCAL Premium
- Bootstrap 5.3.2
- Sistema de diseño ALCAL Premium (`alcal-premium.css`)

### Estructura de Templates
```
templates/
├── base_modern.html          # Template base
├── home.html                  # Dashboard
├── asistencia_selector.html   # Selector de asistencias
├── calificaciones_selector.html
├── consultas_selector.html
├── ingresar_selector.html
└── asistencias/               # Templates específicos de asistencias
    ├── tomar_asistencia_curso.html
    ├── consultar_asistencia_curso.html
    └── ...
```

---

## 🔄 Flujos Principales

### 1. Toma de Asistencia por Curso
```
Usuario → /tomar_asistencia_curso/
  ↓
Selecciona: fecha, curso, turnos (múltiple)
  ↓
AJAX → /lista_alumnos_curso/
  ↓
Usuario marca asistencias (P, A, T, R)
  ↓
POST → /guardar_asistencia_curso/
  ↓
Crea/actualiza Asistencia para cada alumno × cada turno
```

### 2. Cierre Diario
```
Usuario Staff → /cierre_diario/
  ↓
Selecciona: fecha, turnos, cursos/grupos
  ↓
POST → /procesar_cierre_diario/
  ↓
Calcula ResumenDiarioAlumno usando ReglaAsistencia
  ↓
Crea/actualiza CierreDiario
```

### 3. Gestión CRUD
```
Superuser → /gestion/
  ↓
Dashboard con tarjetas
  ↓
Selecciona entidad (ej: /gestion/cursos/)
  ↓
Lista con búsqueda y filtros
  ↓
CRUD: Create, Read, Update, Delete
```

---

## 📦 Dependencias Principales

- **Django 4.2**
- **django-smart-selects**: Campos encadenados
- **django-cors-headers**: CORS para API
- **djangorestframework**: API REST
- **django-extensions**: Utilidades adicionales
- **drf-spectacular**: Documentación OpenAPI
- **django-filters**: Filtros para API
- **grappelli**: Mejoras al admin de Django

---

## 🗄️ Base de Datos

- **Desarrollo:** SQLite (`db.sqlite3`)
- **Producción recomendado:** PostgreSQL
- **Ubicación:** `BASE_DIR / 'db.sqlite3'`

---

## 🚀 Cómo Ejecutar

### Desarrollo Local
```bash
cd /home/esteban/Documentos/alcal
source venv/bin/activate
python manage.py runserver 0.0.0.0:8008
```

### Acceso desde Red Local
```bash
python start_server.py
```
- Detecta IP automáticamente
- Usa puerto 8008
- Muestra URLs de acceso

### Cargar Datos
```bash
# Muestra pequeña
python manage.py setup_datos_muestra --reset

# Desde CSV (si está implementado)
python manage.py setup_datos_csv_corregido --reset

# Script original
python scripts/import_data.py
```

---

## 📊 Estado Actual del Sistema

### Datos en Base de Datos (última ejecución)
- ✅ 12 Cursos
- ✅ 10 Docentes (muestra)
- ✅ 66 Materias
- ✅ 119 Alumnos (muestra)
- ✅ 3 Códigos de Asistencia
- ✅ 2 Turnos

### Datos Reales Disponibles (CSV)
- 📁 63 Docentes activos
- 📁 437 Estudiantes activos
- 📁 1,500 Relaciones materia-docente-curso
- 📁 13 Cursos únicos

---

## 🔍 Características Especiales

### 1. Sistema de Asistencias Multi-Turno
- Permite tomar asistencia para varios turnos simultáneamente
- Soporta: Mañana, Tarde, Educación Física
- Cálculo automático de faltas usando `ReglaAsistencia`

### 2. Cierre Parcial
- Permite cerrar solo algunos cursos
- Permite actualizar cierres existentes
- Calcula `ResumenDiarioAlumno` automáticamente

### 3. Campos Encadenados (ChainedForeignKey)
- Al seleccionar un curso, los alumnos y materias se filtran automáticamente
- Usa `django-smart-selects`

### 4. Panel de Administración Personalizado
- CRUD completo para todas las entidades
- Solo accesible para superusers
- Templates consistentes con Bootstrap 5

---

## 📝 Notas Importantes

1. **Campo `legajo_numero` en Docente**: No es `legajo` (IntegerField), es `legajo_numero` (CharField)

2. **Relación Docente-Materia**: ManyToMany, un docente puede dictar múltiples materias

3. **1,500 registros en DocenteMateria.csv**: Son combinaciones únicas de curso-materia-docente, no duplicados

4. **Cierre Diario**: Sistema complejo que calcula faltas finales usando reglas de combinación de turnos

5. **Calificaciones**: Dos tipos - Trimestrales (por instancia) y Parciales (por fecha)

---

## 🎯 Próximos Pasos Sugeridos

1. ✅ Cargar todos los datos reales desde CSV sin duplicados
2. ✅ Implementar importación completa de padres/madres/tutores
3. ✅ Completar sistema de reportes PDF
4. ✅ Mejorar validaciones en formularios
5. ✅ Implementar tests automatizados
6. ✅ Migrar a PostgreSQL para producción

---

**Documento generado automáticamente**  
**Sistema ALCAL - Colegio Sagrado Corazón**

