from django.db import models
from escuela.models import Curso

class Padre(models.Model):
	nombre_padre = models.CharField(max_length=50)
	apellido_padre = models.CharField(max_length=50)
	dni_padre = models.IntegerField(null=True, blank=True)
	direccion_padre = models.CharField(max_length=100, null=True, blank=True)
	telefono_padre = models.CharField(max_length=20)
	nacionalidad_padre = models.CharField(max_length=20)
	def __str__(self):
		return self.apellido_padre + " " + self.nombre_padre

class Madre(models.Model):
	nombre_madre = models.CharField(max_length=50)
	apellido_madre = models.CharField(max_length=50)
	dni_madre = models.IntegerField(null=True, blank=True)
	direccion_madre = models.CharField(max_length=100, null=True, blank=True)
	telefono_madre = models.CharField(max_length=20)
	nacionalidad_madre = models.CharField(max_length=20)
	def __str__(self):
		return self.apellido_madre + " " + self.nombre_madre


class Tutor(models.Model):
	nombre_tutor = models.CharField(max_length=50)
	apellido_tutor = models.CharField(max_length=50)
	dni_tutor = models.IntegerField(null=True, blank=True)
	direccion_tutor = models.CharField(max_length=100, null=True, blank=True)
	telefono_tutor = models.CharField(max_length=20)
	nacionalidad_tutor = models.CharField(max_length=20)
	def __str__(self):
		return self.apellido_tutor + " " + self.nombre_tutor



class Alumno(models.Model):
	legajo = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	dni = models.IntegerField(null=True, blank=True)
	direccion = models.CharField(max_length=100, null=True, blank=True)
	telefono = models.CharField(max_length=20)
	nacionalidad = models.CharField(max_length=20)
	padre = models.ForeignKey(Padre, null=True, blank=True)
	madre = models.ForeignKey(Madre, null=True, blank=True)
	tutor = models.ForeignKey(Tutor, null=True, blank=True)
	activo = models.BooleanField(default=True)
	libre = models.BooleanField(default=False)
	condicional = models.BooleanField(default=False)
	curso = models.ForeignKey(Curso)
	def __str__(self):
		return self.apellido + " " + self.nombre


