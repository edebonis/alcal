# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Docente, DocenteMateria


class DocenteMateriaInline(admin.TabularInline):
	"""Inline para gestionar las materias del docente con grupos"""
	model = DocenteMateria
	extra = 1
	autocomplete_fields = ['materia']
	verbose_name = "Materia asignada"
	verbose_name_plural = "Materias asignadas"
	
	def formfield_for_choice_field(self, db_field, request, **kwargs):
		"""Personaliza el campo grupo para mostrar ayuda contextual"""
		if db_field.name == 'grupo':
			kwargs['help_text'] = 'Selecciona "Ambos grupos" para materias normales, o un grupo específico para materias técnico-específicas'
		return super().formfield_for_choice_field(db_field, request, **kwargs)


def marcar_activo(modeladmin, request, queryset):
	queryset.update(activo=True)
marcar_activo.short_description = "Marcar como activo"


def marcar_inactivo(modeladmin, request, queryset):
	queryset.update(activo=False)
marcar_inactivo.short_description = "Marcar como inactivo"


def marcar_titular(modeladmin, request, queryset):
	queryset.update(es_titular=True, es_suplente=False)
marcar_titular.short_description = "Marcar como titular"


def marcar_suplente(modeladmin, request, queryset):
	queryset.update(es_suplente=True, es_titular=False)
marcar_suplente.short_description = "Marcar como suplente"


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
	list_display = (
		'legajo_numero', 
		'apellido', 
		'nombre', 
		'cargo', 
		'modalidad', 
		'activo', 
		'horas_totales',
		'email',
		'pdf_button'
	)
	list_filter = (
		'activo', 
		'cargo', 
		'modalidad', 
		'sexo', 
		'es_titular', 
		'es_suplente'
	)
	search_fields = ('legajo_numero', 'apellido', 'nombre', 'dni', 'email')
	list_editable = ('activo',)
	readonly_fields = ('antiguedad_completa', 'pdf_button')
	date_hierarchy = 'fecha_alta'
	list_per_page = 50
	inlines = [DocenteMateriaInline]
	
	actions = [marcar_activo, marcar_inactivo, marcar_titular, marcar_suplente]
	
	fieldsets = (
		('Información Personal', {
			'fields': (
				('nombre', 'apellido'),
				('sexo', 'fecha_nacimiento'),
				('dni', 'nacionalidad'),
				('pdf_button',),
			)
		}),
		('Contacto', {
			'fields': (
				('email',),
				('telefono', 'celular'),
				('direccion',),
			)
		}),
		('Información Laboral', {
			'fields': (
				('legajo_numero', 'fecha_alta'),
				('cargo', 'modalidad'),
				('activo',),
				('horas_totales', 'horas_extension'),
			)
		}),
		('Antigüedad', {
			'fields': (
				('anios_antiguedad', 'meses_antiguedad'),
				('antiguedad_completa',),
			)
		}),
		('Situación de Revista', {
			'fields': (
				('es_titular', 'es_suplente'),
			)
		}),
	)
	
	def get_queryset(self, request):
		"""Optimiza las consultas con prefetch_related"""
		qs = super().get_queryset(request)
		return qs.prefetch_related('materias', 'docentemateria_set__materia')

	def pdf_button(self, obj):
		from django.utils.html import format_html
		from django.urls import reverse
		url = reverse('exportar_ficha_docente', args=[obj.id])
		return format_html('<a class="button" href="{}" target="_blank">📄 PDF</a>', url)
	pdf_button.short_description = 'Ficha'
	pdf_button.allow_tags = True


@admin.register(DocenteMateria)
class DocenteMateriaAdmin(admin.ModelAdmin):
	"""Admin para gestionar asignaciones docente-materia directamente"""
	list_display = ('docente', 'materia', 'grupo', 'es_tecnico_especifica_display')
	list_filter = ('grupo', 'materia__es_tecnico_especifica', 'materia__curso')
	search_fields = ('docente__apellido', 'docente__nombre', 'materia__nombre')
	autocomplete_fields = ['docente', 'materia']
	list_per_page = 100
	
	def es_tecnico_especifica_display(self, obj):
		return "✓" if obj.materia.es_tecnico_especifica else "✗"
	es_tecnico_especifica_display.short_description = 'Técnico-Específica'
	es_tecnico_especifica_display.boolean = True
