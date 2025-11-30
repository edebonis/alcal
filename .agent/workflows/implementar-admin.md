---
description: Implementar sección de administración con CRUD completo
---

# Plan de Implementación - Sección de Administración

## Objetivo
Crear una sección de administración personalizada (no admin de Django) con CRUD completo para:
- Carreras
- Docentes
- Cursos
- Alumnos
- Materias
- Turnos de asistencia
- Configuración de horarios
- Configuración de valores de inasistencia

## Fases de Implementación

### Fase 1: Modelos para Turnos y Asistencias
1. Crear modelo `Turno` (Mañana, Tarde, Noche)
   - nombre
   - hora_inicio
   - hora_fin
   - activo
   
2. Crear modelo `ConfiguracionAsistencia`
   - turno (FK)
   - valor_tarde (numérico, ej: 0.5)
   - valor_ausente (numérico, ej: 1.0)
   - valor_retirado (numérico, ej: 0.25)

3. Actualizar modelo `Asistencia` si es necesario
   - Vincular con Turno
   - Agregar estados: presente, tarde, ausente, retirado

### Fase 2: Aplicación de Administración
1. Crear nueva app Django llamada `administracion`
2. Configurar URLs
3. Crear sistema de autenticación/permisos

### Fase 3: Vistas CRUD
Crear vistas CRUD para cada entidad:
- Lista (con búsqueda y filtros)
- Crear
- Editar
- Eliminar (con confirmación)
- Detalle

### Fase 4: Templates Modernos
1. Layout base con navegación
2. Diseño responsive
3. Uso de CSS moderno (glassmorphism, animaciones)
4. Formularios interactivos
5. Tablas con paginación y búsqueda

### Fase 5: Funcionalidades Adicionales
1. Dashboard con estadísticas
2. Importación/Exportación de datos
3. Búsqueda global
4. Validaciones en tiempo real

## Estado
- [ ] Fase 1: Modelos
- [ ] Fase 2: App de administración
- [ ] Fase 3: Vistas CRUD
- [ ] Fase 4: Templates
- [ ] Fase 5: Funcionalidades adicionales
