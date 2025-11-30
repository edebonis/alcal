# -*- encoding: utf-8 -*-
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from smart_selects.db_fields import ChainedForeignKey

from alumnos.models import Alumno
from escuela.models import Anio, Curso, Materia


class Instancia(models.Model):
    instancia = models.CharField(max_length=50)
    
    def __str__(self):
        return self.instancia


class CalificacionTrimestral(models.Model):  
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Nota del 1 al 10"
    )  
    instancia = models.ForeignKey(Instancia, on_delete=models.CASCADE)  
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    materia = ChainedForeignKey(
        Materia, 
        chained_field="curso", 
        chained_model_field="curso", 
        show_all=False, 
        auto_choose=False,
        null=True, # Temporal para migración si hay datos
        blank=False
    )
    alumno = ChainedForeignKey(  
        Alumno,   
        chained_field="curso",   
        chained_model_field="curso",  
        on_delete=models.CASCADE  
    )  
    ciclo_lectivo = models.ForeignKey(Anio, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True, null=True) # Fecha de carga
      
    class Meta:  
        verbose_name_plural = "Calificaciones Trimestrales"
        unique_together = ['alumno', 'materia', 'instancia', 'ciclo_lectivo']

    def __str__(self):
        return f"{self.alumno} - {self.materia} - {self.instancia}: {self.nota}"


class CalificacionParcial(models.Model):
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Nota del 1 al 10"
    )
    fecha = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    alumno = ChainedForeignKey(
        Alumno, 
        chained_field="curso", 
        chained_model_field="curso", 
        show_all=False, 
        auto_choose=False
    )
    materia = ChainedForeignKey(
        Materia, 
        chained_field="curso", 
        chained_model_field="curso", 
        show_all=False, 
        auto_choose=False
    )
    ciclo_lectivo = models.ForeignKey(Anio, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = "Calificaciones Parciales"

    def __str__(self):
        return f"{self.alumno} - {self.materia} - {self.fecha}: {self.nota}"