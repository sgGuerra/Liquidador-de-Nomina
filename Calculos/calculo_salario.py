from Excepciones.Exceptions import * 
# Constantes
SMLV = 1423500  # Salario mínimo legal vigente en 2025
AUXILIO_TRANSPORTE = 200000  # Auxilio de transporte en 2025
VALOR_UVT = 49799  # Valor de la Unidad de Valor Tributario en 2025
PORCENTAJE_SALUD = 0.04  # Porcentaje de descuento de salud
PORCENTAJE_PENSION = 0.04  # Porcentaje de descuento de pensión
DIVISOR_HORAS_LABORALES = 240 # Varia dependiendo de la frecuencia de pago(Mensual, Semanal, Quincenal, etc.), Se refiere al numero de horas trabajadas diarias por los dias trabajados
MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS = 50



PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL= {
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

def calcular_bonificacion(cargo):
    return BONIFICACIONES_POR_CARGO.get(cargo, 0)

def calcular_valor_hora_extra(salario_base, horas_extras, tipo_hora_extra):
    factor = FACTORES_HORA_EXTRA.get(tipo_hora_extra, 0)
    return (salario_base / DIVISOR_HORAS_LABORALES) * float(factor) * horas_extras

def calcular_salario_bruto(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional):
    bonificacion = calcular_bonificacion(cargo)
    valor_hora_extra = calcular_valor_hora_extra(salario_base, horas_extras, tipo_hora_extra)

    if horas_extras_adicionales > 0 and tipo_hora_extra_adicional != "N/A":
        valor_hora_extra_adiccionales = calcular_valor_hora_extra(salario_base, horas_extras_adicionales, tipo_hora_extra_adicional)
    else:
        valor_hora_extra_adiccionales = 0
    return salario_base + bonificacion + valor_hora_extra + valor_hora_extra_adiccionales

def calcular_deducciones(salario_base, prestamo, cuotas, tasa_interes):
    salud = salario_base * PORCENTAJE_SALUD
    pension = salario_base * PORCENTAJE_PENSION
    tasa_interes_anual = (1+(tasa_interes / 100))
    
    if cuotas <= 1:
        reporte_prestamo = prestamo
    else:
        reporte_prestamo = (prestamo * tasa_interes_anual) / cuotas

    return salud + pension + reporte_prestamo

def calcular_impuestos(salario_bruto):
    
    limite_inferior = 4 * VALOR_UVT
    limite_superior = 16 * VALOR_UVT
    
    if salario_bruto <= limite_inferior:
        return 0
    elif salario_bruto <= limite_superior:
        return (salario_bruto - limite_inferior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite inferior",0) #
    else:
        return (limite_superior - limite_inferior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite inferior",0) + (salario_bruto - limite_superior) * PORCENTAJE_APORTE_FONDO_SOLIDARIDAD_PENSIONAL.get("limite superior",0)

def calcular_nomina(cargo, salario_base, horas_extras=0, tipo_hora_extra="N/A", horas_extras_adicionales=0, tipo_hora_extra_adicional="N/A", prestamo=0, cuotas=0, tasa_interes=6):

    if salario_base <= 0:
        raise SalarioBaseNegativoError()

    salario_bruto = calcular_salario_bruto(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional)
    deducciones = calcular_deducciones(salario_base, prestamo, cuotas, tasa_interes)
    impuestos = calcular_impuestos(salario_bruto)

    total_horas_extra = horas_extras + horas_extras_adicionales
    if total_horas_extra > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
        raise LimiteHorasExtraError(horas_extras, horas_extras_adicionales)

    if tipo_hora_extra not in FACTORES_HORA_EXTRA.keys():
        raise TipoHoraExtraInvalidoError(tipo_hora_extra)

    if tipo_hora_extra_adicional not in FACTORES_HORA_EXTRA.keys():
        raise TipoHoraExtraInvalidoError(tipo_hora_extra_adicional)

    if horas_extras < 0:
        raise ValorHoraExtraNegativoError(horas_extras)
    if horas_extras_adicionales < 0:
        raise ValorHoraExtraNegativoError(horas_extras_adicionales)
     
    if salario_base <= 2 * SMLV:
        auxilio_transporte = AUXILIO_TRANSPORTE
    else:
        auxilio_transporte = 0

    return salario_bruto + auxilio_transporte - deducciones - impuestos


