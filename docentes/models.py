from django.db import models
from escuela.models import Materia

class Docente(models.Model):
	legajo = models.IntegerField()
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	dni = models.IntegerField(null=True, blank=True)
	direccion = models.CharField(max_length=100, null=True, blank=True)
	telefono = models.CharField(max_length=20)
	nacionalidad = models.CharField(max_length=20)
	materia = models.ManyToManyField(Materia)
	
	