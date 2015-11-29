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
	
def ing_asistencia_cur(request):
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
