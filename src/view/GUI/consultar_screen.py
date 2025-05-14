import sys
sys.path.append("src")

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView

from controller.nomina_controller import NominaController

class ConsultarNominaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'consultar'
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        main_layout.add_widget(Label(
            text="CONSULTAR NÓMINA",
            font_size=24,
            size_hint=(1, 0.1),
            bold=True
        ))
        
        # Layout de búsqueda
        search_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        
        # Campo de búsqueda por cédula
        self.cedula_input = TextInput(
            input_filter='int',
            multiline=False,
            hint_text="Ingrese la cédula a consultar",
            size_hint=(0.7, 1)
        )
        search_layout.add_widget(self.cedula_input)
        
        # Botón buscar
        btn_buscar = Button(
            text="Buscar",
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=(0.3, 1)
        )
        btn_buscar.bind(on_press=self.buscar_nomina)
        search_layout.add_widget(btn_buscar)
        
        main_layout.add_widget(search_layout)
        
        # Área de resultados con scroll
        scroll_view = ScrollView(size_hint=(1, 0.6))
        self.resultado_label = Label(
            text="",
            size_hint_y=None,
            halign='left',
            valign='top',
            markup=True
        )
        # Vincular el tamaño del texto
        self.resultado_label.bind(width=lambda *x: self.resultado_label.setter('text_size')(self.resultado_label, (self.resultado_label.width, None)))
        self.resultado_label.bind(texture_size=lambda *x: self.resultado_label.setter('height')(self.resultado_label, self.resultado_label.texture_size[1]))
        scroll_view.add_widget(self.resultado_label)
        
        main_layout.add_widget(scroll_view)
        
        # Botón volver
        btn_volver = Button(
            text="Volver al Menú Principal",
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=(1, 0.1)
        )
        btn_volver.bind(on_press=lambda x: self.volver_menu_principal())
        main_layout.add_widget(btn_volver)
        
        self.add_widget(main_layout)
    
    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje"""
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()
    
    def volver_menu_principal(self):
        """Vuelve a la pantalla principal"""
        self.manager.current = 'main'
    
    def buscar_nomina(self, instance):
        """Busca y muestra la información de la nómina"""
        cedula = self.cedula_input.text.strip()
        if not cedula:
            self.mostrar_popup("Error", "Ingrese una cédula para consultar")
            return
        
        try:
            # Aquí iría la lógica para buscar la nómina en la base de datos
            # Por ahora mostramos un mensaje de ejemplo
            
            empleado = NominaController().ObtenerEmpleadoPorCedula(cedula)
            if empleado:
                resultado = (
                    f"[b]Cédula:[/b] {empleado['cedula']}\n"
                    f"[b]Nombres:[/b] {empleado['nombres']}\n"
                    f"[b]Apellidos:[/b] {empleado['apellidos']}\n"
                    f"[b]Cargo:[/b] {empleado['cargo']}\n"
                    f"[b]Salario Base:[/b] {empleado['salario_base']}"
                )
                self.resultado_label.text = resultado
            else:
                self.resultado_label.text = "No se encontró un empleado con esa cédula."

        except Exception as e:
            self.mostrar_popup("Error", str(e))
