# ALCAL Project Rules & Guidelines

## 📋 Proyecto Overview
- **Nombre**: ALCAL - Sistema de Gestión Académica
- **Framework**: Django 4.2 (LTS)
- **Motor de plantillas**: Django Template Language (NO Jinja2)
- **Base de datos**: SQLite (default)
- **Frontend**: Bootstrap 5 + Custom ALCAL Premium Design System

---

## 🎯 Principios Fundamentales

### 1. NO hacer preguntas innecesarias
- **ACTUAR, no preguntar**: Si la tarea es clara, ejecutar directamente
- **SOLO preguntar** si hay ambigüedad real o falta información crítica
- Evitar: "¿Deseas que...?", "¿Quieres que ejecute...?", "¿Continúo con...?"
- **HACER** y reportar el resultado

### 2. Validación automática
- Después de cada cambio, ejecutar validaciones relevantes sin preguntar
- Ejemplo: Después de modificar templates, ejecutar `check_templates.py`
- Ejemplo: Después de modificar vistas, verificar que el servidor siga corriendo

### 3. Proactividad
- Si encuentras un error relacionado, **arréglalo** sin preguntar
- Si ves código duplicado, **refactoriza** sin preguntar
- Si hay imports faltantes, **agrégalos** sin preguntar

### 3a. CRÍTICO: Verificar archivo correcto ANTES de editar
**NUNCA editar un archivo de template/view sin verificar primero cuál es el que Django usa.**

**PROCESO OBLIGATORIO antes de editar templates:**

1. **Buscar TODOS los archivos** con ese nombre:
   ```bash
   find_by_name(Pattern="nombre_template.html", SearchDirectory="/path/to/project")
   ```

2. **Si hay MÚLTIPLES archivos** con el mismo nombre:
   - Ver la vista que lo renderiza: `grep_search` para encontrar `render(request, 'path/to/template.html')`
   - Django busca templates en este orden:
     a. `templates/` (directorio global) ← **PRIORIDAD MÁXIMA**
     b. `app/templates/` (directorio de la app)
   - **EDITAR el archivo que Django encuentra PRIMERO** según esa prioridad

3. **Verificar con browser_subagent** si es posible:
   - Usar View Source en el navegador
   - Comparar con el archivo que vas a editar
   - Si no coinciden, **DETENTE** y busca el archivo correcto

4. **NUNCA asumir** que solo hay un archivo con ese nombre

**Regla de oro**: 
```
ANTES de editar → find_by_name() → verificar cuál usa Django → editar el correcto
```

**Si editas el archivo incorrecto**:
- Has perdido tiempo valioso del usuario
- Has generado frustración innecesaria
- Has fallado en tu trabajo

**ESTO NO ES ACEPTABLE**

### 3b. Investigación exhaustiva antes de reportar
- **NUNCA** pedir al usuario que haga lo que tú puedes hacer
- **ANTES de reportar** un error, investigar TODAS las posibles causas:
  1. Logs del servidor
  2. Console del navegador (con browser_subagent si es necesario)
  3. Network tab
  4. Source code generado (View Source)
  5. Templates relacionados
  6. JavaScript cargado
  7. Middleware y settings
- **CREAR plan de investigación** exhaustivo y ejecutarlo completamente
- **SOLO preguntar** al usuario si después de investigar TODO no encuentras la causa
- **EVITAR** ciclos de "prueba esto → no funciona → prueba esto otro"

### 4. SIEMPRE revisar reglas antes de cambiar código
- **LEER** `.agent/project_rules.md` antes de cualquier modificación
- **VERIFICAR** que el cambio sigue las convenciones establecidas
- **NO duplicar** secciones, rutas o código existente

### 5. Mantener sidebar y estilos consistentes
- **TODOS los templates** deben heredar de `base_modern.html`
- **VERIFICAR** después de cada desarrollo que el sidebar aparece correctamente
- **VERIFICAR** que los estilos ALCAL Premium se aplican en toda la página
- **NO crear** templates sin sidebar o con diseño diferente

### 6. Verificación de navegación con browser
- **DESPUÉS de crear/modificar** una sección o link, verificar con browser_subagent
- **PROBAR** que el link funciona y lleva a la página correcta
- **VERIFICAR** que la página carga sin errores 404/500
- **CAPTURAR** screenshot de la página funcionando

### 7. Búsqueda y carga automática
- **TODOS los campos de búsqueda** deben funcionar "en vivo" (AJAX/JavaScript)
- **TODOS los selects de filtro** deben cargar datos automáticamente al cambiar
- **NO crear** búsquedas que requieran submit manual si es evitable
- **NO usar botones "Buscar" o "Cargar"** si se puede hacer con eventos `change`/`input`
- **USAR** eventos `change` para selects, `input` para text inputs
- **Ejemplo**: Al seleccionar curso → cargar alumnos automáticamente en la misma vista

