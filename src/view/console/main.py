import sys 
sys.path.append("src")
from src.model.calculo_salario import calcular_nomina
from src.model.excepciones import *
def consola():
    print("Bienvenido al sistema de cálculo de nómina")
    cargo = input("Ingrese el cargo del empleado (Empleado nuevo, Empleado antiguo, Administrador): ")
    try:
        salario_base = float(input("Ingrese el salario base: "))
        horas_extras = float(input("Ingrese las horas extras trabajadas: "))
        tipo_hora_extra = input("Ingrese el tipo de hora extra (Diurnas, Nocturnas, Festivas, N/A): ")
        horas_extras_adicionales = float(input("Ingrese las horas extras adicionales (0 si no aplica): "))
        tipo_hora_extra_adicional = input("Ingrese el tipo de hora extra adicional (Diurnas, Nocturnas, Festivas, N/A): ")
        prestamo = float(input("Ingrese el monto del préstamo (si no tiene, ingrese 0): "))
        cuotas = int(input("Ingrese el número de cuotas del préstamo: "))
        tasa_interes_anual = float(input("Ingrese la tasa de interés anual del préstamo: "))

        salario_neto = calcular_nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)
        print(f"El salario neto del empleado es: {salario_neto:.2f}")

    except SalarioBaseNegativoError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"ocurrió un error inesperado{e}")
        
        
if __name__ == "__main__":
    consola()