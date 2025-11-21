"""
Comando simple para configurar datos básicos del sistema ALCAL
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from escuela.models import Anio, Carrera, Curso, Materia
from alumnos.models import Alumno, Madre, Padre
from docentes.models import Docente
from asistencias.models import CodigoAsistencia, Turno
from calificaciones.models import CicloLectivo
import random
from datetime import date


class Command(BaseCommand):
    help = 'Configura datos básicos del sistema ALCAL'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando configuración del sistema ALCAL...')
        
        # 1. Configurar año lectivo y carrera
        self.stdout.write('📅 Configurando año lectivo...')
        anio, created = Anio.objects.get_or_create(ciclo_lectivo=2025)
        if created:
            self.stdout.write('  ✅ Año lectivo 2025 creado')
        else:
            self.stdout.write('  ℹ️ Año lectivo 2025 ya existe')
        
        self.stdout.write('🏫 Configurando carrera...')
        carrera, created = Carrera.objects.get_or_create(nombre='Bachillerato')
        if created:
            self.stdout.write('  ✅ Carrera Bachillerato creada')
        else:
            self.stdout.write('  ℹ️ Carrera Bachillerato ya existe')
        
        # 2. Crear cursos básicos
        self.stdout.write('📚 Creando cursos...')
        cursos_data = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B']
        cursos_creados = 0
        
        for curso_nombre in cursos_data:
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
            if created:
                cursos_creados += 1
                self.stdout.write(f'  ✅ Curso {curso_nombre} creado')
        
        self.stdout.write(f'📊 Total cursos creados: {cursos_creados}')
        
        # 3. Crear algunos docentes
        self.stdout.write('👨‍🏫 Creando docentes...')
        docentes_data = [
            {'nombre': 'María', 'apellido': 'González', 'legajo': 1001},
            {'nombre': 'Carlos', 'apellido': 'López', 'legajo': 1002},
            {'nombre': 'Ana', 'apellido': 'Martínez', 'legajo': 1003},
        ]
        
        docentes_creados = 0
        for docente_data in docentes_data:
            docente, created = Docente.objects.get_or_create(
                legajo=docente_data['legajo'],
                defaults={
                    'nombre': docente_data['nombre'],
                    'apellido': docente_data['apellido'],
                    'dni': random.randint(10000000, 99999999),
                    'telefono': f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                    'direccion': f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                    'nacionalidad': 'Argentina'
                }
            )
            if created:
                docentes_creados += 1
                self.stdout.write(f'  ✅ Docente {docente_data["nombre"]} {docente_data["apellido"]} creado')
        
        self.stdout.write(f'📊 Total docentes creados: {docentes_creados}')
        
        # 4. Crear algunas materias
        self.stdout.write('📖 Creando materias...')
        materias_data = [
            {'nombre': 'Matemática', 'horas': 4},
            {'nombre': 'Lengua y Literatura', 'horas': 4},
            {'nombre': 'Historia', 'horas': 3},
            {'nombre': 'Geografía', 'horas': 3},
            {'nombre': 'Biología', 'horas': 3},
        ]
        
        materias_creadas = 0
        cursos = Curso.objects.all()[:3]  # Solo primeros 3 cursos
        
        for curso in cursos:
            for materia_data in materias_data:
                materia, created = Materia.objects.get_or_create(
                    nombre=materia_data['nombre'],
                    curso=curso,
                    defaults={'horas': materia_data['horas']}
                )
                if created:
                    materias_creadas += 1
                    self.stdout.write(f'  ✅ Materia {materia_data["nombre"]} para {curso.curso} creada')
        
        self.stdout.write(f'📊 Total materias creadas: {materias_creadas}')
        
        # 5. Crear algunos alumnos
        self.stdout.write('👥 Creando alumnos...')
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Roberto', 'Laura']
        apellidos = ['González', 'López', 'Martínez', 'Fernández', 'Rodríguez', 'Pérez']
        
        alumnos_creados = 0
        cursos = Curso.objects.all()[:3]  # Solo primeros 3 cursos
        
        for curso in cursos:
            self.stdout.write(f'  📚 Procesando curso {curso.curso}...')
            for i in range(3):  # 3 alumnos por curso
                nombre = random.choice(nombres)
                apellido = random.choice(apellidos)
                dni = random.randint(10000000, 99999999)
                
                alumno, created = Alumno.objects.get_or_create(
                    dni=dni,
                    defaults={
                        'nombre': nombre,
                        'apellido': apellido,
                        'telefono': f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                        'direccion': f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                        'nacionalidad': 'Argentina',
                        'curso': curso
                    }
                )
                
                if created:
                    alumnos_creados += 1
                    self.stdout.write(f'    ✅ Alumno {nombre} {apellido} creado')
        
        self.stdout.write(f'📊 Total alumnos creados: {alumnos_creados}')
        
        # 6. Configurar sistema de asistencias
        self.stdout.write('📋 Configurando sistema de asistencias...')
        
        # Códigos de asistencia
        codigos_data = [
            {'codigo': 'P', 'descripcion': 'Presente', 'cantidad_falta': 0.0},
            {'codigo': 'A', 'descripcion': 'Ausente', 'cantidad_falta': 1.0},
            {'codigo': 'T', 'descripcion': 'Tarde', 'cantidad_falta': 0.5},
        ]
        
        codigos_creados = 0
        for codigo_data in codigos_data:
            codigo, created = CodigoAsistencia.objects.get_or_create(
                codigo=codigo_data['codigo'],
                defaults={
                    'descripcion': codigo_data['descripcion'],
                    'cantidad_falta': codigo_data['cantidad_falta']
                }
            )
            if created:
                codigos_creados += 1
                self.stdout.write(f'  ✅ Código {codigo_data["codigo"]} creado')
        
        # Turnos
        turnos_data = [
            {'nombre': 'Mañana', 'hora_inicio': '08:00', 'hora_fin': '12:00'},
            {'nombre': 'Tarde', 'hora_inicio': '13:00', 'hora_fin': '17:00'},
        ]
        
        turnos_creados = 0
        for turno_data in turnos_data:
            turno, created = Turno.objects.get_or_create(
                nombre=turno_data['nombre'],
                defaults={
                    'hora_inicio': turno_data['hora_inicio'],
                    'hora_fin': turno_data['hora_fin']
                }
            )
            if created:
                turnos_creados += 1
                self.stdout.write(f'  ✅ Turno {turno_data["nombre"]} creado')
        
        self.stdout.write(f'📊 Códigos de asistencia creados: {codigos_creados}')
        self.stdout.write(f'📊 Turnos creados: {turnos_creados}')
        
        # 7. Crear superusuario
        self.stdout.write('👤 Configurando superusuario...')
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@alcal.edu.ar',
                password='admin123',
                first_name='Administrador',
                last_name='ALCAL'
            )
            self.stdout.write('  ✅ Superusuario admin creado')
        else:
            self.stdout.write('  ℹ️ Superusuario admin ya existe')
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 ¡Configuración completada exitosamente!'))
        self.stdout.write('')
        self.stdout.write('📋 Resumen:')
        self.stdout.write(f'  • Cursos: {Curso.objects.count()}')
        self.stdout.write(f'  • Docentes: {Docente.objects.count()}')
        self.stdout.write(f'  • Materias: {Materia.objects.count()}')
        self.stdout.write(f'  • Alumnos: {Alumno.objects.count()}')
        self.stdout.write(f'  • Códigos de asistencia: {CodigoAsistencia.objects.count()}')
        self.stdout.write(f'  • Turnos: {Turno.objects.count()}')
        self.stdout.write('')
        self.stdout.write('🌐 Para acceder al sistema:')
        self.stdout.write('  • URL: http://127.0.0.1:8008/')
        self.stdout.write('  • Admin: http://127.0.0.1:8008/admin/')
        self.stdout.write('  • Usuario: admin')
        self.stdout.write('  • Contraseña: admin123')