### 8. Consistencia de secciones y rutas
- **ANTES de crear** nueva ruta, verificar en `alcal/urls.py` que no existe
- **MANTENER** nombres consistentes: `*_selector`, `tomar_*`, `consultar_*`, etc.
- **NO duplicar** funcionalidad existente
- **AGRUPAR** rutas relacionadas con comentarios claros

### 9. Revisar rutas y documentación
- **ANTES de crear** nueva funcionalidad, revisar `ARCHITECTURE.md` para ubicación correcta
- **CONSULTAR** `docs/adr/` para entender decisiones arquitectónicas previas
- **VERIFICAR** que la nueva funcionalidad sigue la estructura existente
- **NO crear** nuevas carpetas/apps sin justificación documentada

### 10. Mantener documentación actualizada
- **DESPUÉS de cambios** arquitectónicos, actualizar `ARCHITECTURE.md`
- **CREAR** ADR en `docs/adr/` para decisiones importantes
- **FORMATO ADR**: `NNNN-titulo-decision.md` (ej: `0001-usar-django-template-language.md`)
- **MANTENER** consistencia entre código y documentación

---

## ⚡ Workflow Obligatorio

Este es el proceso que DEBES seguir en CADA tarea de desarrollo:

### Pre-desarrollo
1. ✅ Leer `.agent/project_rules.md`
2. ✅ Revisar `alcal/urls.py` para evitar duplicados
3. ✅ Verificar que `base_modern.html` está actualizado

### Durante desarrollo
4. ✅ Usar `base_modern.html` como base para templates
5. ✅ Aplicar clases de Bootstrap 5 y ALCAL Premium
6. ✅ NO usar estilos inline
7. ✅ Agregar `@login_required` a todas las vistas
8. ✅ Validar parámetros antes de hacer queries
9. ✅ Usar `get_object_or_404()` en vez de `.get()`
10. ✅ Agregar mensajes de feedback (`messages.success/error`)

### Post-desarrollo (CRÍTICO)
11. ✅ Ejecutar `check_templates.py` si modificaste templates
12. ✅ Verificar con `browser_subagent` que la sección/link funciona
13. ✅ Capturar screenshot de la página funcionando
14. ✅ Verificar que el sidebar aparece correctamente
15. ✅ Verificar que los estilos se aplican correctamente
16. ✅ Confirmar que no hay errores 404/500 en navegación

### Reportar
17. ✅ Mostrar evidencia (output de comandos, screenshots)
18. ✅ Reportar de forma concisa qué se hizo
19. ✅ NO preguntar si todo funcionó correctamente



## 🏗️ Arquitectura del Proyecto

### Estructura de directorios
```
alcal/
├── alcal/                    # Proyecto principal (settings, urls, wsgi)
├── asistencias/             # App de asistencias
├── administracion/          # App de gestión (CRUD)
├── alumnos/                 # App de alumnos
├── escuela/                 # App de estructura escolar
├── calificaciones/          # App de calificaciones
├── templates/               # Templates globales
├── static/                  # Archivos estáticos
├── venv/                    # Entorno virtual
└── .agent/                  # Workflows y reglas de proyecto
```

### Apps y sus responsabilidades
- **asistencias**: Toma y consulta de asistencias (por curso, por alumno, cierre diario)
- **administracion**: CRUD de carreras, cursos, materias, docentes, alumnos, turnos, códigos
- **calificaciones**: Gestión de notas y evaluaciones
- **escuela**: Modelos de Curso, Carrera, Anio
- **alumnos**: Modelo Alumno y relacionados

---

## 🎨 Frontend & Design System

### Sistema de diseño: ALCAL Premium
- **Framework**: Bootstrap 5.3.2
- **Iconos**: Bootstrap Icons (preferido) + Font Awesome (legacy)
- **Paleta**: Clases `alcal-*` definidas en `static/css/alcal-premium.css`
- **Template base**: TODOS los templates deben heredar de `base_modern.html`

### Reglas de templates
1. **SIEMPRE usar** `{% extends 'base_modern.html' %}`
2. **Bloques principales**:
   - `{% block title %}` - Título de la página
   - `{% block content %}` - Contenido principal
   - `{% block extra_css %}` - CSS adicional
   - `{% block extra_js %}` - JavaScript adicional
3. **NO usar** inline styles (usar clases de Bootstrap o ALCAL)
4. **NO crear** `<div class="container">` dentro de `{% block content %}` (ya lo tiene `base_modern.html`)
5. **Usar** componentes de Bootstrap 5:
   - Cards: `.card`, `.card-header`, `.card-body`, `.card-footer`
   - Tables: `.table`, `.table-hover`, `.align-middle`
   - Buttons: `.btn`, `.btn-alcal-primary`, `.btn-outline-secondary`
   - Alerts: `.alert`, `.alert-success`, `.alert-danger`, `.alert-info`

