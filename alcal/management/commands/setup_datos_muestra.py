"""
Comando para cargar una muestra de datos reales del sistema ALCAL
"""
import csv
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from escuela.models import Anio, Carrera, Curso, Materia
from alumnos.models import Alumno, Madre, Padre
from docentes.models import Docente
from asistencias.models import CodigoAsistencia, Turno
from calificaciones.models import CicloLectivo
import random
from datetime import datetime, date


class Command(BaseCommand):
    help = 'Carga una muestra de datos reales del sistema ALCAL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Eliminar todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️ Eliminando datos existentes...')
            self.reset_data()

        self.stdout.write('🚀 Cargando muestra de datos reales...')
        
        # 1. Configurar año lectivo y carrera
        self.setup_escuela()
        
        # 2. Crear algunos docentes
        self.setup_docentes_muestra()
        
        # 3. Crear cursos principales
        self.setup_cursos_muestra()
        
        # 4. Crear algunas materias
        self.setup_materias_muestra()
        
        # 5. Crear algunos alumnos
        self.setup_alumnos_muestra()
        
        # 6. Configurar sistema de asistencias
        self.setup_asistencias()
        
        # 7. Crear superusuario
        self.setup_superusuario()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 ¡Muestra de datos cargada exitosamente!'))
        self.show_resumen()

    def reset_data(self):
        """Eliminar datos existentes"""
        Alumno.objects.all().delete()
        Docente.objects.all().delete()
        Materia.objects.all().delete()
        Curso.objects.all().delete()
        Carrera.objects.all().delete()
        Anio.objects.all().delete()
        CodigoAsistencia.objects.all().delete()
        Turno.objects.all().delete()
        CicloLectivo.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write('  ✅ Datos eliminados')

    def setup_escuela(self):
        """Configurar año lectivo y carrera"""
        self.stdout.write('📅 Configurando año lectivo...')
        Anio.objects.get_or_create(ciclo_lectivo=2025)
        Carrera.objects.get_or_create(nombre='Bachillerato')
        self.stdout.write('  ✅ Año lectivo y carrera configurados')

    def setup_docentes_muestra(self):
        """Crear algunos docentes de muestra"""
        self.stdout.write('👨‍🏫 Creando docentes de muestra...')
        
        # Docentes de muestra basados en los CSV
        docentes_muestra = [
            {"nombre": "Patricia", "apellido": "Herrera", "legajo": 1001, "dni": 12345678},
            {"nombre": "Layla", "apellido": "Barakian", "legajo": 1002, "dni": 12345679},
            {"nombre": "Sabrina", "apellido": "Sequeira", "legajo": 1003, "dni": 12345680},
            {"nombre": "Camila", "apellido": "Sierra Bueno", "legajo": 1004, "dni": 12345681},
            {"nombre": "Sofía", "apellido": "Scalercio", "legajo": 1005, "dni": 12345682},
            {"nombre": "Solange", "apellido": "Trombiero", "legajo": 1006, "dni": 12345683},
            {"nombre": "Noelia", "apellido": "Cajaraville", "legajo": 1007, "dni": 12345684},
            {"nombre": "Paula", "apellido": "Laborde", "legajo": 1008, "dni": 12345685},
            {"nombre": "Nicolás", "apellido": "Cáceres", "legajo": 1009, "dni": 12345686},
            {"nombre": "Graciela", "apellido": "Taliercio", "legajo": 1010, "dni": 12345687},
        ]
        
        self.stdout.write(f'  📋 Procesando {len(docentes_muestra)} docentes...')
        docentes_creados = 0
        
        for i, docente_data in enumerate(docentes_muestra, 1):
            self.stdout.write(f'    👤 Procesando docente {i}/{len(docentes_muestra)}: {docente_data["nombre"]} {docente_data["apellido"]}...')
            
            docente, created = Docente.objects.get_or_create(
                legajo=docente_data['legajo'],
                defaults={
                    'nombre': docente_data['nombre'],
                    'apellido': docente_data['apellido'],
                    'dni': docente_data['dni'],
                    'telefono': f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                    'direccion': f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                    'nacionalidad': 'Argentina'
                }
            )
            
            if created:
                docentes_creados += 1
                # Crear usuario para el docente
                username = f"docente_{docente.legajo}"
                User.objects.create_user(
                    username=username,
                    password='docente123',
                    first_name=docente_data['nombre'],
                    last_name=docente_data['apellido'],
                    email=f"{docente_data['nombre'].lower()}.{docente_data['apellido'].lower().replace(' ', '.')}@alcal.edu.ar"
                )
                self.stdout.write(f'      ✅ Docente {docente_data["nombre"]} {docente_data["apellido"]} creado')
            else:
                self.stdout.write(f'      ℹ️ Docente {docente_data["nombre"]} {docente_data["apellido"]} ya existe')
        
        self.stdout.write(f'  📊 {docentes_creados} docentes creados')

    def setup_cursos_muestra(self):
        """Crear cursos principales"""
        self.stdout.write('📚 Creando cursos principales...')
        
        cursos_principales = ["1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B", "5A", "5B", "6A", "6B"]
        carrera = Carrera.objects.first()
        cursos_creados = 0
        
        self.stdout.write(f'  📋 Procesando {len(cursos_principales)} cursos...')
        
        for i, curso_nombre in enumerate(cursos_principales, 1):
            self.stdout.write(f'    📖 Procesando curso {i}/{len(cursos_principales)}: {curso_nombre}...')
            
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
            if created:
                cursos_creados += 1
                self.stdout.write(f'      ✅ Curso {curso_nombre} creado')
            else:
                self.stdout.write(f'      ℹ️ Curso {curso_nombre} ya existe')
        
        self.stdout.write(f'  📊 {cursos_creados} cursos creados')

    def setup_materias_muestra(self):
        """Crear materias de muestra"""
        self.stdout.write('📖 Creando materias de muestra...')
        
        # Materias por curso
        materias_por_curso = {
            "1A": ["Ciencias Naturales", "Ciencias Sociales", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "1B": ["Ciencias Naturales", "Ciencias Sociales", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "2A": ["Biología", "Historia", "Geografía", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "2B": ["Biología", "Historia", "Geografía", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "3A": ["Biología", "Historia", "Geografía", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "3B": ["Biología", "Historia", "Geografía", "Matemática", "Prácticas del Lenguaje", "Educación Física"],
            "4A": ["Biología", "Historia", "Geografía", "Matemática C.S.", "Literatura", "Educación Física"],
            "4B": ["Biología", "Historia", "Geografía", "Matemática C.S.", "Literatura", "Educación Física"],
            "5A": ["Matemática C.S.", "Literatura", "Educación Física", "Inglés", "Política y Ciudadanía"],
            "5B": ["Matemática C.S.", "Literatura", "Educación Física", "Inglés", "Política y Ciudadanía"],
            "6A": ["Matemática C.S.", "Literatura", "Educación Física", "Inglés", "Política y Ciudadanía"],
            "6B": ["Matemática C.S.", "Literatura", "Educación Física", "Inglés", "Política y Ciudadanía"],
        }
        
        materias_creadas = 0
        docentes = list(Docente.objects.all())
        total_cursos = len(materias_por_curso)
        
        self.stdout.write(f'  📋 Procesando {total_cursos} cursos con materias...')
        
        for i, (curso_nombre, materias) in enumerate(materias_por_curso.items(), 1):
            self.stdout.write(f'    📚 Procesando curso {i}/{total_cursos}: {curso_nombre} ({len(materias)} materias)...')
            
            try:
                curso = Curso.objects.get(curso=curso_nombre)
                
                for j, materia_nombre in enumerate(materias, 1):
                    self.stdout.write(f'      📖 Procesando materia {j}/{len(materias)}: {materia_nombre}...')
                    
                    materia, created = Materia.objects.get_or_create(
                        nombre=materia_nombre,
                        curso=curso,
                        defaults={'horas': random.randint(2, 6)}
                    )
                    
                    if created:
                        # Asignar un docente aleatorio a la materia
                        if docentes:
                            docente = random.choice(docentes)
                            docente.materia.add(materia)
                            materias_creadas += 1
                            self.stdout.write(f'        ✅ Materia {materia_nombre} creada y asignada a {docente.nombre} {docente.apellido}')
                        else:
                            self.stdout.write(f'        ⚠️ Materia {materia_nombre} creada pero sin docente asignado')
                    else:
                        self.stdout.write(f'        ℹ️ Materia {materia_nombre} ya existe')
                            
            except Curso.DoesNotExist:
                self.stdout.write(f'      ❌ Curso {curso_nombre} no encontrado')
                continue
        
        self.stdout.write(f'  📊 {materias_creadas} materias creadas')

    def setup_alumnos_muestra(self):
        """Crear alumnos de muestra"""
        self.stdout.write('👥 Creando alumnos de muestra...')
        
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Roberto', 'Laura', 'Diego', 'Silvia', 'Miguel', 'Patricia', 'Luis', 'Carmen', 'Pedro', 'Elena', 'Antonio', 'Isabel']
        apellidos = ['González', 'López', 'Martínez', 'Fernández', 'Rodríguez', 'Pérez', 'García', 'Sánchez', 'Torres', 'Ramírez', 'Flores', 'Vargas', 'Morales', 'Jiménez', 'Ruiz', 'Díaz']
        
        cursos = Curso.objects.all()
        alumnos_creados = 0
        total_cursos = cursos.count()
        
        self.stdout.write(f'  📋 Procesando {total_cursos} cursos...')
        
        for i, curso in enumerate(cursos, 1):
            # Crear 8-12 alumnos por curso
            num_alumnos = random.randint(8, 12)
            self.stdout.write(f'    📚 Procesando curso {i}/{total_cursos}: {curso.curso} - Creando {num_alumnos} alumnos...')
            
            for j in range(num_alumnos):
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
                
                if created:
                    alumnos_creados += 1
                    
                    # Crear familiar
                    if random.choice([True, False]):
                        familiar = Madre.objects.create(
                            nombre_madre=random.choice(['María', 'Ana', 'Laura', 'Silvia', 'Patricia', 'Carmen', 'Elena', 'Isabel']),
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
                            nombre_padre=random.choice(['Juan', 'Carlos', 'Roberto', 'Diego', 'Miguel', 'Luis', 'Pedro', 'Antonio']),
                            apellido_padre=apellido,
                            dni_padre=random.randint(10000000, 99999999),
                            telefono_padre=f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                            nacionalidad_padre='Argentina',
                            direccion_padre=f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}'
                        )
                        alumno.padre = familiar
                        alumno.save()
                    
                    # Crear usuario para el alumno
                    username = f"alumno_{alumno.dni}"
                    User.objects.create_user(
                        username=username,
                        password='alumno123',
                        first_name=nombre,
                        last_name=apellido
                    )
                    
                    # Log cada 5 alumnos
                    if j % 5 == 0:
                        self.stdout.write(f'      👥 {j+1}/{num_alumnos} alumnos procesados...')
            
            self.stdout.write(f'    ✅ Curso {curso.curso} completado - {num_alumnos} alumnos creados')
        
        self.stdout.write(f'  📊 {alumnos_creados} alumnos creados en total')

    def setup_asistencias(self):
        """Configurar sistema de asistencias"""
        self.stdout.write('📋 Configurando sistema de asistencias...')
        
        # Códigos de asistencia
        codigos_data = [
            {'codigo': 'P', 'descripcion': 'Presente', 'cantidad_falta': 0.0},
            {'codigo': 'A', 'descripcion': 'Ausente', 'cantidad_falta': 1.0},
            {'codigo': 'T', 'descripcion': 'Tarde', 'cantidad_falta': 0.5},
        ]
        
        for codigo_data in codigos_data:
            CodigoAsistencia.objects.get_or_create(
                codigo=codigo_data['codigo'],
                defaults={
                    'descripcion': codigo_data['descripcion'],
                    'cantidad_falta': codigo_data['cantidad_falta']
                }
            )
        
        # Turnos
        turnos_data = [
            {'nombre': 'mañana', 'hora_inicio': '08:00', 'hora_fin': '12:00'},
            {'nombre': 'tarde', 'hora_inicio': '13:00', 'hora_fin': '17:00'},
        ]
        
        for turno_data in turnos_data:
            Turno.objects.get_or_create(
                nombre=turno_data['nombre'],
                defaults={
                    'hora_inicio': turno_data['hora_inicio'],
                    'hora_fin': turno_data['hora_fin']
                }
            )
        
        self.stdout.write('  ✅ Sistema de asistencias configurado')

    def setup_superusuario(self):
        """Crear superusuario"""
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

    def show_resumen(self):
        """Mostrar resumen final"""
        self.stdout.write('')
        self.stdout.write('📋 Resumen Final:')
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
