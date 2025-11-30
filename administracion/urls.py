""

from django.urls import path
from . import views

app_name = 'administracion'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # CRUD Carreras
    path('carreras/', views.carrera_list, name='carrera_list'),
    path('carreras/crear/', views.carrera_create, name='carrera_create'),
    path('carreras/<int:pk>/editar/', views.carrera_update, name='carrera_update'),
    path('carreras/<int:pk>/eliminar/', views.carrera_delete, name='carrera_delete'),
    
    # CRUD Cursos
    path('cursos/', views.curso_list, name='curso_list'),
    path('cursos/crear/', views.curso_create, name='curso_create'),
    path('cursos/<int:pk>/editar/', views.curso_update, name='curso_update'),
    path('cursos/<int:pk>/eliminar/', views.curso_delete, name='curso_delete'),
    
    # CRUD Materias
    path('materias/', views.materia_list, name='materia_list'),
    path('materias/crear/', views.materia_create, name='materia_create'),
    path('materias/<int:pk>/editar/', views.materia_update, name='materia_update'),
    path('materias/<int:pk>/eliminar/', views.materia_delete, name='materia_delete'),
    
    # CRUD Docentes
    path('docentes/', views.docente_list, name='docente_list'),
    path('docentes/crear/', views.docente_create, name='docente_create'),
    path('docentes/<int:pk>/editar/', views.docente_update, name='docente_update'),
    path('docentes/<int:pk>/eliminar/', views.docente_delete, name='docente_delete'),
    path('docentes/<int:pk>/', views.docente_detail, name='docente_detail'),
    
    # CRUD Alumnos
    path('alumnos/', views.alumno_list, name='alumno_list'),
    path('alumnos/crear/', views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/', views.alumno_update, name='alumno_update'),
    path('alumnos/<int:pk>/eliminar/', views.alumno_delete, name='alumno_delete'),
    path('alumnos/<int:pk>/', views.alumno_detail, name='alumno_detail'),
    
    # CRUD Turnos (solo visualización - los turnos son fijos: Mañana, Tarde, Educación Física)
    path('turnos/', views.turno_list, name='turno_list'),
    # path('turnos/crear/', views.turno_create, name='turno_create'),  # Deshabilitado - turnos fijos
    # path('turnos/<int:pk>/editar/', views.turno_update, name='turno_update'),  # Deshabilitado - turnos fijos
    # path('turnos/<int:pk>/eliminar/', views.turno_delete, name='turno_delete'),  # Deshabilitado - turnos fijos
    
    # CRUD Códigos de Asistencia
    path('codigos-asistencia/', views.codigo_asistencia_list, name='codigo_asistencia_list'),
    path('codigos-asistencia/crear/', views.codigo_asistencia_create, name='codigo_asistencia_create'),
    path('codigos-asistencia/<int:pk>/editar/', views.codigo_asistencia_update, name='codigo_asistencia_update'),
    path('codigos-asistencia/<int:pk>/eliminar/', views.codigo_asistencia_delete, name='codigo_asistencia_delete'),
]
