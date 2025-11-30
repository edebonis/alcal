from datetime import date
from escuela.models import Curso, Carrera, Anio
from alumnos.models import Alumno
from asistencias.models import Asistencia, Turno, CodigoAsistencia, CierreDiario, DetalleCierreCurso
from asistencias.services import ServicioCierreAsistencia

def test_logica_cierre():
    print("=== INICIANDO TEST DE LÓGICA DE CIERRE ===")
    
    # 1. Setup Datos Básicos
    anio, _ = Anio.objects.get_or_create(ciclo_lectivo=2025)
    carrera, _ = Carrera.objects.get_or_create(nombre="Test Carrera")
    curso, _ = Curso.objects.get_or_create(curso="1B", carrera=carrera) # Curso B para tener tarde
    
    alumno, _ = Alumno.objects.get_or_create(
        nombre="Test", apellido="Alumno", dni=123456,
        defaults={'curso': curso, 'grupo': 'unico'}
    )
    
    turno_m = Turno.objects.get(nombre='mañana')
    turno_t = Turno.objects.get(nombre='tarde')
    
    cod_a = CodigoAsistencia.objects.get(codigo='A')
    cod_p = CodigoAsistencia.objects.get(codigo='P')
    
    fecha = date(2025, 11, 22)
    
    # Limpiar datos previos
    Asistencia.objects.filter(fecha=fecha).delete()
    CierreDiario.objects.filter(fecha=fecha).delete()
    
    print("✅ Datos de prueba preparados")
    
    # 2. Cargar Asistencias
    # Caso: Ausente a la mañana, Presente a la tarde
    Asistencia.objects.create(
        alumno=alumno, fecha=fecha, turno=turno_m, codigo=cod_a, curso=curso, ciclo_lectivo=anio
    )
    Asistencia.objects.create(
        alumno=alumno, fecha=fecha, turno=turno_t, codigo=cod_p, curso=curso, ciclo_lectivo=anio
    )
    print("✅ Asistencias cargadas: Mañana=A, Tarde=P")
    
    # 3. Crear Cierre Diario
    user = User.objects.first() # Superusuario
    cierre = CierreDiario.objects.create(fecha=fecha, usuario_cierre=user)
    
    # Configurar que hubo Mañana y Tarde para este curso
    DetalleCierreCurso.objects.create(
        cierre=cierre, curso=curso, grupo='unico',
        hubo_turno_manana=True, hubo_turno_tarde=True, hubo_turno_ed_fisica=False
    )
    print("✅ Configuración de cierre creada (Hubo M y T)")
    
    # 4. Ejecutar Proceso
    print("🔄 Ejecutando ServicioCierreAsistencia...")
    ServicioCierreAsistencia.procesar_cierre(cierre)
    
    # 5. Verificar Resultado
    from asistencias.models import ResumenDiarioAlumno
    resumen = ResumenDiarioAlumno.objects.get(cierre_diario=cierre, alumno=alumno)
    
    print(f"\n=== RESULTADO DEL CÁLCULO ===")
    print(f"Códigos: M={resumen.codigo_manana} | T={resumen.codigo_tarde} | E={resumen.codigo_ed_fisica}")
    print(f"Valor Falta Final: {resumen.valor_falta_final}")
    print(f"Observación: {resumen.observacion_calculada}")
    
    # Verificación
    expected_val = 0.5 # Según CSV: A, P, - = 0.5
    if resumen.valor_falta_final == expected_val:
        print("\n✅ PRUEBA EXITOSA: El cálculo coincide con la regla esperada.")
    else:
        print(f"\n❌ PRUEBA FALLIDA: Se esperaba {expected_val} pero se obtuvo {resumen.valor_falta_final}")

from django.contrib.auth.models import User
if __name__ == '__main__':
    test_logica_cierre()
