# -*- encoding: utf-8 -*-
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from asistencias.models import CodigoAsistencia, ReglaAsistencia

class Command(BaseCommand):
    help = 'Importa las reglas de asistencia y códigos desde el CSV'

    def handle(self, *args, **options):
        csv_path = os.path.join(settings.BASE_DIR, 'Asistencia - Codigos.csv')
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo: {csv_path}'))
            return

        self.stdout.write('Iniciando importación de reglas de asistencia...')
        
        codigos_creados = 0
        reglas_creadas = 0
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Saltar encabezado
            
            for row in reader:
                if not row:
                    continue
                    
                # 1. Importar Códigos de Asistencia (Columnas 8 y 9)
                # El CSV tiene definiciones de códigos en las columnas I y J (índices 8 y 9)
                if len(row) >= 10:
                    codigo_val = row[8].strip()
                    descripcion_val = row[9].strip()
                    
                    if codigo_val and descripcion_val:
                        # Definir valor de falta por defecto según el código
                        cantidad_falta = 0.0
                        if codigo_val in ['A']:
                            cantidad_falta = 1.0
                        elif codigo_val in ['P']:
                            cantidad_falta = 0.0
                        elif codigo_val in ['T', 't', 'R', 'r']:
                            cantidad_falta = 0.5 # Valor por defecto, ajustable
                            
                        obj, created = CodigoAsistencia.objects.get_or_create(
                            codigo=codigo_val,
                            defaults={
                                'descripcion': descripcion_val,
                                'cantidad_falta': cantidad_falta
                            }
                        )
                        if created:
                            codigos_creados += 1
                            self.stdout.write(f'Código creado: {codigo_val} - {descripcion_val}')

                # 2. Importar Reglas de Asistencia (Columnas 0-4)
                if len(row) >= 5:
                    manana = row[0].strip()
                    tarde = row[1].strip()
                    ed_fisica = row[2].strip()
                    
                    # Parsear valor de falta (ej: "0,5" -> 0.5)
                    cantidad_str = row[3].strip().replace(',', '.')
                    try:
                        valor_falta = float(cantidad_str) if cantidad_str else 0.0
                    except ValueError:
                        valor_falta = 0.0
                        
                    # Observación (limpiar comillas extra si las hay)
                    observacion = row[4].strip()
                    if observacion.startswith('"') and observacion.endswith('"'):
                        observacion = observacion[1:-1]
                    
                    # Limpiar comas múltiples consecutivas en la observación
                    parts = [p.strip() for p in observacion.split(',') if p.strip()]
                    observacion_limpia = ', '.join(parts)
                    
                    if manana and tarde and ed_fisica:
                        regla, created = ReglaAsistencia.objects.update_or_create(
                            codigo_manana=manana,
                            codigo_tarde=tarde,
                            codigo_ed_fisica=ed_fisica,
                            defaults={
                                'valor_falta': valor_falta,
                                'observacion': observacion_limpia
                            }
                        )
                        if created:
                            reglas_creadas += 1
        
        self.stdout.write(self.style.SUCCESS(f'Importación completada. Códigos nuevos: {codigos_creados}, Reglas nuevas: {reglas_creadas}'))
