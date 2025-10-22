"""
Configuración de la aplicación ALCAL
"""
from django.apps import AppConfig


class AlcalConfig(AppConfig):
    """
    Configuración de la aplicación principal ALCAL
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alcal'
    verbose_name = 'ALCAL - Sistema Académico'
    
    def ready(self):
        """
        Código que se ejecuta cuando la aplicación está lista
        """
        # Importar configuración del admin
        from . import admin 