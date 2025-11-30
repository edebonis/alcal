# -*- encoding: utf-8 -*-
"""
Utilidades para generación de PDFs en ALCAL
"""
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime


def generar_ficha_inscripcion(alumno):
    """
    Genera un PDF con la ficha de inscripción de un alumno.
    Replica EXACTAMENTE el formulario oficial "Fiche de inscripción.pdf"
    
    Args:
        alumno: Instancia del modelo Alumno
        
    Returns:
        HttpResponse con el PDF generado
    """
    from django.utils.text import slugify
    filename = f"ficha_inscripcion_{alumno.legajo}_{slugify(alumno.apellido)}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Crear el PDF usando canvas para control total del layout
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Configuración
    margin_left = 15*mm
    margin_top = height - 20*mm
    line_height = 5*mm
    font_size_normal = 9
    font_size_small = 8
    font_size_title = 12
    
    y = margin_top
    
    # ========== ENCABEZADO ==========
    # AÑO (arriba a la izquierda)
    p.setFont("Helvetica-Bold", font_size_title)
    p.drawString(margin_left, y, "AÑO")
    
    # Año actual
    año_actual = datetime.now().year
    p.setFont("Helvetica", font_size_normal)
    p.drawString(margin_left + 20*mm, y, str(año_actual))
    
    # SOLICITUD DE INSCRIPCIÓN - EDUCACIÓN SECUNDARIA (centrado)
    p.setFont("Helvetica-Bold", font_size_title)
    texto_titulo = "SOLICITUD DE INSCRIPCIÓN - EDUCACIÓN SECUNDARIA"
    texto_width = p.stringWidth(texto_titulo, "Helvetica-Bold", font_size_title)
    p.drawString((width - texto_width) / 2, y, texto_titulo)
    
    # Nro.Insc. (arriba a la derecha)
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(width - margin_left - 30*mm, y, "Nro.Insc.")
    
    # Número de inscripción (legajo)
    p.setFont("Helvetica", font_size_normal)
    p.drawString(width - margin_left - 10*mm, y, str(alumno.legajo))
    
    y -= 2*line_height
    
    # ========== DATOS ESTUDIANTE ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DATOS ESTUDIANTE")
    y -= line_height
    
    # Apellido/s
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "Apellido/s:")
    p.drawString(margin_left + 30*mm, y, alumno.apellido or '')
    y -= line_height
    
    # Nombre/s
    p.drawString(margin_left, y, "Nombre/s:")
    p.drawString(margin_left + 30*mm, y, alumno.nombre or '')
    y -= line_height
    
    # Fecha de Nacimiento
    p.drawString(margin_left, y, "Fecha de Nacimiento:")
    if alumno.fecha_nacimiento:
        fecha_str = alumno.fecha_nacimiento.strftime('%d/%m/%Y')
        # Separar día, mes, año
        partes = fecha_str.split('/')
        p.drawString(margin_left + 50*mm, y, partes[0] if len(partes) > 0 else '')
        p.drawString(margin_left + 55*mm, y, '/')
        p.drawString(margin_left + 58*mm, y, partes[1] if len(partes) > 1 else '')
        p.drawString(margin_left + 63*mm, y, '/')
        p.drawString(margin_left + 66*mm, y, partes[2] if len(partes) > 2 else '')
    y -= line_height
    
    # ¿Posee DNI argentino?
    p.drawString(margin_left, y, "¿Posee DNI argentino?")
    y -= line_height * 0.7
    
    # Opciones DNI (checkboxes)
    opciones_dni = [
        ('tiene_fisico', 'Si, y tiene el DNI físico'),
        ('en_tramite', 'SI, pero NO tiene el DNI físico y se encuentra en trámite'),
        ('no_en_tramite', 'Si, pero NO tiene el DNI físico y NO se encuentra en trámite'),
        ('no_posee', 'NO posee DNI argentino'),
    ]
    
    checkbox_x = margin_left + 5*mm
    checkbox_size = 3*mm
    
    for valor, texto in opciones_dni:
        # Dibujar checkbox
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Marcar si corresponde
        if hasattr(alumno, 'estado_dni') and alumno.estado_dni == valor:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, texto)
        y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # Número de DNI
    p.drawString(margin_left, y, "Si respondió SI, indique número de DNI argentino:")
    if alumno.dni:
        dni_str = str(alumno.dni)
        # Formatear con puntos: 53.174.639
        if len(dni_str) >= 7:
            dni_formateado = f"{dni_str[:2]}.{dni_str[2:5]}.{dni_str[5:]}"
        else:
            dni_formateado = dni_str
        p.drawString(margin_left + 80*mm, y, dni_formateado)
    y -= line_height
    
    # Si respondió que NO tiene DNI argentino
    p.drawString(margin_left, y, "Si respondió que NO tiene DNI argentino:")
    y -= line_height
    
    # Identidad de género
    p.drawString(margin_left, y, "Identidad de género:")
    y -= line_height * 0.7
    
    # Opciones identidad de género (checkboxes)
    opciones_genero = [
        ('F', 'Mujer'),
        ('M', 'Varón'),
        ('MT', 'Mujer trans/travesti'),
        ('VT', 'Varón trans/ masculinidad trans'),
        ('NB', 'No binario'),
        ('O', 'Otra'),
        ('ND', 'No desea responder'),
    ]
    
    checkbox_x = margin_left + 5*mm
    for valor, texto in opciones_genero:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Marcar si corresponde
        identidad = getattr(alumno, 'identidad_genero', None) or alumno.sexo
        if identidad == valor:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, texto)
        y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # Lugar de nacimiento
    p.drawString(margin_left, y, "Lugar de nacimiento:")
    y -= line_height * 0.7
    
    opciones_lugar = [
        ('argentina', 'En Argentina'),
        ('extranjero', 'En el extranjero'),
        ('otra', 'Otra (especificar)'),
    ]
    
    checkbox_x = margin_left + 5*mm
    lugar_es_argentina = False
    for valor, texto in opciones_lugar:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        if alumno.lugar_nacimiento and 'argentina' in (alumno.lugar_nacimiento or '').lower():
            if valor == 'argentina':
                p.setFont("Helvetica-Bold", 12)
                p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
                p.setFont("Helvetica", font_size_small)
                lugar_es_argentina = True
        p.drawString(checkbox_x + 6*mm, y, texto)
        y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # Solo para quienes marcaron Argentina
    if lugar_es_argentina:
        p.drawString(margin_left, y, "Solo para quienes marcaron Argentina:")
        y -= line_height
        
        # Provincia
        p.drawString(margin_left + 5*mm, y, "Provincia")
        p.drawString(margin_left + 30*mm, y, alumno.provincia or '')
        y -= line_height
        
        # Distrito (solo para Buenos Aires)
        p.drawString(margin_left + 5*mm, y, "Solo para quienes marcaron Buenos Aires: Distrito")
        p.drawString(margin_left + 80*mm, y, alumno.distrito or '')
        y -= line_height
    
    # Nacionalidad
    p.drawString(margin_left, y, "Nacionalidad:")
    p.drawString(margin_left + 30*mm, y, alumno.nacionalidad or 'Argentina')
    y -= line_height
    
    # CUIL
    p.drawString(margin_left, y, "CUIL:")
    if hasattr(alumno, 'cuil') and alumno.cuil:
        p.drawString(margin_left + 20*mm, y, alumno.cuil)
    y -= line_height
    
    # ¿Posee certificado de Pre-Identificación (CPI)?
    p.drawString(margin_left, y, "¿Posee certificado de Pre-Identificación (CPI)?")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if hasattr(alumno, 'tiene_certificado_pre_identificacion') and alumno.tiene_certificado_pre_identificacion:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 20*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not (hasattr(alumno, 'tiene_certificado_pre_identificacion') and alumno.tiene_certificado_pre_identificacion):
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 1.2
    
    # ========== DOMICILIO ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DOMICILIO")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    # Calle
    p.drawString(margin_left, y, "Calle:")
    p.drawString(margin_left + 20*mm, y, alumno.direccion or '')
    
    # N°
    p.drawString(margin_left + 80*mm, y, "N°:")
    if hasattr(alumno, 'numero_domicilio'):
        p.drawString(margin_left + 90*mm, y, alumno.numero_domicilio or '')
    y -= line_height
    
    # Piso, Torre, Depto
    p.drawString(margin_left, y, "Piso:")
    if hasattr(alumno, 'piso'):
        p.drawString(margin_left + 20*mm, y, alumno.piso or '')
    
    p.drawString(margin_left + 40*mm, y, "Torre:")
    if hasattr(alumno, 'torre'):
        p.drawString(margin_left + 55*mm, y, alumno.torre or '')
    
    p.drawString(margin_left + 75*mm, y, "Depto:")
    if hasattr(alumno, 'depto'):
        p.drawString(margin_left + 90*mm, y, alumno.depto or '')
    y -= line_height
    
    # Entre calles
    p.drawString(margin_left, y, "Entre calle:")
    if hasattr(alumno, 'entre_calle_1'):
        p.drawString(margin_left + 30*mm, y, alumno.entre_calle_1 or '')
    
    p.drawString(margin_left + 80*mm, y, "Y calle:")
    if hasattr(alumno, 'entre_calle_2'):
        p.drawString(margin_left + 95*mm, y, alumno.entre_calle_2 or '')
    y -= line_height
    
    # Localidad, Provincia, Distrito
    p.drawString(margin_left, y, "Localidad")
    p.drawString(margin_left + 25*mm, y, alumno.localidad or '')
    
    p.drawString(margin_left + 70*mm, y, "Provincia:")
    p.drawString(margin_left + 85*mm, y, alumno.provincia or '')
    y -= line_height
    
    p.drawString(margin_left, y, "Distrito:")
    p.drawString(margin_left + 25*mm, y, alumno.distrito or '')
    y -= line_height
    
    # Teléfono
    p.drawString(margin_left, y, "Teléfono:")
    p.drawString(margin_left + 25*mm, y, "Cod. área:")
    if hasattr(alumno, 'codigo_area_telefono'):
        p.drawString(margin_left + 40*mm, y, alumno.codigo_area_telefono or '')
    p.drawString(margin_left + 55*mm, y, "N°:")
    p.drawString(margin_left + 60*mm, y, alumno.telefono or '')
    y -= line_height
    
    # Teléfono celular
    p.drawString(margin_left, y, "Teléfono celular:")
    p.drawString(margin_left + 40*mm, y, "Cod. área:")
    if hasattr(alumno, 'codigo_area_celular'):
        p.drawString(margin_left + 55*mm, y, alumno.codigo_area_celular or '')
    p.drawString(margin_left + 70*mm, y, "N°:")
    p.drawString(margin_left + 75*mm, y, alumno.celular_alumno or '')
    y -= line_height * 1.5
    
    # ========== OTROS DATOS ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "OTROS DATOS")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    # Hermanas o hermanos
    p.drawString(margin_left, y, "Hermanas o hermanos:")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    tiene_hermanos = hasattr(alumno, 'tiene_hermanos') and alumno.tiene_hermanos
    if tiene_hermanos:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not tiene_hermanos:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO tiene hermanas o hermanos")
    y -= line_height * 0.8
    
    if tiene_hermanos:
        p.drawString(margin_left + 5*mm, y, "Cantidad:")
        if hasattr(alumno, 'cantidad_hermanos'):
            p.drawString(margin_left + 25*mm, y, str(alumno.cantidad_hermanos))
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "Cantidad que asiste al establecimiento:")
        if hasattr(alumno, 'hermanos_en_establecimiento'):
            p.drawString(margin_left + 80*mm, y, str(alumno.hermanos_en_establecimiento))
        y -= line_height
    
    # Lenguas distintas al castellano
    p.drawString(margin_left, y, "¿Se hablan lenguas distintas al castellano en el hogar?")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    habla_lenguas = hasattr(alumno, 'habla_lenguas_distintas_castellano') and alumno.habla_lenguas_distintas_castellano
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if habla_lenguas:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not habla_lenguas:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    if habla_lenguas:
        p.drawString(margin_left + 5*mm, y, "En caso afirmativo: Lengua/s indígena/s:")
        if hasattr(alumno, 'lenguas_indigenas'):
            p.drawString(margin_left + 70*mm, y, alumno.lenguas_indigenas or '')
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "Otra/s lengua/s:")
        if hasattr(alumno, 'otras_lenguas'):
            p.drawString(margin_left + 40*mm, y, alumno.otras_lenguas or '')
        y -= line_height
    
    # Pueblos Originarios
    p.drawString(margin_left, y, "¿Se reconoce perteneciente o descendiente de Pueblos Originarios?")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    pertenece = hasattr(alumno, 'pertenece_pueblos_originarios') and alumno.pertenece_pueblos_originarios
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if pertenece:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not pertenece:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    # AUH
    p.drawString(margin_left, y, "Percibe: Asignación Universal por Hijo (AUH):")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    percibe_auh = hasattr(alumno, 'percibe_auh') and alumno.percibe_auh
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if percibe_auh:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not percibe_auh:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    # Progresar
    p.drawString(margin_left, y, "Progresar:")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    percibe_progresar = hasattr(alumno, 'percibe_progresar') and alumno.percibe_progresar
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if percibe_progresar:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not percibe_progresar:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    # Medio de transporte
    p.drawString(margin_left, y, "Medio de transporte que utiliza para llegar al establecimiento: (marcar todas las opciones que correspondan)")
    y -= line_height * 0.7
    
    medios_transporte = [
        ('pie_bicicleta', 'A pie/bicicleta'),
        ('transporte_escolar', 'Transporte escolar DGCyE'),
        ('colectivo', 'Colectivo'),
        ('tren', 'Tren'),
        ('vehiculo_particular', 'Vehículo particular'),
        ('taxi_remis', 'Taxi/Remis'),
        ('otro', 'Otro'),
    ]
    
    checkbox_x = margin_left + 5*mm
    medio_transporte_str = getattr(alumno, 'medio_transporte', '') or ''
    medios_seleccionados = [m.strip() for m in medio_transporte_str.split(',') if m.strip()]
    
    for valor, texto in medios_transporte:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        if valor in medios_seleccionados or texto.lower() in medio_transporte_str.lower():
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, texto)
        y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== INFORMACIÓN DE SALUD ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "INFORMACIÓN DE SALUD")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    # ¿Posee obra social?
    p.drawString(margin_left, y, "¿Posee obra social?")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    tiene_obra_social = False  # Por ahora, no hay campo en el modelo
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if tiene_obra_social:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not tiene_obra_social:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    if tiene_obra_social:
        p.drawString(margin_left + 5*mm, y, "En caso afirmativo:")
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "Obra social:")
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "N° Afiliado:")
        y -= line_height
    
    y -= line_height * 0.5
    
    # ========== ANTECEDENTES PERSONALES DE SALUD ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "ANTECEDENTES PERSONALES DE SALUD")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "¿Padece o ha padecido alguna o algunas de las siguientes condiciones de salud? (Marcar por SI o por NO)")
    y -= line_height * 0.8
    
    # Lista de condiciones de salud
    condiciones_salud = [
        "Asma / Broncoespasmos a repetición",
        "Celiaquía",
        "Problemas / Condiciones cardíacas",
        "Diabetes",
        "Presión arterial elevada",
        "Convulsiones",
        "Alteraciones sanguíneas",
        "Quemaduras moderadas o severas",
        "Falta o no funcionamiento de algún órgano",
        "Enfermedad oncohematológica",
        "Inmunodeficiencias (bajas defensas) por enfermedad o medicamentos",
        "Fracturas, luxaciones, lesiones ligamentarias previas",
        "Otro problema en los huesos o articulaciones",
        "Traumatismo de cráneo que haya requerido observación por guardia o internación",
        "Problemas de piel",
    ]
    
    checkbox_x_si = margin_left + 5*mm
    checkbox_x_no = margin_left + 20*mm
    
    for condicion in condiciones_salud:
        # Checkbox SI
        p.rect(checkbox_x_si, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Checkbox NO
        p.rect(checkbox_x_no, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Texto de la condición
        p.drawString(checkbox_x_no + 6*mm, y, condicion)
        y -= line_height * 0.8
        
        # Verificar si necesitamos nueva página
        if y < 30*mm:
            p.showPage()
            y = margin_top
    
    y -= line_height * 0.5
    
    # En relación con el ejercicio
    p.drawString(margin_left, y, "En relación con el ejercicio (durante o después), ha padecido alguna vez:")
    y -= line_height * 0.8
    
    sintomas_ejercicio = [
        "Mayor cansancio que sus compañeros o compañeras",
        "Palpitaciones",
        "Dificultad para respirar durante o después de la actividad física",
        "Desmayos",
        "Dolor fuerte en el pecho",
        "Mareos",
    ]
    
    for sintoma in sintomas_ejercicio:
        p.rect(checkbox_x_si, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.rect(checkbox_x_no, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x_no + 6*mm, y, sintoma)
        y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # ¿Tuvo alguna internación?
    p.drawString(margin_left, y, "¿Tuvo alguna internación? (Marcar por SI o por NO y en caso afirmativo, completar las últimas columnas)")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    tuvo_internacion = False  # Por ahora, no hay campo en el modelo
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if tuvo_internacion:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not tuvo_internacion:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    if tuvo_internacion:
        p.drawString(margin_left + 5*mm, y, "¿Cuántas veces?")
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "Internación en sala común")
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "Internación en sala de cuidados intermedios/intensivos")
        y -= line_height
    
    y -= line_height * 0.5
    
    # ¿Padece o ha padecido algún tipo de alergia grave?
    p.drawString(margin_left, y, "¿Padece o ha padecido algún tipo de alergia grave?")
    y -= line_height * 0.7
    
    checkbox_x = margin_left + 5*mm
    tiene_alergia = False  # Por ahora, no hay campo en el modelo
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if tiene_alergia:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    
    checkbox_x = margin_left + 15*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    if not tiene_alergia:
        p.setFont("Helvetica-Bold", 12)
        p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
        p.setFont("Helvetica", font_size_small)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 0.8
    
    if tiene_alergia:
        p.drawString(margin_left + 5*mm, y, "En caso afirmativo, ¿de qué tipo? (Marcar por SI o por NO)")
        y -= line_height * 0.8
        
        tipos_alergia = [
            ("Medicamentos", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
            ("Vacunas", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
            ("Alimentos", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
            ("Picaduras de insectos", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
            ("Estacionales (Polen, ácaros, polvo, etc)", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
            ("Otras", "SI", "NO", "¿Requirió internación?", "SI", "NO"),
        ]
        
        for tipo, si, no, req, si_req, no_req in tipos_alergia:
            p.drawString(margin_left + 5*mm, y, tipo)
            checkbox_x = margin_left + 60*mm
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, si)
            checkbox_x = margin_left + 70*mm
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, no)
            p.drawString(margin_left + 100*mm, y, req)
            checkbox_x = margin_left + 150*mm
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, si_req)
            checkbox_x = margin_left + 160*mm
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, no_req)
            y -= line_height * 0.8
    
    y -= line_height * 0.5
    
    # ¿Tiene disminución auditiva?
    p.drawString(margin_left, y, "¿Tiene disminución auditiva?")
    checkbox_x = margin_left + 60*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 70*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    p.drawString(margin_left + 80*mm, y, "En caso afirmativo: ¿Usa audífonos?")
    checkbox_x = margin_left + 150*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 160*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height
    
    # ¿Tiene disminución visual?
    p.drawString(margin_left, y, "¿Tiene disminución visual?")
    checkbox_x = margin_left + 60*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 70*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    p.drawString(margin_left + 80*mm, y, "En caso afirmativo: ¿Usa lentes?")
    checkbox_x = margin_left + 150*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 160*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height
    
    # ¿Recibe medicación habitual?
    p.drawString(margin_left, y, "¿Recibe de manera habitual algún tipo de medicación?")
    checkbox_x = margin_left + 80*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 90*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    p.drawString(margin_left + 100*mm, y, "En caso afirmativo, ¿cuál?")
    y -= line_height
    
    # ¿Tuvo alguna operación?
    p.drawString(margin_left, y, "¿Tuvo alguna operación?")
    checkbox_x = margin_left + 50*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 60*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height
    
    p.drawString(margin_left, y, "En caso afirmativo, ¿por qué motivo?")
    p.drawString(margin_left + 70*mm, y, "")
    p.drawString(margin_left + 140*mm, y, "¿en qué año?")
    p.drawString(margin_left + 160*mm, y, "")
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== DATOS DE LA PERSONA RESPONSABLE 1 ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DATOS DE LA PERSONA RESPONSABLE 1")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    # Vínculo con el estudiante
    p.drawString(margin_left, y, "Vínculo con el estudiante:")
    y -= line_height * 0.7
    
    vinculos = ['Madre', 'Padre', 'Tutor', 'Tutora', 'Otro']
    checkbox_x = margin_left + 5*mm
    responsable_principal = alumno.get_responsable_principal()
    
    for vinculo in vinculos:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Determinar vínculo
        marcado = False
        if responsable_principal:
            if vinculo == 'Madre' and hasattr(responsable_principal, 'apellido_madre'):
                marcado = True
            elif vinculo == 'Padre' and hasattr(responsable_principal, 'apellido_padre'):
                marcado = True
            elif vinculo in ['Tutor', 'Tutora'] and hasattr(responsable_principal, 'apellido_tutor'):
                marcado = True
        
        if marcado:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, vinculo)
        y -= line_height * 0.8
    
    y -= line_height * 0.3
    
    # Datos del responsable
    if responsable_principal:
        p.drawString(margin_left, y, "Apellido/s:")
        if hasattr(responsable_principal, 'apellido_madre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.apellido_madre or '')
        elif hasattr(responsable_principal, 'apellido_padre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.apellido_padre or '')
        elif hasattr(responsable_principal, 'apellido_tutor'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.apellido_tutor or '')
        y -= line_height
        
        p.drawString(margin_left, y, "Nombre/s:")
        if hasattr(responsable_principal, 'nombre_madre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nombre_madre or '')
        elif hasattr(responsable_principal, 'nombre_padre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nombre_padre or '')
        elif hasattr(responsable_principal, 'nombre_tutor'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nombre_tutor or '')
        y -= line_height
        
        p.drawString(margin_left, y, "SI, tipo de doc:")
        y -= line_height
        
        p.drawString(margin_left, y, "N°:")
        if hasattr(responsable_principal, 'dni_madre'):
            p.drawString(margin_left + 15*mm, y, str(responsable_principal.dni_madre) if responsable_principal.dni_madre else '')
        elif hasattr(responsable_principal, 'dni_padre'):
            p.drawString(margin_left + 15*mm, y, str(responsable_principal.dni_padre) if responsable_principal.dni_padre else '')
        elif hasattr(responsable_principal, 'dni_tutor'):
            p.drawString(margin_left + 15*mm, y, str(responsable_principal.dni_tutor) if responsable_principal.dni_tutor else '')
        y -= line_height
        
        p.drawString(margin_left, y, "Nacionalidad:")
        if hasattr(responsable_principal, 'nacionalidad_madre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nacionalidad_madre or 'Argentina')
        elif hasattr(responsable_principal, 'nacionalidad_padre'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nacionalidad_padre or 'Argentina')
        elif hasattr(responsable_principal, 'nacionalidad_tutor'):
            p.drawString(margin_left + 30*mm, y, responsable_principal.nacionalidad_tutor or 'Argentina')
        y -= line_height
        
        # ¿Posee DNI argentino? (similar al estudiante)
        p.drawString(margin_left, y, "¿Posee DNI argentino?")
        y -= line_height * 0.7
        
        checkbox_x = margin_left + 5*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "Si, y tiene el DNI físico")
        checkbox_x = margin_left + 50*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI, pero NO tiene el DNI físico")
        checkbox_x = margin_left + 100*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO posee DNI argentino")
        y -= line_height * 0.8
        
        # Número de DNI
        p.drawString(margin_left, y, "Si respondió SI, indique número de DNI argentino:")
        dni_resp = ''
        if hasattr(responsable_principal, 'dni_madre') and responsable_principal.dni_madre:
            dni_resp = str(responsable_principal.dni_madre)
        elif hasattr(responsable_principal, 'dni_padre') and responsable_principal.dni_padre:
            dni_resp = str(responsable_principal.dni_padre)
        elif hasattr(responsable_principal, 'dni_tutor') and responsable_principal.dni_tutor:
            dni_resp = str(responsable_principal.dni_tutor)
        if dni_resp and len(dni_resp) >= 7:
            dni_resp = f"{dni_resp[:2]}.{dni_resp[2:5]}.{dni_resp[5:]}"
        p.drawString(margin_left + 80*mm, y, dni_resp)
        y -= line_height
        
        # Certificado de Pre-Identificación
        p.drawString(margin_left, y, "Si respondió que NO tiene DNI argentino:")
        y -= line_height
        
        p.drawString(margin_left, y, "¿Posee certificado de Pre-Identificación (CPI)?")
        checkbox_x = margin_left + 80*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI")
        checkbox_x = margin_left + 90*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO")
        y -= line_height
        
        p.drawString(margin_left, y, "¿Posee documento extranjero?")
        checkbox_x = margin_left + 60*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI, tipo de doc:")
        p.drawString(margin_left + 100*mm, y, "")
        p.drawString(margin_left + 120*mm, y, "N°:")
        p.drawString(margin_left + 130*mm, y, "")
        checkbox_x = margin_left + 150*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO")
        y -= line_height
        
        p.drawString(margin_left, y, "Profesión u ocupación:")
        if hasattr(responsable_principal, 'profesion_madre'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.profesion_madre or '')
        elif hasattr(responsable_principal, 'profesion_padre'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.profesion_padre or '')
        elif hasattr(responsable_principal, 'profesion_tutor'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.profesion_tutor or '')
        y -= line_height
        
        # ¿Asistió a algún establecimiento educativo?
        p.drawString(margin_left, y, "¿Asistió a algún establecimiento educativo?")
        checkbox_x = margin_left + 70*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI")
        checkbox_x = margin_left + 80*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO")
        y -= line_height
        
        p.drawString(margin_left + 5*mm, y, "En caso afirmativo: ¿Cuál es el nivel más alto que cursó?")
        y -= line_height * 0.7
        
        niveles = ["Primario", "Secundario", "Superior", "Superior Universitario", "Posgrado"]
        checkbox_x = margin_left + 5*mm
        for nivel in niveles:
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, nivel)
            checkbox_x += 35*mm
        y -= line_height * 0.8
        
        p.drawString(margin_left + 5*mm, y, "¿Completó ese nivel?")
        checkbox_x = margin_left + 60*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI")
        checkbox_x = margin_left + 70*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO")
        y -= line_height * 1.2
        
        # CONDICIÓN DE ACTIVIDAD
        p.setFont("Helvetica-Bold", font_size_small)
        p.drawString(margin_left, y, "CONDICIÓN DE ACTIVIDAD")
        p.setFont("Helvetica", font_size_small)
        p.drawString(margin_left + 50*mm, y, "(Marcar todas las opciones que correspondan)")
        y -= line_height * 0.7
        
        condiciones_actividad = ["Estudia", "Trabaja", "Busca trabajo", "Realiza tareas de cuidado no pagas", "Recibe jubilación o pensión"]
        checkbox_x = margin_left + 5*mm
        for condicion in condiciones_actividad:
            p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
            p.drawString(checkbox_x + 6*mm, y, condicion)
            checkbox_x += 35*mm
        y -= line_height * 1.2
        
        # DOMICILIO del responsable
        p.setFont("Helvetica-Bold", font_size_small)
        p.drawString(margin_left, y, "DOMICILIO")
        p.setFont("Helvetica", font_size_small)
        p.drawString(margin_left + 30*mm, y, "Convive con el estudiante:")
        checkbox_x = margin_left + 80*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "SI")
        checkbox_x = margin_left + 90*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, "NO")
        p.drawString(margin_left + 100*mm, y, "(En caso afirmativo no completar los datos referidos al domicilio)")
        y -= line_height
        
        p.drawString(margin_left, y, "Calle:")
        if hasattr(responsable_principal, 'direccion_madre'):
            p.drawString(margin_left + 20*mm, y, responsable_principal.direccion_madre or '')
        elif hasattr(responsable_principal, 'direccion_padre'):
            p.drawString(margin_left + 20*mm, y, responsable_principal.direccion_padre or '')
        elif hasattr(responsable_principal, 'direccion_tutor'):
            p.drawString(margin_left + 20*mm, y, responsable_principal.direccion_tutor or '')
        p.drawString(margin_left + 80*mm, y, "N°:")
        p.drawString(margin_left + 90*mm, y, "")
        p.drawString(margin_left + 100*mm, y, "Piso:")
        p.drawString(margin_left + 110*mm, y, "")
        p.drawString(margin_left + 120*mm, y, "Torre:")
        p.drawString(margin_left + 130*mm, y, "")
        p.drawString(margin_left + 140*mm, y, "Depto:")
        y -= line_height
        
        p.drawString(margin_left, y, "Entre calle:")
        p.drawString(margin_left + 30*mm, y, "")
        p.drawString(margin_left + 80*mm, y, "Y calle:")
        p.drawString(margin_left + 90*mm, y, "")
        p.drawString(margin_left + 120*mm, y, "Otro dato:")
        y -= line_height
        
        p.drawString(margin_left, y, "Provincia:")
        p.drawString(margin_left + 30*mm, y, "")
        p.drawString(margin_left + 80*mm, y, "Distrito:")
        p.drawString(margin_left + 100*mm, y, "")
        p.drawString(margin_left + 130*mm, y, "Localidad:")
        y -= line_height
        
        p.drawString(margin_left, y, "Teléfono:")
        p.drawString(margin_left + 30*mm, y, "Cod. área:")
        p.drawString(margin_left + 50*mm, y, "")
        p.drawString(margin_left + 60*mm, y, "N°:")
        if hasattr(responsable_principal, 'telefono_madre'):
            p.drawString(margin_left + 70*mm, y, responsable_principal.telefono_madre or '')
        elif hasattr(responsable_principal, 'telefono_padre'):
            p.drawString(margin_left + 70*mm, y, responsable_principal.telefono_padre or '')
        elif hasattr(responsable_principal, 'telefono_tutor'):
            p.drawString(margin_left + 70*mm, y, responsable_principal.telefono_tutor or '')
        p.drawString(margin_left + 100*mm, y, "Teléfono celular:")
        p.drawString(margin_left + 140*mm, y, "Cod. área:")
        p.drawString(margin_left + 155*mm, y, "")
        p.drawString(margin_left + 165*mm, y, "N°:")
        if hasattr(responsable_principal, 'celular_madre'):
            p.drawString(margin_left + 175*mm, y, responsable_principal.celular_madre or '')
        elif hasattr(responsable_principal, 'celular_padre'):
            p.drawString(margin_left + 175*mm, y, responsable_principal.celular_padre or '')
        elif hasattr(responsable_principal, 'celular_tutor'):
            p.drawString(margin_left + 175*mm, y, responsable_principal.celular_tutor or '')
        y -= line_height
        
        p.drawString(margin_left, y, "Correo electrónico:")
        if hasattr(responsable_principal, 'email_madre'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.email_madre or '')
        elif hasattr(responsable_principal, 'email_padre'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.email_padre or '')
        elif hasattr(responsable_principal, 'email_tutor'):
            p.drawString(margin_left + 50*mm, y, responsable_principal.email_tutor or '')
        y -= line_height
    
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== DATOS DE LA PERSONA RESPONSABLE 2 ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DATOS DE LA PERSONA RESPONSABLE 2")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    # Vínculo con el estudiante
    p.drawString(margin_left, y, "Vínculo con el estudiante:")
    y -= line_height * 0.7
    
    vinculos = ['Madre', 'Padre', 'Tutor', 'Tutora', 'Otro']
    checkbox_x = margin_left + 5*mm
    
    # Determinar segundo responsable (si existe)
    segundo_responsable = None
    if alumno.madre and alumno.padre:
        # Si hay madre y padre, el segundo es el padre
        segundo_responsable = alumno.padre
    elif alumno.tutor and (alumno.madre or alumno.padre):
        segundo_responsable = alumno.tutor
    
    for vinculo in vinculos:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Determinar vínculo
        marcado = False
        if segundo_responsable:
            if vinculo == 'Padre' and hasattr(segundo_responsable, 'apellido_padre'):
                marcado = True
            elif vinculo == 'Tutor' and hasattr(segundo_responsable, 'apellido_tutor'):
                marcado = True
        
        if marcado:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, vinculo)
        y -= line_height * 0.8
    
    y -= line_height * 0.3
    
    # Datos del segundo responsable
    if segundo_responsable:
        p.drawString(margin_left, y, "Apellido/s:")
        if hasattr(segundo_responsable, 'apellido_padre'):
            p.drawString(margin_left + 30*mm, y, segundo_responsable.apellido_padre or '')
        elif hasattr(segundo_responsable, 'apellido_tutor'):
            p.drawString(margin_left + 30*mm, y, segundo_responsable.apellido_tutor or '')
        y -= line_height
        
        p.drawString(margin_left, y, "Nombre/s:")
        if hasattr(segundo_responsable, 'nombre_padre'):
            p.drawString(margin_left + 30*mm, y, segundo_responsable.nombre_padre or '')
        elif hasattr(segundo_responsable, 'nombre_tutor'):
            p.drawString(margin_left + 30*mm, y, segundo_responsable.nombre_tutor or '')
        y -= line_height
        
        p.drawString(margin_left, y, "SI, tipo de doc:")
        y -= line_height
        
        p.drawString(margin_left, y, "N°:")
        if hasattr(segundo_responsable, 'dni_padre'):
            p.drawString(margin_left + 15*mm, y, str(segundo_responsable.dni_padre) if segundo_responsable.dni_padre else '')
        elif hasattr(segundo_responsable, 'dni_tutor'):
            p.drawString(margin_left + 15*mm, y, str(segundo_responsable.dni_tutor) if segundo_responsable.dni_tutor else '')
        y -= line_height
        
        p.drawString(margin_left, y, "Profesión u ocupación:")
        if hasattr(segundo_responsable, 'profesion_padre'):
            p.drawString(margin_left + 50*mm, y, segundo_responsable.profesion_padre or '')
        elif hasattr(segundo_responsable, 'profesion_tutor'):
            p.drawString(margin_left + 50*mm, y, segundo_responsable.profesion_tutor or '')
        y -= line_height
    
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== ANTECEDENTES FAMILIARES DE SALUD ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "ANTECEDENTES FAMILIARES DE SALUD")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "¿Algún familiar directo padece o ha padecido alguna o algunas de las siguientes condiciones de salud? (Marcar por SI o por NO)")
    y -= line_height * 0.8
    
    condiciones_familiares = [
        "Muerte súbita de un familiar directo menor de 50 años",
        "Diabetes",
        "Problemas cardíacos",
        "Tos crónica",
        "Celiaquía",
    ]
    
    checkbox_x_si = margin_left + 5*mm
    checkbox_x_no = margin_left + 20*mm
    
    for condicion in condiciones_familiares:
        p.rect(checkbox_x_si, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.rect(checkbox_x_no, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x_no + 6*mm, y, condicion)
        y -= line_height * 0.8
    
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== DATOS DEL ESTABLECIMIENTO EN EL QUE SE INSCRIBE ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DATOS DEL ESTABLECIMIENTO EN EL QUE SE INSCRIBE")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "Distrito:")
    p.drawString(margin_left + 30*mm, y, "Lanús")  # TODO: obtener del sistema
    
    p.drawString(margin_left + 100*mm, y, "Sector de gestión:")
    checkbox_x = margin_left + 140*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "Estatal")
    checkbox_x = margin_left + 160*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "Privado")
    y -= line_height
    
    p.drawString(margin_left, y, "Nombre escuela:")
    p.drawString(margin_left + 40*mm, y, "Sagrado Corazón ALCAL")
    p.drawString(margin_left + 140*mm, y, "N°:")
    p.drawString(margin_left + 150*mm, y, "4883")
    y -= line_height
    
    p.drawString(margin_left, y, "A completar por el establecimiento:")
    p.drawString(margin_left + 70*mm, y, "Clave provincial")
    p.drawString(margin_left + 120*mm, y, "4111MS4883")
    p.drawString(margin_left + 160*mm, y, "CUE:")
    p.drawString(margin_left + 175*mm, y, "60782300")
    y -= line_height * 1.5
    
    # ========== DATOS DEL ESTABLECIMIENTO DE PROCEDENCIA ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "DATOS DEL ESTABLECIMIENTO DE PROCEDENCIA")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "(Completar solo si el año pasado o este año asistió a otro establecimiento)")
    y -= line_height
    
    p.drawString(margin_left, y, "País:")
    checkbox_x = margin_left + 20*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "Argentina")
    p.drawString(margin_left + 50*mm, y, "Otro país (especificar):")
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Solo para los que marcaron opción Argentina:")
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Provincia:")
    p.drawString(margin_left + 40*mm, y, alumno.provincia or 'Buenos Aires')
    p.drawString(margin_left + 100*mm, y, "Otra (especificar):")
    p.drawString(margin_left + 160*mm, y, "Distrito:")
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Nivel/Modalidad:")
    checkbox_x = margin_left + 50*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "E.P")
    p.drawString(margin_left + 100*mm, y, "Sector de gestión:")
    checkbox_x = margin_left + 140*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "Estatal")
    checkbox_x = margin_left + 160*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "Privado")
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Dependencia:")
    opciones_dep = ["Oficial", "Municipal", "Nacional", "Privada", "Otros organismos"]
    checkbox_x = margin_left + 40*mm
    for dep in opciones_dep:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, dep)
        checkbox_x += 30*mm
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Nombre escuela:")
    p.drawString(margin_left + 50*mm, y, alumno.colegio_procedencia or '')
    p.drawString(margin_left + 140*mm, y, "N°:")
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== INSCRIPCIÓN ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "INSCRIPCIÓN")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "Se inscribe en:")
    opciones_inscripcion = ["Ciclo Básico", "Ciclo Superior", "Aula de Fortalecimiento", "Escuela Profesional Secundaria"]
    checkbox_x = margin_left + 40*mm
    for opcion in opciones_inscripcion:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, opcion)
        checkbox_x += 35*mm
    y -= line_height
    
    p.drawString(margin_left, y, "Orientación:")
    carrera_nombre = alumno.curso.carrera.nombre if alumno.curso and alumno.curso.carrera else ''
    p.drawString(margin_left + 30*mm, y, carrera_nombre)
    p.drawString(margin_left + 120*mm, y, "Año:")
    años = ["1", "2", "3", "4", "5", "6", "7"]
    checkbox_x = margin_left + 140*mm
    for año in años:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Marcar el año correspondiente al curso
        if alumno.curso and str(año) in alumno.curso.curso:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, año)
        checkbox_x += 8*mm
    y -= line_height
    
    p.drawString(margin_left, y, "Turno solicitado:")
    turnos = ["Mañana", "Tarde", "Vespertino", "Noche"]
    checkbox_x = margin_left + 40*mm
    for turno in turnos:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, turno)
        checkbox_x += 25*mm
    y -= line_height
    
    p.drawString(margin_left, y, "Jornada:")
    jornadas = ["Simple", "Extendida", "Completa / Doble escolaridad"]
    checkbox_x = margin_left + 30*mm
    for jornada in jornadas:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, jornada)
        checkbox_x += 40*mm
    y -= line_height * 1.5
    
    # ========== CONDICIÓN EN LA INSCRIPCIÓN ACTUAL ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "CONDICIÓN EN LA INSCRIPCIÓN ACTUAL (Marcar solo una opción)")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    condiciones = ["Ingresante a Nivel", "Promovida / Promovido", "Reinscripta / Reinscripto", "Repitente"]
    checkbox_x = margin_left + 5*mm
    for condicion in condiciones:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        # Marcar según el estado del alumno
        if condicion == "Reinscripta / Reinscripto" and not alumno.activo:
            p.setFont("Helvetica-Bold", 12)
            p.drawString(checkbox_x + 0.5*mm, y - 0.5*mm, "X")
            p.setFont("Helvetica", font_size_small)
        p.drawString(checkbox_x + 6*mm, y, condicion)
        checkbox_x += 45*mm
    y -= line_height * 1.5
    
    # ========== INCLUSIÓN ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "INCLUSIÓN")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "¿Cursa con proyecto de inclusión?")
    checkbox_x = margin_left + 70*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 80*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height
    
    p.drawString(margin_left + 5*mm, y, "Si la respuesta es afirmativa, marque con un cruz lo que corresponda:")
    y -= line_height
    
    opciones_inclusion = [
        "Concurre a una Escuela Especial a contraturno y cuenta con acompañamiento de maestra o maestro de inclusión",
        "No concurre a una Escuela Especial pero cuenta con acompañamiento de maestra o maestro de inclusión",
    ]
    checkbox_x = margin_left + 5*mm
    for opcion in opciones_inclusion:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, opcion)
        y -= line_height * 0.8
    
    p.drawString(margin_left, y, "¿Cursa con acompañante asistente externo?")
    checkbox_x = margin_left + 80*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "SI")
    checkbox_x = margin_left + 90*mm
    p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
    p.drawString(checkbox_x + 6*mm, y, "NO")
    y -= line_height * 1.5
    
    p.drawString(margin_left, y, "¿Asiste a algun de las siguientes instituciones?")
    y -= line_height
    
    instituciones = [
        ("Centro Educativo Complementario (CEC):", "SI", "NO"),
        ("Centro de Educación Física (CEF):", "SI", "NO"),
        ("Escuela de Educación Estética:", "SI", "NO"),
    ]
    for institucion, si, no in instituciones:
        p.drawString(margin_left, y, institucion)
        checkbox_x = margin_left + 80*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, si)
        checkbox_x = margin_left + 90*mm
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, no)
        y -= line_height * 0.8
    
    y -= line_height * 1.5
    
    # ========== SERVICIO ALIMENTARIO ESCOLAR ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "SERVICIO ALIMENTARIO ESCOLAR")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "En caso de que la institución cuente con el servicio")
    y -= line_height
    
    p.drawString(margin_left, y, "¿Solicita la incorporación en el Servicio Alimentario Escolar?")
    y -= line_height
    
    opciones_sae = ["Comedor", "Desayuno y Merienda"]
    checkbox_x = margin_left + 5*mm
    for opcion in opciones_sae:
        p.rect(checkbox_x, y - 1*mm, checkbox_size, checkbox_size, fill=0)
        p.drawString(checkbox_x + 6*mm, y, opcion)
        checkbox_x += 40*mm
    y -= line_height * 1.5
    
    # Verificar si necesitamos nueva página
    if y < 50*mm:
        p.showPage()
        y = margin_top
    
    # ========== RESTRICCIONES POR DECISIONES JUDICIALES ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "RESTRICCIONES POR DECISIONES JUDICIALES")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "Apellido/s:")
    p.drawString(margin_left + 30*mm, y, "")
    y -= line_height
    
    p.drawString(margin_left, y, "Nombre/s:")
    p.drawString(margin_left + 30*mm, y, "")
    y -= line_height
    
    p.drawString(margin_left, y, "Tipo de doc:")
    p.drawString(margin_left + 40*mm, y, "")
    p.drawString(margin_left + 80*mm, y, "N°:")
    p.drawString(margin_left + 90*mm, y, "")
    y -= line_height
    
    p.drawString(margin_left, y, "Describa restricción:")
    y -= line_height * 2
    
    p.drawString(margin_left, y, "La restricción solo operará en caso de acompañarse la resolución judicial certificada.")
    y -= line_height * 1.5
    
    # ========== A COMPLETAR POR LA INSTITUCIÓN ==========
    p.setFont("Helvetica-Bold", font_size_normal)
    p.drawString(margin_left, y, "A COMPLETAR POR LA INSTITUCIÓN")
    y -= line_height
    
    p.setFont("Helvetica", font_size_small)
    p.drawString(margin_left, y, "N° de Legajo:")
    p.drawString(margin_left + 40*mm, y, str(alumno.legajo))
    p.drawString(margin_left + 100*mm, y, "N° de Matriz:")
    p.drawString(margin_left + 150*mm, y, "")
    y -= line_height
    
    p.drawString(margin_left, y, "N° de Folio:")
    p.drawString(margin_left + 40*mm, y, "")
    y -= line_height * 2
    
    p.drawString(margin_left, y, "La totalidad de los datos e información suministrada por quien suscribe la presente tiene carácter de Declaración Jurada.")
    y -= line_height * 0.7
    
    p.drawString(margin_left, y, "La persona abajo firmante se compromete a comunicar al establecimiento cualquier modificación de los datos suministrados en forma inmediata y de manera fehaciente")
    y -= line_height * 1.5
    
    p.drawString(margin_left, y, "Firma persona responsable:")
    p.drawString(margin_left + 60*mm, y, "")
    p.drawString(margin_left + 120*mm, y, "Aclaración:")
    p.drawString(margin_left + 160*mm, y, "")
    y -= line_height
    
    p.drawString(margin_left, y, "Fecha de inscripción:")
    fecha_insc = datetime.now().strftime('%d/%m/%Y')
    p.drawString(margin_left + 50*mm, y, fecha_insc)
    p.drawString(margin_left + 120*mm, y, "Firma Directora o Director:")
    y -= line_height * 1.5
    
    # ========== PIE DE PÁGINA - DOCUMENTACIÓN OBLIGATORIA ==========
    # Esta sección va al final del formulario
    # Por ahora, solo agregamos espacio para que quepa todo
    
    # Finalizar página
    p.showPage()
    
    # Segunda página con documentación obligatoria
    y = margin_top
    
    p.setFont("Helvetica-Bold", font_size_title)
    p.drawString(margin_left, y, "DOCUMENTACIÓN OBLIGATORIA PARA EL LEGAJO")
    y -= 2*line_height
    
    p.setFont("Helvetica", font_size_small)
    documentos = [
        "FICHA DE INSCRIPCIÓN",
        "FECHA",
        "DNI DEL ESTUDIANTE",
        "PARTIDA DE NACIMIENTO",
        "FIRMA RESPONSABLE",
        "CERTIFICADO DE VACUNACIÓN",
        "DNI DEL ADULTO RESPONSABLE",
        "DOCUMENTACIÓN ACADÉMICA PROVISORIA",
        "DOCUMENTACIÓN ACADÉMICA DEFINITIVA",
        "CONS. AN. PARCIAL EN TRÁMITE",
        "CERTIFICADO 6º",
    ]
    
    for doc in documentos:
        p.drawString(margin_left, y, doc)
        # Línea para completar
        p.line(margin_left + 60*mm, y + 2*mm, width - margin_left, y + 2*mm)
        y -= line_height * 1.5
    
    # Finalizar el PDF
    p.save()
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response


