# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count

from escuela.models import Carrera, Curso, Materia, Anio
from docentes.models import Docente
from alumnos.models import Alumno
from asistencias.models import Turno, CodigoAsistencia

# ==================== DASHBOARD ====================

@login_required
def dashboard(request):
    """Dashboard principal de la administración"""
    context = {
        'total_carreras': Carrera.objects.count(),
        'total_cursos': Curso.objects.count(),
        'total_materias': Materia.objects.count(),
        'total_docentes': Docente.objects.count(),
        'total_alumnos': Alumno.objects.count(),
        'total_turnos': Turno.objects.count(),
    }
    return render(request, 'administracion/dashboard.html', context)


# ==================== CARRERAS ====================

@login_required
def carrera_list(request):
    """Lista de carreras con búsqueda"""
    search =request.GET.get('q', '')
    carreras = Carrera.objects.all()
    
    if search:
        carreras = carreras.filter(nombre__icontains=search)
    
    carreras = carreras.order_by('nombre')
    
    context = {
        'carreras': carreras,
        'search': search,
    }
    return render(request, 'administracion/carreras/list.html', context)


@login_required
def carrera_create(request):
    """Crear nueva carrera"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        
        if nombre:
            Carrera.objects.create(nombre=nombre)
            messages.success(request, f'Carrera "{nombre}" creada exitosamente.')
            return redirect('administracion:carrera_list')
        else:
            messages.error(request, 'El nombre de la carrera es requerido.')
    
    return render(request, 'administracion/carreras/form.html', {'action': 'Crear'})


@login_required
def carrera_update(request, pk):
    """Editar carrera"""
    carrera = get_object_or_404(Carrera, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        
        if nombre:
            carrera.nombre = nombre
            carrera.save()
            messages.success(request, f'Carrera actualizada exitosamente.')
            return redirect('administracion:carrera_list')
        else:
            messages.error(request, 'El nombre de la carrera es requerido.')
    
    context = {
        'carrera': carrera,
        'action': 'Editar',
    }
    return render(request, 'administracion/carreras/form.html', context)


@login_required
def carrera_delete(request, pk):
    """Eliminar carrera"""
    carrera = get_object_or_404(Carrera, pk=pk)
    
    if request.method == 'POST':
        nombre = carrera.nombre
        try:
            carrera.delete()
            messages.success(request, f'Carrera "{nombre}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la carrera: {str(e)}')
        return redirect('administracion:carrera_list')
    
    context = {
        'carrera': carrera,
        'cursos_count': Curso.objects.filter(carrera=carrera).count(),
    }
    return render(request, 'administracion/carreras/delete.html', context)


# ==================== CURSOS ====================

@login_required
def curso_list(request):
    """Lista de cursos con búsqueda"""
    search = request.GET.get('q', '')
    carrera_id = request.GET.get('carrera', '')
    
    cursos = Curso.objects.select_related('carrera').all()
    
    if search:
        cursos = cursos.filter(curso__icontains=search)
    
    if carrera_id:
        cursos = cursos.filter(carrera_id=carrera_id)
    
    cursos = cursos.order_by('curso')
    
    context = {
        'cursos': cursos,
        'search': search,
        'carreras': Carrera.objects.all(),
        'carrera_id': carrera_id,
    }
    return render(request, 'administracion/cursos/list.html', context)


@login_required
def curso_create(request):
    """Crear nuevo curso"""
    if request.method == 'POST':
        curso_nombre = request.POST.get('curso', '').strip()
        carrera_id = request.POST.get('carrera')
        
        if curso_nombre and carrera_id:
            carrera = get_object_or_404(Carrera, pk=carrera_id)
            Curso.objects.create(curso=curso_nombre, carrera=carrera)
            messages.success(request, f'Curso "{curso_nombre}" creado exitosamente.')
            return redirect('administracion:curso_list')
        else:
            messages.error(request, 'Todos los campos son requeridos.')
    
    context = {
        'carreras': Carrera.objects.all(),
        'action': 'Crear',
    }
    return render(request, 'administracion/cursos/form.html', context)


@login_required
def curso_update(request, pk):
    """Editar curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        curso_nombre = request.POST.get('curso', '').strip()
        carrera_id = request.POST.get('carrera')
        
        if curso_nombre and carrera_id:
            curso.curso = curso_nombre
            curso.carrera = get_object_or_404(Carrera, pk=carrera_id)
            curso.save()
            messages.success(request, f'Curso actualizado exitosamente.')
            return redirect('administracion:curso_list')
        else:
            messages.error(request, 'Todos los campos son requeridos.')
    
    context = {
        'curso': curso,
        'carreras': Carrera.objects.all(),
        'action': 'Editar',
    }
    return render(request, 'administracion/cursos/form.html', context)


