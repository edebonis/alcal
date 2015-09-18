from django.contrib import admin
from .models import Trimestre, CalificacionTrimestral, CalificacionParcial


admin.site.register(Trimestre)
admin.site.register(CalificacionParcial)
admin.site.register(CalificacionTrimestral)

