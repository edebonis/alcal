from django.contrib import admin
from .models import Curso, Materia, Carrera, Asistencia

admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(Asistencia)