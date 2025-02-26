class SalarioBaseNegativoError(Exception):
    def __init__(self, mensaje="Salario base negativo (Art. 127 CST)"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)