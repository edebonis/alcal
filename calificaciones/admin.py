# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Instancia, CalificacionTrimestral, CalificacionParcial


class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'nota', 'instancia_display', 'fecha', 'curso')
    list_filter = ('ciclo_lectivo', 'curso', 'materia', 'instancia')
    search_fields = ('alumno__apellido', 'alumno__nombre', 'materia__nombre')
    list_editable = ('nota',)
    autocomplete_fields = ['alumno']
    
    def instancia_display(self, obj):
        if hasattr(obj, 'instancia'):
            return obj.instancia
        return "Parcial"
    instancia_display.short_description = "Instancia"


@admin.register(CalificacionTrimestral)
class CalificacionTrimestralAdmin(CalificacionAdmin):
    pass


@admin.register(CalificacionParcial)
class CalificacionParcialAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'materia', 'nota', 'fecha', 'curso')
    list_filter = ('ciclo_lectivo', 'curso', 'materia')
    search_fields = ('alumno__apellido', 'alumno__nombre', 'materia__nombre')
    list_editable = ('nota',)
    date_hierarchy = 'fecha'


admin.site.register(Instancia)
