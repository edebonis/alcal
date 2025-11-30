"""
Script para poblar la base de datos con datos de prueba (falsos) para demostración.
No requiere los archivos CSV originales.
"""
import os
import sys
import django
import random
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
django.setup()

from docentes.models import Docente
from escuela.models import Carrera, Anio, Curso, Materia
from alumnos.models import Alumno

# Intentar importar Faker, si no existe, usar generador simple
try:
    from faker import Faker
    fake = Faker('es_AR')
    USE_FAKER = True
except ImportError:
    USE_FAKER = False
    print("⚠️  Librería 'Faker' no encontrada. Usando generador de datos simple.")
    print("   Para mejores resultados: pip install faker")

def get_random_name():
    if USE_FAKER:
        return fake.first_name(), fake.last_name()
    names = ["Juan", "María", "Pedro", "Ana", "Luis", "Sofía", "Carlos", "Lucía", "Miguel", "Elena"]
    last_names = ["García", "Martínez", "López", "González", "Pérez", "Rodríguez", "Sánchez", "Ramírez"]
    return random.choice(names), random.choice(last_names)

def get_random_email(nombre, apellido):
    if USE_FAKER:
        return fake.email()
    return f"{nombre.lower()}.{apellido.lower()}@example.com"

def limpiar_datos():
    """Elimina todos los datos existentes de la base de datos."""
    print("\n⚠️  LIMPIANDO BASE DE DATOS...")
    
    Alumno.objects.all().delete()
    
    # Limpiar relaciones M2M de docentes antes de borrar
    for docente in Docente.objects.all():
        docente.materia.clear()
    Docente.objects.all().delete()
    
    Materia.objects.all().delete()
    Curso.objects.all().delete()
    Carrera.objects.all().delete()
    Anio.objects.all().delete()
    
    print("✅ Base de datos limpiada.")

def crear_estructura_base():
    """Crea carreras y cursos."""
    print("\n🏗️  Creando estructura académica...")
    
    carrera_a = Carrera.objects.create(nombre="Bachillerato en Economía")
    carrera_b = Carrera.objects.create(nombre="Técnico en Programación")
    
    anio_actual = Anio.objects.create(ciclo_lectivo=datetime.now().year)
    
    cursos_creados = []
    
    # Cursos Economía (1A a 5A)
    for i in range(1, 6):
        curso = Curso.objects.create(
            curso=f"{i}A",
            carrera=carrera_a
        )
        cursos_creados.append(curso)
        
    # Cursos Programación (1B a 6B)
    for i in range(1, 7):
        curso = Curso.objects.create(
            curso=f"{i}B",
            carrera=carrera_b
        )
        cursos_creados.append(curso)
        
    print(f"✅ {len(cursos_creados)} cursos creados.")
    return cursos_creados

def crear_docentes(cantidad=10):
    """Crea docentes falsos."""
    print(f"\n👨‍🏫 Creando {cantidad} docentes...")
    docentes = []
    for i in range(cantidad):
        nombre, apellido = get_random_name()
        email = get_random_email(nombre, apellido)
        
        docente = Docente.objects.create(
            nombre=nombre,
            apellido=apellido,
            email=email,
            legajo=1000 + i,
            dni=random.randint(20000000, 45000000),
            telefono=f"11-{random.randint(1000,9999)}-{random.randint(1000,9999)}",
            nacionalidad="Argentina"
        )
        docentes.append(docente)
    
    print(f"✅ {len(docentes)} docentes creados.")
    return docentes

def crear_materias_y_asignar(cursos, docentes):
    """Crea materias para cada curso y asigna docentes."""
    print("\n📚 Creando materias y asignando docentes...")
    
    materias_nombres = [
        "Matemática", "Lengua", "Historia", "Geografía", "Inglés", 
        "Educación Física", "Biología", "Física", "Química", "Computación"
    ]
    
    total_materias = 0
    
    for curso in cursos:
        # Crear 5 materias aleatorias por curso
        materias_curso = random.sample(materias_nombres, 5)
        
        for nombre_materia in materias_curso:
            materia = Materia.objects.create(
                nombre=nombre_materia,
                curso=curso,
                horas=random.choice([2, 3, 4])
            )
            total_materias += 1
            
            # Asignar un docente aleatorio
            docente = random.choice(docentes)
            docente.materia.add(materia)
            
    print(f"✅ {total_materias} materias creadas y asignadas.")

def crear_alumnos(cursos, alumnos_por_curso=15):
    """Crea alumnos para cada curso."""
    print(f"\n👨‍🎓 Creando alumnos ({alumnos_por_curso} por curso)...")
    
    total_alumnos = 0
    for curso in cursos:
        for _ in range(alumnos_por_curso):
            nombre, apellido = get_random_name()
            
            Alumno.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=random.randint(40000000, 60000000),
                email=get_random_email(nombre, apellido),
                curso=curso,
                fecha_nacimiento=datetime(2005 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28))
            )
            total_alumnos += 1
            
    print(f"✅ {total_alumnos} alumnos creados.")

def main():
    print("="*60)
    print("GENERADOR DE DATOS DE PRUEBA - ALCAL")
    print("="*60)
    
    limpiar_datos()
    cursos = crear_estructura_base()
    docentes = crear_docentes(cantidad=15)
    crear_materias_y_asignar(cursos, docentes)
    crear_alumnos(cursos, alumnos_por_curso=10) # 10 alumnos por curso para no sobrecargar
    
    print("\n" + "="*60)
    print("✅ CARGA DE DATOS DE PRUEBA COMPLETADA")
    print("="*60)

if __name__ == '__main__':
    main()
