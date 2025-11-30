# -*- encoding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Docente
from .pdf_utils import generar_ficha_docente

@login_required
def exportar_ficha_docente(request, docente_id):
    """
    Vista para descargar la ficha de datos de un docente en PDF.
    """
    docente = get_object_or_404(Docente, id=docente_id)
    return generar_ficha_docente(docente)
