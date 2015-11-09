from django.db import models
from escuela.models import Materia
from alumnos.models import Alumno
from escuela.models import Anio


# Create your models here.
class Trimestre(models.Model):
	trimestre = models.IntegerField()
	ciclo_lectivo = models.ForeignKey(Anio)

class CalificacionTrimestral(models.Model):
	nota = models.IntegerField()
	trimestre = models.ForeignKey(Trimestre)
	alumno = models.ForeignKey(Alumno)
	materia = models.ForeignKey(Materia)
	ciclo_lectivo = models.ForeignKey(Anio)
	class Meta:
		verbose_name_plural = "Calificaciones Trimestrales"

class CalificacionParcial(models.Model):
	nota = models.IntegerField()
	trimestre = models.ForeignKey(Trimestre)
	fecha = models.DateField()
	alumno = models.ForeignKey(Alumno)
	materia = models.ForeignKey(Materia)
	ciclo_lectivo = models.ForeignKey(Anio)
	class Meta:
		verbose_name_plural = "Calificaciones Parciales"