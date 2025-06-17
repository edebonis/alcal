from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from alumnos.models import Alumno
from asistencias.models import Asistencia, CodigoAsistencia
from calificaciones.models import CalificacionParcial, CalificacionTrimestral
from escuela.models import Curso


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

def ing_asistencia_cur(request):
	cursos = Curso.objects.all()
	pkcur = 0
	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
		q = request.GET['menu']
		for i in cursos:
			if str(q) == str(i):
				pkcur = i.id
		alumnos = Alumno.objects.filter(curso=pkcur)
		return render(request, 'ing_asis_cur.html',  {'alumnos': alumnos, 'query': q}) 
	else: 
		return HttpResponse('Por favor introduce un termino de busqueda.')

def cons_asistencia_cur(request):
	cursos = Curso.objects.all()
	asistencias = Asistencia.objects.all()
	cod = CodigoAsistencia.objects.all()
	pkcur = 0
	faltas = 0
	if 'menu' in request.GET and request.GET['menu'] and request.GET['menu'] != '0': 
		q = request.GET['menu']
		for i in cursos:
			if str(q) == str(i):
				pkcur = i.id
		alumnos = Alumno.objects.filter(curso=pkcur)
		for j in alumnos:
			for a in asistencias:
				if a.alumno == j.id:
					for k in cod:
						if a.cod == k.id:
							faltas = faltas + k.cantidad

			
				
		return render(request, 'cons_asis_cur.html',  {'alumnos': alumnos, 'query': q, 'faltas':faltas}) 
	else: 
		return HttpResponse('Por favor introduce un termino de busqueda.') 

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

def cons_calificaciones_cur(request):
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
    
    if 'alumno_id' in request.GET and request.GET['alumno_id']:
        alumno_id = request.GET['alumno_id']
        try:
            alumno_seleccionado = Alumno.objects.get(legajo=alumno_id)
            asistencias_alumno = Asistencia.objects.filter(alumno=alumno_seleccionado).order_by('-fecha')
        except Alumno.DoesNotExist:
            pass
    
    var = {
        'alumnos': alumnos,
        'cursos': cursos,
        'alumno_seleccionado': alumno_seleccionado,
        'asistencias_alumno': asistencias_alumno,
    }
    return render(request, 'cons_asistencia_alumno.html', var)

def ing_asistencia_alumno(request):
    """Nueva vista para ingresar asistencias por alumno individual"""
    alumnos = Alumno.objects.all()
    codigos = CodigoAsistencia.objects.all()
    cursos = Curso.objects.all()
    
    if request.method == 'POST':
        # Procesar el formulario de ingreso de asistencia
        # Esta lógica se implementará después
        pass
    
    var = {
        'alumnos': alumnos,
        'codigos': codigos,
        'cursos': cursos,
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
    
    if request.method == 'POST':
        # Procesar el formulario de ingreso de calificaciones
        # Esta lógica se implementará después
        pass
    
    var = {
        'alumnos': alumnos,
        'cursos': cursos,
    }
    return render(request, 'ing_calificaciones_alumno.html', var)

# === VISTAS MEJORADAS PARA SELECCIÓN DUAL ===

def asistencia_selector(request):
    """Vista principal para elegir entre consultar por alumno o por curso"""
    return render(request, 'asistencia_selector.html')

def calificaciones_selector(request):
    """Vista principal para elegir entre consultar calificaciones por alumno o por curso"""
    return render(request, 'calificaciones_selector.html')

def ingresar_selector(request):
    """Vista principal para elegir entre ingresar datos por alumno o por curso"""
    return render(request, 'ingresar_selector.html')

def consultas_selector(request):
    """Vista principal para elegir entre consultar por alumno o por curso"""
    return render(request, 'consultas_selector.html') 