# ADR 0006: Proceso Obligatorio de Verificación de Archivos

## Estado
**Aceptado** - 2025-11-22

## Contexto

### Problema Crítico Encontrado

Durante el desarrollo de la funcionalidad multi-turno de asistencias, perdimos tiempo considerable (más de 30 minutos) editando el archivo **incorrecto** de un template.

**Lo que pasó:**
1. Necesitaba editar `tomar_asistencia_curso.html`
2. Asumí que solo había un archivo con ese nombre
3. Edité `/asistencias/templates/asistencias/tomar_asistencia_curso.html`
4. Django estaba usando `/templates/asistencias/tomar_asistencia_curso.html`
5. Todos los cambios no se reflejaban en el navegador
6. El usuario tuvo que indicarme multiple veces que "sigue igual"
7. Finalmente descubrí que había **DOS archivos** con el mismo nombre

**Consecuencias:**
- ❌ Tiempo del usuario desperdiciado
- ❌ Frustración innecesaria
- ❌ Múltiples iteraciones de "prueba esto" sin resultado
-  ❌ Pérdida de confianza

## Decisión

**Implementar proceso OBLIGATORIO de verificación antes de editar cualquier template o archivo que pueda tener duplicados.**

### Proceso Mandatorio

#### ANTES de editar templates:

```python
# 1. BUSCAR TODOS LOS ARCHIVOS con ese nombre
find_by_name(Pattern="template_name.html", SearchDirectory="/path/to/project")

# 2. Si hay MÚLTIPLESarchivos:
#    a. Buscar la vista que lo renderiza
grep_search(Query="render(request,", Pattern="views.py")

#    b. Verificar orden de búsqueda de Django:
#       - templates/ (global) ← PRIORIDAD 1
#       - app/templates/ ← PRIORIDAD 2

#    c. EDITAR el que Django encuentra PRIMERO

# 3. Verificar con browser si es posible:
#    - View Source en navegador
#    - Comparar HTML con archivo a editar
#    - Si NO coinciden → DETENER y buscar correcto
```

### Regla de Oro

```
NUNCA asumir que solo hay un archivo con ese nombre
SIEMPRE verificar PRIMERO con find_by_name()
SOLO editar después de confirmar cuál usa Django
```

## Consecuencias

### Positivas

✅ **Evita pérdida de tiempo**: No más ediciones de archivos incorrectos  
✅ **Mayor precisión**: Siempre editas el archivo que Django usa  
✅ **Reduce frustración**: Usuario ve cambios inmediatos  
✅ **Proceso verificable**: Cada paso tiene evidencia  
✅ **Documentado**: Queda registrado en ADR y reglas  

### Negativas

⚠️ **Paso adicional**: Requiere verificación antes de editar  
⚠️ **Más tool calls**: 1-2 llamadas extra de find_by_name/grep  

**Pero:** El costo de NO hacerlo es MUCHO mayor (30+ minutos perdidos)

## Casos de Uso

### Caso 1: Template Único

```
USER: "Edita login.html"

AGENT:
1. find_by_name("login.html") → 1 resultado: templates/login.html
2. Editar templates/login.html ✓
```

### Caso 2: Template Duplicado

```
USER: "Edita tomar_asistencia.html"

AGENT:
1. find_by_name("tomar_asistencia.html") → 2 resultados:
   - templates/asistencias/tomar_asistencia.html
   - asistencias/templates/asistencias/tomar_asistencia.html

2. grep_search("render.*tomar_asistencia") → 
   'asistencias/tomar_asistencia.html'

3. Django busca en orden:
   a. templates/asistencias/tomar_asistencia.html ← ESTE
   b. asistencias/templates/asistencias/tomar_asistencia.html

4. Editar templates/asistencias/tomar_asistencia.html ✓
```

### Caso 3: Verificación con Navegador

```
AGENT:
1. find_by_name("footer.html") → 3 resultados

2. browser_subagent:
   - View Source
   - Buscar comentario único o ID
   - Comparar con archivos encontrados

3. Identificar archivo correcto

4. Editar el confirmado ✓
```

## Implementación

### En `.agent/project_rules.md`

Agregada sección **3a. CRÍTICO: Verificar archivo correcto ANTES de editar** con:
- Proceso paso a paso
- Regla de oro
- Consecuencias de NO seguirlo
- Marcado como **ESTO NO ES ACEPTABLE** si se viola

### Checklist Pre-Edición

Antes de editar templates/views/static:

- [ ] Ejecuté `find_by_name()` para buscar duplicados
- [ ] Si hay múltiples, identifiqué cuál usa Django
- [ ] Verifiqué con grep_search la ruta en render()
- [ ] Consideré el orden de búsqueda de Django
- [ ] Si es posible, verifiqué con View Source en navegador
- [ ] Confirmé que voy a editar el archivo CORRECTO

**SOLO después de marcar TODO** → Editar

## Alternativas Consideradas

### Opción A: Eliminar duplicados

**Descripción**: Borrar templates duplicados, mantener solo uno.

**Descartado porque**:
- Puede haber razones históricas para duplicados
- Puede romper cosas que dependen de la estructura actual
- No siempre es seguro eliminar sin investigar

### Opción B: Renombrar para evitar duplicados

**Descripción**: Renombrar templates duplicados con sufijo `_app`.

**Descartado porque**:
- Requiere refactorizar todas las vistas
- Puede romper código existente
- No resuelve el problema de fondo (verificación)

### Opción C: Proceso de verificación (ELEGIDO)

**Descripción**: Verificar SIEMPRE cuál archivo se está usando antes de editar.

**Elegido porque**:
- ✅ No requiere cambios en código existente
- ✅ Previene el problema desde la raíz
- ✅ Aplicable a cualquier tipo de archivo
- ✅ Educativo: aprendo a verificar siempre

## Lecciones Aprendidas

1. **NUNCA asumir**: Siempre verificar, nunca asumir
2. **Tiempo del usuario es sagrado**: 1 minuto de verificación ahorra 30 de debug
3. **Proceso > Velocidad**: Mejor lento y correcto que rápido e incorrecto
4. **Documentar fallos**: Convertir errores en ADRs para no repetirlos

## Referencias

- `.agent/project_rules.md` - Sección 3a
- Error real: Sesión 2025-11-22, tomar_asistencia_curso.html
- Django Template Loading: https://docs.djangoproject.com/en/4.2/ref/templates/api/#template-loaders
