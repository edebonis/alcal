#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Script de prueba para el sistema de cierre diario de asistencias
"""

import os
import sys
from datetime import date, timedelta

import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alcal.settings')
django.setup()

from django.contrib.auth.models import Group, User

from alumnos.models import Alumno
from asistencias.models import (
    Asistencia,
    CierreDiario,
    CodigoAsistencia,
    ResumenDiarioAlumno,
    Turno,
)
from asistencias.services import AsistenciaService
from escuela.models import Anio, Curso


def crear_datos_prueba():
    """Crear datos de prueba para el cierre diario"""
    print("🔧 Creando datos de prueba...")
    
    # Obtener datos existentes
    anio_actual = Anio.objects.first()  # Tomar el primer año disponible
    if not anio_actual:
        # Crear año actual si no existe
        anio_actual = Anio.objects.create(ciclo_lectivo=2025)
        print(f"✅ Creado año lectivo: {anio_actual.ciclo_lectivo}")
    
    curso = Curso.objects.first()
    if not curso:
        print("❌ No hay cursos disponibles")
        return False
    
    alumnos = Alumno.objects.filter(curso=curso)[:5]  # Tomar 5 alumnos
    if not alumnos:
        print("❌ No hay alumnos en el curso")
        return False
    
    turnos = Turno.objects.all()
    codigos = CodigoAsistencia.objects.all()
    
    if not turnos or not codigos:
        print("❌ No hay turnos o códigos configurados")
        return False
    
    # Fecha de prueba (ayer)
    fecha_prueba = date.today() - timedelta(days=1)
    
    print(f"📅 Fecha de prueba: {fecha_prueba}")
    print(f"🎓 Curso: {curso}")
    print(f"👥 Alumnos: {len(alumnos)}")
    
    # Crear asistencias de prueba
    asistencias_creadas = 0
    
    for i, alumno in enumerate(alumnos):
        # Simular diferentes combinaciones de turnos
        if i == 0:
            # Solo mañana - Presente
            turno_mañana = turnos.filter(nombre='mañana').first()
            if turno_mañana:
                Asistencia.objects.get_or_create(
                    alumno=alumno,
                    fecha=fecha_prueba,
                    turno=turno_mañana,
                    ciclo_lectivo=anio_actual,
                    defaults={
                        'curso': curso,
                        'codigo': codigos.get(codigo='P'),
                        'observaciones': 'Prueba - Solo mañana presente'
                    }
                )
                asistencias_creadas += 1
            
        elif i == 1:
            # Solo tarde - Tarde más de 15 min
            turno_tarde = turnos.filter(nombre='tarde').first()
            if turno_tarde:
                Asistencia.objects.get_or_create(
                    alumno=alumno,
                    fecha=fecha_prueba,
                    turno=turno_tarde,
                    ciclo_lectivo=anio_actual,
                    defaults={
                        'curso': curso,
                        'codigo': codigos.get(codigo='T'),
                        'observaciones': 'Prueba - Solo tarde con retraso'
                    }
                )
                asistencias_creadas += 1
            
        elif i == 2:
            # Mañana y tarde - Presente en ambos
            for turno_nombre in ['mañana', 'tarde']:
                turno = turnos.filter(nombre=turno_nombre).first()
                if turno:
                    Asistencia.objects.get_or_create(
                        alumno=alumno,
                        fecha=fecha_prueba,
                        turno=turno,
                        ciclo_lectivo=anio_actual,
                        defaults={
                            'curso': curso,
                            'codigo': codigos.get(codigo='P'),
                            'observaciones': f'Prueba - {turno_nombre} presente'
                        }
                    )
                    asistencias_creadas += 1
                
        elif i == 3:
            # Mañana presente, tarde ausente
            turno_mañana = turnos.filter(nombre='mañana').first()
            turno_tarde = turnos.filter(nombre='tarde').first()
            
            if turno_mañana:
                Asistencia.objects.get_or_create(
                    alumno=alumno,
                    fecha=fecha_prueba,
                    turno=turno_mañana,
                    ciclo_lectivo=anio_actual,
                    defaults={
                        'curso': curso,
                        'codigo': codigos.get(codigo='P'),
                        'observaciones': 'Prueba - Mañana presente'
                    }
                )
                asistencias_creadas += 1
                
            if turno_tarde:
                Asistencia.objects.get_or_create(
                    alumno=alumno,
                    fecha=fecha_prueba,
                    turno=turno_tarde,
                    ciclo_lectivo=anio_actual,
                    defaults={
                        'curso': curso,
                        'codigo': codigos.get(codigo='A'),
                        'observaciones': 'Prueba - Tarde ausente'
                    }
                )
                asistencias_creadas += 1
            
        elif i == 4:
            # Solo educación física - Retirado
            turno_ef = turnos.filter(nombre='educacion_fisica').first()
            if turno_ef:
                Asistencia.objects.get_or_create(
                    alumno=alumno,
                    fecha=fecha_prueba,
                    turno=turno_ef,
                    ciclo_lectivo=anio_actual,
                    defaults={
                        'curso': curso,
                        'codigo': codigos.get(codigo='R'),
                        'observaciones': 'Prueba - Ed. Física retirado'
                    }
                )
                asistencias_creadas += 1
    
    print(f"✅ Creadas {asistencias_creadas} asistencias de prueba")
    return fecha_prueba


def probar_cierre_diario():
    """Probar el proceso de cierre diario"""
    print("\n🧪 INICIANDO PRUEBA DEL CIERRE DIARIO")
    print("=" * 50)
    
    # Crear datos de prueba
    fecha_prueba = crear_datos_prueba()
    if not fecha_prueba:
        return
    
    # Verificar que no esté ya cerrada
    if CierreDiario.objects.filter(fecha=fecha_prueba).exists():
        print(f"⚠️  La fecha {fecha_prueba} ya está cerrada. Eliminando cierre anterior...")
        CierreDiario.objects.filter(fecha=fecha_prueba).delete()
        ResumenDiarioAlumno.objects.filter(fecha=fecha_prueba).delete()
        # Marcar asistencias como no procesadas
        Asistencia.objects.filter(fecha=fecha_prueba).update(procesado=False, valor_falta_calculado=None)
    
    # Obtener usuario para el cierre
    usuario = User.objects.filter(is_superuser=True).first()
    if not usuario:
        print("❌ No hay usuario administrador disponible")
        return
    
    # Mostrar estado antes del cierre
    print(f"\n📊 ESTADO ANTES DEL CIERRE ({fecha_prueba}):")
    asistencias_pendientes = Asistencia.objects.filter(fecha=fecha_prueba, procesado=False)
    print(f"   • Asistencias pendientes: {asistencias_pendientes.count()}")
    
    for asistencia in asistencias_pendientes:
        print(f"     - {asistencia.alumno.apellido}, {asistencia.alumno.nombre}: "
              f"{asistencia.turno.get_nombre_display()} = {asistencia.codigo.codigo}")
    
    # Procesar cierre
    print(f"\n🔄 PROCESANDO CIERRE...")
    resultado = AsistenciaService.procesar_cierre_fecha(fecha_prueba, usuario, "Prueba automática del sistema")
    
    if resultado['success']:
        print(f"✅ CIERRE EXITOSO!")
        print(f"   • Alumnos procesados: {resultado['alumnos_procesados']}")
        print(f"   • Asistencias procesadas: {resultado['asistencias_procesadas']}")
        
        # Mostrar resultados
        print(f"\n📈 RESULTADOS DEL CIERRE:")
        resumenes = ResumenDiarioAlumno.objects.filter(fecha=fecha_prueba).order_by('alumno__apellido')
        
        for resumen in resumenes:
            turnos_info = []
            if resumen.tuvo_mañana:
                turnos_info.append(f"M:{resumen.codigo_mañana}")
            if resumen.tuvo_tarde:
                turnos_info.append(f"T:{resumen.codigo_tarde}")
            if resumen.tuvo_educacion_fisica:
                turnos_info.append(f"EF:{resumen.codigo_educacion_fisica}")
            
            print(f"   • {resumen.alumno.apellido}, {resumen.alumno.nombre}:")
            print(f"     Turnos: {' | '.join(turnos_info) if turnos_info else 'Ninguno'}")
            print(f"     Valor falta final: {resumen.valor_falta_final}")
        
        # Verificar que las asistencias estén marcadas como procesadas
        asistencias_procesadas = Asistencia.objects.filter(fecha=fecha_prueba, procesado=True)
        print(f"\n✅ Asistencias marcadas como procesadas: {asistencias_procesadas.count()}")
        
    else:
        print(f"❌ ERROR EN EL CIERRE: {resultado['error']}")


def limpiar_datos_prueba():
    """Limpiar datos de prueba"""
    fecha_prueba = date.today() - timedelta(days=1)
    
    print(f"\n🧹 LIMPIANDO DATOS DE PRUEBA ({fecha_prueba})...")
    
    # Eliminar cierres
    cierres_eliminados = CierreDiario.objects.filter(fecha=fecha_prueba).count()
    CierreDiario.objects.filter(fecha=fecha_prueba).delete()
    
    # Eliminar resúmenes
    resumenes_eliminados = ResumenDiarioAlumno.objects.filter(fecha=fecha_prueba).count()
    ResumenDiarioAlumno.objects.filter(fecha=fecha_prueba).delete()
    
    # Eliminar asistencias de prueba
    asistencias_eliminadas = Asistencia.objects.filter(
        fecha=fecha_prueba,
        observaciones__icontains='Prueba'
    ).count()
    Asistencia.objects.filter(
        fecha=fecha_prueba,
        observaciones__icontains='Prueba'
    ).delete()
    
    print(f"   • Cierres eliminados: {cierres_eliminados}")
    print(f"   • Resúmenes eliminados: {resumenes_eliminados}")
    print(f"   • Asistencias eliminadas: {asistencias_eliminadas}")
    print("✅ Limpieza completada")


if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'limpiar':
            limpiar_datos_prueba()
        else:
            probar_cierre_diario()
            
            # Preguntar si limpiar
            respuesta = input("\n¿Desea limpiar los datos de prueba? (s/N): ")
            if respuesta.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                limpiar_datos_prueba()
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {str(e)}")
        import traceback
        traceback.print_exc() 