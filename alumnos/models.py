# -*- encoding: utf-8 -*-
from django.db import models
from smart_selects.db_fields import ChainedForeignKey

from escuela.models import Curso


class Padre(models.Model):
	nombre_padre = models.CharField(max_length=50)
	apellido_padre = models.CharField(max_length=50)
	dni_padre = models.IntegerField(null=True, blank=True)
	direccion_padre = models.CharField(max_length=100, null=True, blank=True)
	telefono_padre = models.CharField(max_length=20, null=True, blank=True)
	celular_padre = models.CharField(max_length=20, null=True, blank=True)
	email_padre = models.EmailField(max_length=100, null=True, blank=True)
	profesion_padre = models.CharField(max_length=100, null=True, blank=True)
	nacionalidad_padre = models.CharField(max_length=20, null=True, blank=True)
	
	class Meta:
		verbose_name_plural = "Padres"
	
	def __str__(self):
		return f"{self.apellido_padre}, {self.nombre_padre}"

class Madre(models.Model):
	nombre_madre = models.CharField(max_length=50)
	apellido_madre = models.CharField(max_length=50)
	dni_madre = models.IntegerField(null=True, blank=True)
	direccion_madre = models.CharField(max_length=100, null=True, blank=True)
	telefono_madre = models.CharField(max_length=20, null=True, blank=True)
	celular_madre = models.CharField(max_length=20, null=True, blank=True)
	email_madre = models.EmailField(max_length=100, null=True, blank=True)
	profesion_madre = models.CharField(max_length=100, null=True, blank=True)
	nacionalidad_madre = models.CharField(max_length=20, null=True, blank=True)
	
	class Meta:
		verbose_name_plural = "Madres"
	
	def __str__(self):
		return f"{self.apellido_madre}, {self.nombre_madre}"

class Tutor(models.Model):
	nombre_tutor = models.CharField(max_length=50)
	apellido_tutor = models.CharField(max_length=50)
	dni_tutor = models.IntegerField(null=True, blank=True)
	direccion_tutor = models.CharField(max_length=100, null=True, blank=True)
	telefono_tutor = models.CharField(max_length=20, null=True, blank=True)
	celular_tutor = models.CharField(max_length=20, null=True, blank=True)
	email_tutor = models.EmailField(max_length=100, null=True, blank=True)
	profesion_tutor = models.CharField(max_length=100, null=True, blank=True)
	nacionalidad_tutor = models.CharField(max_length=20, null=True, blank=True)
	vinculo_tutor = models.CharField(max_length=50, null=True, blank=True, help_text="Relación con el estudiante")
	
	class Meta:
		verbose_name_plural = "Tutores"
	
	def __str__(self):
		return f"{self.apellido_tutor}, {self.nombre_tutor}"

