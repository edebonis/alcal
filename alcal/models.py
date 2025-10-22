from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class PerfilUsuario(models.Model):
    """
    Modelo para extender el usuario de Django con roles específicos del sistema ALCAL
    """
    ROLES = [
        ('alumno', 'Alumno'),
        ('docente', 'Docente'),
        ('preceptor', 'Preceptor'),
        ('director', 'Director'),
        ('administrador', 'Administrador'),
        ('familiar', 'Familiar a Cargo'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='alumno')
    legajo = models.CharField(max_length=20, null=True, blank=True, help_text="Legajo institucional")
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    
    # Campos específicos según el rol
    alumno_relacionado = models.ForeignKey(
        'alumnos.Alumno', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="Solo para usuarios con rol de alumno"
    )
    docente_relacionado = models.ForeignKey(
        'docentes.Docente', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        help_text="Solo para usuarios con rol de docente"
    )
    
    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"
        
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_rol_display()})"
    
    @property
    def nombre_completo(self):
        return self.user.get_full_name() or self.user.username
    
    def tiene_permiso(self, permiso):
        """
        Verifica si el usuario tiene un permiso específico basado en su rol
        """
        permisos_por_rol = {
            'administrador': ['all'],
            'director': ['ver_todo', 'editar_todo', 'reportes'],
            'preceptor': ['ver_asistencia', 'editar_asistencia', 'ver_alumnos'],
            'docente': ['ver_calificaciones', 'editar_calificaciones', 'ver_alumnos_curso'],
            'familiar': ['ver_hijo'],
            'alumno': ['ver_propio'],
        }
        
        permisos_usuario = permisos_por_rol.get(self.rol, [])
        return 'all' in permisos_usuario or permiso in permisos_usuario


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    """
    Crea automáticamente un perfil cuando se crea un usuario
    """
    if created:
        PerfilUsuario.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_perfil_usuario(sender, instance, **kwargs):
    """
    Guarda el perfil cuando se guarda el usuario
    """
    if hasattr(instance, 'perfil'):
        instance.perfil.save() 