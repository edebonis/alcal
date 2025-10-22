from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from alcal.models import PerfilUsuario
from alumnos.models import Alumno
from docentes.models import Docente


class Command(BaseCommand):
    help = 'Crea usuarios de demostración con diferentes roles para ALCAL'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina usuarios existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('Eliminando usuarios existentes...')
            User.objects.filter(username__startswith='demo_').delete()

        # Crear usuarios de demostración
        usuarios_demo = [
            {
                'username': 'demo_admin',
                'email': 'admin@alcal.edu.ar',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'password': 'admin123',
                'rol': 'administrador',
                'legajo': 'ADM001',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'demo_director',
                'email': 'director@alcal.edu.ar',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'password': 'director123',
                'rol': 'director',
                'legajo': 'DIR001',
                'is_staff': True,
            },
            {
                'username': 'demo_preceptor',
                'email': 'preceptor@alcal.edu.ar',
                'first_name': 'María',
                'last_name': 'González',
                'password': 'preceptor123',
                'rol': 'preceptor',
                'legajo': 'PRE001',
                'is_staff': True,
            },
            {
                'username': 'demo_docente',
                'email': 'docente@alcal.edu.ar',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'password': 'docente123',
                'rol': 'docente',
                'legajo': 'DOC001',
                'is_staff': True,
            },
            {
                'username': 'demo_familiar',
                'email': 'familiar@alcal.edu.ar',
                'first_name': 'Roberto',
                'last_name': 'López',
                'password': 'familiar123',
                'rol': 'familiar',
                'legajo': 'FAM001',
            },
            {
                'username': 'demo_alumno',
                'email': 'alumno@alcal.edu.ar',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'password': 'alumno123',
                'rol': 'alumno',
                'legajo': 'ALU001',
            },
        ]

        for usuario_data in usuarios_demo:
            # Extraer datos del perfil
            rol = usuario_data.pop('rol')
            legajo = usuario_data.pop('legajo')
            
            # Crear usuario
            user, created = User.objects.get_or_create(
                username=usuario_data['username'],
                defaults=usuario_data
            )
            
            if created:
                user.set_password(usuario_data['password'])
                user.save()
                
                # Actualizar o crear perfil
                perfil, perfil_created = PerfilUsuario.objects.get_or_create(
                    user=user,
                    defaults={
                        'rol': rol,
                        'legajo': legajo,
                        'telefono': f'+54 11 {legajo[-3:]}-{legajo[-3:]}',
                        'direccion': f'Calle {legajo} 123, Buenos Aires',
                    }
                )
                
                # Si el perfil ya existía, actualizar el rol
                if not perfil_created:
                    perfil.rol = rol
                    perfil.legajo = legajo
                    perfil.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Usuario creado: {user.username} ({perfil.get_rol_display()})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠ Usuario ya existe: {user.username}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 ¡Usuarios de demostración creados exitosamente!'
            )
        )
        
        self.stdout.write('\n📋 Credenciales de acceso:')
        self.stdout.write('=' * 50)
        for usuario_data in usuarios_demo:
            username = usuario_data['username']
            password = usuario_data['password']
            self.stdout.write(f'👤 {username} / {password}')
        
        self.stdout.write('\n🌐 Accede al admin en: http://localhost:8005/admin/')
        self.stdout.write('📱 O desde tu red local en: http://192.168.68.13:8005/admin/') 