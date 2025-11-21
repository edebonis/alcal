from rest_framework import serializers
from .models import Carrera, Anio, Curso, Materia


class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ['id', 'nombre']


class AnioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anio
        fields = ['id', 'ciclo_lectivo']


class CursoSerializer(serializers.ModelSerializer):
    carrera_nombre = serializers.CharField(source='carrera.nombre', read_only=True)
    
    class Meta:
        model = Curso
        fields = ['id', 'curso', 'carrera', 'carrera_nombre']


class MateriaSerializer(serializers.ModelSerializer):
    curso_nombre = serializers.CharField(source='curso.curso', read_only=True)
    
    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'curso', 'curso_nombre', 'horas']
