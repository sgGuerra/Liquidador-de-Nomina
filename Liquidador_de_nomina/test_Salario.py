import unittest
import Calculo_Salario

class CalculoSalarioTest(unittest.TestCase):
    
    def test_caso_normal(self):
        
        # Datos entrada
        
        salario_base: float = 1165000
        comisiones: float = 17475
        horas_extras: int = 5
        bonificaciones: int = 40000
        
        # Datos salida
        
        salario_esperado = 1158215.54
        
        resultado = Calculo_Salario.calc_salario(salario_base, comisiones, horas_extras, bonificaciones)
        
        self.assertAlmostEqual(salario_esperado, resultado, 2)
    

    def test_caso_extraordinario_prestamos(self):

        #Datos entrada

        salario_base: float = 1423500
        comisiones: float = 12811
        horas_extras: int = 55
        bonificaciones: int = 70000
        prestamos = 500000

        #Datos salida

        salario_esperado = 1299180.02

        resultado = Calculo_Salario.calc_salario(salario_base, comisiones, horas_extras, bonificaciones, prestamos)

        self.assertAlmostEqual(salario_esperado, resultado, 0)
        
        
if __name__ == '__main__':
    unittest.main()