def generar_constancia_alumno_regular(alumno):
    """
    Genera un PDF con la constancia de alumno regular.
    
    Args:
        alumno: Instancia del modelo Alumno
        
    Returns:
        HttpResponse con el PDF generado
    """
    from django.utils.text import slugify
    filename = f"constancia_alumno_regular_{slugify(alumno.apellido)}_{slugify(alumno.nombre)}.pdf"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Crear el PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2.5*cm, bottomMargin=2.5*cm, leftMargin=2.5*cm, rightMargin=2.5*cm)
    
    # Estilos
    styles = getSampleStyleSheet()
    style_titulo = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.black,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    style_cuerpo = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        spaceAfter=12,
        alignment=TA_LEFT, # Justificado sería ideal pero reportlab básico usa LEFT
        fontName='Helvetica'
    )
    style_firma = ParagraphStyle(
        'CustomSignature',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        spaceBefore=50,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    
    # Elementos del documento
    elementos = []
    
    # Título
    titulo = Paragraph("CONSTANCIA DE ALUMNO REGULAR", style_titulo)
    elementos.append(titulo)
    elementos.append(Spacer(1, 1*cm))
    
    # Cuerpo del texto
    fecha_actual = datetime.now().strftime('%d de %B de %Y')
    
    # Mapeo de meses para español (simple)
    meses = {
        'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
        'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
        'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
    }
    fecha_obj = datetime.now()
    mes_nombre = fecha_obj.strftime('%B')
    mes_espanol = meses.get(mes_nombre, mes_nombre)
    fecha_texto = f"{fecha_obj.day} de {mes_espanol} de {fecha_obj.year}"
    
    texto = f"""
    Por la presente se hace constar que <b>{alumno.apellido}, {alumno.nombre}</b>, 
    DNI N° <b>{alumno.dni}</b>, es alumno regular de este establecimiento, 
    cursando actualmente <b>{alumno.curso}</b> de la carrera <b>{alumno.curso.carrera.nombre if alumno.curso and alumno.curso.carrera else ''}</b>.
    """
    
    elementos.append(Paragraph(texto.strip(), style_cuerpo))
    elementos.append(Spacer(1, 0.5*cm))
    
    texto_cierre = f"""
    Se extiende la presente constancia a pedido del interesado/a para ser presentada ante quien corresponda, 
    en la ciudad de [Ciudad], a los {fecha_texto}.
    """
    elementos.append(Paragraph(texto_cierre.strip(), style_cuerpo))
    
    # Espacio para firma
    elementos.append(Spacer(1, 4*cm))
    
    elementos.append(Paragraph("______________________________________", style_firma))
    elementos.append(Paragraph("Firma y Sello de la Autoridad", style_firma))
    
    # Construir el PDF
    doc.build(elementos)
    
    # Obtener el valor del buffer y escribirlo en la respuesta
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response
