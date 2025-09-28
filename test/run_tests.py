import unittest
import sys
from pathlib import Path
from test_nomina import CalculoSalarioTest
from test_nomina_DB import TestNominaDB

# Añadir el directorio raíz del proyecto al PYTHONPATH
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

def run_all_tests():
    # Crear el test suite
    test_suite = unittest.TestSuite()
    
    # Añadir todas las pruebas de cálculo de nómina
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CalculoSalarioTest))
    
    # Añadir todas las pruebas de base de datos
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestNominaDB))
    
    # Crear el runner y ejecutar las pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Ejecutando todas las pruebas del Liquidador de Nómina...")
    success = run_all_tests()
    sys.exit(0 if success else 1)