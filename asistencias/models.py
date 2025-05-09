# -*- encoding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from alumnos.models import Alumno
from escuela.models import Anio, Curso


class CodigoAsistencia(models.Model):
	CODIGO_CHOICES = (
		('A/A','Ausente'),
		('A/P','A/P'),
		('A/T','A/T'),
		('P/A','P/A'),
		('T/A','T/A'),
		('P/T','P/T'),
		('T/P','T/P'),
		('T/T','T/T'),
		('R/A','R/A'),
		('A/R','A/R'),
		('R/T','R/T'),
		('T/R','T/R'),
		('P/R','P/R'),
		('R/P','R/P'),
		)
	codigo = models.CharField(max_length=5, choices=CODIGO_CHOICES, unique=True)
	cantidad = models.FloatField()
	def __str__(self):
		return self.codigo
		verbose_name_plural = "Codigos de Asistencias"


class Asistencia(models.Model):
	ciclo_lectivo = models.ForeignKey(Anio, on_delete=models.CASCADE)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=True)
	codigo = models.ForeignKey(CodigoAsistencia, on_delete=models.CASCADE)
	fecha = models.DateField()
	
	def __str__(self):
		return str(self.fecha)
	

