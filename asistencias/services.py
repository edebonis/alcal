from datetime import date
from django.db import transaction
from django.contrib.auth.models import User
from .models import (
    Asistencia,
    CierreDiario,
    ResumenDiarioAlumno,
)

class AsistenciaService:
    @staticmethod
    def calcular_valor_falta(
        codigo_mañana: str | None, 
        codigo_tarde: str | None, 
        codigo_ef: str | None, 
        tuvo_mañana: bool, 
        tuvo_tarde: bool, 
        tuvo_ef: bool
    ) -> float:
        """
        Calcula el valor de la falta basado en los códigos de asistencia y los turnos que tuvo el alumno.
        """
        # Mapeo básico de códigos a valores
        valores_base = {
            'P': 0.0,    # Presente
            't': 0.5,    # Tarde menos 15 min
            'T': 1.0,    # Tarde más 15 min  
            'A': 1.0,    # Ausente
            'r': 0.0,    # Retirado menos 15 min
            'R': 0.5,    # Retirado más 15 min
        }
        
        total_turnos = sum([tuvo_mañana, tuvo_tarde, tuvo_ef])
        if total_turnos == 0:
            return 0.0
        
        valor_total = 0.0
        
        # Aplicar valores según turnos
        if tuvo_mañana and codigo_mañana:
            if total_turnos == 1:
                # Solo mañana: valores completos
                valor_total += valores_base.get(codigo_mañana, 0.0)
            else:
                # Múltiples turnos: valores proporcionales
                valor_base = valores_base.get(codigo_mañana, 0.0)
                valor_total += valor_base / total_turnos
        
        if tuvo_tarde and codigo_tarde:
            if total_turnos == 1:
                # Solo tarde: valores completos
                valor_total += valores_base.get(codigo_tarde, 0.0)
            else:
                # Múltiples turnos: valores proporcionales
                valor_base = valores_base.get(codigo_tarde, 0.0)
                valor_total += valor_base / total_turnos
        
        if tuvo_ef and codigo_ef:
            if total_turnos == 1:
                # Solo educación física: valores completos
                valor_total += valores_base.get(codigo_ef, 0.0)
            else:
                # Múltiples turnos: valores proporcionales
                valor_base = valores_base.get(codigo_ef, 0.0)
                valor_total += valor_base / total_turnos
        
        return round(valor_total, 2)

    @staticmethod
    def procesar_cierre_fecha(fecha: date, usuario: User, observaciones: str = '') -> dict:
        """
        Procesa el cierre de una fecha específica.
        """
        try:
            with transaction.atomic():
                # Crear registro de cierre
                cierre = CierreDiario.objects.create(
                    fecha=fecha,
                    usuario_cierre=usuario,
                    observaciones_cierre=observaciones
                )
                
                # Obtener todas las asistencias de la fecha que no han sido procesadas
                asistencias = Asistencia.objects.filter(
                    fecha=fecha,
                    procesado=False
                ).select_related('alumno', 'turno', 'codigo')
                
                # Agrupar por alumno
                alumnos_asistencias = {}
                for asistencia in asistencias:
                    alumno_legajo = asistencia.alumno.legajo  # Usar legajo en lugar de id
                    if alumno_legajo not in alumnos_asistencias:
                        alumnos_asistencias[alumno_legajo] = {
                            'alumno': asistencia.alumno,
                            'turnos': {}
                        }
                    
                    turno_nombre = asistencia.turno.nombre
                    alumnos_asistencias[alumno_legajo]['turnos'][turno_nombre] = {
                        'codigo': asistencia.codigo.codigo,
                        'asistencia': asistencia
                    }
                
                alumnos_procesados = 0
                asistencias_procesadas = 0
                
                # Procesar cada alumno
                for alumno_legajo, data in alumnos_asistencias.items():
                    alumno = data['alumno']
                    turnos = data['turnos']
                    
                    # Determinar qué turnos tuvo clase
                    tuvo_mañana = 'mañana' in turnos
                    tuvo_tarde = 'tarde' in turnos
                    tuvo_educacion_fisica = 'educacion_fisica' in turnos
                    
                    # Obtener códigos
                    codigo_mañana = turnos.get('mañana', {}).get('codigo')
                    codigo_tarde = turnos.get('tarde', {}).get('codigo')
                    codigo_educacion_fisica = turnos.get('educacion_fisica', {}).get('codigo')
                    
                    # Calcular faltas
                    valor_falta_final = AsistenciaService.calcular_valor_falta(
                        codigo_mañana, codigo_tarde, codigo_educacion_fisica,
                        tuvo_mañana, tuvo_tarde, tuvo_educacion_fisica
                    )
                    
                    # Crear resumen diario
                    ResumenDiarioAlumno.objects.create(
                        cierre_diario=cierre,
                        alumno=alumno,
                        fecha=fecha,
                        codigo_mañana=codigo_mañana,
                        codigo_tarde=codigo_tarde,
                        codigo_educacion_fisica=codigo_educacion_fisica,
                        tuvo_mañana=tuvo_mañana,
                        tuvo_tarde=tuvo_tarde,
                        tuvo_educacion_fisica=tuvo_educacion_fisica,
                        valor_falta_final=valor_falta_final
                    )
                    
                    # Actualizar asistencias como procesadas y con valor calculado
                    for turno_data in turnos.values():
                        asistencia = turno_data['asistencia']
                        asistencia.procesado = True
                        asistencia.valor_falta_calculado = valor_falta_final
                        asistencia.save()
                        asistencias_procesadas += 1
                    
                    alumnos_procesados += 1
                
                # Actualizar estadísticas del cierre
                cierre.total_alumnos_procesados = alumnos_procesados
                cierre.total_asistencias_procesadas = asistencias_procesadas
                cierre.total_cursos_procesados = asistencias.values('curso').distinct().count()
                cierre.save()
                
                return {
                    'success': True,
                    'alumnos_procesados': alumnos_procesados,
                    'asistencias_procesadas': asistencias_procesadas
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
