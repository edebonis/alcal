# -*- encoding: utf-8 -*-
"""
Vistas adicionales para la app de alumnos
"""
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Alumno
from .pdf_utils import generar_ficha_inscripcion


@login_required
def exportar_ficha_pdf(request, alumno_id):
    """
    Vista para exportar la ficha de inscripción de un alumno en PDF
    """
    alumno = get_object_or_404(Alumno, legajo=alumno_id)
    return generar_ficha_inscripcion(alumno)


@login_required
def exportar_constancia_alumno_regular(request, alumno_id):
    """
    Vista para exportar la constancia de alumno regular en PDF
    """
    from .pdf_utils import generar_constancia_alumno_regular
    alumno = get_object_or_404(Alumno, legajo=alumno_id)
    return generar_constancia_alumno_regular(alumno)

