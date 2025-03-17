import unittest
import sys
sys.path.append("src")

from model.calculo_nomina import Nomina
from model.excepciones import *

class CalculoSalarioTest(unittest.TestCase):

    def test_caso_normal_1(self):
        cargo = "Empleado nuevo"
        salario_base = 1650000
        horas_extras = 5
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 500000
        cuotas = 12
        tasa_interes = 6
        salario_esperado = 1741902.51

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_2(self):
        cargo = "Empleado nuevo"
        salario_base = 1750000
        horas_extras = 0
        tipo_hora_extra = "N/A"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 600000
        cuotas = 12
        tasa_interes = 7

        salario_esperado = 1780459.80

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_3(self):
        cargo = "Administrador"
        salario_base = 4000000
        horas_extras = 15
        tipo_hora_extra = "Festivas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 100000
        cuotas = 12
        tasa_interes = 6

        salario_esperado = 4360626.47

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_normal_4(self):
        cargo = "Empleado nuevo"
        salario_base = 1850000
        horas_extras = 25
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 0
        cuotas = 12
        tasa_interes = 6

        salario_esperado = 2254454.59

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_SalarioAlto(self):
        cargo = "Administrador"
        salario_base = 50000000
        horas_extras = 25
        tipo_hora_extra = "Festivas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 20000000
        cuotas = 40
        tasa_interes = 6


        salario_esperado = 57387376.47
        
        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_MaxHorasExtras(self):
        cargo = "Empleado nuevo"
        salario_base = 1760800
        horas_extras = 30
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 0
        cuotas = 0
        tasa_interes = 6

        salario_esperado = 2113302.30

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_MaxCuotas(self):
        cargo = "Empleado antiguo"
        salario_base = 2060000
        horas_extras = 10
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 2000000
        cuotas = 60
        tasa_interes = 6

        salario_esperado = 2273830.63

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_caso_extraordinario_HorasExtrasAdiccionales(self):
        cargo = "Administrador"
        salario_base = 5670500.00
        horas_extras = 5
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 2
        tipo_hora_extra_adicional = "Festivas"
        prestamo = 4000000
        cuotas = 10
        tasa_interes = 6

        salario_esperado = 5096898.39

        nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, 
                        tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
        
        resultado = nomina.calcular()
        self.assertAlmostEqual(salario_esperado, resultado, 2)

    def test_salario_negativo(self):
        cargo = "Empleado nuevo"
        salario_base = -1000000
        horas_extras = 15
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 300000
        cuotas = 15
        tasa_interes = 6

        with self.assertRaises(SalarioBaseNegativoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()

    def test_tipo_hora_extra_invalido(self):
        cargo = "Empleado nuevo"
        salario_base = 1650200
        horas_extras = 5
        tipo_hora_extra = "Festibas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 600000
        cuotas = 32
        tasa_interes = 6

        with self.assertRaises(TipoHoraExtraInvalidoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()

    def test_horas_extra_negativas(self):
        cargo = "Empleado antiguo"
        salario_base = 1560300
        horas_extras = -10
        tipo_hora_extra = "Diurnas"
        horas_extras_adicionales = 0
        tipo_hora_extra_adicional = "N/A"
        prestamo = 0
        cuotas = 0
        tasa_interes = 0

        with self.assertRaises(ValorHoraExtraNegativoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()

    def test_limite_horas_extra_excedido(self):
        cargo = "Administrador"
        salario_base = 4350000
        horas_extras = 26
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 25
        tipo_hora_extra_adicional = "Diurnas"
        prestamo = 500000
        cuotas = 10
        tasa_interes = 6

        with self.assertRaises(LimiteHorasExtraError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()
    
    def test_salario_base_menor_minimo(self):
        cargo = "Administrador"
        salario_base = 100000
        horas_extras = 26
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 25
        tipo_hora_extra_adicional = "Diurnas"
        prestamo = 500000
        cuotas = 10
        tasa_interes = 6

        with self.assertRaises(SalarioBaseMenorMinimoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()

    def test_cargo_invalido(self):
        cargo = "Empleado nueva"
        salario_base = 1680000
        horas_extras = 20
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 15
        tipo_hora_extra_adicional = "Diurnas"
        prestamo = 500000
        cuotas = 10
        tasa_interes = 6

        with self.assertRaises(CargoInvalidoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()

    def test_prestamo_negativo(self):
        cargo = "Empleado antiguo"
        salario_base = 2000000
        horas_extras = 16
        tipo_hora_extra = "Nocturnas"
        horas_extras_adicionales = 20
        tipo_hora_extra_adicional = "Diurnas"
        prestamo = -400000
        cuotas = 10
        tasa_interes = 6
        
        with self.assertRaises(PrestamoNegativoError):
            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales,
                            tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes)
            nomina.calcular()
        
        
    
if __name__ == '__main__':
    unittest.main()