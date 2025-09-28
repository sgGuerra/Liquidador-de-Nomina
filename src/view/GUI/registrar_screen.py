import sys
import os

# Permite que encuentre correctamente el paquete model al compilar con PyInstaller
if hasattr(sys, '_MEIPASS'):
    sys.path.append(os.path.join(sys._MEIPASS, "src"))
else:
    sys.path.append("src")

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from model.calculo_nomina import Nomina
from model.excepciones import *
from controller.nomina_controller import NominaController

class RegistrarEmpleadoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'registrar'

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        main_layout.add_widget(Label(
            text="REGISTRAR NUEVO EMPLEADO",
            font_size=24,
            size_hint=(1, 0.5),
            bold=True
        ))

        # Layout del formulario con scroll
        form = GridLayout(
            cols=2,
            spacing=15,
            padding=10,
            size_hint=(1, None),
            height=550
        )
        self.inputs = {}  # Diccionario para almacenar las referencias a los campos

        # Campos del formulario con ejemplos como hint_text
        cedula_input = TextInput(
            input_filter='int',
            multiline=False,
            hint_text="Ej: 1234567890"
        )
        cedula_input.bind(text=self.on_cedula_cambio)  # Vinculamos el evento de cambio de texto

        campos = [
            ("Cédula", cedula_input),
            ("Nombres", TextInput(
                multiline=False,
                hint_text="Ej: Juan Carlos"
            )),
            ("Apellidos", TextInput(
                multiline=False,
                hint_text="Ej: Pérez Gómez"
            )),
            ("Cargo", Spinner(
                values=["Empleado nuevo", "Empleado antiguo", "Administrador"],
                text="Empleado nuevo"
            )),
            ("Salario Base", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 1000000"
            )),
            ("Horas Extras", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 8"
            )),
            ("Tipo Hora Extra", Spinner(
                values=["N/A", "Diurnas", "Nocturnas", "Festivas"],
                text="N/A"
            )),
            ("Horas Extras Adicionales", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 4"
            )),
            ("Tipo Hora Extra Adicional", Spinner(
                values=["N/A", "Diurnas", "Nocturnas", "Festivas"],
                text="N/A"
            )),
            ("Préstamo", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 500000"
            )),
            ("Cuotas", TextInput(
                input_filter='int',
                multiline=False,
                hint_text="Ej: 6"
            )),
            ("Tasa de Interés (%)", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 2.5"
            )),
        ]

        # Se agregan campos al formulario y se registran en el diccionario
        for label_text, widget in campos:
            form.add_widget(Label(text=label_text))
            form.add_widget(widget)
            self.inputs[label_text] = widget

        # Agregamos el formulario al layout principal una sola vez
        main_layout.add_widget(form)

        # Área de botones
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        # Botón registrar
        btn_registrar = Button(
            text="Registrar Empleado",
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint=(0.8, 1)
        )
        btn_registrar.bind(on_press=self.registrar_empleado)

        # Botón volver
        btn_volver = Button(
            text="Volver",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_volver.bind(on_press=lambda x: self.volver_menu_principal())

        button_layout.add_widget(btn_registrar)
        button_layout.add_widget(btn_volver)

        main_layout.add_widget(button_layout)

        # Área de resultados
        self.resultado_label = Label(
            text="",
            halign='left',
            valign='top',
            size_hint=(1, 1)
        )
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        main_layout.add_widget(self.resultado_label)

        self.add_widget(main_layout)

    def on_cedula_cambio(self, instance, value):
        """Limita la longitud de la cédula entre 8 y 10 dígitos y valida que solo sean números"""
        if value:  # Solo si hay valor
            # Remover cualquier caracter que no sea dígito
            value = ''.join(filter(str.isdigit, value))
            # Limitar a 10 dígitos
            if len(value) > 10:
                value = value[:10]
            # Actualizar el texto del input
            instance.text = value

    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje"""
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()

    def validar_campos_requeridos(self):
        """Valida que los campos requeridos no estén vacíos"""
        campos_requeridos = ["Cédula", "Nombres", "Apellidos", "Cargo", "Salario Base"]
        for campo in campos_requeridos:
            if not self.inputs[campo].text.strip():
                raise ValueError(f"El campo {campo} es requerido")

    def crear_objeto_nomina(self):
        """Crea y retorna un objeto Nomina con los datos del formulario"""
        data = self.inputs
        return Nomina(
            cedula_empleado=data["Cédula"].text,
            nombre_empleado=data["Nombres"].text,
            empleado_apellido=data["Apellidos"].text,
            cargo=data["Cargo"].text,
            salario_base=float(data["Salario Base"].text or 0),
            horas_extras=float(data["Horas Extras"].text or 0),
            tipo_hora_extra=data["Tipo Hora Extra"].text,
            horas_extras_adicionales=float(data["Horas Extras Adicionales"].text or 0),
            tipo_hora_extra_adicional=data["Tipo Hora Extra Adicional"].text,
            prestamo=float(data["Préstamo"].text or 0),
            cuotas=int(data["Cuotas"].text or 0),
            tasa_interes=float(data["Tasa de Interés (%)"].text or 0)
        )

    def registrar_empleado(self, instance):
        """
        Registra un nuevo empleado en la base de datos sin calcular nómina.
        """
        try:
            self.validar_campos_requeridos()
            nomina = self.crear_objeto_nomina()

            # Solo registrar el empleado, no calcular nómina
            NominaController.InsertarNomina(nomina)

            self.mostrar_popup("Éxito", "Empleado registrado correctamente")

            # Mostrar los datos registrados
            self.resultado_label.text = f"""
                    Empleado Registrado:
                    Cédula: {nomina.empleado.cedula}
                    Nombres: {nomina.empleado.nombres}
                    Apellidos: {nomina.empleado.apellidos}
                    Cargo: {nomina.cargo}
                    Salario Base: ${nomina.salario_base:,.2f}
                    Horas Extras: {nomina.horas_extras} ({nomina.tipo_hora_extra})
                    Horas Extras Adicionales: {nomina.horas_extras_adicionales} ({nomina.tipo_hora_extra_adicional})
                    Préstamo: ${nomina.prestamo:,.2f} ({nomina.cuotas} cuotas al {nomina.tasa_interes}%)"""

            # Limpiar el formulario después del registro exitoso
            self.limpiar_formulario()

        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        for campo, widget in self.inputs.items():
            if isinstance(widget, TextInput):
                widget.text = ""
            elif isinstance(widget, Spinner):
                if "Tipo Hora Extra" in campo:
                    widget.text = "N/A"
                elif campo == "Cargo":
                    widget.text = "Empleado nuevo"

    def volver_menu_principal(self):
        """Vuelve a la pantalla principal"""
        self.manager.current = 'main'

# Este archivo contiene la pantalla de registro de empleados
# La aplicación principal está en la misma carpeta en app.py

if __name__ == '__main__':
    # Si se ejecuta este archivo directamente, iniciar la aplicación
    from app import NominaApp
    NominaApp().run()
