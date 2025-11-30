# Plan de Investigación: POST inesperado en /lista_alumnos_curso/

## Problema
El endpoint `/lista_alumnos_curso/` recibe POST cuando debería recibir GET.

## Hipótesis a Verificar

### 1. Cache del navegador
- **Qué verificar**: Versión antigua de JavaScript cacheada
- **Acción**: Forzar recarga completa (Ctrl+Shift+R)
- **Evidencia**: Timestamp de archivo vs última modificación

### 2. JavaScript duplicado o conflictivo
- **Qué verificar**: 
  - `base_modern.html` tiene algún listener global
  - Hay algún service worker registrado
  - Conflicto entre scripts
- **Acción**: Revisar todos los scripts cargados

### 3. Template renderizado incorrectamente
- **Qué verificar**: El HTML generado final
- **Acción**: Ver source en navegador, buscar `<form>` inesperados

### 4. Fetch mal configurado
- **Qué verificar**: Método efectivo del fetch
- **Acción**: Console.log antes del fetch con todas las opciones

### 5. CSRF o middleware interferiendo
- **Qué verificar**: Django middleware cambiando método
- **Acción**: Revisar settings.py MIDDLEWARE

### 6. URL reverse generando ruta incorrecta
- **Qué verificar**: `{% url 'lista_alumnos_curso' %}` genera ruta correcta
- **Acción**: Console.log de URL exacta

## Plan de Acción

1. ✅ Verificar HTML generado en navegador (View Source)
2. ✅ Agregar console.log exhaustivo ANTES del fetch
3. ✅ Revisar Network tab para ver request real
4. ✅ Verificar que no haya JavaScript duplicado
5. ✅ Probar endpoint directo con curl
6. ✅ Revisar si hay algún proxy/middleware

## Solución Esperada
Identificar fuente exacta del POST y eliminarlo.
