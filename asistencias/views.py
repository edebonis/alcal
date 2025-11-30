from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction, models
from datetime import date
from django.http import JsonResponse, HttpResponse

from escuela.models import Curso, Anio
from alumnos.models import Alumno
from .models import Asistencia, Turno, CodigoAsistencia, CierreDiario, DetalleCierreCurso
from .forms import CierreDiarioForm
from .services import ServicioCierreAsistencia

# --- VISTAS DE TOMA DE ASISTENCIA ---

@login_required
def ingresar_asistencia_selector(request):
    """Vista principal para seleccionar el modo de ingreso de asistencia"""
    return render(request, 'asistencias/ingresar_asistencia_selector.html')

@login_required
def tomar_asistencia_curso(request):
    """Vista para seleccionar curso y fecha para tomar asistencia masiva"""
    cursos = Curso.objects.all().order_by('curso')
    turnos = Turno.objects.all()
    return render(request, 'asistencias/tomar_asistencia_curso.html', {
        'cursos': cursos,
        'turnos': turnos,
        'hoy': date.today()
    })

@login_required
def tomar_asistencia_alumno(request):
    """Vista para buscar un alumno y cargarle asistencia individualmente"""
    turnos = Turno.objects.all()
    codigos = CodigoAsistencia.objects.all().order_by('codigo')
    
    alumno = None
    asistencias_hoy = []
    
    if request.method == 'POST':
        # Si es búsqueda de alumno
        if 'buscar_alumno' in request.POST:
            query = request.POST.get('query')
            alumnos = Alumno.objects.filter(
                activo=True
            ).filter(
                models.Q(apellido__icontains=query) | 
                models.Q(nombre__icontains=query) | 
                models.Q(dni__icontains=query)
            )[:10] # Limitar resultados
            
            return render(request, 'asistencias/tomar_asistencia_alumno.html', {
                'alumnos_encontrados': alumnos,
                'query': query,
                'turnos': turnos
            })
            
        # Si es selección de alumno
        elif 'seleccionar_alumno' in request.POST:
            alumno_id = request.POST.get('alumno_id')
            alumno = get_object_or_404(Alumno, pk=alumno_id)
            
            # Buscar asistencias de hoy para este alumno
            asistencias_hoy = Asistencia.objects.filter(
                alumno=alumno,
                fecha=date.today()
            )
            
        # Si es guardado de asistencia
        elif 'guardar_asistencia' in request.POST:
            alumno_id = request.POST.get('alumno_id')
            turno_id = request.POST.get('turno_id')
            codigo_str = request.POST.get('codigo')
            fecha = request.POST.get('fecha', date.today())
            observaciones = request.POST.get('observaciones', '')
            
            try:
                alumno = Alumno.objects.get(pk=alumno_id)
                turno = Turno.objects.get(pk=turno_id)
                codigo = CodigoAsistencia.objects.get(codigo=codigo_str)
                ciclo = Anio.objects.last()
                
                Asistencia.objects.update_or_create(
                    alumno=alumno,
                    fecha=fecha,
                    turno=turno,
                    defaults={
                        'curso': alumno.curso,
                        'codigo': codigo,
                        'ciclo_lectivo': ciclo,
                        'observaciones': observaciones
                    }
                )
                messages.success(request, f'Asistencia guardada para {alumno}')
                # Recargar datos del alumno para mostrar actualizado
                asistencias_hoy = Asistencia.objects.filter(alumno=alumno, fecha=fecha)
                
            except Exception as e:
                messages.error(request, f'Error al guardar: {str(e)}')
                
    return render(request, 'asistencias/tomar_asistencia_alumno.html', {
        'alumno': alumno,
        'turnos': turnos,
        'codigos': codigos,
        'asistencias_hoy': asistencias_hoy,
        'hoy': date.today()
    })

