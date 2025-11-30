# -*- encoding: utf-8 -*-
from django.db import models
from escuela.models import Materia

class Docente(models.Model):
	# Identificación
	legajo_numero = models.CharField(max_length=20, blank=True, null=True, help_text="Número de legajo docente")
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	dni = models.IntegerField(null=True, blank=True)
	
	SEXO_CHOICES = (
		('M', 'Masculino'),
		('F', 'Femenino'),
	)
	sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	nacionalidad = models.CharField(max_length=20, null=True, blank=True)
	
	# Contacto
	email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
	direccion = models.CharField(max_length=100, null=True, blank=True)
	telefono = models.CharField(max_length=20, null=True, blank=True)
	celular = models.CharField(max_length=20, null=True, blank=True)
	
	# Laboral
	fecha_alta = models.DateField(null=True, blank=True, help_text="Fecha de ingreso a la institución")
	fecha_baja = models.DateField(null=True, blank=True)
	dispensa = models.BooleanField(default=False, help_text="Dispensa de educación física u otras")
	motivo_dispensa = models.CharField(max_length=200, null=True, blank=True, help_text="Motivo de la dispensa")
	activo = models.BooleanField(default=True)
	
	CARGO_CHOICES = (
		('DOCENTE', 'Docente'),
		('DIRECTOR', 'Director'),
		('VICEDIRECTOR', 'Vicedirector'),
		('JEFE_TALLER', 'Jefe de Taller'),
		('PRECEPTOR', 'Preceptor'),
		('SECRETARIO', 'Secretario/a'),
		('PROSECRETARIO', 'Prosecretario/a'),
		('AYUDANTE_TP', 'Ayudante de Trabajos Prácticos'),
		('OTROS', 'Otros'),
	)
	cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='DOCENTE')
	
	MODALIDAD_CHOICES = (
		('TECNICA', 'Técnica'),
		('ECONOMIA', 'Economía'),
		('AMBAS', 'T/E'),
	)
	modalidad = models.CharField(max_length=10, choices=MODALIDAD_CHOICES, null=True, blank=True)
	
	# Antigüedad y horas
	anios_antiguedad = models.IntegerField(default=0, help_text="Años de antigüedad")
	meses_antiguedad = models.IntegerField(default=0, help_text="Meses de antigüedad")
	horas_totales = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Horas cátedra semanales")
	horas_extension = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Horas de extensión")
	
	# Situación de revista
	es_titular = models.BooleanField(default=False)
	es_suplente = models.BooleanField(default=False)
	
	# Relaciones
	materia = models.ManyToManyField(Materia, blank=True, related_name='docentes')
	
	class Meta:
		verbose_name_plural = "Docentes"
		ordering = ['apellido', 'nombre']
	
	@property
	def antiguedad_completa(self):
		"""Retorna la antigüedad en formato legible"""
		if self.anios_antiguedad or self.meses_antiguedad:
			return f"{self.anios_antiguedad} años, {self.meses_antiguedad} meses"
		return "Sin datos de antigüedad"
	
	def __str__(self):
		cargo_str = f" ({self.get_cargo_display()})" if self.cargo != 'DOCENTE' else ""
		return f"{self.apellido}, {self.nombre}{cargo_str}"
	