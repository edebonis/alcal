# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Asistencia,
    CierreDiario,
    CodigoAsistencia,
    ResumenDiarioAlumno,
    Turno,
)


class CodigoAsistenciaAdmin(admin.ModelAdmin):    
    list_display = ('codigo', 'descripcion', 'cantidad_falta')
    list_filter = ('cantidad_falta',)
    search_fields = ('codigo', 'descripcion')


class TurnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'hora_inicio', 'hora_fin')
    list_filter = ('nombre',)


class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'curso', 'turno', 'codigo', 'fecha', 'procesado', 'valor_falta_calculado')
    list_filter = ('curso', 'turno', 'codigo', 'fecha', 'ciclo_lectivo', 'procesado')
    search_fields = ('alumno__nombre', 'alumno__apellido')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('alumno', 'curso', 'fecha', 'ciclo_lectivo')
        }),
        ('Asistencia', {
            'fields': ('turno', 'codigo', 'observaciones')
        }),
        ('Procesamiento', {
            'fields': ('procesado', 'valor_falta_calculado'),
            'classes': ('collapse',),
            'description': 'Campos calculados automáticamente durante el cierre del día'
        }),
    )
    
    readonly_fields = ('procesado', 'valor_falta_calculado')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('alumno', 'curso', 'turno', 'codigo')


class CierreDiarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario_cierre', 'fecha_cierre', 'total_alumnos_procesados', 'total_asistencias_procesadas')
    list_filter = ('fecha', 'usuario_cierre', 'fecha_cierre')
    search_fields = ('fecha', 'usuario_cierre__username', 'usuario_cierre__first_name', 'usuario_cierre__last_name')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información del Cierre', {
            'fields': ('fecha', 'usuario_cierre', 'fecha_cierre')
        }),
        ('Estadísticas', {
            'fields': ('total_asistencias_procesadas', 'total_alumnos_procesados', 'total_cursos_procesados')
        }),
        ('Observaciones', {
            'fields': ('observaciones_cierre',)
        }),
    )
    
    readonly_fields = ('fecha_cierre', 'total_asistencias_procesadas', 'total_alumnos_procesados', 'total_cursos_procesados')


class ResumenDiarioAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha', 'mostrar_turnos', 'mostrar_codigos', 'valor_falta_final')
    list_filter = ('fecha', 'cierre_diario', 'tuvo_mañana', 'tuvo_tarde', 'tuvo_educacion_fisica', 'valor_falta_final')
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__legajo')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('cierre_diario', 'alumno', 'fecha')
        }),
        ('Turnos Cursados', {
            'fields': ('tuvo_mañana', 'tuvo_tarde', 'tuvo_educacion_fisica')
        }),
        ('Códigos de Asistencia', {
            'fields': ('codigo_mañana', 'codigo_tarde', 'codigo_educacion_fisica')
        }),
        ('Resultado Final', {
            'fields': ('valor_falta_final', 'observaciones_resumen')
        }),
    )
    
    def mostrar_turnos(self, obj):
        turnos = []
        if obj.tuvo_mañana:
            turnos.append('<span class="badge" style="background-color: #ffc107; color: #000;">Mañana</span>')
        if obj.tuvo_tarde:
            turnos.append('<span class="badge" style="background-color: #fd7e14; color: #fff;">Tarde</span>')
        if obj.tuvo_educacion_fisica:
            turnos.append('<span class="badge" style="background-color: #20c997; color: #fff;">Ed. Física</span>')
        return format_html(' '.join(turnos)) if turnos else '-'
    mostrar_turnos.short_description = 'Turnos'
    
    def mostrar_codigos(self, obj):
        codigos = []
        if obj.codigo_mañana:
            codigos.append(f'M:{obj.codigo_mañana}')
        if obj.codigo_tarde:
            codigos.append(f'T:{obj.codigo_tarde}')
        if obj.codigo_educacion_fisica:
            codigos.append(f'EF:{obj.codigo_educacion_fisica}')
        return ' | '.join(codigos) if codigos else '-'
    mostrar_codigos.short_description = 'Códigos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('alumno', 'cierre_diario')


admin.site.register(CodigoAsistencia, CodigoAsistenciaAdmin)
admin.site.register(Turno, TurnoAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(CierreDiario, CierreDiarioAdmin)
admin.site.register(ResumenDiarioAlumno, ResumenDiarioAlumnoAdmin)
