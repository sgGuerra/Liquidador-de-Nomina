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
        
        self.assertAlmostEqual(salario_esperado, resultado)
        
if __name__ == '__main__':
    unittest.main()
