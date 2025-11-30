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


class ReglaAsistencia(models.Model):
	"""
	Matriz de reglas para calcular la falta final basada en la combinación de turnos.
	Importada desde 'Asistencia - Codigos.csv'
	"""
	# Entradas (Códigos por turno) - '-' indica que no hubo turno
	codigo_manana = models.CharField(max_length=1, help_text="Código en turno mañana (P, A, T, R, -)")
	codigo_tarde = models.CharField(max_length=1, help_text="Código en turno tarde (P, A, T, R, -)")
	codigo_ed_fisica = models.CharField(max_length=1, help_text="Código en turno ed. física (P, A, T, R, -)")
	
	# Salidas
	valor_falta = models.FloatField(help_text="Valor numérico de la falta resultante")
	observacion = models.CharField(max_length=255, help_text="Texto explicativo para la familia")
	
	def __str__(self):
		return f"M:{self.codigo_manana} T:{self.codigo_tarde} E:{self.codigo_ed_fisica} = {self.valor_falta}"
	
	class Meta:
		verbose_name = "Regla de Asistencia"
		verbose_name_plural = "Reglas de Asistencia"
		unique_together = ['codigo_manana', 'codigo_tarde', 'codigo_ed_fisica']


class Turno(models.Model):
	TURNO_CHOICES = (
		('mañana', 'Mañana'),
		('tarde', 'Tarde'),
		('educacion_fisica', 'Educación Física'),
	)
	nombre = models.CharField(max_length=20, choices=TURNO_CHOICES, unique=True)
	
	def __str__(self):
		return self.get_nombre_display()
	
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
	Modelo para registrar el cierre diario de asistencias.
	Es el evento global de cierre.
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
	
	observaciones_cierre = models.TextField(
		blank=True, 
		null=True, 
		help_text="Observaciones generales del cierre diario"
	)
	
	def __str__(self):
		return f"Cierre {self.fecha} - {self.usuario_cierre.get_full_name() or self.usuario_cierre.username}"
	
	class Meta:
		verbose_name_plural = "Cierres Diarios"
		ordering = ['-fecha']


class DetalleCierreCurso(models.Model):
	"""
	Configuración específica de qué turnos se dictaron para cada Curso y Grupo en un día específico.
	Esto permite manejar excepciones (ej: un curso no tuvo tarde hoy, o solo Grupo 1 tuvo Ed Física).
	"""
	cierre = models.ForeignKey(CierreDiario, related_name='detalles', on_delete=models.CASCADE)
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	
	GRUPO_CHOICES = (
		('unico', 'Único'),
		('1', 'Grupo 1'),
		('2', 'Grupo 2'),
	)
	grupo = models.CharField(max_length=10, choices=GRUPO_CHOICES, default='unico')
	
	# Qué turnos se dictaron efectivamente
	hubo_turno_manana = models.BooleanField(default=True)
	hubo_turno_tarde = models.BooleanField(default=False)
	hubo_turno_ed_fisica = models.BooleanField(default=False)
	
	def __str__(self):
		return f"{self.curso} ({self.get_grupo_display()}) - M:{self.hubo_turno_manana} T:{self.hubo_turno_tarde} E:{self.hubo_turno_ed_fisica}"
	
	class Meta:
		unique_together = ['cierre', 'curso', 'grupo']
		verbose_name = "Detalle de Cierre por Curso"
		verbose_name_plural = "Detalles de Cierre por Curso"


class ResumenDiarioAlumno(models.Model):
	"""
	Resumen diario de asistencias por alumno después del cierre.
	Se calcula cruzando las Asistencias registradas con el DetalleCierreCurso y la ReglaAsistencia.
	"""
	cierre_diario = models.ForeignKey(CierreDiario, on_delete=models.CASCADE)
	alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
	fecha = models.DateField()
	
	# Códigos por turno (P, A, T, R o - si no hubo turno)
	codigo_manana = models.CharField(max_length=1, default='-')
	codigo_tarde = models.CharField(max_length=1, default='-')
	codigo_ed_fisica = models.CharField(max_length=1, default='-')
	
	# Valor final calculado desde ReglaAsistencia
	valor_falta_final = models.FloatField(
		default=0.0, 
		help_text="Valor final de falta calculado según las combinaciones de turnos"
	)
	
	# Observación automática desde ReglaAsistencia
	observacion_calculada = models.CharField(max_length=255, blank=True, null=True)
	
	def __str__(self):
		return f"{self.alumno} - {self.fecha} - Falta: {self.valor_falta_final}"
	
	class Meta:
		verbose_name_plural = "Resúmenes Diarios por Alumno"
		unique_together = ['alumno', 'fecha']
		ordering = ['-fecha', 'alumno__apellido', 'alumno__nombre']
