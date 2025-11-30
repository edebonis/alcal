# -*- encoding: utf-8 -*-
from django.contrib import admin
from .models import Padre, Madre, Tutor, Alumno


@admin.register(Padre)
class PadreAdmin(admin.ModelAdmin):
	list_display = ('apellido_padre', 'nombre_padre', 'dni_padre', 'telefono_padre', 'celular_padre', 'email_padre')
	search_fields = ('apellido_padre', 'nombre_padre', 'dni_padre', 'email_padre')
	list_filter = ('nacionalidad_padre',)
	
	fieldsets = (
		('Información Personal', {
			'fields': ('nombre_padre', 'apellido_padre', 'dni_padre', 'nacionalidad_padre', 'profesion_padre')
		}),
		('Contacto', {
			'fields': ('telefono_padre', 'celular_padre', 'email_padre', 'direccion_padre')
		}),
	)


@admin.register(Madre)
class MadreAdmin(admin.ModelAdmin):
	list_display = ('apellido_madre', 'nombre_madre', 'dni_madre', 'telefono_madre', 'celular_madre', 'email_madre')
	search_fields = ('apellido_madre', 'nombre_madre', 'dni_madre', 'email_madre')
	list_filter = ('nacionalidad_madre',)
	
	fieldsets = (
		('Información Personal', {
			'fields': ('nombre_madre', 'apellido_madre', 'dni_madre', 'nacionalidad_madre', 'profesion_madre')
		}),
		('Contacto', {
			'fields': ('telefono_madre', 'celular_madre', 'email_madre', 'direccion_madre')
		}),
	)


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
	list_display = ('apellido_tutor', 'nombre_tutor', 'vinculo_tutor', 'dni_tutor', 'telefono_tutor', 'celular_tutor')
	search_fields = ('apellido_tutor', 'nombre_tutor', 'dni_tutor', 'email_tutor')
	list_filter = ('nacionalidad_tutor', 'vinculo_tutor')
	
	fieldsets = (
		('Información Personal', {
			'fields': ('nombre_tutor', 'apellido_tutor', 'dni_tutor', 'nacionalidad_tutor', 'profesion_tutor', 'vinculo_tutor')
		}),
		('Contacto', {
			'fields': ('telefono_tutor', 'celular_tutor', 'email_tutor', 'direccion_tutor')
		}),
	)


def marcar_activo(modeladmin, request, queryset):
	queryset.update(activo=True)
marcar_activo.short_description = "Marcar como activo"


def marcar_inactivo(modeladmin, request, queryset):
	queryset.update(activo=False)
marcar_inactivo.short_description = "Marcar como inactivo"


def asignar_grupo_1(modeladmin, request, queryset):
	queryset.update(grupo='1')
asignar_grupo_1.short_description = "Asignar a Grupo 1"


def asignar_grupo_2(modeladmin, request, queryset):
	queryset.update(grupo='2')
asignar_grupo_2.short_description = "Asignar a Grupo 2"


@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
	list_display = ('legajo', 'apellido', 'nombre', 'curso', 'grupo', 'edad', 'activo', 'sexo', 'descargar_pdf', 'descargar_constancia')
	list_filter = ('activo', 'curso', 'grupo', 'sexo', 'libre', 'condicional', 'curso__carrera')
	search_fields = ('legajo', 'apellido', 'nombre', 'dni', 'email')
	list_editable = ('activo', 'grupo')
	readonly_fields = ('edad', 'descargar_pdf', 'descargar_constancia')
	date_hierarchy = 'fecha_ingreso'
	list_per_page = 50
	
	actions = [marcar_activo, marcar_inactivo, asignar_grupo_1, asignar_grupo_2]
	
	fieldsets = (
		('Información Personal', {
			'fields': (
				('nombre', 'apellido'),
				('sexo', 'fecha_nacimiento', 'edad'),
				('dni', 'documento_tipo'),
				('nacionalidad', 'lugar_nacimiento'),
				('descargar_pdf', 'descargar_constancia'),
			)
		}),
		('Contacto', {
			'fields': (
				('email', 'celular_alumno'),
				('telefono',),
				('direccion', 'localidad'),
			)
		}),
		('Responsables', {
			'fields': (
				('padre', 'madre'),
				('tutor',),
			)
		}),
		('Información Académica', {
			'fields': (
				('curso', 'grupo'),
				('fecha_ingreso', 'colegio_procedencia'),
			)
		}),
		('Estado del Alumno', {
			'fields': (
				('activo', 'libre', 'condicional'),
				('fecha_baja',),
				('dispensa', 'motivo_dispensa'),
			)
		}),
		('Administrativo', {
			'classes': ('collapse',),
			'fields': (
				('porcentaje_beca',),
				('observaciones_admin',),
			)
		}),
	)
	
	def descargar_pdf(self, obj):
		"""Botón para descargar la ficha de inscripción en PDF"""
		from django.urls import reverse
		from django.utils.html import format_html
		
		url = reverse('exportar_ficha_pdf', args=[obj.legajo])
		return format_html(
			'<a class="button" href="{}" target="_blank" style="padding: 5px 10px; background-color: #417690; color: white; text-decoration: none; border-radius: 3px;">📄 PDF</a>',
			url
		)
	descargar_pdf.short_description = 'Ficha'
	descargar_pdf.allow_tags = True
	
	def descargar_constancia(self, obj):
		"""Botón para descargar la constancia de alumno regular en PDF"""
		from django.urls import reverse
		from django.utils.html import format_html
		
		url = reverse('exportar_constancia_alumno_regular', args=[obj.legajo])
		return format_html(
			'<a class="button" href="{}" target="_blank" style="padding: 5px 10px; background-color: #696969; color: white; text-decoration: none; border-radius: 3px;">🎓 Constancia</a>',
			url
		)
	descargar_constancia.short_description = 'Constancia'
	descargar_constancia.allow_tags = True

	
	def get_queryset(self, request):
		"""Optimiza las consultas con select_related"""
		qs = super().get_queryset(request)
		return qs.select_related('curso', 'padre', 'madre', 'tutor', 'curso__carrera')
