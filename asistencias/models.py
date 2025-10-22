# -*- encoding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from alumnos.models import Alumno
from escuela.models import Anio, Curso


class CodigoAsistencia(models.Model):
	CODIGO_CHOICES = (
		('P', 'Presente'),
		('t', 'Tarde (menos de 15 min)'),
		('T', 'Tarde (más de 15 min)'),
		('A', 'Ausente'),
		('r', 'Retirado (menos de 15 min antes del fin)'),
		('R', 'Retirado (más de 15 min antes del fin)'),
	)
	codigo = models.CharField(max_length=1, choices=CODIGO_CHOICES, unique=True)
	descripcion = models.CharField(max_length=100)
	cantidad_falta = models.FloatField(help_text="Valor de falta (0=presente, 0.5=media falta, 1=falta completa)")
	
	def __str__(self):
		return f"{self.codigo} - {self.descripcion}"
	
	class Meta:
		verbose_name_plural = "Códigos de Asistencia"


class Turno(models.Model):
	TURNO_CHOICES = (
		('mañana', 'Mañana'),
		('tarde', 'Tarde'),
		('educacion_fisica', 'Educación Física'),
	)
	nombre = models.CharField(max_length=20, choices=TURNO_CHOICES, unique=True)
	hora_inicio = models.TimeField()
	hora_fin = models.TimeField()
	
	def __str__(self):
		return f"{self.get_nombre_display()} ({self.hora_inicio} - {self.hora_fin})"
	
	class Meta:
		verbose_name_plural = "Turnos"


class Asistencia(models.Model):
	ciclo_lectivo = models.ForeignKey(Anio, on_delete=models.CASCADE)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	alumno = ChainedForeignKey(Alumno, chained_field="curso", chained_model_field="curso", show_all=False, auto_choose=True)
	codigo = models.ForeignKey(CodigoAsistencia, on_delete=models.CASCADE)
	turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
	fecha = models.DateField()
	observaciones = models.TextField(blank=True, null=True, help_text="Observaciones adicionales")
	
	# Campos para el cálculo final de faltas
	valor_falta_calculado = models.FloatField(
		null=True, 
		blank=True, 
		help_text="Valor final de falta calculado después del cierre del día"
	)
	procesado = models.BooleanField(
		default=False, 
		help_text="Indica si esta asistencia ya fue procesada en el cierre del día"
	)
	
	def __str__(self):
		return f"{self.alumno} - {self.fecha} - {self.turno} - {self.codigo}"
	
	class Meta:
		verbose_name_plural = "Asistencias"
		unique_together = ['alumno', 'fecha', 'turno']  # Un alumno no puede tener dos registros el mismo día y turno


class CierreDiario(models.Model):
	"""
	Modelo para registrar el cierre diario de asistencias
	"""
	fecha = models.DateField(unique=True, help_text="Fecha del día que se está cerrando")
	fecha_cierre = models.DateTimeField(auto_now_add=True, help_text="Momento en que se realizó el cierre")
	usuario_cierre = models.ForeignKey(
		User, 
		on_delete=models.CASCADE, 
		help_text="Usuario que realizó el cierre (debe ser preceptor o superior)"
	)
	
	# Estadísticas del cierre
	total_asistencias_procesadas = models.IntegerField(default=0)
	total_alumnos_procesados = models.IntegerField(default=0)
	total_cursos_procesados = models.IntegerField(default=0)
	
	observaciones_cierre = models.TextField(
		blank=True, 
		null=True, 
		help_text="Observaciones del cierre diario"
	)
	
	def __str__(self):
		return f"Cierre {self.fecha} - {self.usuario_cierre.get_full_name() or self.usuario_cierre.username}"
	
	class Meta:
		verbose_name_plural = "Cierres Diarios"
		ordering = ['-fecha']


class ResumenDiarioAlumno(models.Model):
	"""
	Resumen diario de asistencias por alumno después del cierre
	"""
	cierre_diario = models.ForeignKey(CierreDiario, on_delete=models.CASCADE)
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
	fecha = models.DateField()
	
	# Códigos por turno
	codigo_mañana = models.CharField(max_length=1, blank=True, null=True)
	codigo_tarde = models.CharField(max_length=1, blank=True, null=True)
	codigo_educacion_fisica = models.CharField(max_length=1, blank=True, null=True)
	
	# Turnos que tuvo clase
	tuvo_mañana = models.BooleanField(default=False)
	tuvo_tarde = models.BooleanField(default=False)
	tuvo_educacion_fisica = models.BooleanField(default=False)
	
	# Valor final calculado
	valor_falta_final = models.FloatField(
		default=0.0, 
		help_text="Valor final de falta calculado según las combinaciones de turnos"
	)
	
	observaciones_resumen = models.TextField(blank=True, null=True)
	
	def __str__(self):
		return f"{self.alumno} - {self.fecha} - Falta: {self.valor_falta_final}"
	
	class Meta:
		verbose_name_plural = "Resúmenes Diarios por Alumno"
		unique_together = ['alumno', 'fecha']
		ordering = ['-fecha', 'alumno__apellido', 'alumno__nombre']