### Iconos
- **Preferir**: Bootstrap Icons (`bi bi-*`)
- **Legacy**: Font Awesome (`fas fa-*`) solo si ya existe en el código

---

## 🛣️ URLs y Rutas

### Convenciones de nombres
- **Selectores**: `*_selector` (ej: `asistencia_selector`, `consultas_selector`)
- **Acciones**: `tomar_*`, `guardar_*`, `consultar_*`, `ingresar_*`
- **CRUD admin**: `administracion:*_list`, `administracion:*_create`, etc.

### URLs principales (MEMORIZAR)
```python
# Selectores
/consultas/         → consultas_selector
/ingresar/          → ingresar_selector
/asistencia/        → asistencia_selector
/calificaciones/    → calificaciones_selector

# Asistencias por curso
/tomar_asistencia_curso/      → tomar_asistencia_curso
/lista_alumnos_curso/         → lista_alumnos_curso (AJAX only)
/guardar_asistencia_curso/    → guardar_asistencia_curso
/consultar_asistencia_curso/  → consultar_asistencia_curso

# Asistencias por alumno
/ing_asistencia_alumno/       → tomar_asistencia_alumno
/cons_asistencia_alumno/      → cons_asistencia_alumno

# Cierre diario
/cierre_diario/               → cierre_diario_seleccion
/procesar_cierre_diario/      → procesar_cierre_diario

# Administración
/gestion/                     → administracion:dashboard
/admin/                       → Django admin
```

### Reglas de URLs
1. **NO duplicar** rutas (una sola definición por `path()`)
2. **NO duplicar** nombres (`name=` debe ser único)
3. **Agrupar** por funcionalidad con comentarios claros
4. **URLs de AJAX** deben tener validación de parámetros requeridos

---

## 🔐 Seguridad y RBAC

### Decoradores obligatorios
- **Todas las vistas** (excepto login/home): `@login_required`
- **Vistas de modificación de datos**: `@login_required` + validación de `user.is_staff` si aplica

### Control de acceso en templates
```django
{% if user.is_superuser %}
    <!-- Solo Superuser -->
{% endif %}

{% if user.is_staff or user.is_superuser %}
    <!-- Staff o Superuser -->
{% endif %}
```

### Sidebar (base_modern.html)
- **Dashboard**: Todos
- **Asistencias/Calificaciones**: Todos
- **Observaciones/Cierre Diario**: Solo `is_staff` o `is_superuser`
- **Gestión (CRUD)**: Solo `is_superuser`
- **Admin Django**: Solo `is_superuser`

---

## 💾 Base de Datos y Modelos

### Modelos principales
```
Carrera
  ↓
Curso (tiene carrera, año, grupo)
  ↓
Alumno (pertenece a curso)
  ↓
Asistencia (alumno, curso, turno, fecha, codigo)

Materia (pertenece a carrera)
Docente
Turno (M, T, N)
CodigoAsistencia (P, F, T, J, etc.)
```

### Reglas de modelos
1. **SIEMPRE usar** `related_name` en ForeignKey
2. **SIEMPRE definir** `__str__()` para representación legible
3. **Usar** `Meta.ordering` para ordenamiento por defecto
4. **Usar** `Meta.verbose_name` y `verbose_name_plural` en español

### Migraciones
- **Después de cambiar modelos**: `python manage.py makemigrations`
- **Aplicar migraciones**: `python manage.py migrate`
- **NO editar** migraciones ya aplicadas

---

## 📝 Vistas y Lógica de Negocio

### Patrones comunes
```python
@login_required
def mi_vista(request):
    # 1. Validar parámetros
    param = request.GET.get('parametro')
    if not param:
        return HttpResponse('Error: Parámetro requerido', status=400)
    
    # 2. Obtener datos
    objeto = get_object_or_404(Modelo, pk=param)
    
    # 3. Lógica de negocio
    with transaction.atomic():
        # operaciones de BD
        pass
    
    # 4. Mensajes de feedback
    messages.success(request, 'Operación exitosa')
    
    # 5. Renderizar o redirigir
    return render(request, 'template.html', context)
```

### Reglas de vistas
1. **SIEMPRE usar** `transaction.atomic()` para operaciones múltiples de BD
2. **SIEMPRE usar** `get_object_or_404()` en vez de `Model.objects.get()`
3. **SIEMPRE usar** `messages.success/error/info()` para feedback
4. **Validar parámetros** antes de hacer queries
5. **No hacer queries en loops** (usar `select_related`, `prefetch_related`)

