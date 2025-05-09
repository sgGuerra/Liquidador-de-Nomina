from model.clase_empleado import Empleado

class EmpleadoController:
    def __init__(self):
        self.empleados = []  # Lista para almacenar empleados

    def agregar_empleado(self, cedula, nombres, apellidos):
        """
        Agrega un nuevo empleado a la lista.
        """
        empleado = Empleado(cedula, nombres, apellidos)
        self.empleados.append(empleado)
        return empleado

    def obtener_empleado_por_cedula(self, cedula):
        """
        Busca un empleado por su cédula.
        """
        for empleado in self.empleados:
            if empleado.cedula == cedula:
                return empleado
        return None

    def listar_empleados(self):
        """
        Devuelve la lista de empleados.
        """
        return self.empleados