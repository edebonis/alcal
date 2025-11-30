from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from datetime import date

from .models import Asistencia, CodigoAsistencia, Turno, CierreDiario, ResumenDiarioAlumno
from .serializers import (
    AsistenciaSerializer, AsistenciaListSerializer,
    CodigoAsistenciaSerializer, TurnoSerializer,
    CierreDiarioSerializer, ResumenDiarioAlumnoSerializer
)



class CodigoAsistenciaViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para consultar códigos de asistencia (solo lectura)"""
    queryset = CodigoAsistencia.objects.all()
    serializer_class = CodigoAsistenciaSerializer
    ordering = ['codigo']


class TurnoViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para consultar turnos (solo lectura)"""
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    ordering = ['hora_inicio']


class AsistenciaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar asistencias.
    
    Permite filtrar por:
    - curso
    - alumno
    - fecha (fecha, fecha_desde, fecha_hasta)
    - turno
    - procesado
    """
    queryset = Asistencia.objects.select_related(
        'alumno', 'curso', 'codigo', 'turno', 'ciclo_lectivo'
    ).all()
    serializer_class = AsistenciaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['curso', 'alumno', 'turno', 'fecha', 'procesado']
    ordering_fields = ['fecha', 'alumno__apellido']
    ordering = ['-fecha', 'alumno__apellido']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AsistenciaListSerializer
        return AsistenciaSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por rango de fechas
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """Obtener estadísticas de asistencias"""
        curso_id = request.query_params.get('curso')
        fecha = request.query_params.get('fecha', date.today())
        
        queryset = self.get_queryset()
        if curso_id:
            queryset = queryset.filter(curso_id=curso_id)
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        
        # Contar por código
        from django.db.models import Count
        stats = queryset.values('codigo__codigo', 'codigo__descripcion').annotate(
            cantidad=Count('id')
        )
        
        return Response({
            'total': queryset.count(),
            'por_codigo': list(stats)
        })


class CierreDiarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para consultar cierres diarios.
    Solo lectura, el cierre se realiza a través de las vistas tradicionales.
    """
    queryset = CierreDiario.objects.select_related('usuario_cierre').all()
    serializer_class = CierreDiarioSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['fecha']
    ordering = ['-fecha']


class ResumenDiarioAlumnoViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint para consultar resúmenes diarios de alumnos"""
    queryset = ResumenDiarioAlumno.objects.select_related('alumno', 'cierre_diario').all()
    serializer_class = ResumenDiarioAlumnoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['alumno', 'fecha']
    ordering = ['-fecha', 'alumno__apellido']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por rango de fechas
        fecha_desde = self.request.query_params.get('fecha_desde')
        fecha_hasta = self.request.query_params.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
        
        return queryset
