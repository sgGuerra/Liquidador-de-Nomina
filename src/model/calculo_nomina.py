import sys
sys.path.append("src")

from model.excepciones import * 
from model.clase_empleado import Empleado 

# Constantes
SALARIO_MINIMO_LEGAL_VIGENTE = 1423500  # Salario mínimo legal vigente en 2025
AUXILIO_TRANSPORTE = 200000  # Auxilio de transporte en 2025
VALOR_UVT = 49799  # Valor de la Unidad de Valor Tributario en 2025
PORCENTAJE_SALUD = 0.04  # Porcentaje de descuento de salud
PORCENTAJE_PENSION = 0.04  # Porcentaje de descuento de pensión
DIVISOR_HORAS_LABORALES = 240  # Número de horas trabajadas en un mes
MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS = 50  # Límite de horas extra legales
SIN_HORAS_EXTRAS = 0
SIN_PRESTAMO = 0
SIN_CUOTAS = 1

PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL = {
    "limite inferior": 0.01,
    "limite superior": 0.02
}

# Bonificaciones por cargo
BONIFICACIONES_POR_CARGO = {
    "Empleado nuevo": 50000,
    "Empleado antiguo": 100000,
    "Administrador": 150000
}

# Factores de horas extras
FACTORES_HORA_EXTRA = {
    "Diurnas": 1.25,
    "Nocturnas": 1.75,
    "Festivas": 2.5,
    "N/A": 0
}


class Nomina:
    def __init__(self,  cedula_empleado: str, nombre_empleado: str, empleado_apellido, cargo, salario_base, horas_extras=0, tipo_hora_extra="N/A", 
                 horas_extras_adicionales=0, tipo_hora_extra_adicional="N/A", 
                 prestamo=0, cuotas=0, tasa_interes=6):
        
        self.empleado = Empleado(cedula_empleado,nombre_empleado,empleado_apellido)
        self.cargo = cargo
        self.salario_base = salario_base
        self.horas_extras = horas_extras
        self.tipo_hora_extra = tipo_hora_extra
        self.horas_extras_adicionales = horas_extras_adicionales
        self.tipo_hora_extra_adicional = tipo_hora_extra_adicional
        self.prestamo = prestamo
        self.cuotas = cuotas
        self.tasa_interes = tasa_interes

    def calcular_bonificacion(self):
        return BONIFICACIONES_POR_CARGO.get(self.cargo, 0)

    def calcular_valor_hora_extra(self, horas_extras, tipo_hora_extra):
        factor = FACTORES_HORA_EXTRA.get(tipo_hora_extra, 0)
        return (self.salario_base / DIVISOR_HORAS_LABORALES) * factor * horas_extras

    def calcular_salario_bruto(self):
        bonificacion = self.calcular_bonificacion()
        valor_hora_extra = self.calcular_valor_hora_extra(self.horas_extras, self.tipo_hora_extra)

        valor_hora_extra_adiccionales = 0
        if self.horas_extras_adicionales > SIN_HORAS_EXTRAS and self.tipo_hora_extra_adicional != "N/A":
            valor_hora_extra_adiccionales = self.calcular_valor_hora_extra(self.horas_extras_adicionales, self.tipo_hora_extra_adicional)
        
        return self.salario_base + bonificacion + valor_hora_extra + valor_hora_extra_adiccionales

    def calcular_deducciones(self):
        salud = self.salario_base * PORCENTAJE_SALUD
        pension = self.salario_base * PORCENTAJE_PENSION
        tasa_interes_anual = (1 + (self.tasa_interes / 100))

        if self.cuotas <= SIN_CUOTAS:
            reporte_prestamo = self.prestamo
        else:
            reporte_prestamo = (self.prestamo * tasa_interes_anual) / self.cuotas

        return salud + pension + reporte_prestamo

    def calcular_impuestos(self, salario_bruto):
        limite_inferior = 4 * VALOR_UVT
        limite_superior = 16 * VALOR_UVT

        if salario_bruto <= limite_inferior:
            return 0
        elif salario_bruto <= limite_superior:
            return (salario_bruto - limite_inferior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite inferior", 0)
        else:
            return (limite_superior - limite_inferior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite inferior", 0) + \
                   (salario_bruto - limite_superior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite superior", 0)

    def calcular(self):
        # Validación del formato de la cédula
        if not self.empleado.cedula.isdigit():
            raise CedulaInvalidaError(self.empleado.cedula)
        if len(self.empleado.cedula) < 8:
            raise CedulaMuyCortaError(self.empleado.cedula)
        if len(self.empleado.cedula) > 10:
            raise CedulaMuyLargaError(self.empleado.cedula)

        # Validación del formato del nombre
        if not all(c.isalpha() or c.isspace() for c in self.empleado.nombres):
            raise NombreInvalidoError()

        # Validación del formato del apellido
        if not all(c.isalpha() or c.isspace() for c in self.empleado.apellidos):
            raise ApellidoInvalidoError()

        if self.salario_base == 0.0:
            raise SalarioBaseInexistente()
        if self.salario_base < 0:
            raise SalarioBaseNegativoError()
        if self.salario_base < SALARIO_MINIMO_LEGAL_VIGENTE:
            raise SalarioBaseMenorMinimoError(self.salario_base, SALARIO_MINIMO_LEGAL_VIGENTE)

        if self.cargo not in BONIFICACIONES_POR_CARGO:
            raise CargoInvalidoError(self.cargo)

        if self.prestamo < SIN_PRESTAMO:
            raise PrestamoNegativoError(self.prestamo)

        salario_bruto = self.calcular_salario_bruto()
        deducciones = self.calcular_deducciones()
        impuestos = self.calcular_impuestos(salario_bruto)

        total_horas_extra = self.horas_extras + self.horas_extras_adicionales
        if total_horas_extra > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
            raise LimiteHorasExtraError(self.horas_extras, self.horas_extras_adicionales)

        if self.tipo_hora_extra not in FACTORES_HORA_EXTRA:
            raise TipoHoraExtraInvalidoError(self.tipo_hora_extra)

        if self.tipo_hora_extra_adicional not in FACTORES_HORA_EXTRA:
            raise TipoHoraExtraInvalidoError(self.tipo_hora_extra_adicional)

        if self.horas_extras < 0:
            raise ValorHoraExtraNegativoError(self.horas_extras)
        if self.horas_extras_adicionales < 0:
            raise ValorHoraExtraNegativoError(self.horas_extras_adicionales)

        if self.salario_base <= 2 * SALARIO_MINIMO_LEGAL_VIGENTE:
            auxilio_transporte = AUXILIO_TRANSPORTE
        else:
            auxilio_transporte = 0

        neto = salario_bruto + auxilio_transporte - deducciones - impuestos

        return {
            'salario_bruto': salario_bruto,
            'deducciones': deducciones,
            'impuestos': impuestos,
            'auxilio_transporte': auxilio_transporte,
            'neto': neto
        }


