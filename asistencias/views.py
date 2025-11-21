from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from alumnos.models import Alumno
from escuela.models import Anio, Curso

from .models import (
    Asistencia,
    CierreDiario,
    CodigoAsistencia,
    ResumenDiarioAlumno,
    Turno,
)
from .services import AsistenciaService


@login_required
def tomar_asistencia_curso(request):
    """Vista principal para seleccionar curso, turno y fecha"""
    cursos = Curso.objects.all().order_by('curso')
    turnos = Turno.objects.all().order_by('hora_inicio')
    anio_actual = Anio.objects.first()  # Tomar el primer año disponible
    
    context = {
        'cursos': cursos,
        'turnos': turnos,
        'anio_actual': anio_actual,
        'fecha_hoy': date.today().strftime('%Y-%m-%d'),
    }
    return render(request, 'asistencias/tomar_asistencia_curso.html', context)


@login_required
def lista_alumnos_curso(request):
    """Vista para mostrar la lista de alumnos y tomar asistencia"""
    curso_id = request.GET.get('curso')
    turno_id = request.GET.get('turno')
    fecha_str = request.GET.get('fecha')
    
    if not all([curso_id, turno_id, fecha_str]):
        messages.error(request, 'Debe seleccionar curso, turno y fecha.')
        return redirect('tomar_asistencia_curso')
    
    try:
        curso = get_object_or_404(Curso, id=curso_id)
        turno = get_object_or_404(Turno, id=turno_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        anio_actual = Anio.objects.first()
        
        # Obtener alumnos del curso
        alumnos = Alumno.objects.filter(curso=curso).order_by('apellido', 'nombre')
        
        # Obtener códigos de asistencia
        codigos = CodigoAsistencia.objects.all().order_by('codigo')
        
        # Obtener asistencias existentes para esta fecha, curso y turno
        asistencias_existentes = {}
        asistencias = Asistencia.objects.filter(
            curso=curso,
            turno=turno,
            fecha=fecha,
            ciclo_lectivo=anio_actual
        ).select_related('alumno', 'codigo')
        
        for asistencia in asistencias:
            asistencias_existentes[asistencia.alumno.legajo] = {
                'codigo': asistencia.codigo.codigo,
                'observaciones': asistencia.observaciones or ''
            }
        
        context = {
            'curso': curso,
            'turno': turno,
            'fecha': fecha,
            'fecha_str': fecha_str,
            'alumnos': alumnos,
            'codigos': codigos,
            'asistencias_existentes': asistencias_existentes,
            'anio_actual': anio_actual,
        }
        return render(request, 'asistencias/lista_alumnos_curso.html', context)
        
    except ValueError:
        messages.error(request, 'Formato de fecha inválido.')
        return redirect('tomar_asistencia_curso')


@login_required
def guardar_asistencia_curso(request):
    """Vista para procesar y guardar las asistencias"""
    if request.method != 'POST':
        return redirect('tomar_asistencia_curso')
    
    curso_id = request.POST.get('curso_id')
    turno_id = request.POST.get('turno_id')
    fecha_str = request.POST.get('fecha')
    
    try:
        curso = get_object_or_404(Curso, id=curso_id)
        turno = get_object_or_404(Turno, id=turno_id)
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        anio_actual = Anio.objects.first()
        
        alumnos_procesados = 0
        asistencias_creadas = 0
        asistencias_actualizadas = 0
        
        with transaction.atomic():
            # Procesar cada alumno
            for key, value in request.POST.items():
                if key.startswith('codigo_'):
                    alumno_legajo = key.replace('codigo_', '')
                    codigo_asistencia = value
                    observaciones = request.POST.get(f'observaciones_{alumno_legajo}', '')
                    
                    if codigo_asistencia:  # Solo procesar si se seleccionó un código
                        try:
                            alumno = Alumno.objects.get(legajo=alumno_legajo, curso=curso)
                            codigo = CodigoAsistencia.objects.get(codigo=codigo_asistencia)
                            
                            # Buscar si ya existe una asistencia para este alumno, fecha y turno
                            asistencia, created = Asistencia.objects.get_or_create(
                                alumno=alumno,
                                fecha=fecha,
                                turno=turno,
                                ciclo_lectivo=anio_actual,
                                defaults={
                                    'curso': curso,
                                    'codigo': codigo,
                                    'observaciones': observaciones,
                                }
                            )
                            
                            if not created:
                                # Actualizar asistencia existente
                                asistencia.codigo = codigo
                                asistencia.observaciones = observaciones
                                asistencia.save()
                                asistencias_actualizadas += 1
                            else:
                                asistencias_creadas += 1
                            
                            alumnos_procesados += 1
                            
                        except (Alumno.DoesNotExist, CodigoAsistencia.DoesNotExist):
                            continue
        
        # Mensaje de éxito
        mensaje = f'Asistencia guardada exitosamente. '
        mensaje += f'Alumnos procesados: {alumnos_procesados}, '
        mensaje += f'Nuevas: {asistencias_creadas}, '
        mensaje += f'Actualizadas: {asistencias_actualizadas}'
        
        messages.success(request, mensaje)
        
        # Redirigir de vuelta a la lista con los mismos parámetros
        return redirect(f'/lista_alumnos_curso/?curso={curso_id}&turno={turno_id}&fecha={fecha_str}')
        
    except Exception as e:
        messages.error(request, f'Error al guardar asistencia: {str(e)}')
        return redirect('tomar_asistencia_curso')


@login_required
def consultar_asistencia_curso(request):
    """Vista para consultar asistencias con filtros"""
    cursos = Curso.objects.all().order_by('curso')
    turnos = Turno.objects.all().order_by('hora_inicio')
    
    # Filtros
    curso_id = request.GET.get('curso')
    turno_id = request.GET.get('turno')
    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    
    asistencias = None
    estadisticas = None
    
    if curso_id:  # Curso es obligatorio
        try:
            curso = get_object_or_404(Curso, id=curso_id)
            
            # Construir query
            query = Q(curso=curso)
            
            if turno_id:
                query &= Q(turno_id=turno_id)
            
            if fecha_desde:
                fecha_desde_obj = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
                query &= Q(fecha__gte=fecha_desde_obj)
            
            if fecha_hasta:
                fecha_hasta_obj = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
                query &= Q(fecha__lte=fecha_hasta_obj)
            
            # Obtener asistencias
            asistencias = Asistencia.objects.filter(query).select_related(
                'alumno', 'codigo', 'turno'
            ).order_by('-fecha', 'turno__hora_inicio', 'alumno__apellido', 'alumno__nombre')
            
            # Calcular estadísticas
            total_registros = asistencias.count()
            estadisticas_codigos = asistencias.values('codigo__codigo', 'codigo__descripcion').annotate(
                cantidad=Count('id')
            ).order_by('codigo__codigo')
            
            estadisticas = {
                'total_registros': total_registros,
                'por_codigo': list(estadisticas_codigos),
            }
            
        except ValueError:
            messages.error(request, 'Formato de fecha inválido.')
    
    context = {
        'cursos': cursos,
        'turnos': turnos,
        'asistencias': asistencias,
        'estadisticas': estadisticas,
        'filtros': {
            'curso_id': curso_id,
            'turno_id': turno_id,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
    }
    
    return render(request, 'asistencias/consultar_asistencia_curso.html', context)


@login_required
def cierre_diario_seleccion(request):
    """Vista para seleccionar la fecha a cerrar"""
    # Verificar permisos (debe ser preceptor o superior)
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['preceptor', 'director', 'admin']).exists()):
        messages.error(request, 'No tiene permisos para realizar el cierre diario.')
        return redirect('/')
    
    # Obtener fechas que pueden ser cerradas (días anteriores que no han sido cerrados)
    fechas_cerradas = CierreDiario.objects.values_list('fecha', flat=True)
    
    # Sugerir el día anterior como fecha a cerrar
    fecha_sugerida = date.today() - timedelta(days=1)
    
    # Obtener estadísticas de la fecha sugerida
    estadisticas_fecha = None
    if fecha_sugerida not in fechas_cerradas:
        asistencias_pendientes = Asistencia.objects.filter(
            fecha=fecha_sugerida,
            procesado=False
        ).count()
        
        total_alumnos = Asistencia.objects.filter(
            fecha=fecha_sugerida
        ).values('alumno').distinct().count()
        
        total_cursos = Asistencia.objects.filter(
            fecha=fecha_sugerida
        ).values('curso').distinct().count()
        
        estadisticas_fecha = {
            'fecha': fecha_sugerida,
            'asistencias_pendientes': asistencias_pendientes,
            'total_alumnos': total_alumnos,
            'total_cursos': total_cursos,
            'puede_cerrar': asistencias_pendientes > 0
        }
    
    context = {
        'fecha_sugerida': fecha_sugerida,
        'fechas_cerradas': list(fechas_cerradas),
        'estadisticas_fecha': estadisticas_fecha,
    }
    
    return render(request, 'asistencias/cierre_diario_seleccion.html', context)


