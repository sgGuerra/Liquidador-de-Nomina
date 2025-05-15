class SalarioBaseInexistente(Exception):
    """Excepción que se lanza cuando no se ha ingresado un salario base.

    Esta excepción se utiliza para validar que el campo de salario base no esté vacío
    al momento de crear o modificar un empleado.
    """
    def __init__(self):
        super().__init__("Ingrese su salario en el campo de salario base.")

class SalarioBaseNegativoError(Exception):
    """Excepción que se lanza cuando se ingresa un salario base negativo.

    Según el Artículo 127 del Código Sustantivo del Trabajo (CST), el salario
    no puede ser negativo.
    """
    def __init__(self):
        super().__init__("El Salario base del empleado no puede ser negativo (Art. 127 CST)")

class LimiteHorasExtraError(Exception):
    """Excepción que se lanza cuando se excede el límite legal de horas extras.

    La legislación laboral establece un límite de 50 horas extras mensuales.
    Esta excepción valida que la suma de todas las horas extras (normales y adicionales)
    no supere este límite.

    Args:
        horas_extra (float): Número de horas extras normales.
        horas_extras_adicionales (float): Número de horas extras adicionales.
    """
    def __init__(self, horas_extra, horas_extras_adicionales):
        total_horas = horas_extra + horas_extras_adicionales
        super().__init__(
            f"El empleado ha ingresado un total de {total_horas} horas extra, "
            f"superando el límite de 50 horas extra mensuales."
        )

class TipoHoraExtraInvalidoError(Exception):
    """Excepción que se lanza cuando se especifica un tipo de hora extra no válido.

    Los tipos válidos de horas extras son: Diurnas, Nocturnas y Festivas.

    Args:
        tipo_hora_extra (str): El tipo de hora extra inválido que se intentó usar.
    """
    def __init__(self, tipo_hora_extra):
        super().__init__(f"El tipo de hora extra '{tipo_hora_extra}' no es válido." 
                         f"Ingrese: (Diurnas, Nocturnas, Festivas"
        )

class ValorHoraExtraNegativoError(Exception):
    """Excepción que se lanza cuando se ingresa un número negativo de horas extras.

    Las horas extras deben ser un valor positivo entre 0 y 50.

    Args:
        horas_extras (float): El número negativo de horas extras que se intentó registrar.
    """
    def __init__(self, horas_extras):
        super().__init__(f"El valor de horas extra '{horas_extras}' no puede ser negativo. ingrese un valor entre 0-50")

class SalarioBaseMenorMinimoError(Exception):
    """Excepción que se lanza cuando el salario base es menor al salario mínimo legal.

    Según el Artículo 145 del CST, ningún trabajador puede devengar menos
    que el salario mínimo legal vigente.

    Args:
        salario_base (float): El salario base ingresado.
        salario_minimo (float): El salario mínimo legal vigente.
    """
    def __init__(self, salario_base, salario_minimo):
        super().__init__(f"El salario base '{salario_base}' es menor que el salario mínimo legal vigente '{salario_minimo}' (Art. 145 CST)")
        
class CargoInvalidoError(Exception):
    """Excepción que se lanza cuando se especifica un cargo no válido.

    Los cargos válidos son: Empleado nuevo, Empleado antiguo y Administrador.

    Args:
        cargo_opcion (str): El cargo inválido que se intentó usar.
    """
    def __init__(self, cargo_opcion):
        super().__init__(f"El cargo '{cargo_opcion}' no es válido. Ingrese: 1: Empleado nuevo, 2: Empleado antiguo, 3: Administrador")

class PrestamoNegativoError(Exception):
    """Excepción que se lanza cuando se intenta registrar un préstamo con valor negativo.

    El valor del préstamo debe ser mayor o igual a cero.

    Args:
        prestamo (float): El valor negativo del préstamo que se intentó registrar.
    """
    def __init__(self, prestamo):
        super().__init__(f"El valor del préstamo no puede ser negativo. Ingrese un valor mayor o igual a 0. valor ingresado: {prestamo}")

class CargoNoExistenteError(Exception):
    """Excepción que se lanza cuando se intenta usar un cargo que no existe en la base de datos.

    Esta excepción se usa principalmente en operaciones de base de datos cuando
    se referencia un cargo que no está registrado.

    Args:
        cargo (str): El nombre del cargo que no existe en la base de datos.
    """
    def __init__(self, cargo):
        super().__init__(f"No existe un cargo con el nombre '{cargo}' en la base de datos")

