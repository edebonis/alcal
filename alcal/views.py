from django.shortcuts import render
from asistencias.models import Asistencia, CodigoAsistencia
from alumnos.models import Alumno
from escuela.models import Curso
from django.http import HttpResponse

def home(request):
	if request.user.is_authenticated():
		cantidad = CodigoAsistencia.objects.all()
		codigo = CodigoAsistencia.objects.all()
		alumno = Alumno.objects.all()
		return render(request, 'home.html', {'alumno':alumno, 'cantidad':cantidad, 'codigo':codigo})
	else:
		return render(request, 'login.html')

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
		return HttpResponse('Por favor introduce un termino de búsqueda.') 

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
		return HttpResponse('Por favor introduce un termino de búsqueda.')

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
		return HttpResponse('Por favor introduce un termino de búsqueda.')

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
		return HttpResponse('Por favor introduce un termino de búsqueda.')

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
		return HttpResponse('Por favor introduce un termino de búsqueda.') 