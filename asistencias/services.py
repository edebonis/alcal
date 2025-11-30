from django.db import transaction
from alumnos.models import Alumno
from asistencias.models import Asistencia, ReglaAsistencia, ResumenDiarioAlumno, Turno

class ServicioCierreAsistencia:
    @staticmethod
    @transaction.atomic
    def procesar_cierre(cierre_diario):
        """
        Procesa el cierre diario calculando las faltas para todos los alumnos
        basándose en la configuración de turnos (DetalleCierreCurso) y las reglas.
        """
        detalles = cierre_diario.detalles.all()
        total_alumnos = 0
        total_asistencias = 0
        
        # Cachear reglas para evitar miles de queries
        # Diccionario clave: (manana, tarde, ed_fisica) -> (valor, observacion)
        reglas = {}
        for r in ReglaAsistencia.objects.all():
            reglas[(r.codigo_manana, r.codigo_tarde, r.codigo_ed_fisica)] = (r.valor_falta, r.observacion)
            
        # Cachear turnos para buscar IDs rápido
        turnos_map = {t.nombre: t.id for t in Turno.objects.all()}
        id_manana = turnos_map.get('mañana')
        id_tarde = turnos_map.get('tarde')
        id_ed_fisica = turnos_map.get('educacion_fisica')

        for detalle in detalles:
            # Obtener alumnos del curso y grupo
            alumnos = Alumno.objects.filter(curso=detalle.curso, activo=True)
            if detalle.grupo != 'unico':
                alumnos = alumnos.filter(grupo=detalle.grupo)
            
            for alumno in alumnos:
                total_alumnos += 1
                
                # Determinar códigos para cada turno
                cod_m = ServicioCierreAsistencia._obtener_codigo(
                    alumno, cierre_diario.fecha, id_manana, detalle.hubo_turno_manana
                )
                cod_t = ServicioCierreAsistencia._obtener_codigo(
                    alumno, cierre_diario.fecha, id_tarde, detalle.hubo_turno_tarde
                )
                cod_e = ServicioCierreAsistencia._obtener_codigo(
                    alumno, cierre_diario.fecha, id_ed_fisica, detalle.hubo_turno_ed_fisica
                )
                
                # Buscar regla
                clave = (cod_m, cod_t, cod_e)
                regla = reglas.get(clave)
                
                valor_final = 0.0
                observacion = "Combinación no encontrada en reglas"
                
                if regla:
                    valor_final, observacion = regla
                else:
                    # Fallback si no existe la combinación exacta (no debería pasar si el CSV es completo)
                    # Si no hay regla, sumamos valores individuales como fallback básico
                    pass 

                # Crear o actualizar resumen
                ResumenDiarioAlumno.objects.update_or_create(
                    cierre_diario=cierre_diario,
                    alumno=alumno,
                    fecha=cierre_diario.fecha,
                    defaults={
                        'codigo_manana': cod_m,
                        'codigo_tarde': cod_t,
                        'codigo_ed_fisica': cod_e,
                        'valor_falta_final': valor_final,
                        'observacion_calculada': observacion
                    }
                )
                
                # Marcar asistencias como procesadas
                Asistencia.objects.filter(
                    alumno=alumno, 
                    fecha=cierre_diario.fecha
                ).update(procesado=True, valor_falta_calculado=valor_final)

        # Actualizar estadísticas del cierre
        cierre_diario.total_alumnos_procesados = total_alumnos
        cierre_diario.save()
        
        return total_alumnos

    @staticmethod
    def _obtener_codigo(alumno, fecha, turno_id, hubo_turno):
        """
        Retorna el código de asistencia para un turno específico.
        Si no hubo turno -> '-'
        Si hubo turno y hay asistencia -> código registrado (P, A, T, R)
        Si hubo turno y NO hay asistencia -> 'P' (Presente por defecto)
        """
        if not hubo_turno:
            return '-'
            
        try:
            asistencia = Asistencia.objects.get(
                alumno=alumno,
                fecha=fecha,
                turno_id=turno_id
            )
            return asistencia.codigo.codigo
        except Asistencia.DoesNotExist:
            return 'P'  # Asumimos presente si no se cargó nada
