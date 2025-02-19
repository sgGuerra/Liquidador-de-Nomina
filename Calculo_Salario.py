def calc_salario(salario_base: float, comisiones: float, horas_extras: int, bonificaciones: int)-> float:
    valor_hora_extra = ((salario_base/30)/8) *1.25 * horas_extras
    
    
    if (bonificaciones/(salario_base + bonificaciones)) >= (bonificaciones+salario_base) * 0.40:
        pension = ((salario_base + comisiones + bonificaciones) * 0.04)
        salud = ((salario_base + comisiones + bonificaciones) * 0.04)
    else:
        pension = ((salario_base + comisiones) * 0.04)
        salud = ((salario_base + comisiones) * 0.04)
    
    salario_bruto =  salario_base + comisiones + valor_hora_extra + bonificaciones
    
    salario_neto = salario_bruto - (salud + pension)
    
    return round(salario_neto, 2)

print(calc_salario(1165000, 17475, 5, 40000))
   
