import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alcal.settings")
django.setup()

from asistencias.models import ReglaAsistencia

CSV_PATH = '/home/esteban/Documentos/alcal/Asistencia - Codigos.csv'

def importar_reglas():
    print("=== IMPORTANDO REGLAS DE ASISTENCIA ===")
    
    # Limpiar reglas existentes
    ReglaAsistencia.objects.all().delete()
    print("✅ Reglas anteriores eliminadas")
    
    count = 0
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Mapear columnas del CSV a campos del modelo
                # CSV: Mañana,Tarde,Ed Física,CanTidad,Nombre
                
                codigo_manana = row['Mañana']
                codigo_tarde = row['Tarde']
                codigo_ed_fisica = row['Ed Física']
                
                # Convertir valor numérico (reemplazar coma por punto)
                valor_str = row['CanTidad'].replace(',', '.')
                try:
                    valor_falta = float(valor_str) if valor_str else 0.0
                except ValueError:
                    valor_falta = 0.0
                
                observacion = row['Nombre']
                
                # Crear registro
                ReglaAsistencia.objects.create(
                    codigo_manana=codigo_manana,
                    codigo_tarde=codigo_tarde,
                    codigo_ed_fisica=codigo_ed_fisica,
                    valor_falta=valor_falta,
                    observacion=observacion
                )
                count += 1
                
        print(f"✅ {count} reglas importadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error al importar: {e}")

if __name__ == '__main__':
    importar_reglas()
