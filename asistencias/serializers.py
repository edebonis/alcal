from rest_framework import serializers
from .models import Asistencia, CodigoAsistencia, Turno, CierreDiario, ResumenDiarioAlumno


class CodigoAsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodigoAsistencia
        fields = ['id', 'codigo', 'descripcion', 'cantidad_falta']


class TurnoSerializer(serializers.ModelSerializer):
    nombre_display = serializers.CharField(source='get_nombre_display', read_only=True)
    
    class Meta:
        model = Turno
        fields = ['id', 'nombre', 'nombre_display', 'hora_inicio', 'hora_fin']


class AsistenciaSerializer(serializers.ModelSerializer):
    alumno_nombre = serializers.CharField(source='alumno.apellido', read_only=True)
    alumno_completo = serializers.SerializerMethodField()
    curso_nombre = serializers.CharField(source='curso.curso', read_only=True)
    codigo_info = CodigoAsistenciaSerializer(source='codigo', read_only=True)
    turno_info = TurnoSerializer(source='turno', read_only=True)
    
    class Meta:
        model = Asistencia
        fields = ['id', 'ciclo_lectivo', 'curso', 'curso_nombre', 'alumno', 
                  'alumno_nombre', 'alumno_completo', 'codigo', 'codigo_info',
                  'turno', 'turno_info', 'fecha', 'observaciones', 
                  'valor_falta_calculado', 'procesado']
        read_only_fields = ['valor_falta_calculado', 'procesado']
    
    def get_alumno_completo(self, obj):
        return f"{obj.alumno.apellido}, {obj.alumno.nombre}"


class AsistenciaListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas"""
    alumno_completo = serializers.SerializerMethodField()
    codigo_codigo = serializers.CharField(source='codigo.codigo', read_only=True)
    turno_nombre = serializers.CharField(source='turno.get_nombre_display', read_only=True)
    
    class Meta:
        model = Asistencia
        fields = ['id', 'fecha', 'alumno_completo', 'codigo_codigo', 'turno_nombre', 'procesado']
    
    def get_alumno_completo(self, obj):
        return f"{obj.alumno.apellido}, {obj.alumno.nombre}"


class CierreDiarioSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario_cierre.get_full_name', read_only=True)
    
    class Meta:
        model = CierreDiario
        fields = ['id', 'fecha', 'fecha_cierre', 'usuario_cierre', 'usuario_nombre',
                  'total_asistencias_procesadas', 'total_alumnos_procesados',
                  'total_cursos_procesados', 'observaciones_cierre']
        read_only_fields = ['fecha_cierre']


class ResumenDiarioAlumnoSerializer(serializers.ModelSerializer):
    alumno_completo = serializers.SerializerMethodField()
    cierre_fecha = serializers.DateField(source='cierre_diario.fecha', read_only=True)
    
    class Meta:
        model = ResumenDiarioAlumno
        fields = ['id', 'cierre_diario', 'cierre_fecha', 'alumno', 'alumno_completo',
                  'fecha', 'codigo_mañana', 'codigo_tarde', 'codigo_educacion_fisica',
                  'tuvo_mañana', 'tuvo_tarde', 'tuvo_educacion_fisica',
                  'valor_falta_final', 'observaciones_resumen']
    
    def get_alumno_completo(self, obj):
        return f"{obj.alumno.apellido}, {obj.alumno.nombre}"
