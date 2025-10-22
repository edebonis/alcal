from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class RoleBasedAccessMiddleware(MiddlewareMixin):
    """
    Middleware para controlar el acceso basado en roles de usuario
    """
    
    def process_request(self, request):
        # Rutas que no requieren verificación de roles
        rutas_publicas = [
            '/admin/login/',
            '/admin/logout/',
            '/admin/jsi18n/',
            '/static/',
            '/media/',
        ]
        
        # Si la ruta es pública, permitir acceso
        if any(request.path.startswith(ruta) for ruta in rutas_publicas):
            return None
        
        # Si el usuario no está autenticado, redirigir al login
        if not request.user.is_authenticated:
            if request.path.startswith('/admin/'):
                return redirect('/admin/login/')
            return None
        
        # Si el usuario está autenticado pero no tiene perfil, crear uno básico
        if not hasattr(request.user, 'perfil'):
            from .models import PerfilUsuario
            PerfilUsuario.objects.create(
                user=request.user,
                rol='alumno'  # Rol por defecto
            )
        
        # Verificar permisos específicos para rutas del admin
        if request.path.startswith('/admin/'):
            return self._verificar_permisos_admin(request)
        
        return None
    
    def _verificar_permisos_admin(self, request):
        """
        Verifica permisos específicos para el área de administración
        """
        user = request.user
        perfil = getattr(user, 'perfil', None)
        
        if not perfil:
            messages.error(request, 'No tienes un perfil asignado. Contacta al administrador.')
            return redirect('/admin/login/')
        
        # Superusuarios y administradores tienen acceso completo
        if user.is_superuser or perfil.rol == 'administrador':
            return None
        
        # Directores tienen acceso completo al admin
        if perfil.rol == 'director':
            return None
        
        # Para el dashboard principal del admin, permitir acceso a staff
        if request.path == '/admin/' and user.is_staff:
            return None
        
        # Staff puede acceder al admin pero con restricciones específicas
        if user.is_staff:
            # Preceptores pueden acceder a asistencias y alumnos
            if perfil.rol == 'preceptor':
                rutas_permitidas = [
                    '/admin/alumnos/',
                    '/admin/asistencias/',
                    '/admin/auth/user/',
                    '/admin/alcal/perfilusuario/',
                ]
                if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                    return None
            
            # Docentes pueden acceder a calificaciones y sus alumnos
            elif perfil.rol == 'docente':
                rutas_permitidas = [
                    '/admin/calificaciones/',
                    '/admin/alumnos/',
                    '/admin/auth/user/',
                    '/admin/alcal/perfilusuario/',
                ]
                if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                    return None
            
            # Familiares solo pueden ver información de sus hijos
            elif perfil.rol == 'familiar':
                rutas_permitidas = [
                    '/admin/alumnos/',
                    '/admin/calificaciones/',
                    '/admin/asistencias/',
                ]
                if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                    return None
            
            # Alumnos solo pueden ver su propia información
            elif perfil.rol == 'alumno':
                rutas_permitidas = [
                    '/admin/auth/user/',
                    '/admin/alcal/perfilusuario/',
                ]
                if any(request.path.startswith(ruta) for ruta in rutas_permitidas):
                    return None
        
        # Si llegamos aquí, el usuario no tiene permisos para esta ruta específica
        # Redirigir al login con mensaje de error en lugar de crear bucle
        messages.error(request, f'No tienes permisos para acceder a esta sección como {perfil.get_rol_display()}.')
        return redirect('/admin/login/')


class UserProfileMiddleware(MiddlewareMixin):
    """
    Middleware para agregar información del perfil al contexto de las requests
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            # Agregar el perfil del usuario al request para fácil acceso
            if hasattr(request.user, 'perfil'):
                request.user_profile = request.user.perfil
                request.user_role = request.user.perfil.rol
            else:
                request.user_profile = None
                request.user_role = None
        
        return None 