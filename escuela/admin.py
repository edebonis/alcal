from django.contrib import admin
from .models import Curso, Materia, Carrera, Año

class CursoAdmin(admin.ModelAdmin):
    list_display = ('curso', 'carrera')

class MateriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'horas')


admin.site.register(Curso, CursoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Carrera)
admin.site.register(Año)

