class SalarioBaseInexistente(Exception):
    def __init__(self):
        super().__init__("Ingrese su salario en el campo de salario base.")

class SalarioBaseNegativoError(Exception):
    def __init__(self):
        super().__init__("El Salario base del empleado no puede ser negativo (Art. 127 CST)")

class LimiteHorasExtraError(Exception):
    def __init__(self, horas_extra, horas_extras_adicionales):
        total_horas = horas_extra + horas_extras_adicionales
        super().__init__(
            f"El empleado ha ingresado un total de {total_horas} horas extra, "
            f"superando el límite de 50 horas extra mensuales."
        )

class TipoHoraExtraInvalidoError(Exception):
    def __init__(self, tipo_hora_extra):
        super().__init__(f"El tipo de hora extra '{tipo_hora_extra}' no es válido." 
                         f"Ingrese: (Diurnas, Nocturnas, Festivas"
        )

class ValorHoraExtraNegativoError(Exception):
    def __init__(self, horas_extras):
        super().__init__(f"El valor de horas extra '{horas_extras}' no puede ser negativo. ingrese un valor entre 0-50")

class SalarioBaseMenorMinimoError(Exception):
    def __init__(self, salario_base, salario_minimo):
        super().__init__(f"El salario base '{salario_base}' es menor que el salario mínimo legal vigente '{salario_minimo}' (Art. 145 CST)")
        
class CargoInvalidoError(Exception):
    def __init__(self, cargo_opcion):
        super().__init__(f"El cargo '{cargo_opcion}' no es válido. Ingrese: 1: Empleado nuevo, 2: Empleado antiguo, 3: Administrador")

class PrestamoNegativoError(Exception):
    def __init__(self, prestamo):
        super().__init__(f"El valor del préstamo no puede ser negativo. Ingrese un valor mayor o igual a 0. valor ingresado: {prestamo}")

class CargoNoExistenteError(Exception):
    def __init__(self, cargo):
        super().__init__(f"No existe un cargo con el nombre '{cargo}' en la base de datos")

class TipoHoraExtraNoExistenteError(Exception):
    def __init__(self, tipo_hora):
        super().__init__(f"No existe el tipo de hora extra '{tipo_hora}' en la base de datos")

class EmpleadoNoExistenteError(Exception):
    def __init__(self, cedula):
        super().__init__(f"No existe un empleado con cédula '{cedula}' en la base de datos")

class EmpleadoExistenteError(Exception):
    def __init__(self, cedula):
        super().__init__(f"Ya existe un empleado con la cédula {cedula}. Use el botón 'Modificar Empleado' para actualizar sus datos.")

class CedulaInvalidaError(Exception):
    def __init__(self):
        super().__init__("La cédula debe contener solo números y tener entre 8 y 10 dígitos")

class NombreInvalidoError(Exception):
    def __init__(self):
        super().__init__("El nombre debe contener solo letras y espacios")

class ApellidoInvalidoError(Exception):
    def __init__(self):
        super().__init__("El apellido debe contener solo letras y espacios")