### Imports estándar para vistas
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from datetime import date
```

---

## 🧪 Testing y Validación

### Scripts de validación
- `check_templates.py`: Valida sintaxis de todas las plantillas
- Ejecutar **SIEMPRE** después de modificar templates

### Flujo de trabajo
1. Hacer cambio
2. Ejecutar validación automáticamente
3. Reportar resultado
4. Si hay errores, corregir inmediatamente

---

## 📦 Dependencias y Entorno

### Entorno virtual
```bash
source venv/bin/activate         # Activar
pip install -r requirements.txt  # Instalar dependencias
```

### Servidor de desarrollo
```bash
python manage.py runserver 8008
```

### Comandos útiles
```bash
python manage.py migrate                    # Aplicar migraciones
python manage.py createsuperuser           # Crear admin
python manage.py shell                     # Shell de Django
python manage.py check                     # Verificar configuración
python check_templates.py                  # Validar templates
```

---

## 🚫 Errores Comunes y Cómo Evitarlos

### TemplateSyntaxError
- **Causa**: Etiqueta sin cerrar (`{% if %}` sin `{% endif %}`)
- **Prevención**: Usar `check_templates.py`

### NoReverseMatch
- **Causa**: Nombre de URL no existe o está mal escrito
- **Prevención**: Verificar `urls.py` antes de usar `{% url 'nombre' %}`

### MultipleObjectsReturned / DoesNotExist
- **Causa**: Usar `.get()` sin `get_object_or_404()`
- **Prevención**: SIEMPRE usar `get_object_or_404()`

### Apps aren't loaded yet
- **Causa**: No llamar a `django.setup()` en scripts standalone
- **Prevención**: Incluir siempre:
  ```python
  import django
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
  django.setup()
  ```

---

## 🎯 Características Específicas del Proyecto

### Asistencia Multi-Turno
- La vista `lista_alumnos_curso` acepta `turno_id` como cadena separada por comas: `"1,2,3"`
- La vista `guardar_asistencia_curso` crea una fila de `Asistencia` por cada turno
- El template `tomar_asistencia_curso.html` usa un select múltiple para turnos

### Cierre Diario Parcial
- Permite cerrar solo algunos cursos (no todos obligatoriamente)
- Permite actualizar un cierre existente (no solo crear)
- Muestra advertencia si se va a sobrescribir data existente
- Usa `update_or_create` para flexibilidad

### Sistema de Códigos
- `P`: Presente
- `F`: Falta / Ausente
- `T`: Tardanza
- `J`: Justificado
- Los códigos se gestionan en `CodigoAsistencia` (tabla configurable)

---

## 🔄 Workflows Definidos

Ver `.agent/workflows/` para workflows específicos.

Ejemplo:
- `/implementar-admin`: Implementar sección de administración con CRUD completo

---

## ✅ Checklist de Calidad

Antes de reportar una tarea como completa:

### Código y Estructura
- [ ] El código sigue las convenciones de este documento
- [ ] Se revisó `.agent/project_rules.md` antes de hacer cambios
- [ ] No hay duplicación de código, rutas o secciones
- [ ] Los templates heredan de `base_modern.html`
- [ ] No hay estilos inline
- [ ] El sidebar aparece correctamente en todas las páginas
- [ ] Los estilos ALCAL Premium se aplican correctamente

### Validación Técnica
- [ ] Se ejecutó `check_templates.py` y no hay errores
- [ ] Las URLs están en `alcal/urls.py` sin duplicados
- [ ] Los nombres de URL siguen convenciones (`*_selector`, `tomar_*`, etc.)
- [ ] Las vistas tienen `@login_required`
- [ ] Se usan mensajes de feedback (`messages.success/error`)
- [ ] No hay imports innecesarios
- [ ] El código es DRY (Don't Repeat Yourself)

### Verificación con Navegador (OBLIGATORIO)
- [ ] Se probó la funcionalidad en el navegador con `browser_subagent`
- [ ] Todos los links creados/modificados funcionan (no 404/500)
- [ ] Se capturó screenshot de la página funcionando
- [ ] Los campos de búsqueda funcionan en vivo (si aplica)
- [ ] La navegación es consistente con el resto del sistema

### Evidencia
- [ ] Se guardó evidencia de comandos ejecutados
- [ ] Se guardaron screenshots de páginas funcionando
- [ ] Se documentaron los cambios realizados



## 📞 Comunicación con el Usuario

### NO hacer
- ❌ "¿Deseas que ejecute X?"
- ❌ "¿Continúo con Y?"
- ❌ "¿Quieres que verifique Z?"
- ❌ Explicaciones largas previo a actuar

### SÍ hacer
- ✅ Ejecutar la tarea directamente
- ✅ Reportar resultado conciso
- ✅ Mostrar evidencia (ej: output de comandos)
- ✅ Solo preguntar si hay ambigüedad REAL

---

**Última actualización**: 2025-11-22
