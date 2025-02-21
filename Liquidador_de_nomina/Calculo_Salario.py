def deducciones(salario_base: float, prestamos: float) -> float:
    UVT = 49799
    valor_de_impuestos = 0
    if salario_base > (95*UVT) and salario_base <= (150*UVT):
        valor_de_impuestos = salario_base * 0.19
    elif salario_base > (150*UVT) and salario_base <= (360*UVT):
        valor_de_impuestos = salario_base * 0.28
    elif salario_base > (360*UVT):
        valor_de_impuestos = salario_base * 0.33



    return valor_de_impuestos + prestamos



def calc_salario(salario_base: float, comisiones: float, horas_extras: int, bonificaciones: int, prestamos = 0)-> float:
    valor_hora_extra = (((salario_base/30)/8) *1.25 * horas_extras)
    
    
    if (bonificaciones/(salario_base + bonificaciones)) >= (bonificaciones+salario_base) * 0.40:
        pension = ((salario_base + comisiones + bonificaciones) * 0.04)
        salud = ((salario_base + comisiones + bonificaciones) * 0.04)
    else:
        pension = ((salario_base + comisiones) * 0.04)
        salud = ((salario_base + comisiones) * 0.04)
    
    salario_bruto =  salario_base + comisiones + valor_hora_extra + bonificaciones
    
    valor_deducciones = deducciones(salario_base, prestamos)
    salario_neto = salario_bruto - (salud + pension + valor_deducciones)
    
    
    return salario_neto

print(calc_salario(1165000, 17475, 5, 40000))
   
