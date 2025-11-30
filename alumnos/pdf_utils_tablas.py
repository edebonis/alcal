# -*- encoding: utf-8 -*-
"""
Utilidades para generación de PDFs en ALCAL - Versión con Tablas (estilo Excel)
"""
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from io import BytesIO
from datetime import datetime


def crear_celda(texto, ancho=None, estilo='normal', alineacion=TA_LEFT, colspan=1):
    """Crea una celda de tabla con texto"""
    styles = getSampleStyleSheet()
    
    if estilo == 'titulo':
        style = ParagraphStyle(
            'CellTitle',
            parent=styles['Normal'],
            fontSize=12,
            fontName='Helvetica-Bold',
            alignment=alineacion,
            textColor=colors.black
        )
    elif estilo == 'seccion':
        style = ParagraphStyle(
            'CellSection',
            parent=styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            alignment=alineacion,
            textColor=colors.black
        )
    else:
        style = ParagraphStyle(
            'CellNormal',
            parent=styles['Normal'],
            fontSize=9,
            fontName='Helvetica',
            alignment=alineacion,
            textColor=colors.black
        )
    
    if texto is None:
        texto = ''
    elif not isinstance(texto, str):
        texto = str(texto)
    
    return Paragraph(texto, style)


def crear_checkbox(marcado=False):
    """Crea un checkbox visual"""
    if marcado:
        return "☑"
    return "☐"


