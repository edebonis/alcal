"""
Script para importar datos desde los archivos CSV del colegio Sagrado Corazón.
"""
import os
import sys
import django
import csv
from datetime import datetime

# Configurar Django
sys.path.append('/home/esteban/Documentos/alcal')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
django.setup()

from docentes.models import Docente
from escuela.models import Carrera, Anio, Curso, Materia
from alumnos.models import Alumno, Padre, Madre, Tutor

def limpiar_datos():
    """Elimina todos los datos existentes de la base de datos."""
    print("\n⚠️  LIMPIANDO BASE DE DATOS...")
    print("=" * 60)
    
    # Contar registros antes de eliminar
    total_alumnos = Alumno.objects.count()
    total_docentes = Docente.objects.count()
    total_materias = Materia.objects.count()
    total_cursos = Curso.objects.count()
    total_carreras = Carrera.objects.count()
    total_anios = Anio.objects.count()
    total_padres = Padre.objects.count()
    total_madres = Madre.objects.count()
    total_tutores = Tutor.objects.count()
    
    print(f"Registros a eliminar:")
    print(f"  - Alumnos: {total_alumnos}")
    print(f"  - Docentes: {total_docentes}")
    print(f"  - Materias: {total_materias}")
    print(f"  - Cursos: {total_cursos}")
    print(f"  - Carreras: {total_carreras}")
    print(f"  - Años: {total_anios}")
    print(f"  - Padres: {total_padres}")
    print(f"  - Madres: {total_madres}")
    print(f"  - Tutores: {total_tutores}")
    
    # Eliminar en orden correcto (respetando dependencias de FK)
    print("\nEliminando registros...")
    Alumno.objects.all().delete()
    print("  ✓ Alumnos eliminados")
    
    # Eliminar la relación Many-to-Many primero
    for docente in Docente.objects.all():
        docente.materia.clear()
    Docente.objects.all().delete()
    print("  ✓ Docentes eliminados")
    
    Materia.objects.all().delete()
    print("  ✓ Materias eliminadas")
    
    Curso.objects.all().delete()
    print("  ✓ Cursos eliminados")
    
    Carrera.objects.all().delete()
    print("  ✓ Carreras eliminadas")
    
    Anio.objects.all().delete()
    print("  ✓ Años eliminados")
    
    Padre.objects.all().delete()
    print("  ✓ Padres eliminados")
    
    Madre.objects.all().delete()
    print("  ✓ Madres eliminadas")
    
    Tutor.objects.all().delete()
    print("  ✓ Tutores eliminados")
    
    print("\n✅ Base de datos limpiada exitosamente")
    print("=" * 60)

def crear_estructura_base():
    """Crea las carreras y cursos necesarios según la descripción."""
    print("Creando estructura base...")
    
    # Carrera A: Bachillerato en Economía
    carrera_a, _ = Carrera.objects.get_or_create(
        nombre="Bachillerato con orientación en Economía"
    )
    print(f"✓ Carrera A: {carrera_a.nombre}")
    
    # Carrera B: Técnica en Programación
    carrera_b, _ = Carrera.objects.get_or_create(
        nombre="Técnico en Programación"
    )
    print(f"✓ Carrera B: {carrera_b.nombre}")
    
    # Año lectivo 2022 (basado en el nombre del CSV)
    anio_2022, _ = Anio.objects.get_or_create(ciclo_lectivo=2022)
    print(f"✓ Año lectivo: {anio_2022.ciclo_lectivo}")
    
    # Crear cursos (formato: "1A", "1B", "2A", "2B", etc.)
    # Curso A (hasta 6to año)
    for i in range(1, 7):
        curso_nombre = f"{i}A"
        Curso.objects.get_or_create(
            curso=curso_nombre,
            defaults={'carrera': carrera_a}
        )
        print(f"✓ Curso {curso_nombre} - Economía")
    
    # Curso B (hasta 7mo año)
    for i in range(1, 8):
        curso_nombre = f"{i}B"
        Curso.objects.get_or_create(
            curso=curso_nombre,
            defaults={'carrera': carrera_b}
        )
        print(f"✓ Curso {curso_nombre} - Técnica")
    
    return carrera_a, carrera_b


