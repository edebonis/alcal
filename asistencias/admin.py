# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Asistencia, CodigoAsistencia

class CodigoAsistenciaAdmin(admin.ModelAdmin):    
    #readonly_fields = ('cantidad',)
    list_display = ('codigo','cantidad')


class AsistenciaAdmin(admin.ModelAdmin):
    def numero(self, request):
        #self = CodigoAsistenciaAdmin(admin.ModelAdmin).cantidad
        num = CodigoAsistencia.objects.all()
        return num

    list_display = ('alumno', 'curso', 'codigo', 'fecha', 'numero')
    list_filter = ('alumno', 'curso', 'codigo', 'fecha')
	

admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(CodigoAsistencia, CodigoAsistenciaAdmin)
