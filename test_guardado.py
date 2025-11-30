from django.test import RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from datetime import date
from asistencias.views import tomar_asistencia_alumno
from asistencias.models import Asistencia, Turno, CodigoAsistencia
from alumnos.models import Alumno
from escuela.models import Curso, Carrera, Anio

def test_guardado():
    print("=== TEST DE GUARDADO DE ASISTENCIA ===")
    
    # 1. Setup
    anio, _ = Anio.objects.get_or_create(ciclo_lectivo=2025)
    carrera, _ = Carrera.objects.get_or_create(nombre="Test Carrera")
    curso, _ = Curso.objects.get_or_create(curso="1A", carrera=carrera)
    alumno, _ = Alumno.objects.get_or_create(
        nombre="Juan", apellido="Perez", dni=111222,
        defaults={'curso': curso}
    )
    
    turno, _ = Turno.objects.get_or_create(
        nombre='mañana', 
        defaults={'hora_inicio': '08:00', 'hora_fin': '12:00'}
    )
    codigo, _ = CodigoAsistencia.objects.get_or_create(
        codigo='P', defaults={'descripcion': 'Presente', 'cantidad_falta': 0}
    )
    
    # Limpiar asistencias previas
    Asistencia.objects.filter(alumno=alumno, fecha=date.today()).delete()
    
    # 2. Simular POST Request
    factory = RequestFactory()
    data = {
        'guardar_asistencia': 'true',
        'alumno_id': alumno.legajo,
        'turno_id': turno.id,
        'codigo': 'P',
        'fecha': date.today().strftime('%Y-%m-%d'),
        'observaciones': 'Test de guardado automático'
    }
    
    request = factory.post('/ing_asistencia_alumno/', data)
    
    # Agregar soporte de mensajes y usuario (requerido por la vista)
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    
    from django.contrib.auth.models import User
    request.user = User.objects.first() # Superusuario
    
    # 3. Ejecutar Vista
    print("🔄 Ejecutando vista tomar_asistencia_alumno...")
    tomar_asistencia_alumno(request)
    
    # 4. Verificar Base de Datos
    asistencia = Asistencia.objects.filter(
        alumno=alumno, 
        fecha=date.today(),
        turno=turno
    ).first()
    
    if asistencia:
        print(f"\n✅ ASISTENCIA GUARDADA EXITOSAMENTE")
        print(f"Alumno: {asistencia.alumno}")
        print(f"Turno: {asistencia.turno}")
        print(f"Código: {asistencia.codigo}")
        print(f"Observaciones: {asistencia.observaciones}")
        
        if asistencia.codigo.codigo == 'P' and asistencia.observaciones == 'Test de guardado automático':
            print("✅ Los datos coinciden perfectamente.")
        else:
            print("❌ Los datos no coinciden exactamente.")
    else:
        print("\n❌ ERROR: No se encontró el registro en la base de datos.")

if __name__ == '__main__':
    test_guardado()
