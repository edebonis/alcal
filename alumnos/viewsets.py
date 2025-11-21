from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Alumno, Padre, Madre, Tutor
from .serializers import (
    AlumnoSerializer, AlumnoListSerializer,
    PadreSerializer, MadreSerializer, TutorSerializer
)


class AlumnoViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar alumnos.
    
    list: Listar todos los alumnos
    retrieve: Obtener detalle de un alumno
    create: Crear un nuevo alumno
    update: Actualizar un alumno existente
    partial_update: Actualizar parcialmente un alumno
    destroy: Eliminar un alumno
    """
    queryset = Alumno.objects.select_related('curso', 'padre', 'madre', 'tutor').all()
    serializer_class = AlumnoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['curso', 'activo', 'libre', 'condicional']
    search_fields = ['nombre', 'apellido', 'dni']
    ordering_fields = ['apellido', 'nombre', 'legajo']
    ordering = ['apellido', 'nombre']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AlumnoListSerializer
        return AlumnoSerializer
    
    @action(detail=False, methods=['get'])
    def por_curso(self, request):
        """Obtener alumnos filtrados por curso"""
        curso_id = request.query_params.get('curso_id')
        if curso_id:
            alumnos = self.queryset.filter(curso_id=curso_id)
            serializer = AlumnoListSerializer(alumnos, many=True)
            return Response(serializer.data)
        return Response({'error': 'curso_id es requerido'}, status=400)


class PadreViewSet(viewsets.ModelViewSet):
    queryset = Padre.objects.all()
    serializer_class = PadreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre_padre', 'apellido_padre', 'dni_padre']


class MadreViewSet(viewsets.ModelViewSet):
    queryset = Madre.objects.all()
    serializer_class = MadreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre_madre', 'apellido_madre', 'dni_madre']


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre_tutor', 'apellido_tutor', 'dni_tutor']
