"""
Comando de gestión para configurar datos de prueba del sistema ALCAL
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from escuela.models import Anio, Carrera, Curso, Materia
from alumnos.models import Alumno, Madre, Padre, Tutor
from docentes.models import Docente
from asistencias.models import CodigoAsistencia, Turno
from calificaciones.models import CicloLectivo
import random
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Configura datos de prueba para el sistema ALCAL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Eliminar datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando datos existentes...')
            self.reset_data()

        self.stdout.write('Configurando datos de prueba...')
        
        with transaction.atomic():
            # 1. Configurar año lectivo y carrera
            self.setup_escuela()
            
            # 2. Configurar cursos
            self.setup_cursos()
            
            # 3. Configurar materias
            self.setup_materias()
            
            # 4. Crear docentes
            self.setup_docentes()
            
            # 5. Crear alumnos
            self.setup_alumnos()
            
            # 6. Configurar sistema de asistencias
            self.setup_asistencias()
            
            # 7. Crear superusuario si no existe
            self.setup_superusuario()

        self.stdout.write(
            self.style.SUCCESS('✅ Datos de prueba configurados exitosamente!')
        )

    def reset_data(self):
        """Eliminar datos existentes"""
        Alumno.objects.all().delete()
        Docente.objects.all().delete()
        Curso.objects.all().delete()
        Materia.objects.all().delete()
        Carrera.objects.all().delete()
        Anio.objects.all().delete()
        CodigoAsistencia.objects.all().delete()
        Turno.objects.all().delete()
        CicloLectivo.objects.all().delete()
        
        # Eliminar usuarios que no sean superusuarios
        User.objects.filter(is_superuser=False).delete()

    def setup_escuela(self):
        """Configurar año lectivo y carrera"""
        # Crear año lectivo 2025
        anio, created = Anio.objects.get_or_create(
            ciclo_lectivo=2025
        )
        
        # Crear carrera
        carrera, created = Carrera.objects.get_or_create(
            nombre='Bachillerato'
        )
        
        self.stdout.write(f'✅ Año lectivo y carrera configurados')

    def setup_cursos(self):
        """Configurar cursos"""
        cursos_data = [
            '1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B', '6A', '6B', '7B'
        ]
        
        carrera = Carrera.objects.first()
        for curso_nombre in cursos_data:
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
        
        self.stdout.write(f'✅ {len(cursos_data)} cursos creados')

    def setup_materias(self):
        """Configurar materias"""
        materias_data = [
            {'nombre': 'Matemática', 'horas': 4},
            {'nombre': 'Lengua y Literatura', 'horas': 4},
            {'nombre': 'Historia', 'horas': 3},
            {'nombre': 'Geografía', 'horas': 3},
            {'nombre': 'Biología', 'horas': 3},
            {'nombre': 'Física', 'horas': 3},
            {'nombre': 'Química', 'horas': 3},
            {'nombre': 'Educación Física', 'horas': 2},
            {'nombre': 'Inglés', 'horas': 3},
            {'nombre': 'Educación Cívica', 'horas': 2},
        ]
        
        cursos = Curso.objects.all()
        for curso in cursos:
            for materia_data in materias_data:
                materia, created = Materia.objects.get_or_create(
                    nombre=materia_data['nombre'],
                    curso=curso,
                    defaults={'horas': materia_data['horas']}
                )
        
        self.stdout.write(f'✅ {len(materias_data)} materias por curso creadas')

    def setup_docentes(self):
        """Crear docentes de prueba"""
        docentes_data = [
            {'nombre': 'María', 'apellido': 'González', 'dni': 12345678, 'legajo': 1001},
            {'nombre': 'Carlos', 'apellido': 'López', 'dni': 23456789, 'legajo': 1002},
            {'nombre': 'Ana', 'apellido': 'Martínez', 'dni': 34567890, 'legajo': 1003},
            {'nombre': 'Roberto', 'apellido': 'Fernández', 'dni': 45678901, 'legajo': 1004},
            {'nombre': 'Laura', 'apellido': 'Rodríguez', 'dni': 56789012, 'legajo': 1005},
            {'nombre': 'Diego', 'apellido': 'Pérez', 'dni': 67890123, 'legajo': 1006},
            {'nombre': 'Silvia', 'apellido': 'García', 'dni': 78901234, 'legajo': 1007},
            {'nombre': 'Miguel', 'apellido': 'Sánchez', 'dni': 89012345, 'legajo': 1008},
        ]
        
        for docente_data in docentes_data:
            docente, created = Docente.objects.get_or_create(
                dni=docente_data['dni'],
                defaults={
                    'legajo': docente_data['legajo'],
                    'nombre': docente_data['nombre'],
                    'apellido': docente_data['apellido'],
                    'telefono': f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                    'direccion': f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                    'nacionalidad': 'Argentina'
                }
            )
            
            # Crear usuario para el docente
            username = f"docente_{docente_data['dni']}"
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    password='docente123',
                    first_name=docente_data['nombre'],
                    last_name=docente_data['apellido'],
                    email=f"{docente_data['nombre'].lower()}.{docente_data['apellido'].lower()}@alcal.edu.ar"
                )
        
        self.stdout.write(f'✅ {len(docentes_data)} docentes creados')

    def setup_alumnos(self):
        """Crear alumnos de prueba"""
        cursos = Curso.objects.all()
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Roberto', 'Laura', 'Diego', 'Silvia', 'Miguel', 'Patricia']
        apellidos = ['González', 'López', 'Martínez', 'Fernández', 'Rodríguez', 'Pérez', 'García', 'Sánchez', 'Torres', 'Ramírez']
        
        alumno_count = 0
        for curso in cursos:
            # Crear 10 alumnos por curso
            for i in range(10):
                alumno_count += 1
                nombre = random.choice(nombres)
                apellido = random.choice(apellidos)
                dni = random.randint(10000000, 99999999)
                
                # Crear alumno
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
                
                # Crear familiar (madre o padre)
                if random.choice([True, False]):
                    familiar = Madre.objects.create(
                        nombre_madre=random.choice(['María', 'Ana', 'Laura', 'Silvia', 'Patricia']),
                        apellido_madre=apellido,
                        dni_madre=random.randint(10000000, 99999999),
                        telefono_madre=f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                        nacionalidad_madre='Argentina',
                        direccion_madre=f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}'
                    )
                    alumno.madre = familiar
                    alumno.save()
                else:
                    familiar = Padre.objects.create(
                        nombre_padre=random.choice(['Juan', 'Carlos', 'Roberto', 'Diego', 'Miguel']),
                        apellido_padre=apellido,
                        dni_padre=random.randint(10000000, 99999999),
                        telefono_padre=f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                        nacionalidad_padre='Argentina',
                        direccion_padre=f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}'
                    )
                    alumno.padre = familiar
                    alumno.save()
                
                # Crear usuario para el alumno
                username = f"alumno_{alumno_count:04d}"
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(
                        username=username,
                        password='alumno123',
                        first_name=nombre,
                        last_name=apellido
                    )
                
                # Crear usuario para el familiar
                username_familiar = f"familiar_{alumno_count:04d}"
                if not User.objects.filter(username=username_familiar).exists():
                    User.objects.create_user(
                        username=username_familiar,
                        password='familiar123',
                        first_name=familiar.nombre_madre if hasattr(familiar, 'nombre_madre') else familiar.nombre_padre,
                        last_name=familiar.apellido_madre if hasattr(familiar, 'apellido_madre') else familiar.apellido_padre
                    )
        
        self.stdout.write(f'✅ {alumno_count} alumnos creados')

    def setup_asistencias(self):
        """Configurar sistema de asistencias"""
        # Códigos de asistencia
        codigos_data = [
            {'codigo': 'P', 'descripcion': 'Presente', 'valor_falta': 0.0},
            {'codigo': 't', 'descripcion': 'Tarde menos de 15 minutos', 'valor_falta': 0.0},
            {'codigo': 'T', 'descripcion': 'Tarde más de 15 minutos', 'valor_falta': 0.5},
            {'codigo': 'A', 'descripcion': 'Ausente', 'valor_falta': 1.0},
            {'codigo': 'r', 'descripcion': 'Retirado menos de 15 min antes del fin', 'valor_falta': 0.0},
            {'codigo': 'R', 'descripcion': 'Retirado más de 15 min antes del fin', 'valor_falta': 0.5},
        ]
        
        for codigo_data in codigos_data:
            CodigoAsistencia.objects.get_or_create(
                codigo=codigo_data['codigo'],
                defaults={
                    'descripcion': codigo_data['descripcion'],
                    'valor_falta': codigo_data['valor_falta']
                }
            )
        
        # Turnos
        turnos_data = [
            {'nombre': 'Mañana', 'hora_inicio': '08:00', 'hora_fin': '12:00'},
            {'nombre': 'Tarde', 'hora_inicio': '13:00', 'hora_fin': '17:00'},
            {'nombre': 'Educación Física', 'hora_inicio': '14:00', 'hora_fin': '16:00'},
        ]
        
        for turno_data in turnos_data:
            Turno.objects.get_or_create(
                nombre=turno_data['nombre'],
                defaults={
                    'hora_inicio': turno_data['hora_inicio'],
                    'hora_fin': turno_data['hora_fin']
                }
            )
        
        # Ciclo lectivo
        CicloLectivo.objects.get_or_create(
            anio=2025,
            defaults={
                'fecha_inicio': date(2025, 3, 1),
                'fecha_fin': date(2025, 12, 15),
                'activo': True
            }
        )
        
        self.stdout.write('✅ Sistema de asistencias configurado')

    def setup_superusuario(self):
        """Crear superusuario si no existe"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@alcal.edu.ar',
                password='admin123',
                first_name='Administrador',
                last_name='ALCAL'
            )
            self.stdout.write('✅ Superusuario admin creado')
        else:
            self.stdout.write('ℹ️ Superusuario admin ya existe')
