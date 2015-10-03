# -*- encoding: utf-8 -*-
from django.db import models
from alumnos.models import Alumno
from smart_selects.db_fields import ChainedForeignKey
from escuela.models import Curso
from escuela.models import Anio

class TipoObservacion(models.Model):
	nombre = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre
	class Meta:
		verbose_name_plural = "Tipos de Observaciones"

class Observacion(models.Model):
	fecha = models.DateField()
	curso = models.ForeignKey(Curso)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=True)
	mensaje = models.TextField(max_length=500)
	tipo = models.ForeignKey(TipoObservacion)
	ciclo_lectivo = models.ForeignKey(Anio)
	def __str__(self):
		return self.alumno
	class Meta:
		verbose_name_plural = "Observaciones"