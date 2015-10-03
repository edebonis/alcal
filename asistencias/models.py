# -*- encoding: utf-8 -*-
from django.db import models
from alumnos.models import Alumno
from smart_selects.db_fields import ChainedForeignKey
from escuela.models import Curso
from escuela.models import Anio

class CodigoAsistencia(models.Model):
	codigo = models.CharField(max_length=5)
	def __str__(self):
		return self.codigo
	class Meta:
		verbose_name_plural = "Codigos de Asistencias"

class Asistencia(models.Model):
	ciclo_lectivo = models.ForeignKey(Anio)
	cantidad = models.IntegerField()
	curso = models.ForeignKey(Curso)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=True)
	codigo = models.ForeignKey(CodigoAsistencia)
	fecha = models.DateField()
	def __str__(self):
		return str(self.cantidad)
	