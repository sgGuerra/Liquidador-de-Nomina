import unittest
import sys

sys.path.append("src")

from controller.nomina_controller import NominaController
from model.calculo_nomina import Nomina
from model.excepciones import *

import psycopg2

class TestNominaDB(unittest.TestCase):
    """Clase de pruebas para las operaciones de base de datos de la nómina.
    
    Esta clase prueba todas las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con la gestión de nóminas en la base de datos, incluyendo validaciones
    y manejo de errores.
    """
    
    def setUp(self):
        """Configura el ambiente de pruebas antes de cada test.
        
        - Limpia cualquier dato previo eliminando el empleado de prueba si existe
        - Inicializa los objetos de nómina que se usarán en las pruebas
        """
        # Intentar eliminar el empleado si existe, ignorar si no existe
        try:
            NominaController.EliminarEmpleadoPorCedula("123456789")
        except EmpleadoNoExistenteError:
            # Si el empleado no existe, no hacemos nada
            pass

        # Nómina con datos válidos para pruebas básicas
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

        # Nómina con datos válidos para pruebas de modificación
        self.nomina_modificada = Nomina(
            cedula_empleado="123456789",
            nombre_empleado="Juan Gabriel",
            empleado_apellido="Pérez",
            cargo="Empleado Antiguo",
            salario_base=3500000,
            horas_extras=10,
            tipo_hora_extra="Diurnas",
            horas_extras_adicionales=15,
            tipo_hora_extra_adicional="Nocturnas",
            prestamo=500000,
            cuotas=3,
            tasa_interes=6
        )

        # Nómina con nombre inválido para pruebas de validación
        self.nomina_nombre_no_valido = Nomina(
            cedula_empleado="123456789",
            nombre_empleado="1212",
            empleado_apellido="Pérez",
            cargo="Empleado Antiguo",
            salario_base=3500000,
            horas_extras=10,
            tipo_hora_extra="Diurnas",
            horas_extras_adicionales=15,
            tipo_hora_extra_adicional="Nocturnas",
            prestamo=500000,
            cuotas=3,
            tasa_interes=6
        )

        # Nómina con cédula inexistente para pruebas de validación
        self.nomina_cedula_no_existente = Nomina(
            cedula_empleado="123456111",
            nombre_empleado="Juan Gabriel",
            empleado_apellido="Pérez",
            cargo="Empleado Antiguo",
            salario_base=3500000,
            horas_extras=10,
            tipo_hora_extra="Diurnas",
            horas_extras_adicionales=15,
            tipo_hora_extra_adicional="Nocturnas",
            prestamo=500000,
            cuotas=3,
            tasa_interes=6
        )

    def test_insertar_nomina(self):
        """Prueba la inserción exitosa de una nómina en la base de datos.
        
        Verifica que:
        1. Se pueda insertar una nómina con datos válidos
        2. Se pueda recuperar la nómina insertada
        3. Los datos recuperados coincidan con los insertados
        """
        NominaController.InsertarNomina(self.nomina)
        nomina_db = NominaController.ObtenerEmpleadoPorCedula("123456789")
        
        self.assertIsNotNone(nomina_db)
        self.assertEqual(nomina_db["cedula"], "123456789")
        self.assertEqual(nomina_db["nombres"], "Juan")
        self.assertEqual(nomina_db["apellidos"], "Pérez")
        self.assertEqual(nomina_db["cargo"], "Empleado nuevo")
        self.assertEqual(nomina_db["salario_base"], 3500000)

    def test_insertar_empleado_nombre_no_valido(self):
        """Prueba que no se pueda insertar una nómina con un nombre inválido.
        
        Verifica que se lance NombreInvalidoError cuando el nombre contiene números
        en lugar de solo letras y espacios.
        """
        with self.assertRaises(NombreInvalidoError):
            NominaController.InsertarNomina(self.nomina_nombre_no_valido)

    def test_insertar_nomina_empleado_existente(self):
        """Prueba que no se pueda insertar un empleado que ya existe.
        
        Verifica que:
        1. Se pueda insertar el empleado la primera vez
        2. Al intentar insertarlo nuevamente, se lance EmpleadoExistenteError
        """
        NominaController.InsertarNomina(self.nomina)
        with self.assertRaises(EmpleadoExistenteError):
            NominaController.InsertarNomina(self.nomina)

    def test_eliminar_empleado_existente(self):
        """Prueba la eliminación exitosa de un empleado existente.
        
        Verifica que:
        1. Se pueda insertar un empleado
        2. Se pueda eliminar el empleado insertado
        3. Al intentar consultar el empleado eliminado, se lance EmpleadoNoExistenteError
        """
        NominaController.InsertarNomina(self.nomina)
        NominaController.EliminarEmpleadoPorCedula("123456789")
        
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ObtenerEmpleadoPorCedula("123456789")

    def test_eliminar_empleado_no_existente(self):
        """Prueba que no se pueda eliminar un empleado que no existe.
        
        Verifica que se lance EmpleadoNoExistenteError al intentar eliminar
        un empleado con una cédula que no está en la base de datos.
        """
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.EliminarEmpleadoPorCedula("123456789")

    def test_eliminar_empleado_cedula_muy_corta(self):
        """Prueba que no se pueda eliminar un empleado con una cédula muy corta.
        
        Verifica que se lance CedulaMuyCortaError al intentar eliminar un empleado
        usando una cédula con menos de 8 dígitos.
        """
        with self.assertRaises(CedulaMuyCortaError):
            NominaController.EliminarEmpleadoPorCedula("12345")

    def test_consultar_empleado_existente(self):
        """Prueba la consulta de un empleado existente.
        
        Verifica que se lance EmpleadoNoExistenteError al intentar consultar
        un empleado que no está en la base de datos.
        """
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ObtenerEmpleadoPorCedula("123456789")

    def test_consultar_empleado_no_existente(self):
        """Prueba que no se pueda consultar un empleado que no existe.
        
        Verifica que se lance EmpleadoNoExistenteError al intentar consultar
        un empleado con una cédula que no está en la base de datos.
        """
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ObtenerEmpleadoPorCedula("123456781")

    def test_consultar_empleado_cedula_muy_larga(self):
        """Prueba que no se pueda consultar un empleado con una cédula muy larga.
        
        Verifica que se lance CedulaMuyLargaError al intentar consultar un empleado
        usando una cédula con más de 10 dígitos.
        """
        with self.assertRaises(CedulaMuyLargaError):
            NominaController.ObtenerEmpleadoPorCedula("12345678901")

    def test_modificar_empleado_existente(self):
        """Prueba que no se pueda modificar un empleado que no existe.
        
        Verifica que se lance EmpleadoNoExistenteError al intentar modificar
        un empleado que no está en la base de datos.
        """
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ModificarNomina(self.nomina_modificada)

    def test_modificar_empleado_no_existente(self):
        """Prueba que no se pueda modificar un empleado que no existe.
        
        Verifica que se lance EmpleadoNoExistenteError al intentar modificar
        un empleado con una cédula que no está en la base de datos.
        """
        with self.assertRaises(EmpleadoNoExistenteError):
            NominaController.ModificarNomina(self.nomina_cedula_no_existente)

    def test_modificar_empleado_nombre_no_valido(self):
        """Prueba que no se pueda modificar un empleado con un nombre inválido.
        
        Verifica que:
        1. Se pueda insertar un empleado con datos válidos
        2. Al intentar modificarlo con un nombre que contiene números,
           se lance NombreInvalidoError
        """
        NominaController.InsertarNomina(self.nomina)
        with self.assertRaises(NombreInvalidoError):
            NominaController.ModificarNomina(self.nomina_nombre_no_valido)