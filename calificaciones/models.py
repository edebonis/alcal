from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from alumnos.models import Alumno
from escuela.models import Anio, Curso, Materia


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
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)  
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)  
    alumno = ChainedForeignKey(  
        Alumno,   
        chained_field="curso",   
        chained_model_field="curso",  
        on_delete=models.CASCADE  
    )  
    ciclo_lectivo = models.ForeignKey(CicloLectivo, on_delete=models.CASCADE)  
      
    class Meta:  
        verbose_name_plural = "Calificaciones Trimestrales"

class CalificacionParcial(models.Model):
	nota = models.IntegerField()
	fecha = models.DateField()
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=False)
	materia = ChainedForeignKey(Materia, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=False)
	ciclo_lectivo = models.ForeignKey(CicloLectivo, on_delete=models.CASCADE)
	class Meta:
		verbose_name_plural = "Calificaciones Parciales"