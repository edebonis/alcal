from django.db import models
from escuela.models import Materia
from alumnos.models import Alumno
from escuela.models import Anio
from escuela.models import Curso
from smart_selects.db_fields import ChainedForeignKey




# Create your models here.
class Instancia(models.Model):
	instancia= models.CharField(max_length=50)
	def __str__(self):
		return self.instancia

class CicloLectivo(models.Model):
	ciclo_lectivo = models.IntegerField()
	def __str__(self):
		return str(self.ciclo_lectivo)

class CalificacionTrimestral(models.Model):
	nota = models.IntegerField()
	instancia = models.ForeignKey(Instancia)
	curso = models.ForeignKey(Curso)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso")
	ciclo_lectivo = models.ForeignKey(CicloLectivo)
	class Meta:
		verbose_name_plural = "Calificaciones Trimestrales"

class CalificacionParcial(models.Model):
	nota = models.IntegerField()
	fecha = models.DateField()
	curso = models.ForeignKey(Curso)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=False)
	materia = ChainedForeignKey(Materia, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=False)
	ciclo_lectivo = models.ForeignKey(CicloLectivo)
	class Meta:
		verbose_name_plural = "Calificaciones Parciales"