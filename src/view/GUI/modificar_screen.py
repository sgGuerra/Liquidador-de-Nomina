from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from model.calculo_nomina import Nomina
from model.excepciones import *
from controller.nomina_controller import NominaController

class ModificarNominaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'modificar'
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        main_layout.add_widget(Label(
            text="MODIFICAR NÓMINA",
            font_size=24,
            size_hint=(1, 0.1),
            bold=True
        ))
        
        # Layout del formulario
        form = GridLayout(cols=2, spacing=10, size_hint=(1, 1.5))
        self.inputs = {}  # Diccionario para almacenar las referencias a los campos

        # Campo de búsqueda por cédula
        form.add_widget(Label(text="Cédula a buscar"))
        cedula_buscar = TextInput(
            input_filter='int',
            multiline=False,
            hint_text="Ingrese la cédula a buscar"
        )
        form.add_widget(cedula_buscar)
        self.inputs['cedula_buscar'] = cedula_buscar

        # Campos del formulario (similares a la pantalla de calcular)
        campos = [
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
            ))
        ]

        for label_text, widget in campos:
            form.add_widget(Label(text=label_text))
            form.add_widget(widget)
            self.inputs[label_text] = widget

        main_layout.add_widget(form)

        # Área de botones
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.1))
        
        # Botón buscar
        btn_buscar = Button(
            text="Buscar",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_buscar.bind(on_press=self.buscar_nomina)
        
        # Botón modificar
        btn_modificar = Button(
            text="Modificar",
            background_color=(0.8, 0.6, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_modificar.bind(on_press=self.modificar_nomina)
        
        # Botón volver
        btn_volver = Button(
            text="Volver",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_volver.bind(on_press=lambda x: self.volver_menu_principal())
        
        button_layout.add_widget(btn_buscar)
        button_layout.add_widget(btn_modificar)
        button_layout.add_widget(btn_volver)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)

    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje"""
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()

    def volver_menu_principal(self):
        """Vuelve a la pantalla principal"""
        self.manager.current = 'main'

    def buscar_nomina(self, instance):
        """Busca la nómina por cédula y rellena el formulario"""
        cedula = self.inputs['cedula_buscar'].text.strip()
        if not cedula:
            self.mostrar_popup("Error", "Ingrese una cédula para buscar")
            return
        
        try:
            # Aquí iría la lógica para buscar la nómina en la base de datos
            # y rellenar los campos del formulario
            pass
        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def modificar_nomina(self, instance):
        """Modifica la nómina en la base de datos"""
        try:
            # Crear objeto nómina con los datos del formulario
            nomina = self.crear_objeto_nomina()
            
            # Modificar en la base de datos
            if NominaController.ModificarNomina(nomina):
                self.mostrar_popup("Éxito", "Nómina modificada correctamente")
            
        except Exception as e:
            self.mostrar_popup("Error", str(e))

    def crear_objeto_nomina(self):
        """Crea y retorna un objeto Nomina con los datos del formulario"""
        return Nomina(
            cedula_empleado=self.inputs['cedula_buscar'].text,
            nombre_empleado=self.inputs["Nombres"].text,
            empleado_apellido=self.inputs["Apellidos"].text,
            cargo=self.inputs["Cargo"].text,
            salario_base=float(self.inputs["Salario Base"].text or 0),
            horas_extras=float(self.inputs["Horas Extras"].text or 0),
            tipo_hora_extra=self.inputs["Tipo Hora Extra"].text,
            horas_extras_adicionales=float(self.inputs["Horas Extras Adicionales"].text or 0),
            tipo_hora_extra_adicional=self.inputs["Tipo Hora Extra Adicional"].text,
            prestamo=float(self.inputs["Préstamo"].text or 0),
            cuotas=int(self.inputs["Cuotas"].text or 0),
            tasa_interes=float(self.inputs["Tasa de Interés (%)"].text or 0)
        )
