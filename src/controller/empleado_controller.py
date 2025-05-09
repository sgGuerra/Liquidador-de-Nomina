import sys
sys.path.append( "." )
sys.path.append( "src" )

import psycopg2
from model.clase_empleado import Empleado
import SecretConfig


class EmpleadoController:
    
    def CrearTabla():
        cursor = EmpleadoController.Obtener_cursor()
        with open("sql/tabla_empleados.sql", "r") as sql_file:
            consulta = sql_file.read()
            
        cursor.execute(consulta)
        cursor.connection.commit()

    def BorrarTabla():

        cursor = EmpleadoController.Obtener_cursor()
        with open("sql\borrar_empleados.sql", "r") as sql_file:

            consulta = sql_file.read()

        cursor.execute(consulta)
        cursor.connection.commit()
        

    def InsertarEmpleado(empleado: Empleado):
        cursor = EmpleadoController.Obtener_cursor()
        # Consultar el cargo y salario base desde las tablas relacionadas
        cursor.execute(f"SELECT cargo, salario_base FROM tabla_cargos WHERE cedula_empleado = '{empleado.cedula}'")
        resultado = cursor.fetchone()
        if resultado:
            cargo, salario_base = resultado
        else:
            raise ValueError("No se encontraron datos para el empleado con la cédula proporcionada.")

        # Construir la consulta para insertar el empleado
        consulta = f"""INSERT INTO empleados (cedula, nombre, apellido, cargo, salario_base) 
                   VALUES ('{empleado.cedula}', '{empleado.nombres}', '{empleado.apellidos}', '{cargo}', {salario_base})"""
        
        cursor.execute(consulta)
        cursor.connection.commit()




def Obtener_cursor():
    connection = psycopg2.connect(database=SecretConfig.PGDATABASE, user=SecretConfig.PGUSER, password=SecretConfig.PGPASSWORD, host=SecretConfig.PGHOST, port=SecretConfig.PGPORT)
        # Todas las instrucciones se ejecutan a tavés de un cursor
    cursor = connection.cursor()
    return cursor