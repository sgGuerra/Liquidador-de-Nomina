import unittest
import sys

sys.path.append("src")

from controller.nomina_controller import NominaController
from model.calculo_nomina import Nomina
from model.excepciones import *

class TestNominaDB(unittest.TestCase):
    
    def setUp(self):


        # Intentar eliminar el empleado si existe, ignorar si no existe
        try:
            NominaController.EliminarEmpleadoPorCedula("123456789")
        except EmpleadoNoExistenteError:
            # Si el empleado no existe, no hacemos nada
            pass

        
        self.nomina = Nomina(
            cedula_empleado="123456789",
            nombre_empleado="Juan",
            empleado_apellido="Pérez",
            cargo="Empleado nuevo",
            salario_base=3500000,
            horas_extras=10,
            tipo_hora_extra="Diurnas",
            horas_extras_adicionales=5,
            tipo_hora_extra_adicional="Nocturnas",
            prestamo=50000,
            cuotas=3,
            tasa_interes=6
        )
        

    def test_insertar_nomina(self):
        # Insertar la nómina en la base de datos
        NominaController.InsertarNomina(self.nomina)
        # Verificar que la nómina se haya insertado correctamente
        nomina_db = NominaController.ObtenerEmpleadoPorCedula("123456789")
        self.assertIsNotNone(nomina_db)
        self.assertEqual(nomina_db["cedula"], "123456789")
        self.assertEqual(nomina_db["nombres"], "Juan")
        self.assertEqual(nomina_db["apellidos"], "Pérez")
        self.assertEqual(nomina_db["cargo"], "Empleado nuevo")
        self.assertEqual(nomina_db["salario_base"], 3500000)


    def test_insertar_nomina_empleado_existente(self):
        # Insertar la nómina por primera vez
        NominaController.InsertarNomina(self.nomina)
        # Intentar insertar nuevamente el mismo empleado debe lanzar EmpleadoExistenteError
        with self.assertRaises(EmpleadoExistenteError):
            NominaController.InsertarNomina(self.nomina)


    def test_eliminar_empleado_existente(self):
        # Insertar la nómina para asegurarnos de que el empleado existe

        NominaController.InsertarNomina(self.nomina)

        # Eliminar el empleado
        NominaController.EliminarEmpleadoPorCedula("123456789")
        # Verificar que el empleado ya no existe
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ObtenerEmpleadoPorCedula("123456789")

    def test_eliminar_empleado_no_existente(self):
        # Intentar eliminar nuevamente debe lanzar la excepción
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.EliminarEmpleadoPorCedula("123456789")

