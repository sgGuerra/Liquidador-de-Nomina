import sys
sys.path.append(".")
sys.path.append("src")

import psycopg2
from model.calculo_nomina import Nomina
from model.excepciones import (
    CargoNoExistenteError,
    TipoHoraExtraNoExistenteError,
    EmpleadoExistenteError,
    EmpleadoNoExistenteError,
    CedulaInvalidaError,
    CedulaMuyCortaError,
    CedulaMuyLargaError
)
import SecretConfig

class NominaController:
    # Consultas SQL como constantes de clase
    CONSULTA_DATOS_EMPLEADO = """
        SELECT 
            e.cedula, 
            e.nombres, 
            e.apellidos, 
            c.cargo_empleado, 
            e.salario_base
        FROM empleados e
        INNER JOIN cargos c ON e.cargo = c.id
        WHERE e.cedula = %s
    """

    CONSULTA_HORAS_EXTRAS = """
        SELECT h.numero_de_horas, t.nombre_tipo_hora
        FROM horas_extras h
        INNER JOIN tipos_horas_extra t ON h.id_tipo_hora = t.tipo_hora_id
        WHERE h.id_empleado = %s
    """

    CONSULTA_PRESTAMO = """
        SELECT monto, numero_de_cuotas, tasa_interes, fecha_inicio
        FROM prestamos
        WHERE id_empleado = %s
        ORDER BY fecha_inicio DESC
        LIMIT 1
    """

    @staticmethod
    def CrearTabla():
        cursor = NominaController.Obtener_cursor()
        with open("sql/tabla_empleados.sql", "r") as sql_file:
            consulta = sql_file.read()
        cursor.execute(consulta)
        cursor.connection.commit()

    @staticmethod
    def CrearTablaHistorial():
        cursor = NominaController.Obtener_cursor()
        with open("sql/tabla_historial_nomina.sql", "r") as sql_file:
            consulta = sql_file.read()
        cursor.execute(consulta)
        cursor.connection.commit()

    @staticmethod
    def BorrarTabla():
        cursor = NominaController.Obtener_cursor()
        with open("sql/borrar_empleados.sql", "r") as sql_file:
            consulta = sql_file.read()
        cursor.execute(consulta)
        cursor.connection.commit()
           
    @staticmethod
    def InsertarNomina(nomina: Nomina):
        """
        Inserta un nuevo empleado con su cargo y horas extras
        Args:
            nomina: Objeto Nomina con todos los datos necesarios
        Raises:
            CargoNoExistenteError: Si el cargo no existe en la base de datos
            TipoHoraExtraNoExistenteError: Si el tipo de hora extra no existe
            EmpleadoExistenteError: Si ya existe un empleado con la cédula proporcionada
        """
        # Validar los datos antes de intentar insertarlos
        try:
            nomina.calcular()  # Esto ejecutará todas las validaciones definidas en la clase Nomina
        except Exception as e:
            raise e  # Propagar cualquier error de validación
        
        cursor = NominaController.Obtener_cursor()
        try:
            # 0. Verificar si ya existe un empleado con esa cédula
            cursor.execute("SELECT cedula FROM empleados WHERE cedula = %s", (nomina.empleado.cedula,))
            if cursor.fetchone():
                cursor.connection.rollback()
                raise EmpleadoExistenteError(nomina.empleado.cedula)

            # 1. Buscar el ID del cargo
            cursor.execute("SELECT id FROM cargos WHERE cargo_empleado = %s", (nomina.cargo,))
            resultado_cargo = cursor.fetchone()
            if not resultado_cargo:
                cursor.connection.rollback()
                raise CargoNoExistenteError(nomina.cargo)
            cargo_id = resultado_cargo[0]

            # 2. Insertar el empleado
            cursor.execute("""
                INSERT INTO empleados (cedula, nombres, apellidos, cargo, salario_base) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING cedula
            """, (
                nomina.empleado.cedula,
                nomina.empleado.nombres,
                nomina.empleado.apellidos,
                cargo_id,
                nomina.salario_base
            ))
            
            # 3. Si hay horas extras, procesarlas
            if nomina.horas_extras > 0 and nomina.tipo_hora_extra != "N/A":
                cursor.execute("""
                    SELECT tipo_hora_id 
                    FROM tipos_horas_extra 
                    WHERE nombre_tipo_hora = %s
                """, (nomina.tipo_hora_extra,))
                resultado_tipo_hora = cursor.fetchone()
                if not resultado_tipo_hora:
                    cursor.connection.rollback()
                    raise TipoHoraExtraNoExistenteError(nomina.tipo_hora_extra)
                
                cursor.execute("""
                    INSERT INTO horas_extras (id_empleado, id_tipo_hora, numero_de_horas)
                    VALUES (%s, %s, %s)
                """, (
                    nomina.empleado.cedula,
                    resultado_tipo_hora[0],
                    nomina.horas_extras
                ))

            # 4. Si hay horas extras adicionales, procesarlas también
            if nomina.horas_extras_adicionales > 0 and nomina.tipo_hora_extra_adicional != "N/A":
                cursor.execute("""
                    SELECT tipo_hora_id 
                    FROM tipos_horas_extra 
                    WHERE nombre_tipo_hora = %s
                """, (nomina.tipo_hora_extra_adicional,))
                
                resultado_tipo_hora_adicional = cursor.fetchone()
                if not resultado_tipo_hora_adicional:
                    cursor.connection.rollback()
                    raise TipoHoraExtraNoExistenteError(nomina.tipo_hora_extra_adicional)
                
                cursor.execute("""
                    INSERT INTO horas_extras (id_empleado, id_tipo_hora, numero_de_horas)
                    VALUES (%s, %s, %s)
                """, (
                    nomina.empleado.cedula,
                    resultado_tipo_hora_adicional[0],
                    nomina.horas_extras_adicionales
                ))

            # 5. Si hay préstamo, procesarlo
            if nomina.prestamo > 0 and nomina.cuotas > 0:
                cursor.execute("""
                    INSERT INTO prestamos (id_empleado, monto, numero_de_cuotas, tasa_interes)
                    VALUES (%s, %s, %s, %s)
                """, (
                    nomina.empleado.cedula,
                    nomina.prestamo,
                    nomina.cuotas,
                    nomina.tasa_interes
                ))

            cursor.connection.commit()
            return True
            
        except Exception as e:
            cursor.connection.rollback()
            raise e
        
    
    @staticmethod
    def ModificarNomina(nomina: Nomina) -> bool:
        """
        Modifica los datos de un empleado existente en la base de datos.
        Solo actualiza los campos que tienen nuevos valores y mantiene los existentes.
        
        Args:
            nomina: Objeto Nomina con los datos a actualizar del empleado
            
        Returns:
            bool: True si la modificación fue exitosa
            
        Raises:
            EmpleadoNoExistenteError: Si no existe el empleado
            CargoNoExistenteError: Si no existe el cargo especificado
            TipoHoraExtraNoExistenteError: Si no existe el tipo de hora extra especificado
        """
        cursor = NominaController.Obtener_cursor()
        try:
            # 1. Verificar que el empleado existe y obtener datos actuales
            cursor.execute("""
                SELECT e.nombres, e.apellidos, c.cargo_empleado, e.salario_base 
                FROM empleados e 
                JOIN cargos c ON e.cargo = c.id 
                WHERE e.cedula = %s
            """, (nomina.empleado.cedula,))
            
            empleado_actual = cursor.fetchone()
            if not empleado_actual:
                cursor.connection.rollback()
                raise EmpleadoNoExistenteError(nomina.empleado.cedula)
            
            # Mantener valores actuales si no se proporcionan nuevos
            if not nomina.empleado.nombres.strip():
                nomina.empleado.nombres = empleado_actual[0]
            if not nomina.empleado.apellidos.strip():
                nomina.empleado.apellidos = empleado_actual[1]
            if not nomina.cargo.strip():
                nomina.cargo = empleado_actual[2]
            if nomina.salario_base == 0:
                nomina.salario_base = empleado_actual[3]

            # Validar los datos antes de intentar modificarlos
            try:
                nomina.calcular()
            except Exception as e:
                raise e

            # 2. Buscar el ID del cargo
            cursor.execute("SELECT id FROM cargos WHERE cargo_empleado = %s", (nomina.cargo,))
            resultado_cargo = cursor.fetchone()
            if not resultado_cargo:
                cursor.connection.rollback()
                raise CargoNoExistenteError(nomina.cargo)
            cargo_id = resultado_cargo[0]

            # 3. Actualizar datos básicos del empleado
            cursor.execute("""
                UPDATE empleados 
                SET nombres = %s, 
                    apellidos = %s, 
                    cargo = %s, 
                    salario_base = %s
                WHERE cedula = %s
            """, (
                nomina.empleado.nombres,
                nomina.empleado.apellidos,
                cargo_id,
                nomina.salario_base,
                nomina.empleado.cedula
            ))

            # 4. Manejar horas extras
            if nomina.horas_extras > 0 or nomina.horas_extras_adicionales > 0:
                # Eliminar registros anteriores solo si hay nuevos registros para insertar
                cursor.execute("DELETE FROM horas_extras WHERE id_empleado = %s", (nomina.empleado.cedula,))

                # Insertar horas extras principales si existen
                if nomina.horas_extras > 0 and nomina.tipo_hora_extra != "N/A":
                    cursor.execute("""
                        SELECT tipo_hora_id 
                        FROM tipos_horas_extra 
                        WHERE nombre_tipo_hora = %s
                    """, (nomina.tipo_hora_extra,))
                    resultado_tipo_hora = cursor.fetchone()
                    if not resultado_tipo_hora:
                        raise TipoHoraExtraNoExistenteError(nomina.tipo_hora_extra)
                    
                    cursor.execute("""
                        INSERT INTO horas_extras (id_empleado, id_tipo_hora, numero_de_horas)
                        VALUES (%s, %s, %s)
                    """, (
                        nomina.empleado.cedula,
                        resultado_tipo_hora[0],
                        nomina.horas_extras
                    ))

                # Insertar horas extras adicionales si existen
                if nomina.horas_extras_adicionales > 0 and nomina.tipo_hora_extra_adicional != "N/A":
                    cursor.execute("""
                        SELECT tipo_hora_id 
                        FROM tipos_horas_extra 
                        WHERE nombre_tipo_hora = %s
                    """, (nomina.tipo_hora_extra_adicional,))
                    
                    resultado_tipo_hora_adicional = cursor.fetchone()
                    if not resultado_tipo_hora_adicional:
                        raise TipoHoraExtraNoExistenteError(nomina.tipo_hora_extra_adicional)
                    
                    cursor.execute("""
                        INSERT INTO horas_extras (id_empleado, id_tipo_hora, numero_de_horas)
                        VALUES (%s, %s, %s)
                    """, (
                        nomina.empleado.cedula,
                        resultado_tipo_hora_adicional[0],
                        nomina.horas_extras_adicionales
                    ))

            # 5. Manejar préstamo
            if nomina.prestamo > 0 and nomina.cuotas > 0:
                # Verificar si ya existe un préstamo activo
                cursor.execute("""
                    SELECT id_prestamo 
                    FROM prestamos 
                    WHERE id_empleado = %s
                """, (nomina.empleado.cedula,))
                prestamo_existente = cursor.fetchone()

                if prestamo_existente:
                    # Actualizar préstamo existente
                    cursor.execute("""
                        UPDATE prestamos
                        SET monto = %s,
                            numero_de_cuotas = %s,
                            tasa_interes = %s,
                            fecha_inicio = current_date
                        WHERE id_prestamo = %s
                    """, (
                        nomina.prestamo,
                        nomina.cuotas,
                        nomina.tasa_interes,
                        prestamo_existente[0]
                    ))
                else:
                    # Crear nuevo préstamo
                    cursor.execute("""
                        INSERT INTO prestamos (id_empleado, monto, numero_de_cuotas, tasa_interes)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        nomina.empleado.cedula,
                        nomina.prestamo,
                        nomina.cuotas,
                        nomina.tasa_interes
                    ))

            cursor.connection.commit()
            return True
            
        except Exception as e:
            cursor.connection.rollback()
            raise e
        
    
    @staticmethod
    def ObtenerEmpleadoPorCedula(cedula):
        """
        Obtiene los datos de un empleado por su cédula.
        Args:
            cedula: Cédula del empleado a buscar.
        Returns:
            dict: Diccionario con los datos del empleado y toda su información de nómina.
        Raises:
            CedulaInvalidaError: Si la cédula contiene caracteres no numéricos.
            CedulaMuyCortaError: Si la cédula tiene menos de 8 dígitos.
            CedulaMuyLargaError: Si la cédula tiene más de 10 dígitos.
            EmpleadoNoExistenteError: Si no existe el empleado con la cédula dada.
        """
        # Validar formato de cédula
        if not cedula.isdigit():
            raise CedulaInvalidaError(cedula)
        if len(cedula) < 8:
            raise CedulaMuyCortaError(cedula)
        if len(cedula) > 10:
            raise CedulaMuyLargaError(cedula)

        cursor = NominaController.Obtener_cursor()
        try:
            # Consulta principal para datos del empleado
            cursor.execute(NominaController.CONSULTA_DATOS_EMPLEADO, (cedula,))
            
            empleado_base = cursor.fetchone()
            if not empleado_base:
                raise EmpleadoNoExistenteError(cedula)
            
            # Consulta para horas extras
            cursor.execute(NominaController.CONSULTA_HORAS_EXTRAS, (cedula,))
            
            horas_extras = cursor.fetchall()
            
            # Consulta para préstamos
            cursor.execute(NominaController.CONSULTA_PRESTAMO, (cedula,))
            
            prestamo = cursor.fetchone()
            
            # Construir el diccionario de respuesta
            resultado = {
                "cedula": empleado_base[0],
                "nombres": empleado_base[1],
                "apellidos": empleado_base[2],
                "cargo": empleado_base[3],
                "salario_base": empleado_base[4],
                "horas_extras": [],
                "prestamo": None
            }
            
            # Agregar información de horas extras si existen
            if horas_extras:
                for horas, tipo in horas_extras:
                    resultado["horas_extras"].append({
                        "numero_de_horas": horas,
                        "tipo_hora_extra": tipo
                    })
            
            # Agregar información del préstamo si existe
            if prestamo:
                resultado["prestamo"] = {
                    "monto": prestamo[0],
                    "numero_de_cuotas": prestamo[1],
                    "tasa_interes": prestamo[2],
                    "fecha_inicio": prestamo[3]
                }
            
            return resultado
            
        except Exception as e:
            cursor.connection.rollback()
            raise e
        finally:
            cursor.connection.close()

    @staticmethod
    def EliminarEmpleadoPorCedula(cedula):
        """
        Elimina un empleado y sus registros asociados por su cédula.
        Args:
            cedula: Cédula del empleado a eliminar.
        Raises:
            CedulaInvalidaError: Si la cédula contiene caracteres no numéricos.
            CedulaMuyCortaError: Si la cédula tiene menos de 8 dígitos.
            CedulaMuyLargaError: Si la cédula tiene más de 10 dígitos.
            EmpleadoNoExistenteError: Si no existe el empleado con la cédula dada.
        Returns:
            bool: True si la eliminación fue exitosa.
        """
        # Validar formato de cédula
        if not cedula.isdigit():
            raise CedulaInvalidaError(cedula)
        if len(cedula) < 8:
            raise CedulaMuyCortaError(cedula)
        if len(cedula) > 10:
            raise CedulaMuyLargaError(cedula)

        cursor = NominaController.Obtener_cursor()
        try:
            # Verificar que el empleado existe
            cursor.execute("SELECT cedula FROM empleados WHERE cedula = %s", (cedula,))
            if not cursor.fetchone():
                cursor.connection.rollback()
                raise EmpleadoNoExistenteError(cedula)

            # Eliminar registros relacionados en otras tablas
            cursor.execute("DELETE FROM horas_extras WHERE id_empleado = %s", (cedula,))
            cursor.execute("DELETE FROM prestamos WHERE id_empleado = %s", (cedula,))
            # Eliminar el empleado
            cursor.execute("DELETE FROM empleados WHERE cedula = %s", (cedula,))
            cursor.connection.commit()
            return True
        except Exception as e:
            cursor.connection.rollback()
            raise e
        finally:
            cursor.connection.close()
          
    
    

    @staticmethod
    def GuardarHistorialNomina(cedula, salario_bruto, deducciones, impuestos, auxilio_transporte, neto):
        """
        Guarda el historial de una nómina calculada en la base de datos.
        Args:
            cedula: Cédula del empleado.
            salario_bruto: Salario bruto calculado.
            deducciones: Deducciones calculadas.
            impuestos: Impuestos calculados.
            auxilio_transporte: Auxilio de transporte.
            neto: Salario neto.
        """
        cursor = NominaController.Obtener_cursor()
        try:
            cursor.execute("""
                INSERT INTO historial_nomina (cedula, salario_bruto, deducciones, impuestos, auxilio_transporte, neto)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cedula, salario_bruto, deducciones, impuestos, auxilio_transporte, neto))
            cursor.connection.commit()
        except Exception as e:
            cursor.connection.rollback()
            raise e
        finally:
            cursor.connection.close()

    @staticmethod
    def ObtenerHistorialNomina(cedula):
        """
        Obtiene el historial de nóminas de un empleado.
        Args:
            cedula: Cédula del empleado.
        Returns:
            list: Lista de diccionarios con el historial.
        """
        cursor = NominaController.Obtener_cursor()
        try:
            cursor.execute("""
                SELECT fecha_calculo, salario_bruto, deducciones, impuestos, auxilio_transporte, neto
                FROM historial_nomina
                WHERE cedula = %s
                ORDER BY fecha_calculo DESC
            """, (cedula,))
            resultados = cursor.fetchall()
            historial = []
            for row in resultados:
                historial.append({
                    'fecha': row[0],
                    'salario_bruto': row[1],
                    'deducciones': row[2],
                    'impuestos': row[3],
                    'auxilio_transporte': row[4],
                    'neto': row[5]
                })
            return historial
        except Exception as e:
            raise e
        finally:
            cursor.connection.close()

    @staticmethod
    def Obtener_cursor():
        connection = psycopg2.connect(
            database=SecretConfig.PGDATABASE,
            user=SecretConfig.PGUSER,
            password=SecretConfig.PGPASSWORD,
            host=SecretConfig.PGHOST,
            port=SecretConfig.PGPORT
        )
        cursor = connection.cursor()
        return cursor


