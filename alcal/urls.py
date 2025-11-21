from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import include, path

from alcal import views
from asistencias import views as asistencias_views

urlpatterns = [  
    path('', views.home, name='home'),  
    path('grappelli/', include('grappelli.urls')),  
    path('admin/', admin.site.urls),  
    path('chaining/', include('smart_selects.urls')),
    
    # API v1
    path('api/v1/', include('alcal.api_urls')),
    
    # URLs principales de navegación - SELECTORES
    path('consultas/', views.consultas_selector, name='consultas'),  
    path('consultas/', views.consultas_selector, name='consultas_selector'),  
    path('ingresar/', views.ingresar_selector, name='ingresar'),  
    path('ingresar/', views.ingresar_selector, name='ingresar_selector'),  
    
    # URLs SELECTORES específicos
    path('asistencia/', views.asistencia_selector, name='asistencia_selector'),  
    path('calificaciones/', views.calificaciones_selector, name='calificaciones_selector'),  
    
    # URLs para asistencias POR CURSO (existentes)
    path('ing_asistencia/', views.ing_asistencia, name='ing_asistencia'),  
    # path('ing_asistencia_cur/', views.ing_asistencia_cur, name='ing_asistencia_cur'),  # Replaced by tomar_asistencia_curso
    path('cons_asistencia/', views.cons_asistencia, name='cons_asistencia'),  
    # path('cons_asistencia_cur/', views.cons_asistencia_cur, name='cons_asistencia_cur'),  # Replaced by consultar_asistencia_curso
    
    # URLs para asistencias POR ALUMNO (nuevas)
    path('ing_asistencia_alumno/', views.ing_asistencia_alumno, name='ing_asistencia_alumno'),
    path('cons_asistencia_alumno/', views.cons_asistencia_alumno, name='cons_asistencia_alumno'),
    
    # URLs para NUEVO SISTEMA DE ASISTENCIAS
    path('tomar_asistencia_curso/', asistencias_views.tomar_asistencia_curso, name='tomar_asistencia_curso'),
    path('lista_alumnos_curso/', asistencias_views.lista_alumnos_curso, name='lista_alumnos_curso'),
    path('guardar_asistencia_curso/', asistencias_views.guardar_asistencia_curso, name='guardar_asistencia_curso'),
    path('consultar_asistencia_curso/', asistencias_views.consultar_asistencia_curso, name='consultar_asistencia_curso'),
    
    # URLs para calificaciones POR CURSO (existentes)
    path('ing_calificaciones/', views.ing_calificaciones, name='ing_calificaciones'),  
    path('ingresar_calificaciones_curso/', views.ingresar_calificaciones_curso, name='ingresar_calificaciones_curso'),  
    path('cons_calificaciones/', views.cons_calificaciones, name='cons_calificaciones'),  
    path('cons_calificaciones/', views.cons_calificaciones, name='cons_calificaciones'),  
    # path('cons_calificaciones_cur/', views.cons_calificaciones_cur, name='cons_calificaciones_cur'),  # Replaced by consultar_calificaciones_curso
    path('consultar_calificaciones_curso/', views.consultar_calificaciones_curso, name='consultar_calificaciones_curso'),
    
    # URLs para calificaciones POR ALUMNO (nuevas)
    path('ing_calificaciones_alumno/', views.ing_calificaciones_alumno, name='ing_calificaciones_alumno'),
    path('cons_calificaciones_alumno/', views.cons_calificaciones_alumno, name='cons_calificaciones_alumno'),
    path('consultar_calificaciones_alumno/', views.cons_calificaciones_alumno, name='consultar_calificaciones_alumno'),
    path('ingresar_calificaciones/', views.ingresar_calificaciones, name='ingresar_calificaciones'),
    
    # URLs para observaciones (mantener existentes)
    path('observaciones/', views.observaciones, name='observaciones'),
    path('ing_observaciones/', views.ing_observaciones, name='ing_observaciones'),  
    path('ing_observaciones_cur/', views.ing_observaciones_cur, name='ing_observaciones_cur'),  
    path('cons_observaciones/', views.cons_observaciones, name='cons_observaciones'),  
    path('cons_observaciones_cur/', views.cons_observaciones_cur, name='cons_observaciones_cur'),  
    
    # URLs para cierre diario
    path('cierre_diario/', asistencias_views.cierre_diario_seleccion, name='cierre_diario_seleccion'),
    path('procesar_cierre_diario/', asistencias_views.procesar_cierre_diario, name='procesar_cierre_diario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)