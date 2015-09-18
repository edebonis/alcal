from django.db import models
from escuela.models import Materia
from alumnos.models import Alumno

class Trimestre(models.Model):
	trimestre = models.IntegerField()

class CalificacionTrimestral(models.Model):
	nota = models.IntegerField()
	trimestre = models.ForeignKey(Trimestre)
	alumno = models.ForeignKey(Alumno)
	materia = models.ForeignKey(Materia)

class CalificacionParcial(models.Model):
	nota = models.IntegerField()
	trimestre = models.ForeignKey(Trimestre)
	fecha = models.DateField()
	alumno = models.ForeignKey(Alumno)
	materia = models.ForeignKey(Materia)

