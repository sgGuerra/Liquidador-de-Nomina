import unittest
from Calculos.calculo_salario import calcular_nomina

class CalculoSalarioTest(unittest.TestCase):

    def test_caso_normal_1(self):
        # Datos entrada
        cargo = "Empleado nuevo"
        salario_base = 1650000
        horas_extras = 5
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 500000
        cuotas = 12
        tasa_interes_anual = 6

        # Datos salida

        salario_esperado = 1741902.51

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_2(self):
        # Datos entrada
        cargo = "Empleado nuevo"
        salario_base = 1750000
        horas_extras = 0
        tipo_hora_extra = "N/A"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 600000
        cuotas = 12
        tasa_interes_anual = 7

        # Datos salida

        salario_esperado = 1780459.80

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_3(self):
        # Datos entrada
        cargo = "Administrador"
        salario_base = 4000000
        horas_extras = 15
        tipo_hora_extra = "Festivas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 100000
        cuotas = 12
        tasa_interes_anual = 6

        # Datos salida

        salario_esperado = 4360626.47

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_4(self):
        # Datos entrada
        cargo = "Empleado nuevo"
        salario_base = 1850000
        horas_extras = 25
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 0
        cuotas = 12
        tasa_interes_anual = 6

        # Datos salida

        salario_esperado = 2254454.59

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_SalarioAlto(self):
        
        # Datos entrada
        cargo = "Administrador"
        salario_base =  50000000
        horas_extras = 25
        tipo_hora_extra = "Festivas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 20000000
        cuotas = 40
        tasa_interes_anual = 6
        
        
        # Datos salida
        
        salario_esperado =  57387376.47 
        
        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)
        
        self.assertAlmostEqual(salario_esperado, resultado, 2)
        
    def test_caso_extraordinario_MaxHorasExtras(self):
        
        # Datos entrada
        cargo = "Empleado nuevo"
        salario_base = 1760800
        horas_extras = 30
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 0
        cuotas = 0
        tasa_interes_anual = 6
        
        
        # Datos salida
        
        salario_esperado =  2113302.30 

        
        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)
        
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_MaxCuotas(self):
        # Datos entrada
        cargo = "Empleado antiguo"
        salario_base = 2060000
        horas_extras = 10
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 2000000
        cuotas = 60
        tasa_interes_anual = 6

        # Datos salida

        salario_esperado =  2273830.63

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_HorasExtrasAdiccionales(self):

        # Datos entrada
        cargo = "Administrador"
        salario_base = 5670500.00
        horas_extras = 5
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 2
        tipo_hora_extra_adicional = "Festivas"
        prestamo = 4000000
        cuotas = 10
        tasa_interes_anual = 6

        # Datos salida

        salario_esperado = 5096898.39

        resultado = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                                    tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)

        self.assertAlmostEqual(salario_esperado, resultado, 2)
        
        
if __name__ == '__main__':
    unittest.main()