@login_required
def curso_delete(request, pk):
    """Eliminar curso"""
    curso = get_object_or_404(Curso, pk=pk)
    
    if request.method == 'POST':
        nombre = curso.curso
        try:
            curso.delete()
            messages.success(request, f'Curso "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el curso: {str(e)}')
        return redirect('administracion:curso_list')
    
    context = {
        'curso': curso,
        'alumnos_count': Alumno.objects.filter(curso=curso).count(),
        'materias_count': Materia.objects.filter(curso=curso).count(),
    }
    return render(request, 'administracion/cursos/delete.html', context)


# ==================== MATERIAS ====================

@login_required
def materia_list(request):
    """Lista de materias con búsqueda"""
    search = request.GET.get('q', '')
    curso_id = request.GET.get('curso', '')
    
    materias = Materia.objects.select_related('curso', 'curso__carrera').all()
    
    if search:
        materias = materias.filter(nombre__icontains=search)
    
    if curso_id:
        materias = materias.filter(curso_id=curso_id)
    
    materias = materias.order_by('curso__curso', 'nombre')
    
    # Paginar
    paginator = Paginator(materias, 20)
    page = request.GET.get('page', 1)
    materias_page = paginator.get_page(page)
    
    context = {
        'materias': materias_page,
        'search': search,
        'cursos': Curso.objects.all().order_by('curso'),
        'curso_id': curso_id,
    }
    return render(request, 'administracion/materias/list.html', context)


@login_required
def materia_create(request):
    """Crear nueva materia"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        curso_id = request.POST.get('curso')
        horas = request.POST.get('horas', '3')
        
        if nombre and curso_id:
            curso = get_object_or_404(Curso, pk=curso_id)
            Materia.objects.create(
                nombre=nombre,
                curso=curso,
                horas=int(horas) if horas.isdigit() else 3
            )
            messages.success(request, f'Materia "{nombre}" creada exitosamente.')
            return redirect('administracion:materia_list')
        else:
            messages.error(request, 'El nombre y el curso son requeridos.')
    
    context = {
        'cursos': Curso.objects.all().order_by('curso'),
        'action': 'Crear',
    }
    return render(request, 'administracion/materias/form.html', context)


@login_required
def materia_update(request, pk):
    """Editar materia"""
    materia = get_object_or_404(Materia, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        curso_id = request.POST.get('curso')
        horas = request.POST.get('horas', '3')
        
        if nombre and curso_id:
            materia.nombre = nombre
            materia.curso = get_object_or_404(Curso, pk=curso_id)
            materia.horas = int(horas) if horas.isdigit() else 3
            materia.save()
            messages.success(request, f'Materia actualizada exitosamente.')
            return redirect('administracion:materia_list')
        else:
            messages.error(request, 'El nombre y el curso son requeridos.')
    
    context = {
        'materia': materia,
        'cursos': Curso.objects.all().order_by('curso'),
        'action': 'Editar',
    }
    return render(request, 'administracion/materias/form.html', context)


@login_required
def materia_delete(request, pk):
    """Eliminar materia"""
    materia = get_object_or_404(Materia, pk=pk)
    
    if request.method == 'POST':
        nombre = materia.nombre
        try:
            materia.delete()
            messages.success(request, f'Materia "{nombre}" eliminada exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar la materia: {str(e)}')
        return redirect('administracion:materia_list')
    
    context = {
        'materia': materia,
        'docentes_count': materia.docente_set.count(),
    }
    return render(request, 'administracion/materias/delete.html', context)


# ==================== DOCENTES ====================

@login_required
def docente_list(request):
    """Lista de docentes con búsqueda"""
    search = request.GET.get('q', '')
    
    docentes = Docente.objects.prefetch_related('materia').all()
    
    if search:
        docentes = docentes.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(email__icontains=search) |
            Q(dni__icontains=search)
        )
    
    docentes = docentes.order_by('apellido', 'nombre')
    
    # Paginar
    paginator = Paginator(docentes, 20)
    page = request.GET.get('page', 1)
    docentes_page = paginator.get_page(page)
    
    context = {
        'docentes': docentes_page,
        'search': search,
    }
    return render(request, 'administracion/docentes/list.html', context)


@login_required
def docente_detail(request, pk):
    """Detalle de docente"""
    docente = get_object_or_404(Docente.objects.prefetch_related('materia__curso'), pk=pk)
    
    context = {
        'docente': docente,
    }
    return render(request, 'administracion/docentes/detail.html', context)


@login_required
def docente_create(request):
    """Crear nuevo docente"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        dni = request.POST.get('dni', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        nacionalidad = request.POST.get('nacionalidad', 'Argentina').strip()
        legajo = request.POST.get('legajo', '').strip()
        materias_ids = request.POST.getlist('materias')
        
        if nombre and apellido:
            docente = Docente.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=int(dni) if dni and dni.isdigit() else None,
                email=email if email else None,
                telefono=telefono,
                direccion=direccion,
                nacionalidad=nacionalidad,
                legajo=int(legajo) if legajo and legajo.isdigit() else (Docente.objects.count() + 1),
            )
            
            if materias_ids:
                materias = Materia.objects.filter(id__in=materias_ids)
                docente.materia.set(materias)
            
            messages.success(request, f'Docente "{nombre} {apellido}" creado exitosamente.')
            return redirect('administracion:docente_list')
        else:
            messages.error(request, 'El nombre y apellido son requeridos.')
    
    context = {
        'action': 'Crear',
        'materias': Materia.objects.all().order_by('curso__curso', 'nombre'),
    }
    return render(request, 'administracion/docentes/form.html', context)