@login_required
def lista_alumnos_curso(request):
    """Devuelve la lista de alumnos para tomar asistencia.
    Ahora acepta uno o varios turnos (separados por coma en el parámetro GET).
    """
    curso_id = request.GET.get('curso_id')
    
    # Validar que curso_id esté presente
    if not curso_id:
        return HttpResponse(
            '<div class="alert alert-warning d-flex align-items-center">'
            '<i class="bi bi-exclamation-triangle-fill me-2"></i>'
            'Debe seleccionar un curso para cargar la lista de alumnos.'
            '</div>',
            status=400
        )
    
    fecha = request.GET.get('fecha', date.today())
    # Obtener turnos, pueden venir como lista o cadena separada por comas
    turno_ids_param = request.GET.get('turno_id')
    turno_ids = []
    if turno_ids_param:
        # Si viene como "1,2" o "1"
        turno_ids = [int(t) for t in turno_ids_param.split(',') if t.isdigit()]
    
    curso = get_object_or_404(Curso, pk=curso_id)
    alumnos = Alumno.objects.filter(curso=curso, activo=True).order_by('apellido', 'nombre')
    codigos = CodigoAsistencia.objects.all().order_by('codigo')
    turnos = Turno.objects.filter(id__in=turno_ids) if turno_ids else []

    # Buscar asistencias existentes para los turnos indicados
    asistencias_existentes = {}
    if turno_ids:
        asistencias = Asistencia.objects.filter(
            curso=curso,
            fecha=fecha,
            turno_id__in=turno_ids
        )
        for a in asistencias:
            # Guardamos por alumno_id: {codigo, observaciones}
            asistencias_existentes[a.alumno_id] = {
                'codigo': a.codigo.codigo,
                'observaciones': a.observaciones or ''
            }

    # Pasar turnos como cadena para el template (para que el hidden input mantenga valor)
    turno_id_str = ','.join(map(str, turno_ids))
    return render(request, 'asistencias/lista_alumnos_curso.html', {
        'curso': curso,
        'alumnos': alumnos,
        'codigos': codigos,
        'fecha': fecha,
        'turno_id': turno_id_str,
        'turnos': turnos,
        'asistencias_existentes': asistencias_existentes
    })

@login_required
def guardar_asistencia_curso(request):
    """Guarda la asistencia enviada desde el formulario.
    Soporta múltiples turnos y observaciones por alumno.
    """
    if request.method == 'POST':
        try:
            curso_id = request.POST.get('curso_id')
            fecha = request.POST.get('fecha')
            turno_ids_str = request.POST.get('turno_id', '')
            
            # Parsear los IDs de turnos (pueden ser múltiples separados por coma)
            turno_ids = [int(t) for t in turno_ids_str.split(',') if t.strip().isdigit()]
            
            if not turno_ids:
                messages.error(request, 'Debe seleccionar al menos un turno')
                return redirect('tomar_asistencia_curso')
            
            curso = get_object_or_404(Curso, pk=curso_id)
            turnos = Turno.objects.filter(id__in=turno_ids)
            ciclo = Anio.objects.last()  # Asumimos el último año lectivo
            
            asistencias_guardadas = 0
            
            with transaction.atomic():
                # Iterar sobre los datos del POST
                for key, value in request.POST.items():
                    if key.startswith('codigo_'):
                        alumno_id = key.split('_')[1]
                        codigo_str = value
                        
                        # Buscar observaciones para este alumno
                        obs_key = f'observaciones_{alumno_id}'
                        observaciones = request.POST.get(obs_key, '').strip()
                        
                        alumno = Alumno.objects.get(pk=alumno_id)
                        codigo = CodigoAsistencia.objects.get(codigo=codigo_str)
                        
                        # Crear o actualizar asistencia para CADA turno seleccionado
                        for turno in turnos:
                            Asistencia.objects.update_or_create(
                                alumno=alumno,
                                fecha=fecha,
                                turno=turno,
                                defaults={
                                    'curso': curso,
                                    'codigo': codigo,
                                    'ciclo_lectivo': ciclo,
                                    'observaciones': observaciones
                                }
                            )
                            asistencias_guardadas += 1
            
            turnos_nombres = ', '.join([t.get_nombre_display() for t in turnos])
            messages.success(
                request, 
                f'Asistencia guardada correctamente ({asistencias_guardadas} registros para turnos: {turnos_nombres})'
            )
            return redirect('tomar_asistencia_curso')
            
        except Exception as e:
            messages.error(request, f'Error al guardar: {str(e)}')
            return redirect('tomar_asistencia_curso')
            
    return redirect('tomar_asistencia_curso')

@login_required
def consultar_asistencia_curso(request):
    """Vista para consultar asistencias"""
    cursos = Curso.objects.all()
    return render(request, 'asistencias/consultar_asistencia_curso.html', {'cursos': cursos})


# --- VISTAS DE CIERRE DIARIO (Nuevas) ---

