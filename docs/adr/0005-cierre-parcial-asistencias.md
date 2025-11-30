# 0005. Permitir Cierre Parcial de Asistencias Diarias

## Estado
**Aceptado** - 2025-11-22

## Contexto

### Problema Original

El sistema de **Cierre Diario de Asistencias** originalmente funcionaba así:

```python
# Versión original (simplificada)
@login_required
def cierre_asistencia(request):
    fecha = request.POST.get('fecha')
    
    # Verificar si ya existe cierre
    if CierreDiario.objects.filter(fecha=fecha).exists():
        messages.error(request, 'Ya existe un cierre para esta fecha')
        return redirect('cierre_diario_seleccion')
    
    # Procesar TODOS los cursos obligatoriamente
    cursos = Curso.objects.all()
    for curso in cursos:
        # crear registros...
```

**Limitaciones**:
1. ❌ **Obligatorio cerrar todos los cursos**: No se puede cerrar solo algunos
2. ❌ **No se puede actualizar**: Si ya existe cierre, error y no se puede modificar
3. ❌ **Todo o nada**: Si falta data de un curso, no se puede cerrar ninguno
4. ❌ **Sin feedback**: No se informa qué se va a sobrescribir

### Caso de Uso Real

**Escenario**: Escuela con 15 cursos.

- **09:00**: Preceptor quiere cerrar asistencia de los 5 cursos de la mañana
  - Versión original: ❌ ERROR - Debe esperar a tener data de TODOS los cursos
  
- **15:00**: Preceptor quiere agregar cierre de 6 cursos de la tarde
  - Versión original: ❌ ERROR - Ya existe cierre para hoy
  
- **16:30**: Se detecta error en asistencia de ayer
  - Versión original: ❌ ERROR - No se puede modificar cierre de ayer

**Resultado**: Sistema rígido, frustración de usuarios.

## Decisión

Implementar **Cierre Parcial y Modificable** con las siguientes características:

### 1. Cierre Parcial

Usuario puede seleccionar **qué cursos/grupos cerrar** mediante checkboxes:

```html
<!-- cierre_form.html -->
{% for item in cursos_grupos_turnos %}
<div class="form-check">
    <input type="checkbox" name="{{ item.prefix }}_m" 
           {% if item.default_manana %}checked{% endif %}>
    <label>{{ item.curso }} - Grupo {{ item.grupo }} - Mañana</label>
</div>
{% endfor %}
```

**Resultado**: Usuario cierra solo lo que tiene completo, no bloquea el resto.

### 2. Actualización de Cierres Existentes

```python
@login_required
def procesar_cierre_diario(request):
    fecha = request.POST.get('fecha')
    
    # Buscar cierre existente
    cierre_existente = CierreDiario.objects.filter(fecha=fecha).first()
    
    if cierre_existente:
        # Mostrar advertencia
        messages.info(request, 
            '⚠️ Ya existe un cierre para esta fecha. '
            'Los cambios actualizarán el cierre existente.')
    
    # Usar update_or_create para flexibilidad
    cierre, created = CierreDiario.objects.update_or_create(
        fecha=fecha,
        defaults={
            'usuario': request.user,
            # ... otros campos
        }
    )
    
    # Procesar solo cursos seleccionados
    for key, value in request.POST.items():
        if key.endswith('_m') or key.endswith('_t') or key.endswith('_n'):
            # Crear/actualizar DetalleCierreCurso
            DetalleCierreCurso.objects.update_or_create(...)
```

### 3. Carga de Datos Existentes

Cuando se accede al formulario de cierre para una fecha ya cerrada:

```python
# Pre-llenar checkboxes con data existente
cierre_previo = CierreDiario.objects.filter(fecha=fecha).first()
if cierre_previo:
    detalles = DetalleCierreCurso.objects.filter(cierre=cierre_previo)
    # Marcar checkboxes correspondientes
    for detalle in detalles:
        item.default_manana = (detalle.turno.nombre == 'M')
        item.default_tarde = (detalle.turno.nombre == 'T')
```

**Resultado**: Usuario ve exactamente qué había seleccionado antes.

### 4. Advertencias Claras

```python
if cierre_existente:
    messages.info(request, 
        f'⚠️ Cierre existente: {cierre_existente.fecha} '
        f'creado por {cierre_existente.usuario}. '
        f'Los cambios sobrescribirán este cierre.')
```

