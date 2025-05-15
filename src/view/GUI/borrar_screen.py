from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from model.excepciones import *
from controller.nomina_controller import NominaController

class BorrarNominaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'borrar'
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título con advertencia
        main_layout.add_widget(Label(
            text="BORRAR NÓMINA\n[ADVERTENCIA: Esta acción no se puede deshacer]",
            font_size=24,
            size_hint=(1, 0.2),
            bold=True,
            halign='center',
            color=(1, 0.2, 0.2, 1)  # Color rojo para advertencia
        ))
        
        # Layout de búsqueda
        search_layout = GridLayout(cols=2, spacing=10, size_hint=(1, 0.3))
        
        # Campo de la cédula
        search_layout.add_widget(Label(text="Cédula del empleado:"))
        self.cedula_input = TextInput(
            input_filter='int',
            multiline=False,
            hint_text="Ingrese la cédula del empleado"
        )
        search_layout.add_widget(self.cedula_input)
        
        # Campo de confirmación
        search_layout.add_widget(Label(text="Escriba 'CONFIRMAR' para borrar:"))
        self.confirmar_input = TextInput(
            multiline=False,
            hint_text="CONFIRMAR"
        )
        search_layout.add_widget(self.confirmar_input)
        
        main_layout.add_widget(search_layout)
        
        # Área de botones
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        
        # Botón borrar
        btn_borrar = Button(
            text="Borrar Nómina",
            background_color=(0.8, 0, 0, 1),  
        )
        btn_borrar.bind(on_press=self.borrar_nomina)
        
        # Botón volver
        btn_volver = Button(
            text="Volver",
            background_color=(0.2, 0.6, 0.8, 1),
            size_hint=(0.5, 1)
        )
        btn_volver.bind(on_press=lambda x: self.volver_menu_principal())
        
        button_layout.add_widget(btn_borrar)
        button_layout.add_widget(btn_volver)
        
        main_layout.add_widget(button_layout)
        
        self.add_widget(main_layout)
    
    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje"""
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()
    
    def volver_menu_principal(self):
        """Vuelve a la pantalla principal"""
        self.manager.current = 'main'
        
    def borrar_nomina(self, instance):
        """Borra la nómina después de validar la confirmación"""
        cedula = self.cedula_input.text.strip()
        confirmacion = self.confirmar_input.text.strip()
        
        if not cedula:
            self.mostrar_popup("Error", "Ingrese la cédula del empleado")
            return
            
        if confirmacion != "CONFIRMAR":
            self.mostrar_popup("Error", "Debe escribir 'CONFIRMAR' para borrar la nómina")
            return
            
        try:
            NominaController().EliminarEmpleadoPorCedula(cedula)
            self.mostrar_popup("Éxito", f"Se ha borrado la nómina del empleado con cédula {cedula}")
            
            # Limpiar los campos
            self.cedula_input.text = ""
            self.confirmar_input.text = ""
            
        except EmpleadoNoExistenteError:
            self.mostrar_popup("Error", f"No existe un empleado con la cédula {cedula}")
        except Exception as e:
            self.mostrar_popup("Error", str(e))
