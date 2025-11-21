from rest_framework import serializers
from .models import Alumno, Padre, Madre, Tutor


class PadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Padre
        fields = ['id', 'nombre_padre', 'apellido_padre', 'dni_padre', 
                  'direccion_padre', 'telefono_padre', 'nacionalidad_padre']


class MadreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Madre
        fields = ['id', 'nombre_madre', 'apellido_madre', 'dni_madre',
                  'direccion_madre', 'telefono_madre', 'nacionalidad_madre']


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ['id', 'nombre_tutor', 'apellido_tutor', 'dni_tutor',
                  'direccion_tutor', 'telefono_tutor', 'nacionalidad_tutor']


class AlumnoSerializer(serializers.ModelSerializer):
    padre_info = PadreSerializer(source='padre', read_only=True)
    madre_info = MadreSerializer(source='madre', read_only=True)
    tutor_info = TutorSerializer(source='tutor', read_only=True)
    curso_nombre = serializers.CharField(source='curso.curso', read_only=True)
    
    class Meta:
        model = Alumno
        fields = ['legajo', 'nombre', 'apellido', 'dni', 'direccion', 
                  'telefono', 'nacionalidad', 'padre', 'madre', 'tutor',
                  'padre_info', 'madre_info', 'tutor_info',
                  'activo', 'libre', 'condicional', 'curso', 'curso_nombre']
        read_only_fields = ['legajo']


class AlumnoListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listas"""
    curso_nombre = serializers.CharField(source='curso.curso', read_only=True)
    
    class Meta:
        model = Alumno
        fields = ['legajo', 'nombre', 'apellido', 'dni', 'curso', 'curso_nombre', 'activo']
