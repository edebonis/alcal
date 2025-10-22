from django.contrib.auth.models import User
from django.test import TestCase

from escuela.models import Carrera, Curso

from .models import Alumno, Madre, Padre, Tutor


class AlumnoModelTest(TestCase):
    """Test basic functionality of Alumno models"""
    
    def setUp(self):
        """Set up test data"""
        # Create Carrera and Curso
        self.carrera = Carrera.objects.create(nombre="Bachillerato")
        self.curso = Curso.objects.create(curso="5A", carrera=self.carrera)
        
        # Create Padre, Madre, Tutor
        self.padre = Padre.objects.create(
            nombre_padre="Juan",
            apellido_padre="Pérez",
            dni_padre=12345678,
            telefono_padre="1234567890",
            nacionalidad_padre="Argentina"
        )
        
        self.madre = Madre.objects.create(
            nombre_madre="María",
            apellido_madre="García",
            dni_madre=87654321,
            telefono_madre="0987654321",
            nacionalidad_madre="Argentina"
        )
    
    def test_alumno_creation(self):
        """Test that we can create an Alumno"""
        alumno = Alumno.objects.create(
            nombre="Carlos",
            apellido="Pérez",
            dni=99999999,
            curso=self.curso,
            padre=self.padre,
            madre=self.madre
        )
        
        self.assertEqual(alumno.nombre, "Carlos")
        self.assertEqual(alumno.apellido, "Pérez")
        self.assertEqual(str(alumno), "Pérez Carlos")
        self.assertEqual(alumno.curso, self.curso)
        self.assertTrue(alumno.activo)
        self.assertFalse(alumno.libre)
        self.assertFalse(alumno.condicional)
    
    def test_padre_creation(self):
        """Test Padre model"""
        self.assertEqual(str(self.padre), "Pérez Juan")
        self.assertEqual(self.padre.dni_padre, 12345678)
    
    def test_madre_creation(self):
        """Test Madre model"""
        self.assertEqual(str(self.madre), "García María")
        self.assertEqual(self.madre.dni_madre, 87654321)


class AdminViewTest(TestCase):
    """Test admin interface access"""
    
    def setUp(self):
        """Create test user"""
        self.user = User.objects.create_user(
            username='admin',
            password='testpass',
            is_staff=True,
            is_superuser=True
        )
    
    def test_admin_login_redirect(self):
        """Test that accessing admin redirects to login"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response.url)
    
    def test_admin_access_after_login(self):
        """Test admin access after login"""
        self.client.login(username='admin', password='testpass')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
