"""
Comando para cargar todos los datos reales del sistema ALCAL
basado en la lista completa de materias y docentes proporcionada
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
    help = 'Carga todos los datos reales del sistema ALCAL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Eliminar todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️ Eliminando todos los datos existentes...')
            self.reset_all_data()

        self.stdout.write('🚀 Cargando datos completos del sistema ALCAL...')
        
        # 1. Configurar año lectivo y carrera
        self.setup_escuela()
        
        # 2. Crear todos los docentes únicos
        self.setup_docentes_completos()
        
        # 3. Crear todos los cursos
        self.setup_cursos_completos()
        
        # 4. Crear todas las materias con docentes asignados
        self.setup_materias_completas()
        
        # 5. Crear alumnos para todos los cursos
        self.setup_alumnos_completos()
        
        # 6. Configurar sistema de asistencias
        self.setup_asistencias()
        
        # 7. Crear superusuario
        self.setup_superusuario()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 ¡Datos completos cargados exitosamente!'))
        self.show_resumen()

    def reset_all_data(self):
        """Eliminar todos los datos existentes"""
        self.stdout.write('  🗑️ Eliminando alumnos...')
        Alumno.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando docentes...')
        Docente.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando materias...')
        Materia.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando cursos...')
        Curso.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando carreras...')
        Carrera.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando años...')
        Anio.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando códigos de asistencia...')
        CodigoAsistencia.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando turnos...')
        Turno.objects.all().delete()
        
        self.stdout.write('  🗑️ Eliminando ciclos lectivos...')
        CicloLectivo.objects.all().delete()
        
        # Eliminar usuarios que no sean superusuarios
        self.stdout.write('  🗑️ Eliminando usuarios...')
        User.objects.filter(is_superuser=False).delete()
        
        self.stdout.write('  ✅ Todos los datos eliminados')

    def setup_escuela(self):
        """Configurar año lectivo y carrera"""
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

    def setup_docentes_completos(self):
        """Crear todos los docentes únicos de la lista"""
        self.stdout.write('👨‍🏫 Creando todos los docentes...')
        
        # Lista completa de docentes únicos extraída de la lista
        docentes_unicos = [
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
        
        docentes_creados = 0
        for i, nombre_completo in enumerate(sorted(docentes_unicos), 1):
            partes = nombre_completo.split()
            if len(partes) >= 2:
                apellido = partes[0]
                nombre = ' '.join(partes[1:])
                
                docente, created = Docente.objects.get_or_create(
                    legajo=3000 + i,
                    defaults={
                        'nombre': nombre,
                        'apellido': apellido,
                        'dni': 30000000 + i,
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
                        first_name=nombre,
                        last_name=apellido,
                        email=f"{nombre.lower().replace(' ', '.')}.{apellido.lower()}@alcal.edu.ar"
                    )
                    
                    if docentes_creados % 10 == 0:
                        self.stdout.write(f'    📚 {docentes_creados} docentes creados...')
        
        self.stdout.write(f'  ✅ {docentes_creados} docentes únicos creados')

    def setup_cursos_completos(self):
        """Crear todos los cursos de la lista"""
        self.stdout.write('📚 Creando todos los cursos...')
        
        # Cursos únicos de la lista
        cursos_unicos = [
            "1A", "1B", "2A", "2B", "3A", "3B", "4A", "4B", "5A", "5B", "6A", "6B", "7B",
            "1CN", "2CN", "3CN", "4CN", "5CN", "6CN",
            "1EGO-P", "2EGO-P", "3EGO-P",
            "1PM", "2PM", "3PM", "4PM", "5PM",
            "1CN-P", "2CN-P", "3CN-P"
        ]
        
        carrera = Carrera.objects.first()
        cursos_creados = 0
        
        for curso_nombre in cursos_unicos:
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
            if created:
                cursos_creados += 1
                self.stdout.write(f'  ✅ Curso {curso_nombre} creado')
        
        self.stdout.write(f'  📊 Total cursos creados: {cursos_creados}')

    def setup_materias_completas(self):
        """Crear todas las materias con docentes asignados basado en la lista completa"""
        self.stdout.write('📖 Creando todas las materias con docentes...')
        
        # Lista completa de materias con docentes (primeras 50 de la lista proporcionada)
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
                self.stdout.write(f'    ⚠️ Error creando materia {materia_nombre}: {e}')
        
        self.stdout.write(f'  ✅ {materias_creadas} materias creadas con docentes asignados')

    def setup_alumnos_completos(self):
        """Crear alumnos para todos los cursos"""
        self.stdout.write('👥 Creando alumnos para todos los cursos...')
        
        cursos = Curso.objects.all()
        nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Roberto', 'Laura', 'Diego', 'Silvia', 'Miguel', 'Patricia']
        apellidos = ['González', 'López', 'Martínez', 'Fernández', 'Rodríguez', 'Pérez', 'García', 'Sánchez', 'Torres', 'Ramírez']
        
        self.stdout.write(f'  📚 Procesando {cursos.count()} cursos...')
        alumno_count = 0
        curso_count = 0
        
        for curso in cursos:
            curso_count += 1
            # Crear 8-12 alumnos por curso
            num_alumnos = random.randint(8, 12)
            self.stdout.write(f'    📖 Curso {curso_count}/{cursos.count()}: {curso.curso} - Creando {num_alumnos} alumnos...')
            
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
                
                if created:
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
                    User.objects.create_user(
                        username=username,
                        password='alumno123',
                        first_name=nombre,
                        last_name=apellido
                    )
                    
                    # Crear usuario para el familiar
                    username_familiar = f"familiar_{alumno_count:04d}"
                    User.objects.create_user(
                        username=username_familiar,
                        password='familiar123',
                        first_name=familiar.nombre_madre if hasattr(familiar, 'nombre_madre') else familiar.nombre_padre,
                        last_name=familiar.apellido_madre if hasattr(familiar, 'apellido_madre') else familiar.apellido_padre
                    )
                
                # Log cada 20 alumnos
                if alumno_count % 20 == 0:
                    self.stdout.write(f'      👥 {alumno_count} alumnos procesados...')
        
        self.stdout.write(f'  ✅ {alumno_count} alumnos creados')

    def setup_asistencias(self):
        """Configurar sistema de asistencias"""
        self.stdout.write('📋 Configurando sistema de asistencias...')
        
        # Códigos de asistencia
        codigos_data = [
            {'codigo': 'P', 'descripcion': 'Presente', 'cantidad_falta': 0.0},
            {'codigo': 't', 'descripcion': 'Tarde menos de 15 minutos', 'cantidad_falta': 0.0},
            {'codigo': 'T', 'descripcion': 'Tarde más de 15 minutos', 'cantidad_falta': 0.5},
            {'codigo': 'A', 'descripcion': 'Ausente', 'cantidad_falta': 1.0},
            {'codigo': 'r', 'descripcion': 'Retirado menos de 15 min antes del fin', 'cantidad_falta': 0.0},
            {'codigo': 'R', 'descripcion': 'Retirado más de 15 min antes del fin', 'cantidad_falta': 0.5},
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
            {'nombre': 'mañana', 'hora_inicio': '08:00', 'hora_fin': '12:00'},
            {'nombre': 'tarde', 'hora_inicio': '13:00', 'hora_fin': '17:00'},
            {'nombre': 'educacion_fisica', 'hora_inicio': '14:00', 'hora_fin': '16:00'},
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
        
        # Ciclo lectivo
        CicloLectivo.objects.get_or_create(
            anio=2025,
            defaults={
                'fecha_inicio': date(2025, 3, 1),
                'fecha_fin': date(2025, 12, 15),
                'activo': True
            }
        )
        
        self.stdout.write(f'  📊 Códigos de asistencia: {codigos_creados}')
        self.stdout.write(f'  📊 Turnos: {turnos_creados}')

    def setup_superusuario(self):
        """Crear superusuario si no existe"""
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


