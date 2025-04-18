import sys
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

        self.inputs = {}

        self.add_widget(Label(text="LIQUIDADOR DE NÓMINA", font_size=24, size_hint=(1, 0.1), bold=True))

        form = GridLayout(cols=2, spacing=10, size_hint=(1, 1.5))

        campos = [
            ("Cargo", Spinner(values=["Empleado nuevo", "Empleado antiguo", "Administrador"], text="Empleado nuevo")),
            ("Salario Base", TextInput(input_filter='float', multiline=False)),
            ("Horas Extras", TextInput(input_filter='float', multiline=False)),
            ("Tipo Hora Extra", Spinner(values=["N/A", "Diurnas", "Nocturnas", "Festivas"], text="N/A")),
            ("Horas Extras Adicionales", TextInput(input_filter='float', multiline=False)),
            ("Tipo Hora Extra Adicional", Spinner(values=["N/A", "Diurnas", "Nocturnas", "Festivas"], text="N/A")),
            ("Préstamo", TextInput(input_filter='float', multiline=False)),
            ("Cuotas", TextInput(input_filter='int', multiline=False)),
            ("Tasa de Interés (%)", TextInput(input_filter='float', multiline=False)),
        ]

        for label_text, widget in campos:
            form.add_widget(Label(text=label_text))
            form.add_widget(widget)
            self.inputs[label_text] = widget

        self.add_widget(form)

        btn = Button(text="Calcular Nómina", size_hint=(1, 0.1), background_color=(0.2, 0.6, 0.8, 1))
        btn.bind(on_press=self.calcular_nomina)
        self.add_widget(btn)

        self.resultado_label = Label(text="", halign='left', valign='top', size_hint=(1, 0.5))
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        self.add_widget(self.resultado_label)

    def calcular_nomina(self, instance):
        try:
            data = self.inputs

            nomina = Nomina(
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

            salario_neto = nomina.calcular()
            bonificacion = nomina.calcular_bonificacion()
            valor_extra = nomina.calcular_valor_hora_extra(nomina.horas_extras, nomina.tipo_hora_extra)
            valor_extra_adicional = nomina.calcular_valor_hora_extra(nomina.horas_extras_adicionales, nomina.tipo_hora_extra_adicional)

            self.resultado_label.text = f"""
Resultado de Nómina:
Cargo: {nomina.cargo}
Salario Base: ${nomina.salario_base:,.2f}
Bonificación: ${bonificacion:,.2f}
Valor Horas Extra: ${valor_extra:,.2f}
Valor Horas Extra Adicionales: ${valor_extra_adicional:,.2f}
Salario Neto: ${salario_neto:,.2f}"
"""

        except Exception as e:
            Popup(title="Error", content=Label(text=str(e)), size_hint=(0.8, 0.3)).open()

class NominaApp(App):
    def build(self):
        return NominaGUI()

if __name__ == '__main__':
    NominaApp().run()

