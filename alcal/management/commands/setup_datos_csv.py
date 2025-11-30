"""
Comando para cargar datos reales desde archivos CSV
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
    help = 'Carga datos reales desde archivos CSV'

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

        self.stdout.write('🚀 Cargando datos reales desde archivos CSV...')
        
        # 1. Configurar año lectivo y carrera
        self.setup_escuela()
        
        # 2. Crear docentes desde CSV
        self.setup_docentes_csv()
        
        # 3. Crear cursos únicos
        self.setup_cursos_csv()
        
        # 4. Crear materias con docentes desde CSV
        self.setup_materias_csv()
        
        # 5. Crear alumnos desde CSV
        self.setup_alumnos_csv()
        
        # 6. Configurar sistema de asistencias
        self.setup_asistencias()
        
        # 7. Crear superusuario
        self.setup_superusuario()

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('🎉 ¡Datos reales cargados exitosamente!'))
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

    def setup_docentes_csv(self):
        """Crear docentes desde archivo CSV"""
        self.stdout.write('👨‍🏫 Cargando docentes desde CSV...')
        
        csv_file = 'Legajo Docente - Legajo.csv'
        if not os.path.exists(csv_file):
            self.stdout.write(f'  ❌ Archivo {csv_file} no encontrado')
            return
        
        docentes_creados = 0
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ACTIVX'] == 'SI':  # Solo docentes activos
                    try:
                        # Extraer nombre y apellido
                        nombre_completo = row['NOMBRES'].strip()
                        apellido = row['APELLIDOS'].strip()
                        
                        # Crear docente
                        docente, created = Docente.objects.get_or_create(
                            legajo=int(row['Nº de Registro'].replace('.', '')),
                            defaults={
                                'nombre': nombre_completo,
                                'apellido': apellido,
                                'dni': int(row['DOCUMENTO'].replace('.', '')),
                                'telefono': row['TELÉFONOS'] or f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                                'direccion': row['DOMICILIO'] or f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                                'nacionalidad': row['NACIONALIDAD'] or 'Argentina'
                            }
                        )
                        
                        if created:
                            docentes_creados += 1
                            # Crear usuario para el docente
                            username = f"docente_{docente.legajo}"
                            User.objects.create_user(
                                username=username,
                                password='docente123',
                                first_name=nombre_completo,
                                last_name=apellido,
                                email=row['EMAIL'] or f"{nombre_completo.lower().replace(' ', '.')}.{apellido.lower()}@alcal.edu.ar"
                            )
                            
                            if docentes_creados % 10 == 0:
                                self.stdout.write(f'    📚 {docentes_creados} docentes creados...')
                    
                    except Exception as e:
                        self.stdout.write(f'    ⚠️ Error con docente {row.get("NOMBRES", "N/A")}: {e}')
        
        self.stdout.write(f'  ✅ {docentes_creados} docentes creados desde CSV')

    def setup_cursos_csv(self):
        """Crear cursos únicos desde archivo de estudiantes"""
        self.stdout.write('📚 Creando cursos desde CSV de estudiantes...')
        
        csv_file = 'Legajo Estudiantes 2022 - LegajoGral.csv'
        if not os.path.exists(csv_file):
            self.stdout.write(f'  ❌ Archivo {csv_file} no encontrado')
            return
        
        cursos_unicos = set()
        carrera = Carrera.objects.first()
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ACTIVX'] == 'SI' and row['CURSO']:  # Solo estudiantes activos
                    curso_nombre = row['CURSO'].strip()
                    cursos_unicos.add(curso_nombre)
        
        cursos_creados = 0
        for curso_nombre in sorted(cursos_unicos):
            curso, created = Curso.objects.get_or_create(
                curso=curso_nombre,
                defaults={'carrera': carrera}
            )
            if created:
                cursos_creados += 1
                self.stdout.write(f'  ✅ Curso {curso_nombre} creado')
        
        self.stdout.write(f'  📊 Total cursos creados: {cursos_creados}')

    def setup_materias_csv(self):
        """Crear materias con docentes desde archivo CSV"""
        self.stdout.write('📖 Creando materias con docentes desde CSV...')
        
        csv_file = 'Legajo Docente - DocenteMateria.csv'
        if not os.path.exists(csv_file):
            self.stdout.write(f'  ❌ Archivo {csv_file} no encontrado')
            return
        
        materias_creadas = 0
        total_rows = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total_rows += 1
        
        self.stdout.write(f'  📋 Procesando {total_rows} materias...')
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, 1):
                try:
                    curso_nombre = row['CURSO'].strip()
                    materia_nombre = row['MATERIA'].strip()
                    docente_nombre = row['DOCENTE'].strip()
                    
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
                        
                        # Log cada 50 materias
                        if i % 50 == 0:
                            self.stdout.write(f'    📚 {i}/{total_rows} materias procesadas...')
                    
                except Exception as e:
                    self.stdout.write(f'    ⚠️ Error con materia {row.get("MATERIA", "N/A")}: {e}')
        
        self.stdout.write(f'  ✅ {materias_creadas} materias creadas con docentes asignados')

    def setup_alumnos_csv(self):
        """Crear alumnos desde archivo CSV"""
        self.stdout.write('👥 Cargando alumnos desde CSV...')
        
        csv_file = 'Legajo Estudiantes 2022 - LegajoGral.csv'
        if not os.path.exists(csv_file):
            self.stdout.write(f'  ❌ Archivo {csv_file} no encontrado')
            return
        
        alumnos_creados = 0
        total_rows = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['ACTIVX'] == 'SI':
                    total_rows += 1
        
        self.stdout.write(f'  📋 Procesando {total_rows} estudiantes activos...')
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader, 1):
                if row['ACTIVX'] == 'SI':  # Solo estudiantes activos
                    try:
                        # Buscar curso
                        curso = Curso.objects.get(curso=row['CURSO'].strip())
                        
                        # Crear alumno
                        alumno, created = Alumno.objects.get_or_create(
                            dni=int(row['NUMERO'].replace('.', '').replace(',', '')),
                            defaults={
                                'nombre': row['NOMBRES'].strip(),
                                'apellido': row['APELLIDO'].strip(),
                                'telefono': row['TELÉFONOS'] or f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                                'direccion': row['DOMICILIO'] or f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}',
                                'nacionalidad': row['NACIONALIDAD'] or 'Argentina',
                                'curso': curso
                            }
                        )
                        
                        if created:
                            alumnos_creados += 1
                            
                            # Crear familiar si hay datos
                            if row['NOMBRE MADRE'] and row['NOMBRE MADRE'].strip():
                                familiar = Madre.objects.create(
                                    nombre_madre=row['NOMBRE MADRE'].strip(),
                                    apellido_madre=row['APELLIDO'].strip(),
                                    dni_madre=random.randint(10000000, 99999999),
                                    telefono_madre=row['Tel Madre'] or f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                                    nacionalidad_madre=row['NACIONALIDAD P'] or 'Argentina',
                                    direccion_madre=row['DOMICILIO'] or f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}'
                                )
                                alumno.madre = familiar
                                alumno.save()
                            elif row['NOMBRE PADRE'] and row['NOMBRE PADRE'].strip():
                                familiar = Padre.objects.create(
                                    nombre_padre=row['NOMBRE PADRE'].strip(),
                                    apellido_padre=row['APELLIDO'].strip(),
                                    dni_padre=random.randint(10000000, 99999999),
                                    telefono_padre=row['Tel Padre'] or f'11-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}',
                                    nacionalidad_padre=row['NACIONALIDAD P'] or 'Argentina',
                                    direccion_padre=row['DOMICILIO'] or f'Calle {random.randint(100, 9999)} #{random.randint(1, 999)}'
                                )
                                alumno.padre = familiar
                                alumno.save()
                            
                            # Crear usuario para el alumno
                            username = f"alumno_{alumno.dni}"
                            User.objects.create_user(
                                username=username,
                                password='alumno123',
                                first_name=row['NOMBRES'].strip(),
                                last_name=row['APELLIDO'].strip(),
                                email=row['EMAIL'] or f"{row['NOMBRES'].lower().replace(' ', '.')}.{row['APELLIDO'].lower()}@alcal.edu.ar"
                            )
                            
                            # Log cada 50 alumnos
                            if alumnos_creados % 50 == 0:
                                self.stdout.write(f'    👥 {alumnos_creados} alumnos creados...')
                    
                    except Exception as e:
                        self.stdout.write(f'    ⚠️ Error con alumno {row.get("NOMBRES", "N/A")}: {e}')
        
        self.stdout.write(f'  ✅ {alumnos_creados} alumnos creados desde CSV')

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
            {'nombre': 'educacion_fisica', 'hora_inicio': '14:00', 'hora_fin': '16:00'},
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



