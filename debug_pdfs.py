import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
django.setup()

from alumnos.models import Alumno
from docentes.models import Docente
from alumnos.pdf_utils import generar_ficha_inscripcion, generar_constancia_alumno_regular
from docentes.pdf_utils import generar_ficha_docente

def test_pdfs():
    print("Iniciando prueba de PDFs...")
    
    # Obtener un alumno y un docente de prueba
    alumno = Alumno.objects.first()
    docente = Docente.objects.first()
    
    if not alumno:
        print("ERROR: No hay alumnos en la base de datos.")
        return
    if not docente:
        print("ERROR: No hay docentes en la base de datos.")
        return
        
    print(f"Probando con Alumno: {alumno} y Docente: {docente}")
    
    # 1. Ficha Inscripción Alumno
    try:
        print("Generando Ficha Inscripción Alumno...")
        resp = generar_ficha_inscripcion(alumno)
        if resp.status_code == 200:
            print("✅ Ficha Inscripción OK")
            with open("debug_ficha_inscripcion.pdf", "wb") as f:
                f.write(resp.content)
        else:
            print(f"❌ Ficha Inscripción falló con status {resp.status_code}")
    except Exception as e:
        print(f"❌ Ficha Inscripción EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()

    # 2. Constancia Alumno Regular
    try:
        print("Generando Constancia Alumno Regular...")
        resp = generar_constancia_alumno_regular(alumno)
        if resp.status_code == 200:
            print("✅ Constancia Alumno OK")
            with open("debug_constancia_alumno.pdf", "wb") as f:
                f.write(resp.content)
        else:
            print(f"❌ Constancia Alumno falló con status {resp.status_code}")
    except Exception as e:
        print(f"❌ Constancia Alumno EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()

    # 3. Ficha Docente
    try:
        print("Generando Ficha Docente...")
        resp = generar_ficha_docente(docente)
        if resp.status_code == 200:
            print("✅ Ficha Docente OK")
            with open("debug_ficha_docente.pdf", "wb") as f:
                f.write(resp.content)
        else:
            print(f"❌ Ficha Docente falló con status {resp.status_code}")
    except Exception as e:
        print(f"❌ Ficha Docente EXCEPCIÓN: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pdfs()
