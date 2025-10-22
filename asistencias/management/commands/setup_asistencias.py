from django.core.management.base import BaseCommand
from django.db import transaction

from asistencias.models import CodigoAsistencia, Turno
from escuela.models import Anio


class Command(BaseCommand):
    help = 'Configura los datos iniciales del sistema de asistencias'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Elimina datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['reset']:
            self.stdout.write('🗑️  Eliminando datos existentes...')
            CodigoAsistencia.objects.all().delete()
            Turno.objects.all().delete()

        with transaction.atomic():
            # 1. Crear códigos de asistencia
            self.crear_codigos_asistencia()
            
            # 2. Crear turnos
            self.crear_turnos()
            
            # 3. Crear año lectivo si no existe
            self.crear_anio_lectivo()

        self.stdout.write(
            self.style.SUCCESS('\n🎉 ¡Sistema de asistencias configurado exitosamente!')
        )
        
        self.mostrar_resumen()

    def crear_codigos_asistencia(self):
        """Crea los códigos de asistencia según las especificaciones"""
        codigos_data = [
            {
                'codigo': 'P',
                'descripcion': 'Presente',
                'cantidad_falta': 0.0
            },
            {
                'codigo': 't',
                'descripcion': 'Tarde (menos de 15 minutos)',
                'cantidad_falta': 0.0
            },
            {
                'codigo': 'T',
                'descripcion': 'Tarde (más de 15 minutos)',
                'cantidad_falta': 0.5
            },
            {
                'codigo': 'A',
                'descripcion': 'Ausente',
                'cantidad_falta': 1.0
            },
            {
                'codigo': 'r',
                'descripcion': 'Retirado (menos de 15 min antes del fin)',
                'cantidad_falta': 0.0
            },
            {
                'codigo': 'R',
                'descripcion': 'Retirado (más de 15 min antes del fin)',
                'cantidad_falta': 0.5
            },
        ]
        
        self.stdout.write('\n📝 Creando códigos de asistencia...')
        
        for codigo_data in codigos_data:
            codigo, created = CodigoAsistencia.objects.get_or_create(
                codigo=codigo_data['codigo'],
                defaults=codigo_data
            )
            if created:
                self.stdout.write(f'  ✓ {codigo.codigo} - {codigo.descripcion}')
            else:
                self.stdout.write(f'  ⚠ {codigo.codigo} - Ya existe')

    def crear_turnos(self):
        """Crea los turnos de clases"""
        turnos_data = [
            {
                'nombre': 'mañana',
                'hora_inicio': '08:00:00',
                'hora_fin': '12:00:00'
            },
            {
                'nombre': 'tarde',
                'hora_inicio': '13:00:00',
                'hora_fin': '17:00:00'
            },
            {
                'nombre': 'educacion_fisica',
                'hora_inicio': '14:00:00',
                'hora_fin': '16:00:00'
            },
        ]
        
        self.stdout.write('\n🕐 Creando turnos...')
        
        for turno_data in turnos_data:
            turno, created = Turno.objects.get_or_create(
                nombre=turno_data['nombre'],
                defaults=turno_data
            )
            if created:
                self.stdout.write(f'  ✓ {turno.get_nombre_display()} ({turno.hora_inicio} - {turno.hora_fin})')
            else:
                self.stdout.write(f'  ⚠ {turno.get_nombre_display()} - Ya existe')

    def crear_anio_lectivo(self):
        """Crea el año lectivo actual si no existe"""
        from datetime import datetime
        anio_actual = datetime.now().year
        
        anio, created = Anio.objects.get_or_create(
            ciclo_lectivo=anio_actual,
            defaults={'ciclo_lectivo': anio_actual}
        )
        
        if created:
            self.stdout.write(f'\n📅 Año lectivo creado: {anio_actual}')
        else:
            self.stdout.write(f'\n📅 Año lectivo existente: {anio_actual}')

    def mostrar_resumen(self):
        """Muestra un resumen de lo creado"""
        total_codigos = CodigoAsistencia.objects.count()
        total_turnos = Turno.objects.count()
        
        self.stdout.write('\n📊 Resumen del sistema de asistencias:')
        self.stdout.write('=' * 50)
        self.stdout.write(f'📝 Códigos de asistencia: {total_codigos}')
        self.stdout.write(f'🕐 Turnos configurados: {total_turnos}')
        self.stdout.write('=' * 50)
        
        self.stdout.write('\n📋 Códigos disponibles:')
        for codigo in CodigoAsistencia.objects.all():
            self.stdout.write(f'   {codigo.codigo} = {codigo.descripcion} (Falta: {codigo.cantidad_falta})')
        
        self.stdout.write('\n🕐 Turnos disponibles:')
        for turno in Turno.objects.all():
            self.stdout.write(f'   {turno.get_nombre_display()}: {turno.hora_inicio} - {turno.hora_fin}')
        
        self.stdout.write('\n🎯 Sistema listo para tomar asistencias por curso') 