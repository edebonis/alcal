# -*- encoding: utf-8 -*-
"""
Utilidades para generación de PDFs en ALCAL - Docentes
"""
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime
from django.utils.text import slugify


def generar_ficha_docente(docente):
    """
    Genera un PDF con la ficha de datos personales de un docente.
    
    Args:
        docente: Instancia del modelo Docente
        
    Returns:
        HttpResponse con el PDF generado
    """
    # Crear el objeto HttpResponse con header de PDF
    filename = f"ficha_docente_{slugify(docente.apellido)}_{slugify(docente.nombre)}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)
    
    # Estilos
    styles = getSampleStyleSheet()
    style_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1a237e'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    style_seccion = ParagraphStyle(
        'CustomSection',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#283593'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    style_normal = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica'
    )
    
    # Elementos del documento
    elementos = []
    
    # Encabezado
    titulo = Paragraph("FICHA DE DATOS DEL DOCENTE", style_titulo)
    elementos.append(titulo)
    
    if docente.legajo_numero:
        subtitulo = Paragraph(f"Legajo N° {docente.legajo_numero}", style_normal)
        elementos.append(subtitulo)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Sección: Datos Personales
    elementos.append(Paragraph("DATOS PERSONALES", style_seccion))
    
    datos_personales = [
        ['Apellido:', docente.apellido or ''],
        ['Nombre:', docente.nombre or ''],
        ['DNI:', str(docente.dni) if docente.dni else ''],
        ['Sexo:', docente.get_sexo_display() if docente.sexo else ''],
        ['Fecha de Nacimiento:', docente.fecha_nacimiento.strftime('%d/%m/%Y') if docente.fecha_nacimiento else ''],
        ['Nacionalidad:', docente.nacionalidad or ''],
    ]
    
    tabla_personales = Table(datos_personales, colWidths=[5*cm, 12*cm])
    tabla_personales.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla_personales)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Sección: Datos de Contacto
    elementos.append(Paragraph("DATOS DE CONTACTO", style_seccion))
    
    datos_contacto = [
        ['Domicilio:', docente.direccion or ''],
        ['Teléfono:', docente.telefono or ''],
        ['Celular:', docente.celular or ''],
        ['Email:', docente.email or ''],
    ]
    
    tabla_contacto = Table(datos_contacto, colWidths=[5*cm, 12*cm])
    tabla_contacto.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8eaf6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1a237e')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla_contacto)
    elementos.append(Spacer(1, 0.5*cm))
    
    # Sección: Datos Laborales
    elementos.append(Paragraph("DATOS LABORALES Y REVISTA", style_seccion))
    
    datos_laborales = [
        ['Cargo:', docente.cargo or ''],
        ['Modalidad:', docente.modalidad or ''],
        ['Situación de Revista:', 'Titular' if docente.es_titular else 'Suplente' if docente.es_suplente else 'Interino'],
        ['Horas Totales:', str(docente.horas_totales) if docente.horas_totales else '0'],
        ['Horas Extensión:', str(docente.horas_extension) if docente.horas_extension else '0'],
        ['Fecha de Alta:', docente.fecha_alta.strftime('%d/%m/%Y') if docente.fecha_alta else ''],
        ['Antigüedad:', docente.antiguedad_completa],
    ]
    
    if docente.fecha_baja:
        datos_laborales.append(['Fecha de Baja:', docente.fecha_baja.strftime('%d/%m/%Y')])
    
    tabla_laborales = Table(datos_laborales, colWidths=[5*cm, 12*cm])
    tabla_laborales.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1b5e20')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabla_laborales)
    
    # Pie de página
    elementos.append(Spacer(1, 1*cm))
    fecha_generacion = Paragraph(
        f"<i>Ficha generada el {datetime.now().strftime('%d/%m/%Y a las %H:%M')}</i>",
        ParagraphStyle('Footer', parent=styles['Normal'], fontSize=8, textColor=colors.grey, alignment=TA_CENTER)
    )
    elementos.append(fecha_generacion)
    
    # Construir el PDF
    doc.build(elementos)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