class TipoHoraExtraNoExistenteError(Exception):
    """Excepción que se lanza cuando se intenta usar un tipo de hora extra que no existe en la base de datos.

    Esta excepción se usa principalmente en operaciones de base de datos cuando
    se referencia un tipo de hora extra que no está registrado.

    Args:
        tipo_hora (str): El tipo de hora extra que no existe en la base de datos.
    """
    def __init__(self, tipo_hora):
        super().__init__(f"No existe el tipo de hora extra '{tipo_hora}' en la base de datos")

class EmpleadoNoExistenteError(Exception):
    """Excepción que se lanza cuando se intenta acceder a un empleado que no existe en la base de datos.

    Esta excepción se usa en operaciones de consulta, modificación o eliminación
    cuando se proporciona una cédula que no corresponde a ningún empleado registrado.

    Args:
        cedula (str): El número de cédula del empleado que no existe.
    """
    def __init__(self, cedula):
        super().__init__(f"No existe un empleado con cédula '{cedula}' en la base de datos")

class EmpleadoExistenteError(Exception):
    """Excepción que se lanza cuando se intenta crear un empleado con una cédula que ya existe.

    Esta excepción previene la duplicación de registros de empleados en la base de datos.
    Si se necesita modificar los datos de un empleado existente, se debe usar la función de modificación.

    Args:
        cedula (str): El número de cédula que ya está registrado en la base de datos.
    """
    def __init__(self, cedula):
        super().__init__(f"Ya existe un empleado con la cédula {cedula}. Use el botón 'Modificar Empleado' para actualizar sus datos.")

class CedulaInvalidaError(Exception):
    """Excepción que se lanza cuando la cédula contiene caracteres no numéricos.

    La cédula debe:
    - Contener solo números
    - No debe contener letras, espacios ni caracteres especiales

    Args:
        cedula (str): La cédula ingresada que contiene caracteres no válidos.
    """
    def __init__(self, cedula):
        self.message = f"La cédula '{cedula}' contiene caracteres no válidos. La cédula debe contener únicamente números."
        super().__init__(self.message)

class CedulaMuyCortaError(CedulaInvalidaError):
    """Excepción que se lanza cuando la cédula tiene menos de 8 dígitos.

    La cédula debe tener como mínimo 8 dígitos según las reglas de negocio.

    Args:
        cedula (str): La cédula ingresada que es muy corta.
        longitud_minima (int): La longitud mínima requerida (8 dígitos).
    """
    def __init__(self, cedula, longitud_minima=8):
        super().__init__(cedula)
        self.message = f"La cédula '{cedula}' tiene {len(cedula)} dígitos. Debe tener mínimo {longitud_minima} dígitos."
        Exception.__init__(self, self.message)

class CedulaMuyLargaError(CedulaInvalidaError):
    """Excepción que se lanza cuando la cédula tiene más de 10 dígitos.

    La cédula debe tener como máximo 10 dígitos según las reglas de negocio.

    Args:
        cedula (str): La cédula ingresada que es muy larga.
        longitud_maxima (int): La longitud máxima permitida (10 dígitos).
    """
    def __init__(self, cedula, longitud_maxima=10):
        super().__init__(cedula)
        self.message = f"La cédula '{cedula}' tiene {len(cedula)} dígitos. Debe tener máximo {longitud_maxima} dígitos."
        Exception.__init__(self, self.message)

class NombreInvalidoError(Exception):
    """Excepción que se lanza cuando el formato del nombre no es válido.

    El nombre debe:
    - Contener solo letras
    - Puede contener espacios entre palabras
    - No debe contener números ni caracteres especiales
    """
    def __init__(self):
        super().__init__("El nombre debe contener solo letras y espacios")

class ApellidoInvalidoError(Exception):
    """Excepción que se lanza cuando el formato del apellido no es válido.

    El apellido debe:
    - Contener solo letras
    - Puede contener espacios entre palabras
    - No debe contener números ni caracteres especiales
    """
    def __init__(self):
        super().__init__("El apellido debe contener solo letras y espacios")
