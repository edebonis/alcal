from django.shortcuts import render
from asistencias.models import Asistencia, CodigoAsistencia
from alumnos.models import Alumno

def home(request):
	#Lista de códigos y cantidades de inasistencias
	cantidad = CodigoAsistencia.objects.all()
	codigo = CodigoAsistencia.objects.all()
	alumno = Alumno.objects.all()
	#return render(request, 'home.html', {'cantidad':cantidad, 'codigo':codigo})
	return render(request, 'home.html', {'alumno':alumno, 'cantidad':cantidad, 'codigo':codigo})