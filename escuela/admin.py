# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Curso, Materia, Carrera, Anio

class CursoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'carrera')

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'horas', 'es_tecnico_especifica')
    list_filter = ('es_tecnico_especifica', 'curso__carrera')
    search_fields = ('nombre',)


admin.site.register(Curso, CursoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Carrera)
admin.site.register(Anio)

