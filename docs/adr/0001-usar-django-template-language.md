# 0001. Usar Django Template Language en lugar de Jinja2

## Estado
**Aceptado** - 2025-11-22

## Contexto

Al iniciar el proyecto ALCAL, debíamos elegir un sistema de plantillas para el frontend. Las opciones principales eran:

1. **Django Template Language (DTL)**: Motor de plantillas integrado en Django
2. **Jinja2**: Motor de plantillas más potente y flexible, popular en Flask

### Consideraciones

**Ventajas de DTL**:
- Integración nativa con Django (sin configuración adicional)
- Compatibilidad automática con todas las características de Django (admin, messages, forms)
- Documentación oficial de Django
- Menor curva de aprendizaje para desarrolladores Django
- Seguridad por defecto (auto-escaping, protección CSRF)

**Ventajas de Jinja2**:
- Sintaxis más flexible y potente
- Mejor rendimiento en algunos casos
- Capacidad de definir macros complejas
- Popular en comunidad Python

**Desventajas de usar Jinja2 en Django**:
- Requiere configuración manual
- Puede tener problemas de compatibilidad con apps de terceros (Grappelli, Django Admin)
- Duplicación de contexto en algunos casos
- Menor soporte en la comunidad Django

## Decisión

**Usar Django Template Language como motor de plantillas único del proyecto**.

Justificación:
- El proyecto usa extensivamente Django Admin y Grappelli, que dependen de DTL
- No necesitamos la flexibilidad adicional de Jinja2 para este proyecto
- La integración nativa reduce complejidad y bugs potenciales
- El equipo tiene más experiencia con DTL

## Consecuencias

### Positivas
✅ **Cero configuración adicional**: Funciona out-of-the-box  
✅ **Compatibilidad total** con Django Admin, Grappelli, y otras apps  
✅ **Documentación unificada**: Solo necesitamos consultar docs de Django  
✅ **Mensajes de error claros**: Django reporta errores de template de forma estándar  
✅ **Validación automática**: Podemos usar `check_templates.py` fácilmente  

### Negativas
⚠️ **Menor flexibilidad**: No podemos usar macros avanzadas de Jinja2  
⚠️ **Sintaxis ligeramente más verbosa**: `{% endif %}` vs `{% end %}`  
⚠️ **Sin expresiones Python arbitrarias** en templates (es una ventaja de seguridad, pero limita flexibilidad)

### Impacto en el Código

- **Templates**: Todos usan sintaxis Django (`{% extends %}`, `{% block %}`, `{{ variable }}`)
- **Filtros personalizados**: Se crean en `templatetags/` según convención Django
- **Validación**: Script `check_templates.py` usa `django.template.loader`
- **Reglas de proyecto**: `.agent/project_rules.md` especifica "NO Jinja2"

## Notas de Implementación

- Todos los templates deben heredar de `base_modern.html`
- Usar `{% load static %}` para archivos estáticos
- Usar `{% url 'name' %}` para URLs reversas
- NO usar sintaxis Jinja2 (`{{ }}` sin filtros, `{% end %}`, etc.)

## Referencias

- [Django Template Language - Documentación oficial](https://docs.djangoproject.com/en/4.2/ref/templates/language/)
- `.agent/project_rules.md` - Sección "Frontend & Design System"
- `ARCHITECTURE.md` - Sección "Sistema de Diseño"