@login_required
def docente_update(request, pk):
    """Editar docente"""
    docente = get_object_or_404(Docente, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        dni = request.POST.get('dni', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        nacionalidad = request.POST.get('nacionalidad', 'Argentina').strip()
        legajo = request.POST.get('legajo', '').strip()
        materias_ids = request.POST.getlist('materias')
        
        if nombre and apellido:
            docente.nombre = nombre
            docente.apellido = apellido
            docente.dni = int(dni) if dni and dni.isdigit() else None
            docente.email = email if email else None
            docente.telefono = telefono
            docente.direccion = direccion
            docente.nacionalidad = nacionalidad
            docente.legajo = int(legajo) if legajo and legajo.isdigit() else docente.legajo
            docente.save()
            
            if materias_ids:
                materias = Materia.objects.filter(id__in=materias_ids)
                docente.materia.set(materias)
            else:
                docente.materia.clear()
            
            messages.success(request, f'Docente actualizado exitosamente.')
            return redirect('administracion:docente_list')
        else:
            messages.error(request, 'El nombre y apellido son requeridos.')
    
    context = {
        'docente': docente,
        'action': 'Editar',
        'materias': Materia.objects.all().order_by('curso__curso', 'nombre'),
    }
    return render(request, 'administracion/docentes/form.html', context)


@login_required
def docente_delete(request, pk):
    """Eliminar docente"""
    docente = get_object_or_404(Docente, pk=pk)
    
    if request.method == 'POST':
        nombre = f"{docente.nombre} {docente.apellido}"
        try:
            docente.delete()
            messages.success(request, f'Docente "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el docente: {str(e)}')
        return redirect('administracion:docente_list')
    
    context = {
        'docente': docente,
    }
    return render(request, 'administracion/docentes/delete.html', context)


# ==================== ALUMNOS ====================

@login_required
def alumno_list(request):
    """Lista de alumnos con búsqueda"""
    search = request.GET.get('q', '')
    curso_id = request.GET.get('curso', '')
    
    alumnos = Alumno.objects.select_related('curso', 'curso__carrera').all()
    
    if search:
        alumnos = alumnos.filter(
            Q(nombre__icontains=search) |
            Q(apellido__icontains=search) |
            Q(dni__icontains=search) |
            Q(email__icontains=search)
        )
    
    if curso_id:
        alumnos = alumnos.filter(curso_id=curso_id)
    
    alumnos = alumnos.order_by('apellido', 'nombre')
    
    # Paginar
    paginator = Paginator(alumnos, 30)
    page = request.GET.get('page', 1)
    alumnos_page = paginator.get_page(page)
    
    context = {
        'alumnos': alumnos_page,
        'search': search,
        'cursos': Curso.objects.all().order_by('curso'),
        'curso_id': curso_id,
    }
    return render(request, 'administracion/alumnos/list.html', context)


@login_required
def alumno_detail(request, pk):
    """Detalle de alumno"""
    alumno = get_object_or_404(
        Alumno.objects.select_related('curso', 'padre', 'madre', 'tutor'), 
        pk=pk
    )
    
    context = {
        'alumno': alumno,
    }
    return render(request, 'administracion/alumnos/detail.html', context)


@login_required
def alumno_create(request):
    """Crear nuevo alumno"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        dni = request.POST.get('dni', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        nacionalidad = request.POST.get('nacionalidad', 'Argentina').strip()
        curso_id = request.POST.get('curso')
        activo = request.POST.get('activo') == 'on'
        libre = request.POST.get('libre') == 'on'
        condicional = request.POST.get('condicional') == 'on'
        
        if nombre and apellido and curso_id:
            curso = get_object_or_404(Curso, pk=curso_id)
            Alumno.objects.create(
                nombre=nombre,
                apellido=apellido,
                dni=int(dni) if dni and dni.isdigit() else None,
                email=email if email else None,
                telefono=telefono,
                direccion=direccion,
                nacionalidad=nacionalidad,
                curso=curso,
                activo=activo,
                libre=libre,
                condicional=condicional,
            )
            messages.success(request, f'Alumno "{nombre} {apellido}" creado exitosamente.')
            return redirect('administracion:alumno_list')
        else:
            messages.error(request, 'El nombre, apellido y curso son requeridos.')
    
    context = {
        'action': 'Crear',
        'cursos': Curso.objects.all().order_by('curso'),
    }
    return render(request, 'administracion/alumnos/form.html', context)


@login_required
def alumno_update(request, pk):
    """Editar alumno"""
    alumno = get_object_or_404(Alumno, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        dni = request.POST.get('dni', '').strip()
        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        nacionalidad = request.POST.get('nacionalidad', 'Argentina').strip()
        curso_id = request.POST.get('curso')
        activo = request.POST.get('activo') == 'on'
        libre = request.POST.get('libre') == 'on'
        condicional = request.POST.get('condicional') == 'on'
        
        if nombre and apellido and curso_id:
            alumno.nombre = nombre
            alumno.apellido = apellido
            alumno.dni = int(dni) if dni and dni.isdigit() else None
            alumno.email = email if email else None
            alumno.telefono = telefono
            alumno.direccion = direccion
            alumno.nacionalidad = nacionalidad
            alumno.curso = get_object_or_404(Curso, pk=curso_id)
            alumno.activo = activo
            alumno.libre = libre
            alumno.condicional = condicional
            alumno.save()
            messages.success(request, f'Alumno actualizado exitosamente.')
            return redirect('administracion:alumno_list')
        else:
            messages.error(request, 'El nombre, apellido y curso son requeridos.')
    
    context = {
        'alumno': alumno,
        'action': 'Editar',
        'cursos': Curso.objects.all().order_by('curso'),
    }
    return render(request, 'administracion/alumnos/form.html', context)


@login_required
def alumno_delete(request, pk):
    """Eliminar alumno"""
    alumno = get_object_or_404(Alumno, pk=pk)
    
    if request.method == 'POST':
        nombre = f"{alumno.nombre} {alumno.apellido}"
        try:
            alumno.delete()
            messages.success(request, f'Alumno "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el alumno: {str(e)}')
        return redirect('administracion:alumno_list')
    
    context = {
        'alumno': alumno,
    }
    return render(request, 'administracion/alumnos/delete.html', context)


# ==================== TURNOS ====================

@login_required
def turno_list(request):
    """Lista de turnos"""
    turnos = Turno.objects.all().order_by('hora_inicio')
    
    context = {
        'turnos': turnos,
    }
    return render(request, 'administracion/turnos/list.html', context)


@login_required
def turno_create(request):
    """Crear nuevo turno"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        if nombre and hora_inicio and hora_fin:
            Turno.objects.create(
                nombre=nombre,
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
            )
            messages.success(request, f'Turno creado exitosamente.')
            return redirect('administracion:turno_list')
        else:
            messages.error(request, 'Todos los campos son requeridos.')
    
    context = {
        'action': 'Crear',
        'turno_choices': Turno.TURNO_CHOICES,
    }
    return render(request, 'administracion/turnos/form.html', context)


@login_required
def turno_update(request, pk):
    """Editar turno"""
    turno = get_object_or_404(Turno, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        
        if nombre and hora_inicio and hora_fin:
            turno.nombre = nombre
            turno.hora_inicio = hora_inicio
            turno.hora_fin = hora_fin
            turno.save()
            messages.success(request, f'Turno actualizado exitosamente.')
            return redirect('administracion:turno_list')
        else:
            messages.error(request, 'Todos los campos son requeridos.')
    
    context = {
        'turno': turno,
        'action': 'Editar',
        'turno_choices': Turno.TURNO_CHOICES,
    }
    return render(request, 'administracion/turnos/form.html', context)


@login_required
def turno_delete(request, pk):
    """Eliminar turno"""
    turno = get_object_or_404(Turno, pk=pk)
    
    if request.method == 'POST':
        nombre = turno.get_nombre_display()
        try:
            turno.delete()
            messages.success(request, f'Turno "{nombre}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el turno: {str(e)}')
        return redirect('administracion:turno_list')
    
    context = {
        'turno': turno,
    }
    return render(request, 'administracion/turnos/delete.html', context)


# ==================== CÓDIGOS DE ASISTENCIA ====================

@login_required
def codigo_asistencia_list(request):
    """Lista de códigos de asistencia"""
    codigos = CodigoAsistencia.objects.all().order_by('codigo')
    
    context = {
        'codigos': codigos,
    }
    return render(request, 'administracion/codigos/list.html', context)


@login_required
def codigo_asistencia_create(request):
    """Crear nuevo código de asistencia"""
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion', '').strip()
        cantidad_falta = request.POST.get('cantidad_falta', '0')
        
        if codigo and descripcion:
            try:
                CodigoAsistencia.objects.create(
                    codigo=codigo,
                    descripcion=descripcion,
                    cantidad_falta=float(cantidad_falta),
                )
                messages.success(request, f'Código de asistencia creado exitosamente.')
                return redirect('administracion:codigo_asistencia_list')
            except Exception as e:
                messages.error(request, f'Error al crear el código: {str(e)}')
        else:
            messages.error(request, 'El código y la descripción son requeridos.')
    
    context = {
        'action': 'Crear',
        'codigo_choices': CodigoAsistencia.CODIGO_CHOICES,
    }
    return render(request, 'administracion/codigos/form.html', context)


@login_required
def codigo_asistencia_update(request, pk):
    """Editar código de asistencia"""
    codigo_obj = get_object_or_404(CodigoAsistencia, pk=pk)
    
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion', '').strip()
        cantidad_falta = request.POST.get('cantidad_falta', '0')
        
        if codigo and descripcion:
            try:
                codigo_obj.codigo = codigo
                codigo_obj.descripcion = descripcion
                codigo_obj.cantidad_falta = float(cantidad_falta)
                codigo_obj.save()
                messages.success(request, f'Código de asistencia actualizado exitosamente.')
                return redirect('administracion:codigo_asistencia_list')
            except Exception as e:
                messages.error(request, f'Error al actualizar el código: {str(e)}')
        else:
            messages.error(request, 'El código y la descripción son requeridos.')
    
    context = {
        'codigo_obj': codigo_obj,
        'action': 'Editar',
        'codigo_choices': CodigoAsistencia.CODIGO_CHOICES,
    }
    return render(request, 'administracion/codigos/form.html', context)


@login_required
def codigo_asistencia_delete(request, pk):
    """Eliminar código de asistencia"""
    codigo_obj = get_object_or_404(CodigoAsistencia, pk=pk)
    
    if request.method == 'POST':
        descripcion = codigo_obj.descripcion
        try:
            codigo_obj.delete()
            messages.success(request, f'Código "{descripcion}" eliminado exitosamente.')
        except Exception as e:
            messages.error(request, f'No se pudo eliminar el código: {str(e)}')
        return redirect('administracion:codigo_asistencia_list')
    
    context = {
        'codigo_obj': codigo_obj,
    }
    return render(request, 'administracion/codigos/delete.html', context)
