from django.db import models


class Carrera(models.Model):
	nombre = models.CharField(max_length=50)
	def __str__(self):
		return self.nombre

class Año(models.Model):
	año = models.IntegerField()
	def __str__(self):
		return str(self.año)

class Curso(models.Model):
	curso = models.CharField(max_length=5)
	año = models.ForeignKey(Año)
	carrera = models.ForeignKey(Carrera)
	def __str__(self):
		return self.curso

class Materia(models.Model):
	nombre = models.CharField(max_length=50)
	curso = models.ForeignKey(Curso)
	def __str__(self):
		return '%s %s' % (self.nombre, self.curso)




