from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Carrera, Anio, Curso, Materia
from .serializers import CarreraSerializer, AnioSerializer, CursoSerializer, MateriaSerializer


class CarreraViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar carreras"""
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']


class AnioViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar años lectivos"""
    queryset = Anio.objects.all()
    serializer_class = AnioSerializer
    ordering = ['-ciclo_lectivo']


class CursoViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar cursos"""
    queryset = Curso.objects.select_related('carrera').all()
    serializer_class = CursoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['carrera']
    search_fields = ['curso']
    ordering = ['curso']


class MateriaViewSet(viewsets.ModelViewSet):
    """API endpoint para gestionar materias"""
    queryset = Materia.objects.select_related('curso').all()
    serializer_class = MateriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['curso']
    search_fields = ['nombre']
    ordering = ['curso', 'nombre']
