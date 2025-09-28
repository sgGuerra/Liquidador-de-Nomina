import unittest
import sys

sys.path.append("src")

from controller.nomina_controller import NominaController
from model.calculo_nomina import Nomina
from model.excepciones import NombreInvalidoError, EmpleadoExistenteError, EmpleadoNoExistenteError, CedulaMuyCortaError, CedulaMuyLargaError
import SecretConfig
import os
import psycopg2

class TestNominaDB(unittest.TestCase):
    """Clase de pruebas para las operaciones de base de datos de la nómina.
    
    Esta clase prueba todas las operaciones CRUD (Crear, Leer, Actualizar, Eliminar)
    relacionadas con la gestión de nóminas en la base de datos, incluyendo validaciones
    y manejo de errores.
    """
    
    @classmethod
    def setUpClass(cls):
        """Configura el ambiente de pruebas antes de ejecutar cualquier test.
        
        Este método:
        1. Verifica la conexión a la base de datos
        2. Crea las tablas si no existen
        3. Inserta los datos iniciales necesarios (cargos)
        """
        try:
            connection = psycopg2.connect(
                host=SecretConfig.PGHOST,
                database=SecretConfig.PGDATABASE,
                user=SecretConfig.PGUSER,
                password=SecretConfig.PGPASSWORD,
                port=SecretConfig.PGPORT,
                sslmode='require'
            )
            cursor = connection.cursor()
            
            # Obtener la ruta base del proyecto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Crear tabla de cargos si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_cargos.sql'), 'r') as file:
                cursor.execute(file.read())
            
            # Crear tabla de empleados si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_empleados.sql'), 'r') as file:
                cursor.execute(file.read())

            # Crear tabla de tipos de horas extra si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_tipo_hora_extra.sql'), 'r') as file:
                cursor.execute(file.read())

            # Crear tabla de horas extra si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_horas_extra.sql'), 'r') as file:
                cursor.execute(file.read())

            # Crear tabla de prestamo si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_prestamo.sql'), 'r') as file:
                cursor.execute(file.read())

            # Crear tabla de historial de nomina si no existe
            with open(os.path.join(base_dir, 'sql', 'tabla_historial_nomina.sql'), 'r') as file:
                cursor.execute(file.read())

            # Verificar si ya existen cargos
            cursor.execute("SELECT COUNT(*) FROM cargos")
            count = cursor.fetchone()[0]

            # Si no hay cargos, insertar los predeterminados
            if count == 0:
                with open(os.path.join(base_dir, 'sql', 'insertar_cargos.sql'), 'r') as file:
                    cursor.execute(file.read())

            # Verificar si ya existen tipos de horas extra
            cursor.execute("SELECT COUNT(*) FROM tipos_horas_extra")
            count = cursor.fetchone()[0]

            # Si no hay tipos, insertar los predeterminados
            if count == 0:
                with open(os.path.join(base_dir, 'sql', 'insertar_tipo_de_horas_extra.sql'), 'r') as file:
                    cursor.execute(file.read())
            
            connection.commit()
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"Error configurando la base de datos: {str(e)}")
            raise
    

    
    def setUp(self):
        """Configura el ambiente de pruebas antes de cada test.

        - Limpia cualquier dato previo eliminando el empleado de prueba si existe
        - Inicializa los objetos de nómina que se usarán en las pruebas
        """
        # Limpiar historial de nómina para este empleado primero
        try:
            cursor = NominaController.Obtener_cursor()
            cursor.execute("DELETE FROM historial_nomina WHERE cedula = %s", ("123456789",))
            cursor.connection.commit()
            cursor.connection.close()
        except Exception:
            pass

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

    def test_guardar_historial_nomina(self):
        """Prueba el guardado y recuperación del historial de nómina.

        Verifica que:
        1. Se pueda insertar un empleado
        2. Se pueda calcular la nómina
        3. Se pueda guardar el historial con los resultados del cálculo
        4. Se pueda recuperar el historial y verificar que los datos coincidan
        """
        # Insertar empleado
        NominaController.InsertarNomina(self.nomina)

        # Calcular nómina
        resultados = self.nomina.calcular()

        # Guardar historial
        NominaController.GuardarHistorialNomina(
            self.nomina.empleado.cedula,
            resultados['salario_bruto'],
            resultados['deducciones'],
            resultados['impuestos'],
            resultados['auxilio_transporte'],
            resultados['neto']
        )

        # Obtener historial
        historial = NominaController.ObtenerHistorialNomina(self.nomina.empleado.cedula)

        self.assertEqual(len(historial), 1)
        h = historial[0]
        self.assertEqual(h['salario_bruto'], resultados['salario_bruto'])
        self.assertEqual(h['deducciones'], resultados['deducciones'])
        self.assertEqual(h['impuestos'], resultados['impuestos'])
        self.assertEqual(h['auxilio_transporte'], resultados['auxilio_transporte'])
        self.assertEqual(h['neto'], resultados['neto'])

    def test_obtener_historial_nomina_no_existente(self):
        """Prueba la obtención de historial para un empleado sin historial.

        Verifica que se retorne una lista vacía cuando no hay historial para la cédula.
        """
        historial = NominaController.ObtenerHistorialNomina("999999999")
        self.assertEqual(historial, [])

    def test_guardar_multiple_historial_nomina(self):
        """Prueba el guardado de múltiples entradas de historial para el mismo empleado.

        Verifica que:
        1. Se puedan guardar múltiples historiales
        2. Se recuperen en orden descendente por fecha
        3. Todas las entradas se recuperen correctamente
        """
        # Insertar empleado
        NominaController.InsertarNomina(self.nomina)

        # Primer cálculo y guardado
        resultados1 = self.nomina.calcular()
        NominaController.GuardarHistorialNomina(
            self.nomina.empleado.cedula,
            resultados1['salario_bruto'],
            resultados1['deducciones'],
            resultados1['impuestos'],
            resultados1['auxilio_transporte'],
            resultados1['neto']
        )

        # Modificar salario para segundo cálculo
        self.nomina.salario_base = 4000000
        resultados2 = self.nomina.calcular()
        NominaController.GuardarHistorialNomina(
            self.nomina.empleado.cedula,
            resultados2['salario_bruto'],
            resultados2['deducciones'],
            resultados2['impuestos'],
            resultados2['auxilio_transporte'],
            resultados2['neto']
        )

        # Obtener historial
        historial = NominaController.ObtenerHistorialNomina(self.nomina.empleado.cedula)

        self.assertEqual(len(historial), 2)
        # El más reciente primero
        self.assertEqual(historial[0]['salario_bruto'], resultados2['salario_bruto'])
        self.assertEqual(historial[1]['salario_bruto'], resultados1['salario_bruto'])
