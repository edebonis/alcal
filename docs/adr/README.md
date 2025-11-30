# Architecture Decision Records (ADRs)

Este directorio contiene los registros de decisiones arquitectónicas (ADRs) del proyecto ALCAL.

## ¿Qué es un ADR?

Un ADR documenta una decisión arquitectónica significativa junto con su contexto y consecuencias. Esto ayuda a:
- Entender el "por qué" detrás de decisiones pasadas
- Prevenir la repetición de discusiones ya resueltas
- Facilitar la incorporación de nuevos miembros al proyecto

## Formato

Cada ADR sigue esta estructura:

```markdown
# NNNN. Título de la Decisión

## Estado
[Propuesto | Aceptado | Rechazado | Deprecado | Sustituido por ADR-XXXX]

## Contexto
[Descripción del problema o situación que requiere una decisión]

## Decisión
[La decisión que se tomó]

## Consecuencias
[Impactos positivos y negativos de la decisión]
```

## Índice de ADRs

| ADR | Título | Estado | Fecha |
|-----|--------|--------|-------|
| [0001](0001-usar-django-template-language.md) | Usar Django Template Language en lugar de Jinja2 | Aceptado | 2025-11-22 |
| [0002](0002-centralizacion-urls.md) | Centralizar URLs en alcal/urls.py | Aceptado | 2025-11-22 |
| [0003](0003-bootstrap-5-sistema-diseno.md) | Adoptar Bootstrap 5 como framework CSS | Aceptado | 2025-11-22 |
| [0004](0004-multi-turno-asistencias.md) | Soporte multi-turno en toma de asistencias | Aceptado | 2025-11-22 |
| [0005](0005-cierre-parcial-asistencias.md) | Permitir cierre parcial de asistencias diarias | Aceptado | 2025-11-22 |
| [0006](0006-proceso-verificacion-archivos.md) | Proceso obligatorio de verificación antes de editar archivos | Aceptado | 2025-11-22 |

## Cómo Crear un Nuevo ADR

1. Determinar el número siguiente (actualmente: 0006)
2. Crear archivo `docs/adr/NNNN-titulo-decision.md`
3. Usar el formato estándar
4. Actualizar este README.md con la nueva entrada
5. Referenciar el ADR en `ARCHITECTURE.md` si corresponde
