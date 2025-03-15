import sys 
sys.path.append("src")
from model.calculo_nomina import Nomina, SALARIO_MINIMO_LEGAL_VIGENTE, MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS
from model.excepciones import *

# Constantes
SIN_HORAS_EXTRAS = 0
SIN_PRESTAMO = 0

def consola():
    """
    Función principal de la consola para el cálculo de nómina.
    Permite al usuario ingresar los datos necesarios para calcular la nómina de un empleado.
    """
    cargos = {1: "Empleado nuevo", 2: "Empleado antiguo", 3: "Administrador"}
    tipos_hora_extra = {1: "Diurnas", 2: "Nocturnas", 3: "Festivas"}
    resultados = []

    print("Bienvenido al sistema de cálculo de nómina\n------------------------------------------\n")
    while True:
        print("Seleccione el cargo del empleado:")
        for key, value in cargos.items():
            print(f"{key}. {value}")
        cargo_opcion = int(input("Ingrese el número correspondiente al cargo: "))
        cargo = cargos.get(cargo_opcion, None)
        if not cargo:
            print("Opción inválida. Por favor, intente nuevamente.")
            continue

        try:
            salario_base = float(input("Ingrese el salario base: "))
            if salario_base < 0:
                raise SalarioBaseNegativoError()
            if salario_base < SALARIO_MINIMO_LEGAL_VIGENTE:
                raise SalarioBaseMenorMinimoError(salario_base, SALARIO_MINIMO_LEGAL_VIGENTE)

            horas_extras = float(input("Ingrese las horas extras trabajadas: "))
            if horas_extras < 0:
                raise ValorHoraExtraNegativoError(horas_extras) 
            if horas_extras > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
                raise LimiteHorasExtraError(horas_extras, 0)

            tipo_hora_extra = "N/A"
            if horas_extras > SIN_HORAS_EXTRAS:
                print("Seleccione el tipo de hora extra:")
                for key, value in tipos_hora_extra.items():
                    print(f"{key}. {value}")
                tipo_hora_extra_opcion = int(input("Ingrese el número correspondiente al tipo de hora extra: "))
                tipo_hora_extra = tipos_hora_extra.get(tipo_hora_extra_opcion, None)
                if not tipo_hora_extra:
                    raise TipoHoraExtraInvalidoError(tipo_hora_extra)

            horas_extras_adicionales = float(input("Ingrese las horas extras adicionales (0 si no aplica): "))
            if horas_extras_adicionales < 0:
                raise ValorHoraExtraNegativoError(horas_extras_adicionales) 
            if horas_extras_adicionales > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
                raise LimiteHorasExtraError(horas_extras, horas_extras_adicionales)

            tipo_hora_extra_adicional = "N/A"
            if horas_extras_adicionales > SIN_HORAS_EXTRAS:
                print("Seleccione el tipo de hora extra adicional:")
                for key, value in tipos_hora_extra.items():
                    print(f"{key}. {value}")
                tipo_hora_extra_adicional_opcion = int(input("Ingrese el número correspondiente al tipo de hora extra adicional: "))
                tipo_hora_extra_adicional = tipos_hora_extra.get(tipo_hora_extra_adicional_opcion, None)
                if not tipo_hora_extra_adicional:
                    raise TipoHoraExtraInvalidoError(tipo_hora_extra_adicional)

            prestamo = float(input("Ingrese el monto del préstamo (si no tiene, ingrese 0): "))
            if prestamo < 0:
                raise ValueError("El monto del préstamo no puede ser negativo.")

            cuotas = 0
            tasa_interes_anual = 0
            if prestamo > SIN_PRESTAMO:
                cuotas = int(input("Ingrese el número de cuotas del préstamo: "))
                tasa_interes_anual = float(input("Ingrese la tasa de interés anual del préstamo: "))

            nomina = Nomina(cargo, salario_base, horas_extras, tipo_hora_extra, horas_extras_adicionales, tipo_hora_extra_adicional, prestamo, cuotas, tasa_interes_anual)
            salario_neto = nomina.calcular()
            bonificacion = nomina.calcular_bonificacion()
            valor_horas_extra = nomina.calcular_valor_hora_extra(horas_extras, tipo_hora_extra)
            valor_horas_extra_adicionales = nomina.calcular_valor_hora_extra(horas_extras_adicionales, tipo_hora_extra_adicional)
            total_horas_extra = (valor_horas_extra * horas_extras) + (valor_horas_extra_adicionales * horas_extras_adicionales)
            resultados.append({
                "cargo": cargo,
                "salario_base": salario_base,
                "bonificacion": bonificacion,       
                "horas_extras": horas_extras,
                "tipo_hora_extra": tipo_hora_extra,
                "horas_extras_adicionales": horas_extras_adicionales,
                "tipo_hora_extra_adicional": tipo_hora_extra_adicional,
                "total_horas_extra": total_horas_extra,
                "prestamo": prestamo,
                "cuotas": cuotas,
                "tasa_interes_anual": tasa_interes_anual,
                "salario_neto": salario_neto
            })

            otra_nomina = input("¿Desea calcular otra nómina? (s/n): ").strip().lower()
            if otra_nomina != 's':
                break

        except SalarioBaseNegativoError as e:
            print(f"{e}")
        except SalarioBaseMenorMinimoError as e:
            print(f"Error: {e}")
        except LimiteHorasExtraError as e:
            print(f"Error: {e}")
        except TipoHoraExtraInvalidoError as e:
            print(f"Error: {e}")
        except ValorHoraExtraNegativoError as e:
            print(f"Error: {e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
        print("Por favor, intente nuevamente.\n")

    print("\nFactura de Nóminas Calculadas:")
    for i, resultado in enumerate(resultados, 1):
        print(f"\nEmpleado {i}:")
        print(f"  Cargo: {resultado['cargo']}")
        print(f"  Salario Base: ${resultado['salario_base']:.2f}")
        print(f"  Bonificación por cargo: ${resultado['bonificacion']:.2f}")
        print(f"  Horas Extras: {int(resultado['horas_extras'])} - Tipo de Hora Extra: {resultado['tipo_hora_extra']}")
        print(f"  Horas Extras Adicionales: {int(resultado['horas_extras_adicionales'])} - Tipo de Hora Extra Adicional: {resultado['tipo_hora_extra_adicional']}")
        print(f"  Valor total de horas extra: ${resultado['total_horas_extra']:.2f}")
        print(f"  Préstamo: ${resultado['prestamo']:.2f}")
        print(f"  Cuotas: {resultado['cuotas']}")
        print(f"  Tasa de Interés Anual: {resultado['tasa_interes_anual']:.1f}%")
        print(f"  Salario Neto: ${resultado['salario_neto']:.2f}")

if __name__ == "__main__":
    consola()