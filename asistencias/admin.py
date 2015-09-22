from django.contrib import admin
from .models import Asistencia, CodigoAsistencia


class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'cantidad', 'curso', 'codigo', 'fecha')


admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(CodigoAsistencia)
# Register your models here.