def generar_ficha_inscripcion(alumno):
    """
    Genera un PDF con la ficha de inscripción de un alumno.
    Replica EXACTAMENTE el formulario oficial "Fiche de inscripción.pdf"
    Usa tablas de ReportLab para replicar la estructura de Excel.
    
    Args:
        alumno: Instancia del modelo Alumno
        
    Returns:
        HttpResponse con el PDF generado
    """
    from django.utils.text import slugify
    filename = f"ficha_inscripcion_{alumno.legajo}_{slugify(alumno.apellido)}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4,
        topMargin=10*mm,
        bottomMargin=10*mm,
        leftMargin=10*mm,
        rightMargin=10*mm
    )
    
    # Estilos
    styles = getSampleStyleSheet()
    elementos = []
    
    # Anchos de columnas (ajustar según necesidad)
    ancho_total = A4[0] - 20*mm
    col_ancho_1 = ancho_total * 0.15  # 15% para etiquetas
    col_ancho_2 = ancho_total * 0.35  # 35% para datos
    col_ancho_3 = ancho_total * 0.15  # 15% para etiquetas
    col_ancho_4 = ancho_total * 0.35  # 35% para datos
    
    # ========== ENCABEZADO ==========
    encabezado_data = [
        [
            crear_celda("AÑO", estilo='titulo', alineacion=TA_LEFT),
            crear_celda(str(datetime.now().year), estilo='normal', alineacion=TA_LEFT),
            crear_celda("", estilo='normal'),
            crear_celda("", estilo='normal'),
            crear_celda("Nro.Insc.", estilo='titulo', alineacion=TA_RIGHT),
            crear_celda(str(alumno.legajo), estilo='normal', alineacion=TA_RIGHT),
        ]
    ]
    
    tabla_encabezado = Table(encabezado_data, colWidths=[15*mm, 20*mm, ancho_total*0.3, ancho_total*0.15, 25*mm, 20*mm])
    tabla_encabezado.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (4, 0), (5, 0), 'RIGHT'),
    ]))
    elementos.append(tabla_encabezado)
    elementos.append(Spacer(1, 3*mm))
    
    # Título principal (centrado)
    titulo_data = [[crear_celda("SOLICITUD DE INSCRIPCIÓN - EDUCACIÓN SECUNDARIA", estilo='titulo', alineacion=TA_CENTER)]]
    tabla_titulo = Table(titulo_data, colWidths=[ancho_total])
    tabla_titulo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos.append(tabla_titulo)
    elementos.append(Spacer(1, 5*mm))
    
    # ========== DATOS ESTUDIANTE ==========
    elementos.append(crear_celda("DATOS ESTUDIANTE", estilo='seccion'))
    elementos.append(Spacer(1, 2*mm))
    
    # Apellido/s y Nombre/s en la misma fila
    datos_estudiante_1 = [
        [
            crear_celda("Apellido/s:", estilo='normal'),
            crear_celda(alumno.apellido or '', estilo='normal'),
            crear_celda("Nombre/s:", estilo='normal'),
            crear_celda(alumno.nombre or '', estilo='normal'),
        ]
    ]
    tabla_est_1 = Table(datos_estudiante_1, colWidths=[col_ancho_1, col_ancho_2, col_ancho_1, col_ancho_2])
    tabla_est_1.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla_est_1)
    elementos.append(Spacer(1, 2*mm))
    
    # Fecha de Nacimiento
    fecha_nac = ''
    if alumno.fecha_nacimiento:
        fecha_nac = alumno.fecha_nacimiento.strftime('%d/%m/%Y')
        partes = fecha_nac.split('/')
        fecha_nac = f"{partes[0]} / {partes[1]} / {partes[2]}"
    
    datos_estudiante_2 = [
        [
            crear_celda("Fecha de Nacimiento:", estilo='normal'),
            crear_celda(fecha_nac, estilo='normal'),
            crear_celda("", estilo='normal'),
            crear_celda("", estilo='normal'),
        ]
    ]
    tabla_est_2 = Table(datos_estudiante_2, colWidths=[col_ancho_1, col_ancho_2*2, col_ancho_1, col_ancho_2])
    tabla_est_2.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla_est_2)
    elementos.append(Spacer(1, 2*mm))
    
    # ¿Posee DNI argentino?
    estado_dni = getattr(alumno, 'estado_dni', None)
    tiene_fisico = estado_dni == 'tiene_fisico'
    en_tramite = estado_dni == 'en_tramite'
    no_en_tramite = estado_dni == 'no_en_tramite'
    no_posee = estado_dni == 'no_posee'
    
    datos_dni = [
        [
            crear_celda("¿Posee DNI argentino?", estilo='normal'),
            crear_celda(f"{crear_checkbox(tiene_fisico)} Si, y tiene el DNI físico", estilo='normal'),
            crear_celda(f"{crear_checkbox(en_tramite)} SI, pero NO tiene el DNI físico y se encuentra en trámite", estilo='normal'),
            crear_celda("", estilo='normal'),
        ],
        [
            crear_celda("", estilo='normal'),
            crear_celda(f"{crear_checkbox(no_en_tramite)} Si, pero NO tiene el DNI físico y NO se encuentra en trámite", estilo='normal'),
            crear_celda(f"{crear_checkbox(no_posee)} NO posee DNI argentino", estilo='normal'),
            crear_celda("", estilo='normal'),
        ]
    ]
    tabla_dni = Table(datos_dni, colWidths=[col_ancho_1, col_ancho_2, col_ancho_2, col_ancho_1])
    tabla_dni.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla_dni)
    elementos.append(Spacer(1, 2*mm))
    
    # Número de DNI y CUIL
    dni_str = ''
    if alumno.dni:
        dni_str = str(alumno.dni)
        if len(dni_str) >= 7:
            dni_str = f"{dni_str[:2]}.{dni_str[2:5]}.{dni_str[5:]}"
    
    cuil_str = getattr(alumno, 'cuil', '') or ''
    if cuil_str and len(cuil_str) >= 11:
        # Formatear CUIL: 20-53174639-3
        cuil_formateado = f"{cuil_str[:2]}-{cuil_str[2:10]}-{cuil_str[10:]}"
    else:
        cuil_formateado = cuil_str
    
    datos_dni_cuil = [
        [
            crear_celda("Si respondió SI, indique número de DNI argentino:", estilo='normal'),
            crear_celda(dni_str, estilo='normal'),
            crear_celda("CUIL:", estilo='normal'),
            crear_celda(cuil_formateado, estilo='normal'),
        ]
    ]
    tabla_dni_cuil = Table(datos_dni_cuil, colWidths=[col_ancho_1*1.5, col_ancho_2, col_ancho_1*0.5, col_ancho_2])
    tabla_dni_cuil.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla_dni_cuil)
    elementos.append(Spacer(1, 2*mm))
    
    # Certificado de Pre-Identificación
    tiene_cpi = getattr(alumno, 'tiene_certificado_pre_identificacion', False)
    datos_cpi = [
        [
            crear_celda("¿Posee certificado de Pre-Identificación (CPI)?", estilo='normal'),
            crear_celda(f"{crear_checkbox(tiene_cpi)} SI", estilo='normal'),
            crear_celda(f"{crear_checkbox(not tiene_cpi)} NO", estilo='normal'),
            crear_celda("", estilo='normal'),
        ]
    ]
    tabla_cpi = Table(datos_cpi, colWidths=[col_ancho_1*2, col_ancho_1, col_ancho_1, col_ancho_2])
    tabla_cpi.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(tabla_cpi)
    elementos.append(Spacer(1, 3*mm))
    
    # Continuar con más secciones...
    # Por ahora, esta es una estructura base. Necesito agregar todas las secciones restantes.
    
    # Construir el PDF
    doc.build(elementos)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response