@login_required
def cierre_asistencia(request):
    fecha_param = request.GET.get('fecha')
    fecha_inicial = date.fromisoformat(fecha_param) if fecha_param else date.today()
    
    cierre_existente = CierreDiario.objects.filter(fecha=fecha_inicial).first()
    
    if request.method == 'POST':
        form = CierreDiarioForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            
            try:
                with transaction.atomic():
                    # 1. Crear o Actualizar CierreDiario
                    cierre, created = CierreDiario.objects.update_or_create(
                        fecha=fecha,
                        defaults={
                            'usuario_cierre': request.user,
                            'observaciones_cierre': form.cleaned_data['observaciones_cierre']
                        }
                    )
                    
                    # 2. Procesar cursos seleccionados
                    cursos = Curso.objects.all()
                    grupos_posibles = ['unico', '1', '2']
                    cursos_procesados_count = 0
                    
                    for curso in cursos:
                        for grupo in grupos_posibles:
                            prefix = f"c_{curso.id}_g_{grupo}"
                            
                            # Verificar si hay alumnos (para no procesar cursos vacíos innecesariamente)
                            if not Alumno.objects.filter(curso=curso, grupo=grupo, activo=True).exists():
                                continue

                            # Verificar si se marcó para procesar
                            procesar = request.POST.get(f"{prefix}_procesar") == 'on'
                            
                            if procesar:
                                hubo_manana = request.POST.get(f"{prefix}_m") == 'on'
                                hubo_tarde = request.POST.get(f"{prefix}_t") == 'on'
                                hubo_ed_fisica = request.POST.get(f"{prefix}_e") == 'on'
                                
                                DetalleCierreCurso.objects.update_or_create(
                                    cierre=cierre,
                                    curso=curso,
                                    grupo=grupo,
                                    defaults={
                                        'hubo_turno_manana': hubo_manana,
                                        'hubo_turno_tarde': hubo_tarde,
                                        'hubo_turno_ed_fisica': hubo_ed_fisica
                                    }
                                )
                                cursos_procesados_count += 1
                    
                    # 3. Ejecutar el cálculo
                    if cursos_procesados_count > 0:
                        total = ServicioCierreAsistencia.procesar_cierre(cierre)
                        msg = f'Cierre {"creado" if created else "actualizado"} con éxito. Se procesaron registros.'
                        messages.success(request, msg)
                    else:
                        messages.warning(request, 'Se guardó la cabecera del cierre pero no se seleccionaron cursos para procesar.')
                        
                    return redirect('administracion:dashboard')
                    
            except Exception as e:
                messages.error(request, f'Error al realizar el cierre: {str(e)}')
                # No redirigir, permitir corregir
    
    else:
        # GET: Cargar formulario con datos existentes si hay
        initial_data = {'fecha': fecha_inicial}
        if cierre_existente:
            initial_data['observaciones_cierre'] = cierre_existente.observaciones_cierre
            messages.info(request, f'Visualizando cierre existente del {fecha_inicial.strftime("%d/%m/%Y")}. Al guardar se actualizarán los datos.')
            
        form = CierreDiarioForm(initial=initial_data)

    # Preparar datos para la grilla
    cursos_data = []
    cursos = Curso.objects.all().order_by('curso')
    
    # Mapa de detalles existentes para pre-llenar
    detalles_map = {}
    if cierre_existente:
        for det in cierre_existente.detalle_cursos.all():
            key = f"{det.curso.id}_{det.grupo}"
            detalles_map[key] = det
    
    for curso in cursos:
        tiene_grupo_1 = Alumno.objects.filter(curso=curso, grupo='1', activo=True).exists()
        tiene_grupo_2 = Alumno.objects.filter(curso=curso, grupo='2', activo=True).exists()
        
        es_curso_b = 'B' in curso.curso.upper()
        
        grupos_a_mostrar = []
        if tiene_grupo_1 or tiene_grupo_2:
            if tiene_grupo_1: grupos_a_mostrar.append(('1', 'Grupo 1'))
            if tiene_grupo_2: grupos_a_mostrar.append(('2', 'Grupo 2'))
        else:
            grupos_a_mostrar.append(('unico', 'Único'))
            
        for grp_cod, grp_name in grupos_a_mostrar:
            prefix = f"c_{curso.id}_g_{grp_cod}"
            key = f"{curso.id}_{grp_cod}"
            
            detalle = detalles_map.get(key)
            
            # Valores por defecto
            checked_procesar = detalle is not None # Si existe detalle, marcar procesar por defecto
            checked_m = detalle.hubo_turno_manana if detalle else True
            checked_t = detalle.hubo_turno_tarde if detalle else es_curso_b
            checked_e = detalle.hubo_turno_ed_fisica if detalle else False
            
            # Si es un cierre nuevo (no existente), marcar todos para procesar por defecto
            if not cierre_existente:
                checked_procesar = True

            cursos_data.append({
                'curso': curso,
                'grupo': grp_cod,
                'grupo_display': grp_name,
                'prefix': prefix,
                'checked_procesar': checked_procesar,
                'checked_m': checked_m,
                'checked_t': checked_t,
                'checked_e': checked_e
            })

    return render(request, 'asistencias/cierre_form.html', {
        'form': form,
        'cursos_data': cursos_data,
        'cierre_existente': cierre_existente,
        'fecha_seleccionada': fecha_inicial.isoformat()
    })

# Alias para compatibilidad con urls.py
cierre_diario_seleccion = cierre_asistencia
procesar_cierre_diario = cierre_asistencia