def importar_docentes():
    """Importa los docentes desde el CSV."""
    print("\nImportando docentes...")
    
    archivo = '/home/esteban/Documentos/alcal/Legajo Docente - Legajo.csv'
    
    with open(archivo, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # Saltar filas vacías
            if not row.get('APELLIDOS') or not row.get('NOMBRES'):
                continue
            
            apellido = row.get('APELLIDOS', '').strip()
            nombre = row.get('NOMBRES', '').strip()
            email = row.get('EMAIL', '').strip()
            documento = row.get('DOCUMENTO', '').strip()
            
            if not email or not apellido:
                continue
            
            # Parsear DNI (puede tener puntos)
            dni = None
            if documento:
                try:
                    dni = int(documento.replace('.', '').replace(',', ''))
                except:
                    pass
            
            # Crear o actualizar docente (legajo temporal basado en count)
            docente, created = Docente.objects.update_or_create(
                email=email,
                defaults={
                    'apellido': apellido,
                    'nombre': nombre,
                    'dni': dni,
                    'legajo': count + 1,
                    'telefono': row.get('CELULAR', ''),
                    'nacionalidad': row.get('NACIONALIDAD', 'Argentina'),
                }
            )
            
            count += 1
            status = "creado" if created else "actualizado"
            print(f"  {status}: {docente.nombre} {docente.apellido}")
    
    print(f"✓ {count} docentes importados")

def importar_materias():
    """Importa las materias y la relación docente-materia desde el CSV."""
    print("\nImportando materias...")
    
    archivo = '/home/esteban/Documentos/alcal/Legajo Docente - DocenteMateria.csv'
    
    with open(archivo, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar header
        
        materias_count = 0
        relaciones_count = 0
        
        for row in reader:
            if len(row) < 6:
                continue
            
            try:
                # Columnas: 0=id, 1=año, 2=curso(A/B), 3=nombre_materia, 4=nombre_docente, 5=email_docente
                anio_numero = int(row[1])
                division = row[2].strip()
                nombre_materia = row[3].strip()
                email_docente = row[5].strip()
                
                if not nombre_materia or not division:
                    continue
                
                # Construir nombre del curso (ej: "1A", "2B")
                curso_nombre = f"{anio_numero}{division}"
                
                # Obtener curso
                try:
                    curso = Curso.objects.get(curso=curso_nombre)
                except Curso.DoesNotExist:
                    print(f"  ⚠ Curso no encontrado: {curso_nombre}")
                    continue
                
                # Crear materia (horas por defecto: 3)
                materia, created = Materia.objects.get_or_create(
                    nombre=nombre_materia,
                    curso=curso,
                    defaults={'horas': 3}
                )
                
                if created:
                    materias_count += 1
                    print(f"  Materia: {nombre_materia} - {curso_nombre}")
                
                # Buscar docente y crear relación ManyToMany
                if email_docente:
                    try:
                        docente = Docente.objects.filter(email=email_docente).first()
                        
                        if docente and materia not in docente.materia.all():
                            # Agregar materia al docente usando ManyToMany
                            docente.materia.add(materia)
                            relaciones_count += 1
                        
                    except Docente.DoesNotExist:
                        print(f"  ⚠ Docente no encontrado: {email_docente}")
                
            except Exception as e:
                print(f"  ⚠ Error en fila {row}: {e}")
                continue
    
    print(f"✓ {materias_count} materias creadas")
    print(f"✓ {relaciones_count} asignaciones docente-materia creadas")

def importar_alumnos():
    """Importa los alumnos desde el CSV."""
    print("\nImportando alumnos...")
    
    archivo = '/home/esteban/Documentos/alcal/Legajo Estudiantes 2022 - LegajoGral.csv'
    
    with open(archivo, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        
        for row in reader:
            # Saltar filas vacías o sin apellido
            if not row.get('APELLIDO') or not row.get('NOMBRES'):
                continue
            
            apellido = row.get('APELLIDO', '').strip()
            nombres = row.get('NOMBRES', '').strip()
            email = row.get('EMAIL', '').strip()
            documento = row.get('NUMERO', '').strip()
            curso_str = row.get('CURSO', '').strip()  # Ej: "1A", "2B"
            
            if not apellido or not curso_str:
                continue
            
            # Buscar curso directamente por nombre (ej: "1A", "2B")
            try:
                curso = Curso.objects.get(curso=curso_str)
                
                # Parsear DNI
                dni = None
                if documento:
                    try:
                        dni = int(documento.replace('.', '').replace(',', ''))
                    except:
                        dni = None
                
                # Crear o actualizar alumno (usando email o DNI como clave única)
                if email:
                    alumno, created = Alumno.objects.update_or_create(
                        email=email,
                        defaults={
                            'apellido': apellido,
                            'nombre': nombres,
                            'dni': dni,
                            'curso': curso,
                        }
                    )
                elif dni:
                    alumno, created = Alumno.objects.update_or_create(
                        dni=dni,
                        defaults={
                            'apellido': apellido,
                            'nombre': nombres,
                            'email': email if email else None,
                            'curso': curso,
                        }
                    )
                else:
                    # Si no hay email ni DNI válido, simplemente crear
                    alumno = Alumno.objects.create(
                        apellido=apellido,
                        nombre=nombres,
                        curso=curso,
                    )
                    created = True
                
                count += 1
                if created:
                    print(f"  Alumno: {alumno.nombre} {alumno.apellido} - {curso_str}")
                
            except Exception as e:
                print(f"  ⚠ Error procesando alumno {apellido} {nombres}: {e}")
                continue
    
    print(f"✓ {count} alumnos importados")

def main():
    """Función principal del script."""
    print("="*60)
    print("IMPORTACIÓN DE DATOS - SAGRADO CORAZÓN ALCAL")
    print("="*60)
    
    try:
        # 0. Limpiar datos existentes
        limpiar_datos()
        
        # 1. Crear estructura base (carreras, años, cursos)
        carrera_a, carrera_b = crear_estructura_base()
        
        # 2. Importar docentes
        importar_docentes()
        
        # 3. Importar materias y asignaciones
        importar_materias()
        
        # 4. Importar alumnos
        importar_alumnos()
        
        print("\n" + "="*60)
        print("✅ IMPORTACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
