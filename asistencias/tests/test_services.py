from django.test import TestCase
from django.contrib.auth.models import User
from asistencias.services import AsistenciaService
from asistencias.models import CodigoAsistencia, Turno, Asistencia, CierreDiario, ResumenDiarioAlumno
from alumnos.models import Alumno
from escuela.models import Curso, Anio
from datetime import date

class AsistenciaServiceTest(TestCase):
    def setUp(self):
        # Setup básico para pruebas de integración si fuera necesario
        pass

    def test_calcular_valor_falta_simple(self):
        """Prueba cálculo simple de faltas"""
        # Solo mañana, Presente -> 0.0
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('P', None, None, True, False, False),
            0.0
        )
        # Solo mañana, Ausente -> 1.0
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('A', None, None, True, False, False),
            1.0
        )
        # Solo mañana, Tarde -> 1.0
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('T', None, None, True, False, False),
            1.0
        )
        # Solo mañana, Tarde leve -> 0.5
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('t', None, None, True, False, False),
            0.5
        )

    def test_calcular_valor_falta_doble_turno(self):
        """Prueba cálculo con doble turno"""
        # Mañana Presente (0), Tarde Ausente (1) -> (0 + 1) / 2 = 0.5
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('P', 'A', None, True, True, False),
            0.5
        )
        # Mañana Ausente (1), Tarde Ausente (1) -> (1 + 1) / 2 = 1.0
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('A', 'A', None, True, True, False),
            1.0
        )
        # Mañana Tarde leve (0.5), Tarde Presente (0) -> (0.5 + 0) / 2 = 0.25
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('t', 'P', None, True, True, False),
            0.25
        )

    def test_calcular_valor_falta_triple_turno(self):
        """Prueba cálculo con triple turno (incluye EF)"""
        # P, P, P -> 0
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('P', 'P', 'P', True, True, True),
            0.0
        )
        # A, A, A -> 1
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('A', 'A', 'A', True, True, True),
            1.0
        )
        # P, P, A -> (0 + 0 + 1) / 3 = 0.33
        self.assertEqual(
            AsistenciaService.calcular_valor_falta('P', 'P', 'A', True, True, True),
            0.33
        )

    def test_calcular_valor_falta_sin_turnos(self):
        """Prueba caso borde sin turnos"""
        self.assertEqual(
            AsistenciaService.calcular_valor_falta(None, None, None, False, False, False),
            0.0
        )