class Alumno(models.Model):
	# Identificación
	legajo = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
	apellido = models.CharField(max_length=50)
	dni = models.IntegerField(null=True, blank=True)
	documento_tipo = models.CharField(max_length=10, default='DNI', null=True, blank=True)
	cuil = models.CharField(max_length=15, null=True, blank=True, help_text="CUIL del estudiante (formato: XX-XXXXXXXX-X)")
	
	# Estado del DNI
	DNI_ESTADO_CHOICES = (
		('tiene_fisico', 'Si, y tiene el DNI físico'),
		('en_tramite', 'SI, pero NO tiene el DNI físico y se encuentra en trámite'),
		('no_en_tramite', 'Si, pero NO tiene el DNI físico y NO se encuentra en trámite'),
		('no_posee', 'NO posee DNI argentino'),
	)
	estado_dni = models.CharField(max_length=20, choices=DNI_ESTADO_CHOICES, null=True, blank=True)
	tiene_certificado_pre_identificacion = models.BooleanField(default=False, help_text="¿Posee certificado de Pre-Identificación (CPI)?")
	
	# Identidad de género (ampliada según ficha)
	IDENTIDAD_GENERO_CHOICES = (
		('M', 'Varón'),
		('F', 'Mujer'),
		('MT', 'Mujer trans/travesti'),
		('VT', 'Varón trans/masculinidad trans'),
		('NB', 'No binario'),
		('O', 'Otra'),
		('ND', 'No desea responder'),
	)
	identidad_genero = models.CharField(max_length=2, choices=IDENTIDAD_GENERO_CHOICES, null=True, blank=True, help_text="Identidad de género")
	
	# Mantener sexo para compatibilidad (deprecated, usar identidad_genero)
	SEXO_CHOICES = (
		('M', 'Masculino'),
		('F', 'Femenino'),
	)
	sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, null=True, blank=True)
	
	fecha_nacimiento = models.DateField(null=True, blank=True)
	lugar_nacimiento = models.CharField(max_length=100, null=True, blank=True)
	nacionalidad = models.CharField(max_length=20, null=True, blank=True)
	
	# Contacto
	email = models.EmailField(max_length=100, null=True, blank=True)
	
	# Domicilio detallado
	direccion = models.CharField(max_length=100, null=True, blank=True, help_text="Calle")
	numero_domicilio = models.CharField(max_length=10, null=True, blank=True, help_text="Número")
	piso = models.CharField(max_length=10, null=True, blank=True)
	torre = models.CharField(max_length=20, null=True, blank=True)
	depto = models.CharField(max_length=10, null=True, blank=True, help_text="Departamento")
	entre_calle_1 = models.CharField(max_length=100, null=True, blank=True, help_text="Entre calle")
	entre_calle_2 = models.CharField(max_length=100, null=True, blank=True, help_text="Y calle")
	localidad = models.CharField(max_length=100, null=True, blank=True)
	provincia = models.CharField(max_length=50, null=True, blank=True)
	distrito = models.CharField(max_length=50, null=True, blank=True, help_text="Distrito/Partido")
	codigo_postal = models.CharField(max_length=10, null=True, blank=True)
	
	# Teléfonos con código de área separado
	codigo_area_telefono = models.CharField(max_length=5, null=True, blank=True, help_text="Código de área")
	telefono = models.CharField(max_length=20, null=True, blank=True, help_text="Número de teléfono")
	codigo_area_celular = models.CharField(max_length=5, null=True, blank=True, help_text="Código de área celular")
	celular_alumno = models.CharField(max_length=20, null=True, blank=True, help_text="Número de celular")
	
	# Responsables
	padre = models.ForeignKey(Padre, null=True, blank=True, on_delete=models.SET_NULL, related_name='hijos')
	madre = models.ForeignKey(Madre, null=True, blank=True, on_delete=models.SET_NULL, related_name='hijos')
	tutor = models.ForeignKey(Tutor, null=True, blank=True, on_delete=models.SET_NULL, related_name='tutelados')
	
	# Académico
	curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
	GRUPO_CHOICES = (
		('unico', 'Único'),
		('1', 'Grupo 1'),
		('2', 'Grupo 2'),
	)
	grupo = models.CharField(max_length=10, choices=GRUPO_CHOICES, default='unico')
	fecha_ingreso = models.DateField(null=True, blank=True)
	colegio_procedencia = models.CharField(max_length=200, null=True, blank=True)
	
	# Estado
	activo = models.BooleanField(default=True)
	libre = models.BooleanField(default=False)
	condicional = models.BooleanField(default=False)
	fecha_baja = models.DateField(null=True, blank=True)
	dispensa = models.BooleanField(default=False, help_text="Dispensa de educación física u otras")
	motivo_dispensa = models.CharField(max_length=200, null=True, blank=True)
	
	# Familia
	tiene_hermanos = models.BooleanField(default=False, help_text="¿Tiene hermanas o hermanos?")
	cantidad_hermanos = models.IntegerField(default=0, help_text="Cantidad total de hermanos")
	hermanos_en_establecimiento = models.IntegerField(default=0, help_text="Cantidad de hermanos que asisten a este establecimiento")
	
	# Cultural y Social
	habla_lenguas_distintas_castellano = models.BooleanField(default=False, help_text="¿Se hablan lenguas distintas al castellano en el hogar?")
	lenguas_indigenas = models.CharField(max_length=200, null=True, blank=True, help_text="Lengua/s indígena/s")
	otras_lenguas = models.CharField(max_length=200, null=True, blank=True, help_text="Otra/s lengua/s")
	pertenece_pueblos_originarios = models.BooleanField(default=False, help_text="¿Se reconoce perteneciente o descendiente de Pueblos Originarios?")
	
	# Beneficios Sociales
	percibe_auh = models.BooleanField(default=False, help_text="Percibe Asignación Universal por Hijo (AUH)")
	percibe_progresar = models.BooleanField(default=False, help_text="Percibe Progresar")
	
	# Transporte (múltiple selección usando JSONField o ManyToMany)
	TRANSPORTE_CHOICES = (
		('pie_bicicleta', 'A pie/bicicleta'),
		('transporte_escolar', 'Transporte escolar DGCyE'),
		('colectivo', 'Colectivo'),
		('tren', 'Tren'),
		('vehiculo_particular', 'Vehículo particular'),
		('taxi_remis', 'Taxi/Remis'),
		('otro', 'Otro'),
	)
	# Usaremos un campo CharField con valores separados por comas para múltiple selección
	medio_transporte = models.CharField(max_length=200, null=True, blank=True, help_text="Medios de transporte (separados por comas)")
	
	# Administrativo
	observaciones_admin = models.TextField(null=True, blank=True)
	porcentaje_beca = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Porcentaje de beca")
	
	class Meta:
		verbose_name_plural = "Alumnos"
		ordering = ['apellido', 'nombre']
	
	@property
	def edad(self):
		"""Calcula la edad del alumno basado en fecha_nacimiento"""
		if self.fecha_nacimiento:
			from datetime import date
			hoy = date.today()
			return hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
		return None
	
	def get_responsable_principal(self):
		"""Retorna el responsable principal (madre > padre > tutor)"""
		if self.madre:
			return self.madre
		elif self.padre:
			return self.padre
		elif self.tutor:
			return self.tutor
		return None
	
	def __str__(self):
		return f"[{self.legajo}] {self.apellido}, {self.nombre}"


