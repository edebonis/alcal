from django.contrib import admin
from .models import Instancia, CalificacionTrimestral, CalificacionParcial, CicloLectivo


admin.site.register(Instancia)
admin.site.register(CalificacionParcial)
admin.site.register(CalificacionTrimestral)
admin.site.register(CicloLectivo)
