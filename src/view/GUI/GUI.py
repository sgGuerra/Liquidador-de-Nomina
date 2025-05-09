import sys
import os

# Permite que encuentre correctamente el paquete model al compilar con PyInstaller
if hasattr(sys, '_MEIPASS'):
    sys.path.append(os.path.join(sys._MEIPASS, "src"))
else:
    sys.path.append("src")

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from model.calculo_nomina import Nomina
from model.excepciones import *

class NominaGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)

        self.inputs = {}  # Diccionario para almacenar las referencias a los campos

        # Título de la aplicación
        self.add_widget(Label(text="LIQUIDADOR DE NÓMINA", font_size=24, size_hint=(1, 0.1), bold=True))

        # Layout del formulario
        form = GridLayout(cols=2, spacing=10, size_hint=(1, 1.5))

        # Campos del formulario con ejemplos como hint_text
        campos = [
            ("Cédula", TextInput(
                input_filter='int',
                multiline=False,
                hint_text="Ej: 1234567890"
            )),
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

        self.add_widget(form)  # Se agrega el formulario completo al layout principal

        # Botón para calcular la nómina
        btn = Button(text="Calcular Nómina", size_hint=(1, 0.1), background_color=(0.2, 0.6, 0.8, 1))
        btn.bind(on_press=self.calcular_nomina)
        self.add_widget(btn)

        # Área de resultados
        self.resultado_label = Label(text="", halign='left', valign='top', size_hint=(1, 0.5))
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        self.add_widget(self.resultado_label)

    def calcular_nomina(self, instance):
        """
        Método que recoge los datos del formulario, crea un objeto Nomina y muestra los resultados.
        También maneja excepciones mostrando un popup en caso de error.
        """
        try:
            data = self.inputs

            # Se crea una instancia de Nomina con los valores ingresados por el usuario
            nomina = Nomina(
                cedula_empelado=data["Cédula"].text,
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

            # Se realizan los cálculos
            salario_neto = nomina.calcular()
            bonificacion = nomina.calcular_bonificacion()
            valor_extra = nomina.calcular_valor_hora_extra(nomina.horas_extras, nomina.tipo_hora_extra)
            valor_extra_adicional = nomina.calcular_valor_hora_extra(nomina.horas_extras_adicionales, nomina.tipo_hora_extra_adicional)

            # Mostrar los resultados
            self.resultado_label.text = f"""
Resultado de Nómina:
Cédula: {nomina.empleado.cedula}
Nombres: {nomina.empleado.nombres}
Apellidos: {nomina.empleado.apellidos}
Cargo: {nomina.cargo}
Salario Base: ${nomina.salario_base:,.2f}
Bonificación: ${bonificacion:,.2f}
Valor Horas Extra: ${valor_extra:,.2f}
Valor Horas Extra Adicionales: ${valor_extra_adicional:,.2f}
Salario Neto: ${salario_neto:,.2f}"""
        except Exception as e:
            Popup(title="Error", content=Label(text=str(e)), size_hint=(0.8, 0.3)).open()

# Clase principal de la app
class NominaApp(App):
    def build(self):
        return NominaGUI()

# Punto de entrada
if __name__ == '__main__':
    NominaApp().run()