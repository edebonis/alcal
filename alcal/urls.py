from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from alcal import views
from asistencias import views as asistencias_views
from alumnos import views as alumnos_views
from docentes import views as docentes_views

urlpatterns = [
    # Home and admin
    path('', views.home, name='home'),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),

    # API v1
    path('api/v1/', include('alcal.api_urls')),

    # Administración personalizada
    path('gestion/', include('administracion.urls')),

    # Selectores principales
    path('consultas/', views.consultas_selector, name='consultas_selector'),
    path('ingresar/', views.ingresar_selector, name='ingresar_selector'),

    # Selectores específicos
    path('asistencia/', views.asistencia_selector, name='asistencia_selector'),
    path('calificaciones/', views.calificaciones_selector, name='calificaciones_selector'),

    # Asistencias por curso (existentes)
    path('ing_asistencia/', asistencias_views.ingresar_asistencia_selector, name='ing_asistencia'),
    path('cons_asistencia/', views.cons_asistencia, name='cons_asistencia'),

    # Asistencias por alumno (nuevas)
    path('ing_asistencia_alumno/', asistencias_views.tomar_asistencia_alumno, name='tomar_asistencia_alumno'),
    path('cons_asistencia_alumno/', views.cons_asistencia_alumno, name='cons_asistencia_alumno'),

    # Asistencias por curso (específicas)
    path('tomar_asistencia_curso/', asistencias_views.tomar_asistencia_curso, name='tomar_asistencia_curso'),
    path('lista_alumnos_curso/', asistencias_views.lista_alumnos_curso, name='lista_alumnos_curso'),
    path('guardar_asistencia_curso/', asistencias_views.guardar_asistencia_curso, name='guardar_asistencia_curso'),
    path('consultar_asistencia_curso/', asistencias_views.consultar_asistencia_curso, name='consultar_asistencia_curso'),

    # Calificaciones por curso (existentes)
    path('ing_calificaciones/', views.ing_calificaciones, name='ing_calificaciones'),
    path('ingresar_calificaciones_curso/', views.ingresar_calificaciones_curso, name='ingresar_calificaciones_curso'),
    path('cons_calificaciones/', views.cons_calificaciones, name='cons_calificaciones'),
    path('consultar_calificaciones_curso/', views.consultar_calificaciones_curso, name='consultar_calificaciones_curso'),

    # Calificaciones por alumno (nuevas)
    path('ing_calificaciones_alumno/', views.ing_calificaciones_alumno, name='ing_calificaciones_alumno'),
    path('cons_calificaciones_alumno/', views.cons_calificaciones_alumno, name='cons_calificaciones_alumno'),
    path('consultar_calificaciones_alumno/', views.cons_calificaciones_alumno, name='consultar_calificaciones_alumno'),
    path('ingresar_calificaciones/', views.ingresar_calificaciones, name='ingresar_calificaciones'),

    # Observaciones (mantener existentes)
    path('observaciones/', views.observaciones, name='observaciones'),
    path('ing_observaciones/', views.ing_observaciones, name='ing_observaciones'),
    path('ing_observaciones_cur/', views.ing_observaciones_cur, name='ing_observaciones_cur'),
    path('cons_observaciones/', views.cons_observaciones, name='cons_observaciones'),
    path('cons_observaciones_cur/', views.cons_observaciones_cur, name='cons_observaciones_cur'),

    # Cierre diario
    path('cierre_diario/', asistencias_views.cierre_diario_seleccion, name='cierre_diario_seleccion'),
    path('procesar_cierre_diario/', asistencias_views.procesar_cierre_diario, name='procesar_cierre_diario'),
    
    # Exportaciones PDF
    path('alumnos/<int:alumno_id>/ficha-pdf/', alumnos_views.exportar_ficha_pdf, name='exportar_ficha_pdf'),
    path('docentes/pdf/<int:docente_id>/', docentes_views.exportar_ficha_docente, name='exportar_ficha_docente'),
    path('alumnos/<int:alumno_id>/constancia-pdf/', alumnos_views.exportar_constancia_alumno_regular, name='exportar_constancia_alumno_regular'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)