@login_required
def procesar_cierre_diario(request):
    """Vista para procesar el cierre diario"""
    if request.method != 'POST':
        return redirect('cierre_diario_seleccion')
    
    # Verificar permisos
    if not (request.user.is_superuser or 
            request.user.groups.filter(name__in=['preceptor', 'director', 'admin']).exists()):
        messages.error(request, 'No tiene permisos para realizar el cierre diario.')
        return redirect('/')
    
    fecha_str = request.POST.get('fecha')
    observaciones = request.POST.get('observaciones', '')
    
    try:
        fecha_cierre = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        
        # Verificar que no esté ya cerrada
        if CierreDiario.objects.filter(fecha=fecha_cierre).exists():
            messages.error(request, f'La fecha {fecha_cierre} ya ha sido cerrada.')
            return redirect('cierre_diario_seleccion')
        
        # Procesar cierre
        resultado = AsistenciaService.procesar_cierre_fecha(fecha_cierre, request.user, observaciones)
        
        if resultado['success']:
            messages.success(request, 
                f'Cierre procesado exitosamente. '
                f'Alumnos: {resultado["alumnos_procesados"]}, '
                f'Asistencias: {resultado["asistencias_procesadas"]}'
            )
        else:
            messages.error(request, f'Error en el cierre: {resultado["error"]}')
            
    except ValueError:
        messages.error(request, 'Formato de fecha inválido.')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')
    
    return redirect('cierre_diario_seleccion')


