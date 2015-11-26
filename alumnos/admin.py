# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Alumno, Padre, Madre, Tutor


class AlumnoAdmin(admin.ModelAdmin):    
    #readonly_fields = ('cantidad',)
   list_display = ('nombre','apellido','curso')


admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Padre)
admin.site.register(Madre)
admin.site.register(Tutor)
# Register your models here

