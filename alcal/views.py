from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from alumnos.models import Alumno
from asistencias.models import Asistencia, CodigoAsistencia, Turno
from calificaciones.models import CalificacionParcial, CalificacionTrimestral, Instancia
from escuela.models import Curso, Materia, Anio


@login_required  
def home(request):  
    cantidad = CodigoAsistencia.objects.all()  
    codigo = CodigoAsistencia.objects.all()  
    alumno = Alumno.objects.all()  
    return render(request, 'home.html', {'alumno': alumno, 'cantidad': cantidad, 'codigo': codigo})

def consultas(request):
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	return render(request, 'consultas.html', {'alumno':alumno, 'cursos':cursos,})

def ingresar(request):
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	return render(request, 'ingresar.html', {'alumno':alumno, 'cursos':cursos,})

def asistencia(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	return render(request, 'asistencia.html', {'alumno':alumno, 'cursos':cursos,})

def calificaciones(request):
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	return render(request, 'calificaciones.html', {'alumno':alumno, 'cursos':cursos,})

def observaciones(request):
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	return render(request, 'observaciones.html', {'alumno':alumno, 'cursos':cursos,})

def ing_asistencia(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'ingresar_asistencia.html', var)

def cons_asistencia(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'cons_asistencia.html', var)

# def ing_asistencia_cur(request):
# 	cursos = Curso.objects.all()
# 	pkcur = 0
# 	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
# 		q = request.GET['menu']
# 		for i in cursos:
# 			if str(q) == str(i):
# 				pkcur = i.id
# 		alumnos = Alumno.objects.filter(curso=pkcur)
# 		return render(request, 'ing_asis_cur.html',  {'alumnos': alumnos, 'query': q}) 
# 	else: 
# 		return HttpResponse('Por favor introduce un termino de busqueda.')

# def cons_asistencia_cur(request):
# 	cursos = Curso.objects.all()
# 	asistencias = Asistencia.objects.all()
# 	cod = CodigoAsistencia.objects.all()
# 	pkcur = 0
# 	faltas = 0
# 	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
# 		q = request.GET['menu']
# 		for i in cursos:
# 			if str(q) == str(i):
# 				pkcur = i.id
# 		alumnos = Alumno.objects.filter(curso=pkcur)
# 		for j in alumnos:
# 			for a in asistencias:
# 				if a.alumno == j.id:
# 					for k in cod:
# 						if a.cod == k.id:
# 							faltas = faltas + k.cantidad
# 
# 			
# 				
# 		return render(request, 'cons_asis_cur.html',  {'alumnos': alumnos, 'query': q, 'faltas':faltas}) 
# 	else: 
# 		return HttpResponse('Por favor introduce un termino de busqueda.') 

def ing_calificaciones(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'ingresar_calificaciones.html', var)

def cons_calificaciones(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'cons_calificaciones.html', var)

def ing_calificaciones_cur(request):
	cursos = Curso.objects.all()
	pkcur = 0
	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
		q = request.GET['menu']
		for i in cursos:
			if str(q) == str(i):
				pkcur = i.id
		alumnos = Alumno.objects.filter(curso=pkcur)
		return render(request, 'resultados.html',  {'alumnos': alumnos, 'query': q}) 
	else: 
		return HttpResponse('Por favor introduce un termino de busqueda.')

# def cons_calificaciones_cur(request):
# 	cursos = Curso.objects.all()
# 	pkcur = 0
# 	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
# 		q = request.GET['menu']
# 		for i in cursos:
# 			if str(q) == str(i):
# 				pkcur = i.id
# 		alumnos = Alumno.objects.filter(curso=pkcur)
# 		return render(request, 'cons_resultados.html',  {'alumnos': alumnos, 'query': q}) 
# 	else: 
# 		return HttpResponse('Por favor introduce un termino de busqueda.')

def ing_observaciones(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'ingresar_observaciones.html', var)

def cons_observaciones(request):
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	cursos = Curso.objects.all()
	var = {
	'alumno':alumno,
	'cantidad':cantidad,
	'codigo':codigo,
	'cursos':cursos,
	}
	return render(request, 'cons_observaciones.html', var)

def ing_observaciones_cur(request):
	cursos = Curso.objects.all()
	pkcur = 0
	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
		q = request.GET['menu']
		for i in cursos:
			if str(q) == str(i):
				pkcur = i.id
		alumnos = Alumno.objects.filter(curso=pkcur)
		return render(request, 'resultados.html',  {'alumnos': alumnos, 'query': q}) 
	else: 
		return HttpResponse('Por favor introduce un termino de busqueda.')

def cons_observaciones_cur(request):
	cursos = Curso.objects.all()
	pkcur = 0
	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
		q = request.GET['menu']
		for i in cursos:
			if str(q) == str(i):
				pkcur = i.id
		alumnos = Alumno.objects.filter(curso=pkcur)
		return render(request, 'cons_resultados.html',  {'alumnos': alumnos, 'query': q}) 
	else: 
		return HttpResponse('Por favor introduce un termino de busqueda.') 

# === NUEVAS VISTAS PARA FUNCIONALIDADES POR ALUMNO ===

def cons_asistencia_alumno(request):
    """Nueva vista para consultar asistencias por alumno individual"""
    alumnos = Alumno.objects.all()
    cursos = Curso.objects.all()
    
    alumno_seleccionado = None
    asistencias_alumno = []
    stats = {'presentes': 0, 'faltas': 0, 'tardanzas': 0, 'retiros': 0}
    
    if 'alumno_id' in request.GET and request.GET['alumno_id']:
        alumno_id = request.GET['alumno_id']
        try:
            alumno_seleccionado = Alumno.objects.get(legajo=alumno_id)
            asistencias_alumno = Asistencia.objects.filter(alumno=alumno_seleccionado).order_by('-fecha')
            
            # Calculate statistics
            for asistencia in asistencias_alumno:
                if asistencia.codigo.cantidad == 0.0:
                    stats['presentes'] += 1
                else:
                    stats['faltas'] += asistencia.codigo.cantidad
                
                if 'T' in asistencia.codigo.codigo:
                    stats['tardanzas'] += 1
                if 'R' in asistencia.codigo.codigo:
                    stats['retiros'] += 1
        except Alumno.DoesNotExist:
            pass
    
    var = {
        'alumnos': alumnos,
        'cursos': cursos,
        'alumno_seleccionado': alumno_seleccionado,
        'asistencias_alumno': asistencias_alumno,
        'stats': stats,
    }
    return render(request, 'cons_asistencia_alumno.html', var)

def ing_asistencia_alumno(request):
    """Nueva vista para ingresar asistencias por alumno individual"""
    alumnos = Alumno.objects.all()
    codigos = CodigoAsistencia.objects.all()
    cursos = Curso.objects.all()
    turnos = Turno.objects.all()
    
    registros_recientes = Asistencia.objects.order_by('-fecha', '-id')[:5]

    if request.method == 'POST':
        try:
            alumno_id = request.POST.get('alumno')
            fecha = request.POST.get('fecha')
            turno_id = request.POST.get('turno')
            codigo_val = request.POST.get('estado')
            observaciones = request.POST.get('observaciones')
            
            alumno = Alumno.objects.get(id=alumno_id)
            turno = Turno.objects.get(id=turno_id)
            codigo = CodigoAsistencia.objects.get(codigo=codigo_val)
            
            # Obtener o crear el ciclo lectivo actual (esto es una simplificación, idealmente debería ser dinámico)
            anio_actual = fecha.split('-')[0]
            ciclo, _ = Anio.objects.get_or_create(ciclo_lectivo=int(anio_actual))
            
            # Verificar si ya existe
            if Asistencia.objects.filter(alumno=alumno, fecha=fecha, turno=turno).exists():
                messages.error(request, f'Ya existe una asistencia para {alumno} en esa fecha y turno.')
            else:
                Asistencia.objects.create(
                    ciclo_lectivo=ciclo,
                    curso=alumno.curso,
                    alumno=alumno,
                    codigo=codigo,
                    turno=turno,
                    fecha=fecha,
                    observaciones=observaciones
                )
                messages.success(request, f'Asistencia guardada correctamente para {alumno}.')
                return redirect('ing_asistencia_alumno')
                
        except Exception as e:
            messages.error(request, f'Error al guardar asistencia: {str(e)}')
    
    var = {
        'alumnos': alumnos,
        'codigos': codigos,
        'cursos': cursos,
        'turnos': turnos,
        'registros_recientes': registros_recientes,
    }
    return render(request, 'ing_asistencia_alumno.html', var)

def cons_calificaciones_alumno(request):
    """Nueva vista para consultar calificaciones por alumno individual"""
    alumnos = Alumno.objects.all()
    cursos = Curso.objects.all()
    
    alumno_seleccionado = None
    calificaciones_trimestre = []
    calificaciones_parciales = []
    
    if 'alumno_id' in request.GET and request.GET['alumno_id']:
        alumno_id = request.GET['alumno_id']
        try:
            alumno_seleccionado = Alumno.objects.get(legajo=alumno_id)
            calificaciones_trimestre = CalificacionTrimestral.objects.filter(alumno=alumno_seleccionado)
            calificaciones_parciales = CalificacionParcial.objects.filter(alumno=alumno_seleccionado).order_by('-fecha')
        except Alumno.DoesNotExist:
            pass
    
    var = {
        'alumnos': alumnos,
        'cursos': cursos,
        'alumno_seleccionado': alumno_seleccionado,
        'calificaciones_trimestre': calificaciones_trimestre,
        'calificaciones_parciales': calificaciones_parciales,
    }
    return render(request, 'cons_calificaciones_alumno.html', var)

def ing_calificaciones_alumno(request):
    """Nueva vista para ingresar calificaciones por alumno individual"""
    alumnos = Alumno.objects.all()
    cursos = Curso.objects.all()
    materias = Materia.objects.all()
    
    # Obtener calificaciones recientes (combinando parciales y trimestrales)
    # Esto es un poco complejo de hacer en una sola query, así que por ahora mostramos las últimas creadas
    # Idealmente deberíamos tener un modelo unificado o una vista SQL, pero para este MVP haremos dos queries
    calificaciones_recientes = []
    trimestrales = CalificacionTrimestral.objects.select_related('alumno', 'curso', 'instancia').order_by('-id')[:5]
    parciales = CalificacionParcial.objects.select_related('alumno', 'curso', 'materia').order_by('-id')[:5]
    
    for t in trimestrales:
        calificaciones_recientes.append({
            'fecha': None, # Trimestrales no tienen fecha exacta en el modelo, solo ciclo
            'alumno': t.alumno,
            'materia': None, # Trimestrales son generales o por materia? El modelo NO tiene materia!
            'tipo': 'trimestral',
            'calificacion': t.nota,
            'estado': 'A' if t.nota >= 7 else 'R' if t.nota >= 4 else 'D'
        })
        
    for p in parciales:
        calificaciones_recientes.append({
            'fecha': p.fecha,
            'alumno': p.alumno,
            'materia': p.materia,
            'tipo': 'parcial',
            'calificacion': p.nota,
            'estado': 'A' if p.nota >= 7 else 'R' if p.nota >= 4 else 'D'
        })
    
    if request.method == 'POST':
        try:
            alumno_id = request.POST.get('alumno')
            materia_id = request.POST.get('materia')
            tipo = request.POST.get('tipo_calificacion')
            nota = float(request.POST.get('calificacion'))
            fecha = request.POST.get('fecha')
            observaciones = request.POST.get('observaciones')
            
            alumno = Alumno.objects.get(id=alumno_id)
            
            # Obtener ciclo lectivo
            anio_actual = fecha.split('-')[0]
            ciclo, _ = Anio.objects.get_or_create(ciclo_lectivo=int(anio_actual))
            
            if tipo == 'trimestral':
                trimestre_val = request.POST.get('trimestre')
                instancia_nombre = f"{trimestre_val}º Trimestre"
                instancia, _ = Instancia.objects.get_or_create(instancia=instancia_nombre)
                
                # NOTA: El modelo CalificacionTrimestral NO tiene campo materia.
                # Esto parece ser un error de diseño o una simplificación (promedio general?).
                # Asumiremos que es por curso/alumno/instancia.
                
                CalificacionTrimestral.objects.create(
                    nota=int(nota),
                    instancia=instancia,
                    curso=alumno.curso,
                    alumno=alumno,
                    ciclo_lectivo=ciclo
                )
                messages.success(request, f'Nota trimestral guardada para {alumno}.')
                
            elif tipo == 'parcial':
                materia = Materia.objects.get(id=materia_id)
                
                CalificacionParcial.objects.create(
                    nota=int(nota),
                    fecha=fecha,
                    curso=alumno.curso,
                    alumno=alumno,
                    materia=materia,
                    ciclo_lectivo=ciclo
                )
                messages.success(request, f'Nota parcial de {materia} guardada para {alumno}.')
                
            return redirect('ing_calificaciones_alumno')
            
        except Exception as e:
            messages.error(request, f'Error al guardar calificación: {str(e)}')
    
    var = {
        'alumnos': alumnos,
        'cursos': cursos,
        'materias': materias,
        'calificaciones_recientes': calificaciones_recientes,
    }
    return render(request, 'ing_calificaciones_alumno.html', var)

# === VISTAS MEJORADAS PARA SELECCIÓN DUAL ===

def asistencia_selector(request):
    """Vista principal para elegir entre consultar por alumno o por curso"""
    return render(request, 'asistencia_selector.html')

def calificaciones_selector(request):
    """Vista principal para elegir entre consultar calificaciones por alumno o por curso"""
    return render(request, 'calificaciones_selector.html')

def ingresar_calificaciones(request):
    """Vista selectora para ingresar calificaciones"""
    from escuela.models import Curso, Materia
    cursos = Curso.objects.all()
    materias = Materia.objects.all()
    return render(request, 'ingresar_calificaciones.html', {
        'cursos': cursos,
        'materias': materias
    })

def ingresar_calificaciones_curso(request):
    """Vista para ingresar calificaciones masivas por curso"""
    
    curso_id = request.GET.get('curso')
    materia_id = request.GET.get('materia')
    
    curso_seleccionado = None
    materia_seleccionada = None
    alumnos = []
    
    if curso_id and materia_id:
        try:
            curso_seleccionado = Curso.objects.get(id=curso_id)
            materia_seleccionada = Materia.objects.get(id=materia_id)
            alumnos = Alumno.objects.filter(curso=curso_id).order_by('apellido', 'nombre')
        except (Curso.DoesNotExist, Materia.DoesNotExist):
            pass
            
    if request.method == 'POST':
        # Aquí iría la lógica de guardado (similar a guardar_asistencia_curso pero para notas)
        # Por ahora solo renderizamos
        pass
        
    return render(request, 'ingresar_calificaciones_curso.html', {
        'curso_seleccionado': curso_seleccionado,
        'materia_seleccionada': materia_seleccionada,
        'alumnos': alumnos
    })

def consultar_calificaciones_curso(request):
    """Vista para consultar la planilla de calificaciones de un curso"""
    from escuela.models import Curso, Materia, Alumno
    
    curso_id = request.GET.get('curso')
    materia_id = request.GET.get('materia')
    
    curso_seleccionado = None
    materia_seleccionada = None
    alumnos = []
    
    if curso_id and materia_id:
        try:
            curso_seleccionado = Curso.objects.get(id=curso_id)
            materia_seleccionada = Materia.objects.get(id=materia_id)
            alumnos = Alumno.objects.filter(curso=curso_id).order_by('apellido', 'nombre')
            # Aquí deberíamos obtener las notas reales para cada alumno
            # Por ahora pasamos solo los alumnos para la estructura
        except (Curso.DoesNotExist, Materia.DoesNotExist):
            pass
            
    return render(request, 'consultar_calificaciones_curso.html', {
        'curso_seleccionado': curso_seleccionado,
        'materia_seleccionada': materia_seleccionada,
        'alumnos': alumnos
    })

def ingresar_selector(request):
    """Vista principal para elegir entre ingresar datos por alumno o por curso"""
    return render(request, 'ingresar_selector.html')

def consultas_selector(request):
    """Vista principal para elegir entre consultar por alumno o por curso"""
    return render(request, 'consultas_selector.html') 