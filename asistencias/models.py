from django.db import models
from alumnos.models import Alumno

class Asistencia(models.Model):
	cantidad = models.IntegerField()
	alumno = models.ForeignKey(Alumno)
	codigo = models.CharField(max_length=5)
	fecha = models.DateField()
	def __str__(self):
		return '%s %s %s' % (self.fecha, self.codigo, self.cantidad)
