# -*- encoding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

class Carrera(models.Model):
	nombre = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre

class Anio(models.Model):
	ciclo_lectivo = models.IntegerField()
	def __str__(self):
		return str(self.ciclo_lectivo)

class Curso(models.Model):
	curso = models.CharField(max_length=5)
	carrera = models.ForeignKey(Carrera)
	def __str__(self):
		return self.curso


class Materia(models.Model):
	nombre = models.CharField(max_length=50)
	curso = models.ForeignKey(Curso)
	horas = models.IntegerField()
	def __str__(self):
		return self.nombre

