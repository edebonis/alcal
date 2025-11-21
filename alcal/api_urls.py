"""
API v1 URLs configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from alumnos.viewsets import AlumnoViewSet, PadreViewSet, MadreViewSet, TutorViewSet
from escuela.viewsets import CarreraViewSet, AnioViewSet, CursoViewSet, MateriaViewSet
from asistencias.viewsets import (
    AsistenciaViewSet, CodigoAsistenciaViewSet, TurnoViewSet,
    CierreDiarioViewSet, ResumenDiarioAlumnoViewSet
)

# Create router
router = DefaultRouter()

# Alumnos app
router.register(r'alumnos', AlumnoViewSet, basename='alumno')
router.register(r'padres', PadreViewSet, basename='padre')
router.register(r'madres', MadreViewSet, basename='madre')
router.register(r'tutores', TutorViewSet, basename='tutor')

# Escuela app
router.register(r'carreras', CarreraViewSet, basename='carrera')
router.register(r'anios', AnioViewSet, basename='anio')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'materias', MateriaViewSet, basename='materia')

# Asistencias app
router.register(r'asistencias', AsistenciaViewSet, basename='asistencia')
router.register(r'codigos-asistencia', CodigoAsistenciaViewSet, basename='codigo-asistencia')
router.register(r'turnos', TurnoViewSet, basename='turno')
router.register(r'cierres-diarios', CierreDiarioViewSet, basename='cierre-diario')
router.register(r'resumenes-diarios', ResumenDiarioAlumnoViewSet, basename='resumen-diario')

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    
    # API Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
