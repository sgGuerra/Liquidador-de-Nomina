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

class CalcularNominaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'calcular'
        self.empleado_data = None  # Para almacenar los datos del empleado cargado

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Título
        main_layout.add_widget(Label(
            text="CALCULAR NÓMINA",
            font_size=24,
            size_hint=(1, 0.3),
            bold=True
        ))

        # Sección de búsqueda de empleado
        search_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        search_layout.add_widget(Label(text="Cédula del Empleado:", size_hint=(0.3, 1)))

        self.cedula_input = TextInput(
            input_filter='int',
            multiline=False,
            hint_text="Ingrese cédula",
            size_hint=(0.4, 1)
        )
        self.cedula_input.bind(text=self.on_cedula_cambio)
        search_layout.add_widget(self.cedula_input)

        btn_buscar = Button(
            text="Buscar Empleado",
            background_color=(0.4, 0.8, 0.4, 1),
            size_hint=(0.3, 1)
        )
        btn_buscar.bind(on_press=self.buscar_empleado)
        search_layout.add_widget(btn_buscar)

        main_layout.add_widget(search_layout)

        # Información del empleado (se mostrará cuando se cargue)
        self.info_empleado_label = Label(
            text="",
            halign='left',
            valign='top',
            size_hint=(1, 0.3),
            font_size=14
        )
        self.info_empleado_label.bind(size=self.info_empleado_label.setter('text_size'))
        main_layout.add_widget(self.info_empleado_label)

        # Layout del formulario de cálculo
        form = GridLayout(
            cols=2,
            spacing=15,
            padding=10,
            size_hint=(1, None),
            height=300
        )
        self.inputs = {}  # Diccionario para almacenar las referencias a los campos

        campos = [
            ("Horas Extras", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 8",
                text="0"
            )),
            ("Tipo Hora Extra", Spinner(
                values=["N/A", "Diurnas", "Nocturnas", "Festivas"],
                text="N/A"
            )),
            ("Horas Extras Adicionales", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 4",
                text="0"
            )),
            ("Tipo Hora Extra Adicional", Spinner(
                values=["N/A", "Diurnas", "Nocturnas", "Festivas"],
                text="N/A"
            )),
            ("Préstamo", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 500000",
                text="0"
            )),
            ("Cuotas", TextInput(
                input_filter='int',
                multiline=False,
                hint_text="Ej: 6",
                text="0"
            )),
            ("Tasa de Interés (%)", TextInput(
                input_filter='float',
                multiline=False,
                hint_text="Ej: 2.5",
                text="0"
            )),
        ]

        # Se agregan campos al formulario y se registran en el diccionario
        for label_text, widget in campos:
            form.add_widget(Label(text=label_text))
            form.add_widget(widget)
            self.inputs[label_text] = widget

        main_layout.add_widget(form)

        # Área de botones
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))

        # Botón calcular
        btn_calcular = Button(
            text="Calcular Nómina",
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint=(0.8, 1)
        )
        btn_calcular.bind(on_press=self.calcular_nomina)

        # Botón volver
        btn_volver = Button(
            text="Volver",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_volver.bind(on_press=lambda x: self.volver_menu_principal())

        button_layout.add_widget(btn_calcular)
        button_layout.add_widget(btn_volver)

        main_layout.add_widget(button_layout)

        # Área de resultados
        self.resultado_label = Label(
            text="",
            halign='left',
            valign='top',
            size_hint=(1, 1),
            font_size=12
        )
        self.resultado_label.bind(size=self.resultado_label.setter('text_size'))
        main_layout.add_widget(self.resultado_label)

        self.add_widget(main_layout)

    def on_cedula_cambio(self, instance, value):
        """Limita la longitud de la cédula entre 8 y 10 dígitos"""
        if value:
            value = ''.join(filter(str.isdigit, value))
            if len(value) > 10:
                value = value[:10]
            instance.text = value

    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje"""
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()

    def buscar_empleado(self, instance):
        """Busca un empleado por cédula y carga sus datos"""
        try:
            cedula = self.cedula_input.text.strip()
            if not cedula:
                self.mostrar_popup("Error", "Por favor ingrese una cédula")
                return

            # Buscar empleado en la base de datos
            self.empleado_data = NominaController.ObtenerEmpleadoPorCedula(cedula)

            # Mostrar información del empleado
            prestamo_info = "Sin préstamo activo"
            if self.empleado_data['prestamo']:
                prestamo_info = f"${self.empleado_data['prestamo']['monto']:,.2f} ({self.empleado_data['prestamo']['numero_de_cuotas']} cuotas) al {self.empleado_data['prestamo']['tasa_interes']}%"

            self.info_empleado_label.text = f"""
            Empleado encontrado:
            Cédula: {self.empleado_data['cedula']}
            Nombre: {self.empleado_data['nombres']} {self.empleado_data['apellidos']}
            Cargo: {self.empleado_data['cargo']}
            Salario Base: ${self.empleado_data['salario_base']:,.2f}

            Información adicional:
            Horas Extras: {', '.join([f"{h['numero_de_horas']} {h['tipo_hora_extra']}" for h in self.empleado_data['horas_extras']]) if self.empleado_data['horas_extras'] else 'Ninguna'}
            Préstamo: {prestamo_info}
            """

            # Limpiar resultados anteriores
            self.resultado_label.text = ""

        except EmpleadoNoExistenteError:
            self.mostrar_popup("Error", f"No se encontró un empleado con la cédula {cedula}")
            self.empleado_data = None
            self.info_empleado_label.text = ""
        except Exception as e:
            self.mostrar_popup("Error", str(e))
            self.empleado_data = None
            self.info_empleado_label.text = ""

    def crear_objeto_nomina_calculo(self):
        """Crea un objeto Nomina para cálculo usando datos del empleado y campos del formulario"""
        if not self.empleado_data:
            raise ValueError("Debe buscar un empleado primero")

        # Usar datos del empleado como base
        return Nomina(
            cedula_empleado=self.empleado_data['cedula'],
            nombre_empleado=self.empleado_data['nombres'],
            empleado_apellido=self.empleado_data['apellidos'],
            cargo=self.empleado_data['cargo'],
            salario_base=self.empleado_data['salario_base'],
            # Usar valores del formulario para el cálculo actual
            horas_extras=float(self.inputs["Horas Extras"].text or 0),
            tipo_hora_extra=self.inputs["Tipo Hora Extra"].text,
            horas_extras_adicionales=float(self.inputs["Horas Extras Adicionales"].text or 0),
            tipo_hora_extra_adicional=self.inputs["Tipo Hora Extra Adicional"].text,
            prestamo=float(self.inputs["Préstamo"].text or 0),
            cuotas=int(self.inputs["Cuotas"].text or 0),
            tasa_interes=float(self.inputs["Tasa de Interés (%)"].text or 0)
        )

    def calcular_nomina(self, instance):
        """Calcula la nómina para el empleado seleccionado"""
        try:
            if not self.empleado_data:
                self.mostrar_popup("Error", "Debe buscar un empleado primero")
                return

            nomina = self.crear_objeto_nomina_calculo()

            # Realizar los cálculos
            resultados = nomina.calcular()
            bonificacion = nomina.calcular_bonificacion()
            valor_extra = nomina.calcular_valor_hora_extra(nomina.horas_extras, nomina.tipo_hora_extra)
            valor_extra_adicional = nomina.calcular_valor_hora_extra(nomina.horas_extras_adicionales, nomina.tipo_hora_extra_adicional)

            # Guardar historial de la nómina calculada
            NominaController.GuardarHistorialNomina(
                nomina.empleado.cedula,
                resultados['salario_bruto'],
                resultados['deducciones'],
                resultados['impuestos'],
                resultados['auxilio_transporte'],
                resultados['neto']
            )

            self.mostrar_popup("Éxito", "Nómina calculada y guardada en el historial")

            # Mostrar los resultados
            self.resultado_label.text = f"""
                    RESULTADO DE NÓMINA CALCULADA:

                    Empleado: {nomina.empleado.nombres} {nomina.empleado.apellidos}
                    Cédula: {nomina.empleado.cedula}
                    Cargo: {nomina.cargo}

                    SALARIO BASE: ${nomina.salario_base:,.2f}
                    BONIFICACIÓN: ${bonificacion:,.2f}

                    HORAS EXTRAS:
                    - Principales: {nomina.horas_extras} horas ({nomina.tipo_hora_extra}) = ${valor_extra:,.2f}
                    - Adicionales: {nomina.horas_extras_adicionales} horas ({nomina.tipo_hora_extra_adicional}) = ${valor_extra_adicional:,.2f}

                    PRÉSTAMO: ${nomina.prestamo:,.2f} ({nomina.cuotas} cuotas al {nomina.tasa_interes}%)

                    RESUMEN FINANCIERO:
                    Salario Bruto: ${resultados['salario_bruto']:,.2f}
                    Deducciones: ${resultados['deducciones']:,.2f}
                    Impuestos: ${resultados['impuestos']:,.2f}
                    Auxilio Transporte: ${resultados['auxilio_transporte']:,.2f}
                    SALARIO NETO: ${resultados['neto']:,.2f}

                    *Esta nómina ha sido guardada en el historial del empleado*"""

        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def volver_menu_principal(self):
        """Vuelve a la pantalla principal"""
        self.manager.current = 'main'

# Este archivo contiene la pantalla de cálculo de nómina
# La aplicación principal está en la misma carpeta en app.py

if __name__ == '__main__':
    # Si se ejecuta este archivo directamente, iniciar la aplicación
    from app import NominaApp
    NominaApp().run()
