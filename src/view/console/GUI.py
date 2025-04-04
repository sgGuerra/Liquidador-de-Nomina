import sys
import os
sys.path.append("src")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from model.calculo_nomina import Nomina, SALARIO_MINIMO_LEGAL_VIGENTE, MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS
from model.excepciones import *

class NominaGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        
        self.add_widget(Label(text='Salario Base:'))
        self.salario_input = TextInput(multiline=False)
        self.add_widget(self.salario_input)
        
        self.add_widget(Label(text='Horas Extras:'))
        self.horas_extra_input = TextInput(multiline=False)
        self.add_widget(self.horas_extra_input)
        
        self.add_widget(Label(text='Cargo:'))
        self.cargo_spinner = Spinner(text='Empleado nuevo', values=['Empleado nuevo', 'Empleado antiguo', 'Administrador'])
        self.add_widget(self.cargo_spinner)
        
        self.calcular_button = Button(text='Calcular Nómina')
        self.calcular_button.bind(on_press=self.calcular_nomina)
        self.add_widget(self.calcular_button)
        
        self.resultado_label = Label(text='')
        self.add_widget(self.resultado_label)

    def calcular_nomina(self, instance):
        try:
            salario_base = float(self.salario_input.text)
            horas_extra = float(self.horas_extra_input.text)
            cargo = self.cargo_spinner.text
            
            if salario_base < 0:
                raise SalarioBaseNegativoError()
            if salario_base < SALARIO_MINIMO_LEGAL_VIGENTE:
                raise SalarioBaseMenorMinimoError(salario_base, SALARIO_MINIMO_LEGAL_VIGENTE)
            if horas_extra < 0:
                raise ValorHoraExtraNegativoError(horas_extra)
            if horas_extra > MAXIMO_HORAS_EXTRA_LEGALES_PERMITIDAS:
                raise LimiteHorasExtraError(horas_extra, 0)
            
            nomina = Nomina(cargo, salario_base, horas_extra, 'Diurnas', 0, 'N/A', 0, 0, 0)
            salario_neto = nomina.calcular()
            
            self.resultado_label.text = f'Salario Neto: ${salario_neto:.2f}'
        except Exception as e:
            self.resultado_label.text = f'Error: {e}'

class NominaApp(App):
    def build(self):
        return NominaGUI()

if __name__ == '__main__':
    NominaApp().run()
