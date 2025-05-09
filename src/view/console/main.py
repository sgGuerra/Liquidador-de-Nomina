import sys 
sys.path.append("src")
from model.calculo_nomina import Nomina, SALARIO_MINIMO_LEGAL_VIGENTE, MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS, SIN_HORAS_EXTRAS, SIN_PRESTAMO
from model.excepciones import *

class ConsolaNomina:
    """
    Función principal de la consola para el cálculo de nómina.
    """
    
    def __init__(self):
        self.cargos = {1: "Empleado nuevo", 2: "Empleado antiguo", 3: "Administrador"}
        self.tipos_hora_extra = {1: "Diurnas", 2: "Nocturnas", 3: "Festivas"}
        self.resultados = []
        self.cargo = None
        self.salario_base = None
        self.horas_extras = None
        self.tipo_hora_extra = None
        self.horas_extras_adicionales = None
        self.tipo_hora_extra_adicional = None
        self.prestamo = None
        self.cuotas = None
        self.tasa_interes_anual = None
        self.cedula = None
        self.nombres = None
        self.apellidos = None

    def _solicitar_datos_personales(self):
        """
        Solicita al usuario los datos personales del empleado.
        """
        while True:
            try:
                self.cedula = input("Ingrese la cédula del empleado: ").strip()
                if not self.cedula:
                    raise ValueError("La cédula no puede estar vacía.")

                self.nombres = input("Ingrese los nombres del empleado: ").strip()
                if not self.nombres:
                    raise ValueError("Los nombres no pueden estar vacíos.")

                self.apellidos = input("Ingrese los apellidos del empleado: ").strip()
                if not self.apellidos:
                    raise ValueError("Los apellidos no pueden estar vacíos.")

                break
            except ValueError as e:
                print(f"Error: {e}")
    
    def _solicitar_cargo(self):
        """
        Solicita al usuario el cargo del empleado.
        """
        while True:
            print("Seleccione el cargo del empleado:")
            for key, value in self.cargos.items():
                print(f"{key}. {value}")
            try:
                cargo_opcion = int(input("Ingrese el número correspondiente al cargo: "))
                cargo = self.cargos.get(cargo_opcion, None)
                if not cargo:
                    raise CargoInvalidoError(cargo_opcion)
                self.cargo = cargo
                break
            except CargoInvalidoError as e:
                print(f"Error: {e}")
    
    def _solicitar_salario_base(self):
        """
        Solicita al usuario el salario base del empleado.
        """
        while True:
            try:
                salario_base = float(input("Ingrese el salario base: "))
                if salario_base < 0:
                    raise SalarioBaseNegativoError()
                if salario_base < SALARIO_MINIMO_LEGAL_VIGENTE:
                    raise SalarioBaseMenorMinimoError(salario_base, SALARIO_MINIMO_LEGAL_VIGENTE)
                self.salario_base = salario_base
                break
            except SalarioBaseNegativoError as e:
                print(f"Error: {e}")
            except SalarioBaseMenorMinimoError as e:
                print(f"Error: {e}")
    
    def _solicitar_horas_extras(self):
        """
        Solicita al usuario las horas extras trabajadas por el empleado.
        """
        while True:
            try:
                horas_extras = float(input("Ingrese las horas extras trabajadas: "))
                if horas_extras < 0:
                    raise ValorHoraExtraNegativoError(horas_extras) 
                if horas_extras > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
                    raise LimiteHorasExtraError(horas_extras, 0)
                self.horas_extras = horas_extras
                break            
            except LimiteHorasExtraError as e:
                print(f"Error: {e}")
            except ValorHoraExtraNegativoError as e:
                print(f"Error: {e}")
    
    def _solicitar_tipo_hora_extra(self):
        """
        Solicita al usuario el tipo de hora extra trabajada por el empleado.
        """
        while True:
            try:
                tipo_hora_extra = "N/A"
                if self.horas_extras > SIN_HORAS_EXTRAS:
                    print("Seleccione el tipo de hora extra:")
                    for key, value in self.tipos_hora_extra.items():
                        print(f"{key}. {value}")
                    tipo_hora_extra_opcion = int(input("Ingrese el número correspondiente al tipo de hora extra: "))
                    tipo_hora_extra = self.tipos_hora_extra.get(tipo_hora_extra_opcion, None)
                    if not tipo_hora_extra:
                        raise TipoHoraExtraInvalidoError(tipo_hora_extra)
                self.tipo_hora_extra = tipo_hora_extra
                break
            except TipoHoraExtraInvalidoError as e:
                print(f"Error: {e}")
    
    def _solicitar_horas_extras_adicionales(self):
        """
        Solicita al usuario las horas extras adicionales trabajadas por el empleado.
        """
        while True:
            try:
                horas_extras_adicionales = float(input("Ingrese las horas extras adicionales (0 si no aplica): "))
                if horas_extras_adicionales < 0:
                    raise ValorHoraExtraNegativoError(horas_extras_adicionales) 
                if horas_extras_adicionales > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
                    raise LimiteHorasExtraError(self.horas_extras, horas_extras_adicionales)
                self.horas_extras_adicionales = horas_extras_adicionales
                break
            except LimiteHorasExtraError as e:
                print(f"Error: {e}")
            except ValorHoraExtraNegativoError as e:
                print(f"Error: {e}")
    
    def _solicitar_tipo_hora_extra_adicional(self):
        """
        Solicita al usuario el tipo de hora extra adicional trabajada por el empleado.
        """
        while True:
            try:
                tipo_hora_extra_adicional = "N/A"
                if self.horas_extras_adicionales > SIN_HORAS_EXTRAS:
                    print("Seleccione el tipo de hora extra adicional:")
                    for key, value in self.tipos_hora_extra.items():
                        print(f"{key}. {value}")
                    tipo_hora_extra_adicional_opcion = int(input("Ingrese el número correspondiente al tipo de hora extra adicional: "))
                    tipo_hora_extra_adicional = self.tipos_hora_extra.get(tipo_hora_extra_adicional_opcion, None)
                    if not tipo_hora_extra_adicional:
                        raise TipoHoraExtraInvalidoError(tipo_hora_extra_adicional)
                self.tipo_hora_extra_adicional = tipo_hora_extra_adicional
                break               
            except TipoHoraExtraInvalidoError as e:
                print(f"Error: {e}")
        
    def _solicitar_prestamo(self):
        """
        Solicita al usuario el monto del préstamo del empleado.
        """
        while True:
            try:
                prestamo = float(input("Ingrese el monto del préstamo (si no tiene, ingrese 0): "))
                if prestamo < 0:
                    raise PrestamoNegativoError(prestamo)
                self.prestamo = prestamo
                break            
            except PrestamoNegativoError as e:
                print(f"Error: {e}")
    
    def _solicitar_cuotas(self):
        """
        Solicita al usuario el número de cuotas del préstamo del empleado.
        """
        while True:
            try:
                cuotas = 0
                tasa_interes_anual = 0
                if self.prestamo > SIN_PRESTAMO:
                    cuotas = int(input("Ingrese el número de cuotas del préstamo: "))
                    tasa_interes_anual = float(input("Ingrese la tasa de interés anual del préstamo: "))
                self.cuotas = cuotas
                self.tasa_interes_anual = tasa_interes_anual
                break
            except ValueError as e:
                print(f"Error: {e}")

    def procesar_nomina(self):
        print("\n------------------------------------------\nBienvenido al sistema de cálculo de nómina\n------------------------------------------\n")
        while True:
            self._solicitar_datos_personales()
            self._solicitar_cargo()
            self._solicitar_salario_base()
            self._solicitar_horas_extras()
            self._solicitar_tipo_hora_extra()
            self._solicitar_horas_extras_adicionales()
            self._solicitar_tipo_hora_extra_adicional()
            self._solicitar_prestamo()
            self._solicitar_cuotas()
            self._calcular_nomina()
            
            otra_nomina = input("¿Desea calcular otra nómina? (s/n): ").strip().lower()
            if otra_nomina != 's':
                break

        self.mostrar_resultados()

    def _calcular_nomina(self):
        nomina = Nomina(self.cedula, self.nombres, self.apellidos, self.cargo, self.salario_base, self.horas_extras, self.tipo_hora_extra, self.horas_extras_adicionales, self.tipo_hora_extra_adicional, self.prestamo, self.cuotas, self.tasa_interes_anual)
        salario_neto = nomina.calcular()
        bonificacion = nomina.calcular_bonificacion()
        valor_horas_extra = nomina.calcular_valor_hora_extra(self.horas_extras, self.tipo_hora_extra)
        valor_horas_extra_adicionales = nomina.calcular_valor_hora_extra(self.horas_extras_adicionales, self.tipo_hora_extra_adicional)
        total_horas_extra = (valor_horas_extra * self.horas_extras) + (valor_horas_extra_adicionales * self.horas_extras_adicionales)
        self.resultados.append({
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "cargo": self.cargo,
            "salario_base": self.salario_base,
            "bonificacion": bonificacion,       
            "horas_extras": self.horas_extras,
            "tipo_hora_extra": self.tipo_hora_extra,
            "horas_extras_adicionales": self.horas_extras_adicionales,
            "tipo_hora_extra_adicional": self.tipo_hora_extra_adicional,
            "total_horas_extra": total_horas_extra,
            "prestamo": self.prestamo,
            "cuotas": self.cuotas,
            "tasa_interes_anual": self.tasa_interes_anual,
            "salario_neto": salario_neto
        })

    def mostrar_resultados(self):
        print("\nFactura de Nóminas Calculadas:")
        for i, resultado in enumerate(self.resultados, 1):
            print(f"\nEmpleado {i}:")
            print(f"  Cédula: {resultado['cedula']}")
            print(f"  Nombres: {resultado['nombres']}")
            print(f"  Apellidos: {resultado['apellidos']}")
            print(f"  Cargo: {resultado['cargo']}")
            print(f"  Salario Base: ${resultado['salario_base']:.2f}")
            print(f"  Bonificación por cargo: ${resultado['bonificacion']:.2f}")
            print(f"  Horas Extras: {int(resultado['horas_extras'])}")
            print(f"  Tipo de Hora Extra: {resultado['tipo_hora_extra']}")
            print(f"  Horas Extras Adicionales: {int(resultado['horas_extras_adicionales'])}")
            print(f"  Tipo de Hora Extra Adicional: {resultado['tipo_hora_extra_adicional']}")
            print(f"  Valor total de horas extra: ${resultado['total_horas_extra']:.2f}")
            print(f"  Préstamo: ${resultado['prestamo']:.2f}")
            print(f"  Cuotas: {resultado['cuotas']}")
            print(f"  Tasa de Interés Anual: {resultado['tasa_interes_anual']:.1f}%")
            print(f"  Salario Neto: ${resultado['salario_neto']:.2f}")

if __name__ == "__main__":
    ConsolaNomina().procesar_nomina()