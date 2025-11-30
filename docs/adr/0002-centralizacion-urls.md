# 0002. Centralización de URLs en alcal/urls.py

## Estado
**Aceptado** - 2025-11-22

## Contexto

Django permite organizar URLs de dos formas principales:

1. **URLs centralizadas**: Todas las rutas en el archivo `urls.py` del proyecto principal
2. **URLs distribuidas**: Cada app tiene su propio `urls.py` que se incluye con `include()`

### Situación Inicial

El proyecto ALCAL tenía URLs duplicadas y dispersas:
- Misma ruta definida múltiples veces (ej: `/consultas/` aparecía 2 veces)
- Nombres de URL duplicados causando `NoReverseMatch`
- Dificultad para encontrar dónde estaba definida una ruta específica
- Inconsistencia entre apps

### Opciones Evaluadas

**Opción A: URLs completamente centralizadas**
- Todas las rutas en `alcal/urls.py`
- Única excepción: `administracion` con namespace

**Opción B: URLs distribuidas por app**
- Cada app tiene su `urls.py`
- `alcal/urls.py` solo hace `include()`

**Opción C: Híbrido**
- URLs principales centralizadas
- Apps grandes con su propio `urls.py`

## Decisión

**Adoptar Opción A: Centralización completa en `alcal/urls.py`**, con única excepción para `administracion` que usa namespace.

### Razones

1. **Elimina duplicados**: Una única fuente de verdad para todas las rutas
2. **Facilita auditoría**: Ver todas las URLs en un solo archivo
3. **Previene conflictos**: Imposible tener dos rutas con mismo `name=`
4. **Más simple para proyecto ALCAL**: No es suficientemente grande para requerir distribución
5. **Coherencia**: Misma convención para todas las apps (excepto admin)

### Excepción: `administracion`

La app `administracion` mantiene su propio `urls.py` porque:
- Tiene ~20 rutas CRUD (list, create, update, delete × 7 entidades)
- Usa namespace `administracion:` para evitar conflictos
- Es un módulo autocontenido
- Incluido en `alcal/urls.py` con: `path('gestion/', include('administracion.urls'))`

## Consecuencias

### Positivas

✅ **Cero duplicación**: Cada ruta existe exactamente una vez  
✅ **Fácil auditoría**: `alcal/urls.py` es el único archivo a revisar  
✅ **Prevención de conflictos**: Django falla si se duplica un `name=`  
✅ **Documentación clara**: Comentarios agrupan rutas por funcionalidad  
✅ **Refactorización simple**: Renombrar ruta afecta un solo lugar  

### Negativas

⚠️ **Archivo largo**: `alcal/urls.py` tiene ~75 líneas (aceptable)  
⚠️ **Imports mezclados**: Vistas de diferentes apps importadas juntas  
⚠️ **Menos encapsulación**: Apps no son completamente independientes  

### Impacto en el Código

**Archivo `alcal/urls.py`** estructura:
```python
urlpatterns = [
    # Home and admin
    path('', views.home, name='home'),
    
    # Selectores principales
    path('consultas/', views.consultas_selector, name='consultas_selector'),
    path('ingresar/', views.ingresar_selector, name='ingresar_selector'),
    
    # Asistencias por curso (específicas)
    path('tomar_asistencia_curso/', asistencias_views.tomar_asistencia_curso, 
         name='tomar_asistencia_curso'),
    path('lista_alumnos_curso/', asistencias_views.lista_alumnos_curso,
         name='lista_alumnos_curso'),
    
    # Administración
    path('gestion/', include('administracion.urls')),  # ÚNICA excepción
]
```

**Apps sin `urls.py`**:
- `asistencias/` - NO tiene urls.py (todo en alcal/urls.py)
- `alumnos/` - NO tiene urls.py
- `escuela/` - NO tiene urls.py
- `calificaciones/` - NO tiene urls.py

**Única app con `urls.py`**:
- `administracion/urls.py` - Namespace `administracion:`

## Reglas Derivadas

1. **ANTES de crear ruta**: Verificar `alcal/urls.py` que no existe
2. **Nombres consistentes**: Seguir convención `*_selector`, `tomar_*`, `consultar_*`
3. **Agrupar con comentarios**: Por funcionalidad (Asistencias, Calificaciones, etc.)
4. **NO crear** nuevos `urls.py` en apps sin justificación documentada

## Referencias

- `alcal/urls.py` - Implementación actual
- `.agent/project_rules.md` - Sección "URLs y Rutas"
- `ARCHITECTURE.md` - Sección "Routing y URLs"
