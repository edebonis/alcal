from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from alcal.models import PerfilUsuario
from alumnos.models import Alumno
from escuela.models import Curso


class Command(BaseCommand):
    help = 'Configura el sistema ALCAL con usuarios, alumnos y familiares'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Eliminando datos existentes...')
            User.objects.filter(username__in=['edebonis']).delete()
            User.objects.filter(username__startswith='alumno_').delete()
            User.objects.filter(username__startswith='familiar_').delete()

        with transaction.atomic():
            # 1. Crear usuario administrador edebonis
            self.crear_usuario_edebonis()
            
            # 2. Obtener cursos existentes
            cursos = self.obtener_cursos()
            
            # 3. Crear alumnos, usuarios y familiares para cada curso
            for curso in cursos:
                self.crear_alumnos_para_curso(curso)

        self.stdout.write(
            self.style.SUCCESS('\n🎉 ¡Sistema ALCAL configurado exitosamente!')
        )
        
        self.mostrar_resumen()

    def crear_usuario_edebonis(self):
        """Crea el usuario administrador edebonis"""
        user, created = User.objects.get_or_create(
            username='edebonis',
            defaults={
                'email': 'edebonis@alcal.edu.ar',
                'first_name': 'Eduardo',
                'last_name': 'De Bonis',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        
        if created:
            user.set_password('admin123')  # Cambiar por una contraseña segura
            user.save()
            
            # Crear perfil de administrador
            PerfilUsuario.objects.get_or_create(
                user=user,
                defaults={
                    'rol': 'administrador',
                    'legajo': 'ADM-EDB',
                    'telefono': '+54 11 1234-5678',
                    'direccion': 'Dirección Administrativa',
                }
            )
            
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario administrador creado: {user.username}')
            )
        else:
            # Actualizar perfil si ya existe
            perfil, _ = PerfilUsuario.objects.get_or_create(user=user)
            perfil.rol = 'administrador'
            perfil.legajo = 'ADM-EDB'
            perfil.save()
            
            self.stdout.write(
                self.style.WARNING(f'⚠ Usuario ya existe, actualizado: {user.username}')
            )

    def obtener_cursos(self):
        """Obtiene los cursos existentes o crea algunos básicos"""
        cursos = list(Curso.objects.all())
        
        if not cursos:
            # Primero necesitamos crear una carrera
            from escuela.models import Carrera
            carrera, _ = Carrera.objects.get_or_create(
                nombre='Bachillerato',
                defaults={'nombre': 'Bachillerato'}
            )
            
            # Crear cursos básicos si no existen
            cursos_data = [
                {'curso': '1A', 'carrera': carrera},
                {'curso': '1B', 'carrera': carrera},
                {'curso': '2A', 'carrera': carrera},
                {'curso': '2B', 'carrera': carrera},
                {'curso': '3A', 'carrera': carrera},
            ]
            
            for curso_data in cursos_data:
                curso, created = Curso.objects.get_or_create(
                    curso=curso_data['curso'],
                    defaults=curso_data
                )
                if created:
                    cursos.append(curso)
                    self.stdout.write(f'✓ Curso creado: {curso.curso}')
        
        return cursos

    def crear_alumnos_para_curso(self, curso):
        """Crea 10 alumnos con usuarios y familiares para un curso"""
        self.stdout.write(f'\n📚 Creando alumnos para {curso.curso}...')
        
        for i in range(1, 11):
            # Datos del alumno
            numero_alumno = f"{curso.id:02d}{i:02d}"
            
            # Crear usuario del alumno
            username_alumno = f'alumno_{numero_alumno}'
            user_alumno, created = User.objects.get_or_create(
                username=username_alumno,
                defaults={
                    'email': f'{username_alumno}@alcal.edu.ar',
                    'first_name': self.generar_nombre(),
                    'last_name': self.generar_apellido(),
                    'is_staff': False,
                }
            )
            
            if created:
                user_alumno.set_password('alumno123')
                user_alumno.save()
                
                # Crear perfil del alumno
                PerfilUsuario.objects.get_or_create(
                    user=user_alumno,
                    defaults={
                        'rol': 'alumno',
                        'legajo': f'ALU-{numero_alumno}',
                        'telefono': f'+54 11 {numero_alumno}-{numero_alumno}',
                        'direccion': f'Calle {numero_alumno} 123, Buenos Aires',
                    }
                )
            
            # Crear o actualizar alumno
            alumno, created = Alumno.objects.get_or_create(
                dni=int(f'40{numero_alumno}'),
                defaults={
                    'nombre': user_alumno.first_name,
                    'apellido': user_alumno.last_name,
                    'telefono': f'+54 11 {numero_alumno}-{numero_alumno}',
                    'direccion': f'Calle {numero_alumno} 123, Buenos Aires',
                    'curso': curso,
                    'nacionalidad': 'Argentina',
                }
            )
            
            # Asociar usuario al alumno en el perfil
            if hasattr(user_alumno, 'perfil'):
                user_alumno.perfil.alumno_relacionado = alumno
                user_alumno.perfil.save()
            
            # Crear usuario familiar
            username_familiar = f'familiar_{numero_alumno}'
            user_familiar, created = User.objects.get_or_create(
                username=username_familiar,
                defaults={
                    'email': f'{username_familiar}@alcal.edu.ar',
                    'first_name': self.generar_nombre_familiar(),
                    'last_name': user_alumno.last_name,  # Mismo apellido que el alumno
                    'is_staff': False,
                }
            )
            
            if created:
                user_familiar.set_password('familiar123')
                user_familiar.save()
                
                # Crear perfil del familiar
                PerfilUsuario.objects.get_or_create(
                    user=user_familiar,
                    defaults={
                        'rol': 'familiar',
                        'legajo': f'FAM-{numero_alumno}',
                        'telefono': f'+54 11 {numero_alumno}-{numero_alumno}',
                        'direccion': f'Calle {numero_alumno} 123, Buenos Aires',
                    }
                )
            
            if created:
                self.stdout.write(f'  ✓ Alumno: {user_alumno.get_full_name()} | Familiar: {user_familiar.get_full_name()}')

    def generar_nombre(self):
        """Genera nombres aleatorios para los alumnos"""
        nombres = [
            'Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Laura', 'Diego', 'Sofia',
            'Mateo', 'Valentina', 'Santiago', 'Camila', 'Nicolás', 'Isabella',
            'Sebastián', 'Martina', 'Alejandro', 'Lucía', 'Gabriel', 'Emma'
        ]
        import random
        return random.choice(nombres)

    def generar_apellido(self):
        """Genera apellidos aleatorios"""
        apellidos = [
            'García', 'Rodríguez', 'González', 'Fernández', 'López', 'Martínez',
            'Sánchez', 'Pérez', 'Gómez', 'Martín', 'Jiménez', 'Ruiz',
            'Hernández', 'Díaz', 'Moreno', 'Muñoz', 'Álvarez', 'Romero',
            'Alonso', 'Gutiérrez'
        ]
        import random
        return random.choice(apellidos)

    def generar_nombre_familiar(self):
        """Genera nombres para familiares"""
        nombres = [
            'Roberto', 'Carmen', 'Miguel', 'Patricia', 'José', 'Elena',
            'Francisco', 'Rosa', 'Antonio', 'Pilar', 'Manuel', 'Mercedes',
            'Rafael', 'Dolores', 'Ángel', 'Josefa', 'Jesús', 'Cristina',
            'Javier', 'Francisca'
        ]
        import random
        return random.choice(nombres)

    def mostrar_resumen(self):
        """Muestra un resumen de lo creado"""
        total_usuarios = User.objects.count()
        total_alumnos = Alumno.objects.count()
        total_cursos = Curso.objects.count()
        
        self.stdout.write('\n📊 Resumen del sistema:')
        self.stdout.write('=' * 50)
        self.stdout.write(f'👥 Total usuarios: {total_usuarios}')
        self.stdout.write(f'🎒 Total alumnos: {total_alumnos}')
        self.stdout.write(f'📚 Total cursos: {total_cursos}')
        self.stdout.write('=' * 50)
        
        self.stdout.write('\n🔑 Credenciales principales:')
        self.stdout.write('   edebonis / admin123 (Administrador)')
        self.stdout.write('   alumno_XXXX / alumno123 (Alumnos)')
        self.stdout.write('   familiar_XXXX / familiar123 (Familiares)')
        
        self.stdout.write('\n🌐 Acceso: http://localhost:8080/admin/') 