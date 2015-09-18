from django.db import models
from alumnos.models import Alumno

class TipoObservacion(models.Model):
	nombre = models.CharField(max_length=50)

class Observacion(models.Model):
	fecha = models.DateField()
	alumno = models.ForeignKey(Alumno)
	mensaje = models.CharField(max_length=500)
	tipo = models.ForeignKey(TipoObservacion)