# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Asistencia,
    CierreDiario,
    CodigoAsistencia,
    DetalleCierreCurso,
    ReglaAsistencia,
    ResumenDiarioAlumno,
    Turno,
)


class CodigoAsistenciaAdmin(admin.ModelAdmin):    
    list_display = ('codigo', 'descripcion', 'cantidad_falta')
    list_filter = ('cantidad_falta',)
    search_fields = ('codigo', 'descripcion')


class ReglaAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('codigo_manana', 'codigo_tarde', 'codigo_ed_fisica', 'valor_falta', 'observacion')
    list_filter = ('valor_falta', 'codigo_manana', 'codigo_tarde', 'codigo_ed_fisica')
    search_fields = ('observacion',)


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


class DetalleCierreCursoInline(admin.TabularInline):
    model = DetalleCierreCurso
    extra = 0
    fields = ('curso', 'grupo', 'hubo_turno_manana', 'hubo_turno_tarde', 'hubo_turno_ed_fisica')


class CierreDiarioAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'usuario_cierre', 'fecha_cierre', 'total_alumnos_procesados', 'total_asistencias_procesadas')
    list_filter = ('fecha', 'usuario_cierre', 'fecha_cierre')
    search_fields = ('fecha', 'usuario_cierre__username', 'usuario_cierre__first_name', 'usuario_cierre__last_name')
    date_hierarchy = 'fecha'
    inlines = [DetalleCierreCursoInline]
    
    fieldsets = (
        ('Información del Cierre', {
            'fields': ('fecha', 'usuario_cierre', 'fecha_cierre')
        }),
        ('Estadísticas', {
            'fields': ('total_asistencias_procesadas', 'total_alumnos_procesados')
        }),
        ('Observaciones', {
            'fields': ('observaciones_cierre',)
        }),
    )
    
    readonly_fields = ('fecha_cierre', 'total_asistencias_procesadas', 'total_alumnos_procesados')


class ResumenDiarioAlumnoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha', 'mostrar_codigos', 'valor_falta_final', 'observacion_calculada')
    list_filter = ('fecha', 'cierre_diario', 'valor_falta_final')
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__legajo')
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('cierre_diario', 'alumno', 'fecha')
        }),
        ('Códigos de Asistencia', {
            'fields': ('codigo_manana', 'codigo_tarde', 'codigo_ed_fisica')
        }),
        ('Resultado Final', {
            'fields': ('valor_falta_final', 'observacion_calculada')
        }),
    )
    
    def mostrar_codigos(self, obj):
        codigos = []
        if obj.codigo_manana != '-':
            codigos.append(f'M:{obj.codigo_manana}')
        if obj.codigo_tarde != '-':
            codigos.append(f'T:{obj.codigo_tarde}')
        if obj.codigo_ed_fisica != '-':
            codigos.append(f'EF:{obj.codigo_ed_fisica}')
        return ' | '.join(codigos) if codigos else '-'
    mostrar_codigos.short_description = 'Códigos'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('alumno', 'cierre_diario')


admin.site.register(CodigoAsistencia, CodigoAsistenciaAdmin)
admin.site.register(ReglaAsistencia, ReglaAsistenciaAdmin)
admin.site.register(Turno, TurnoAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(CierreDiario, CierreDiarioAdmin)
admin.site.register(ResumenDiarioAlumno, ResumenDiarioAlumnoAdmin)
