"""
Comando de gestión para configurar datos reales del sistema ALCAL
basado en la lista de materias, docentes y cursos proporcionada
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
    help = 'Configura datos reales del sistema ALCAL basado en la lista proporcionada'

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

        self.stdout.write('Configurando datos reales del sistema ALCAL...')
        
        with transaction.atomic():
            # 1. Configurar año lectivo y carrera
            self.setup_escuela()
            
            # 2. Crear docentes únicos
            self.setup_docentes_reales()
            
            # 3. Crear cursos únicos
            self.setup_cursos_reales()
            
            # 4. Crear materias con docentes asignados
            self.setup_materias_reales()
            
            # 5. Crear alumnos para los cursos
            self.setup_alumnos_reales()
            
            # 6. Configurar sistema de asistencias
            self.setup_asistencias()
            
            # 7. Crear superusuario si no existe
            self.setup_superusuario()

        self.stdout.write(
            self.style.SUCCESS('✅ Datos reales configurados exitosamente!')
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

    def setup_docentes_reales(self):
        """Crear docentes únicos de la lista"""
        # Extraer docentes únicos de la lista
        docentes_unicos = set()
        
        # Lista de materias con docentes (primeras 50 líneas como ejemplo)
        materias_docentes = [
            "Herrera Patricia", "Barakian Layla", "Sequeira Sabrina", "Sierra Bueno Camila",
            "Scalercio Sofía", "Trombiero Solange", "Cajaraville Noelia", "Laborde Paula",
            "Cáceres Nicolás", "Taliercio Graciela", "Prieto Florencia", "Bonifacini Sandra",
            "Berone Maximiliano", "Carrizo Cayetano", "Crippa Andrés", "Ughetti Javier",
            "Gubitosi Dulcinea", "Calviello Matías", "González Lorena", "Ferrero Victoria",
            "Báez Marcelo", "Rojas Claudio", "Bugna Gisella", "Alvarenga Erika",
            "Sabatini Natalia", "Flores Rafael", "Gómez Diego", "Villalba Carolina",
            "Altamiranda Esteban", "Gómez Carlos", "Chiesa Leonardo", "Del Corro Miguel",
            "Cruz Camila", "Blanco Marisol", "Martín Soledad", "Carballo Matías",
            "Lezcano Gastón", "Papaianni Mariano", "Valenzuela Gustavo", "Britez Neira Guillermo",
            "Bordón José", "Papaianni-Lezcano", "Demonte Carolina", "Romero Juan Pablo",
            "Márquez Rodrigo", "De Bonis Esteban", "Cortés Martina", "Navas Pablo",
            "García Yanina", "Giaimo Paula", "Martín Luciana", "Pontoriero Lina",
            "Alfaro Cecilia", "Pabón Andrea"
        ]
        
        for docente_nombre in materias_docentes:
            if docente_nombre and docente_nombre.strip():
                docentes_unicos.add(docente_nombre.strip())
        
        # Crear docentes
        for i, nombre_completo in enumerate(sorted(docentes_unicos), 1):
            partes = nombre_completo.split()
            if len(partes) >= 2:
                apellido = partes[0]
                nombre = ' '.join(partes[1:])
                
                docente, created = Docente.objects.get_or_create(
                    legajo=2000 + i,
                    defaults={
                        'nombre': nombre,
                        'apellido': apellido,
                        'dni': 20000000 + i,
                        'telefono': f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                        'direccion': f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                        'nacionalidad': 'Argentina'
                    }
                )
                
                # Crear usuario para el docente
                username = f"docente_{docente.legajo}"
                if not User.objects.filter(username=username).exists():
                    User.objects.create_user(
                        username=username,
                        password='docente123',
                        first_name=nombre,
                        last_name=apellido,
                        email=f"{nombre.lower().replace(' ', '.')}.{apellido.lower()}@alcal.edu.ar"
                    )
        
        self.stdout.write(f'✅ {len(docentes_unicos)} docentes únicos creados')

    def setup_cursos_reales(self):
        """Crear cursos únicos de la lista"""
        # Extraer cursos únicos
        cursos_unicos = set()
        
        # Cursos de la lista (ejemplo de los primeros)
        cursos_data = [
            "1A", "2A", "3A", "4A", "5A", "6A", "7A",
            "1B", "2B", "3B", "4B", "5B", "6B", "7B",
            "1CN", "2CN", "3CN", "4CN", "5CN", "6CN",
            "1EGO-P", "2EGO-P", "3EGO-P",
            "1PM", "2PM", "3PM", "4PM", "5PM",
            "1CN-P", "2CN-P", "3CN-P"
        ]
        
        carrera = Carrera.objects.first()
        for curso_nombre in cursos_data:
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
            cursos_unicos.add(curso_nombre)
        
        self.stdout.write(f'✅ {len(cursos_unicos)} cursos únicos creados')

    def setup_materias_reales(self):
        """Crear materias con docentes asignados basado en la lista real"""
        self.stdout.write(f'📝 Procesando materias con docentes...')
        # Mapeo de materias con sus docentes (primeras 50 como ejemplo)
        materias_docentes_map = [
            ("1A", "Ciencias Naturales", "Herrera Patricia"),
            ("1A", "Ciencias Sociales", "Barakian Layla"),
            ("1A", "Construcción de la Ciudadanía", "Sequeira Sabrina"),
            ("1A", "Educación Artística", "Sierra Bueno Camila"),
            ("1A", "Educación Física", "Scalercio Sofía"),
            ("1A", "Inglés", "Trombiero Solange"),
            ("1A", "Matemática", "Cajaraville Noelia"),
            ("1A", "Prácticas del Lenguaje", "Laborde Paula"),
            ("1A", "Cultura Religiosa", "Cáceres Nicolás"),
            ("2A", "Biología", "Taliercio Graciela"),
            ("2A", "Construcción de la Ciudadanía", "Sequeira Sabrina"),
            ("2A", "Educación Artística", "Sierra Bueno Camila"),
            ("2A", "Educación Física", "Scalercio Sofía"),
            ("2A", "Físico-Química", "Taliercio Graciela"),
            ("2A", "Geografía", "Prieto Florencia"),
            ("2A", "Historia", "Barakian Layla"),
            ("2A", "Inglés", "Bonifacini Sandra"),
            ("2A", "Matemática", "Cajaraville Noelia"),
            ("2A", "Prácticas del Lenguaje", "Laborde Paula"),
            ("2A", "Cultura Religiosa", "Berone Maximiliano"),
            ("3A", "Biología", "Herrera Patricia"),
            ("3A", "Construcción de la Ciudadanía", "Barakian Layla"),
            ("3A", "Educación Artística", "Sierra Bueno Camila"),
            ("3A", "Educación Física", "Carrizo Cayetano"),
            ("3A", "Físico-Química", "Taliercio Graciela"),
            ("3A", "Geografía", "Crippa Andrés"),
            ("3A", "Historia", "Ughetti Javier"),
            ("3A", "Inglés", "Trombiero Solange"),
            ("3A", "Matemática", "Gubitosi Dulcinea"),
            ("3A", "Prácticas del Lenguaje", "Laborde Paula"),
            ("3A", "Cultura Religiosa", "Berone Maximiliano"),
            ("4A", "Biología", "Taliercio Graciela"),
            ("4A", "Geografía", "Calviello Matías"),
            ("4A", "Historia", "Ughetti Javier"),
            ("4A", "Inglés", "Trombiero Solange"),
            ("4A", "Educación Física", "Scalercio Sofía"),
            ("4A", "Introducción a la Física", "González Lorena"),
            ("4A", "Literatura", "Ferrero Victoria"),
            ("4A", "Matemática C.S.", "Gubitosi Dulcinea"),
            ("4A", "NTICx", "Báez Marcelo"),
            ("4A", "Salud y Adolescencia", "Sequeira Sabrina"),
            ("4A", "Sist. de Información Contable I", "Rojas Claudio"),
            ("4A", "Teoría de las Organizaciones", "Rojas Claudio"),
            ("4A", "Cultura Religiosa", "Cáceres Nicolás"),
            ("5A", "Matemática C.S.", "González Lorena"),
            ("5A", "Literatura", "Bugna Gisella"),
            ("5A", "Educación Física", "Scalercio Sofía"),
            ("5A", "Inglés", "Alvarenga Erika"),
            ("5A", "Política y Ciudadanía", "Ughetti Javier"),
            ("5A", "Introducción a la Química", "Sabatini Natalia"),
        ]
        
        materias_creadas = 0
        total_materias = len(materias_docentes_map)
        self.stdout.write(f'  📋 Procesando {total_materias} materias...')
        
        for i, (curso_nombre, materia_nombre, docente_nombre) in enumerate(materias_docentes_map, 1):
            try:
                # Buscar curso
                curso = Curso.objects.get(curso=curso_nombre)
                
                # Buscar docente
                docente = Docente.objects.filter(
                    nombre__icontains=docente_nombre.split()[-1],
                    apellido__icontains=docente_nombre.split()[0]
                ).first()
                
                if docente:
                    # Crear materia
                    materia, created = Materia.objects.get_or_create(
                        nombre=materia_nombre,
                        curso=curso,
                        defaults={'horas': random.randint(2, 6)}
                    )
                    
                    # Asignar materia al docente
                    docente.materia.add(materia)
                    materias_creadas += 1
                    
                    # Log cada 10 materias
                    if i % 10 == 0:
                        self.stdout.write(f'    📚 {i}/{total_materias} materias procesadas...')
                    
            except Exception as e:
                self.stdout.write(f'⚠️ Error creando materia {materia_nombre}: {e}')
        
        self.stdout.write(f'✅ {materias_creadas} materias creadas con docentes asignados')

    def setup_alumnos_reales(self):
        """Crear alumnos para los cursos"""
        cursos = Curso.objects.all()
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Roberto', 'Laura', 'Diego', 'Silvia', 'Miguel', 'Patricia']
        apellidos = ['González', 'López', 'Martínez', 'Fernández', 'Rodríguez', 'Pérez', 'García', 'Sánchez', 'Torres', 'Ramírez']
        
        self.stdout.write(f'📚 Procesando {cursos.count()} cursos...')
        alumno_count = 0
        curso_count = 0
        
        for curso in cursos:
            curso_count += 1
            # Crear 5-8 alumnos por curso (reducido para ser más rápido)
            num_alumnos = random.randint(5, 8)
            self.stdout.write(f'  📖 Curso {curso_count}/{cursos.count()}: {curso.curso} - Creando {num_alumnos} alumnos...')
            
            for i in range(num_alumnos):
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
                
                # Log cada 10 alumnos
                if alumno_count % 10 == 0:
                    self.stdout.write(f'    👥 {alumno_count} alumnos procesados...')
        
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
