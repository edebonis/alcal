# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Observacion, TipoObservacion

admin.site.register(Observacion)
admin.site.register(TipoObservacion)

# Register your models here.
