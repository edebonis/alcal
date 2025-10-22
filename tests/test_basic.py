"""
Basic tests to verify the application setup
"""
import pytest
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class BasicSetupTest(TestCase):
    """Test basic application setup"""
    
    def test_django_setup(self):
        """Test that Django is properly configured"""
        from django.conf import settings
        self.assertTrue(settings.configured)
    
    def test_database_connection(self):
        """Test that database connection works"""
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
    
    def test_admin_accessible(self):
        """Test that admin panel is accessible"""
        response = self.client.get('/admin/')
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)


class ModelsTest(TestCase):
    """Test basic model functionality"""
    
    def test_user_creation(self):
        """Test that user creation works"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpass123'))


@pytest.mark.django_db
def test_basic_models_import():
    """Test that all models can be imported"""
    from alumnos.models import Alumno, Madre, Padre, Tutor
    from asistencias.models import Asistencia, CodigoAsistencia
    from calificaciones.models import CalificacionParcial, CalificacionTrimestral
    from docentes.models import Docente
    from escuela.models import Anio, Carrera, Curso, Materia
    from observaciones.models import Observacion, TipoObservacion

    # If we get here without errors, imports are working
    assert True 