**Resultado**: Usuario informado antes de sobrescribir data.

## Consecuencias

### Positivas

✅ **Flexibilidad total**: Cerrar 1, 5 o 15 cursos según disponibilidad de data  
✅ **Corrección de errores**: Posibilidad de re-abrir y modificar cierres  
✅ **Workflow iterativo**: Cerrar por partes durante el día  
✅ **Transparencia**: Usuario ve qué va a sobrescribir  
✅ **No blocking**: Un curso sin data no bloquea el cierre de otros  
✅ **Auditoría**: Se mantiene registro de quién modificó qué  

### Negativas

⚠️ **Complejidad**: Lógica de `update_or_create` más compleja que simple `create`  
⚠️ **UI más compleja**: Muchos checkboxes pueden ser abrumadores  
⚠️ **Riesgo de sobrescritura accidental**: Usuario puede sobrescribir sin querer  

### Mitigaciones

**Complejidad**:
- Usar `transaction.atomic()` para garantizar atomicidad
- Tests unitarios para casos edge (update, partial, full)

**UI compleja**:
- Agrupar checkboxes por curso
- Añadir "Seleccionar todos" / "Deseleccionar todos"
- Mostrar contador de cursos seleccionados

**Sobrescritura accidental**:
- Mensaje de advertencia claro con `messages.info()`
- Futuro: Modal de confirmación antes de sobrescribir

## Flujo Completo

### Caso 1: Cierre Nuevo (Primera Vez)

```
Usuario → /cierre_diario/
  ↓
Selecciona fecha: 2025-11-22
  ↓
Sistema muestra form con todos los checkboxes vacíos
  ↓
Usuario marca: Curso A-Mañana, Curso B-Tarde, Curso C-Mañana
  ↓
Submit → procesar_cierre_diario
  ↓
No existe cierre previo → Crear nuevo
  ↓
Crear 3 DetalleCierreCurso (solo los marcados)
  ↓
Mensaje: "Cierre creado exitosamente para 3 cursos"
```

### Caso 2: Actualización de Cierre

```
Usuario → /cierre_diario/
  ↓
Selecciona fecha: 2025-11-21 (ya cerrada)
  ↓
Sistema carga cierre existente
  ↓
Pre-marca checkboxes según cierre previo
  ↓
Mensaje: "⚠️ Ya existe cierre. Los cambios actualizarán."
  ↓
Usuario cambia: Desmarca Curso B-Tarde, Marca Curso D-Noche
  ↓
Submit → procesar_cierre_diario
  ↓
Existe cierre previo → Actualizar
  ↓
Eliminar Curso B-Tarde, Agregar Curso D-Noche
  ↓
Mensaje: "Cierre actualizado exitosamente"
```

### Caso 3: Cierre Parcial Progresivo

```
09:00 - Usuario cierra 5 cursos de mañana
  ↓
CierreDiario (fecha=hoy) con 5 DetalleCierreCurso
  ↓
15:00 - Usuario vuelve, agrega 6 cursos de tarde
  ↓
Actualiza CierreDiario existente, ahora tiene 11 DetalleCierreCurso
  ↓
18:00 - Usuario agrega 4 cursos de noche
  ↓
Actualiza CierreDiario existente, ahora tiene 15 DetalleCierreCurso
```

**Resultado**: 3 operaciones parciales = 1 cierre completo al final del día.

## Decisiones Relacionadas

- **ADR-0004**: Multi-turno (permite cerrar múltiples turnos por curso)
- **ADR-0002**: URLs centralizadas (`/cierre_diario/`, `/procesar_cierre_diario/`)

## Alternativas Consideradas

### Opción A: Por Turno (No Parcial)
Cerrar todos los cursos de un turno específico.
**Descartado**: Poco flexible, sigue bloqueando si falta data.

### Opción B: Cierre Automático
Sistema cierra automáticamente al final del día.
**Descartado**: No permite correcciones, pérdida de control.

### Opción C: Versioning de Cierres
Mantener historial de versiones de cada cierre.
**Pendiente**: Útil para auditoría, considerar en futuro.

## Referencias

- `asistencias/views.py` - Función `procesar_cierre_diario`
- `asistencias/templates/asistencias/cierre_form.html` - Formulario con checkboxes
- `asistencias/models.py` - Modelos `CierreDiario`, `DetalleCierreCurso`
- `.agent/project_rules.md` - Sección "Características Específicas"
