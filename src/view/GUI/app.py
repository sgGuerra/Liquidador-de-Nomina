import sys
import os

# Permite que encuentre correctamente el paquete model al compilar con PyInstaller
if hasattr(sys, '_MEIPASS'):
    sys.path.append(os.path.join(sys._MEIPASS, "src"))
else:
    sys.path.append("src")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.resources import resource_add_path, resource_find

# Importar todas las pantallas usando rutas relativas
from view.GUI.main_screen import MainScreen
from view.GUI.calcular_screen import CalcularNominaScreen
from view.GUI.modificar_screen import ModificarNominaScreen
from view.GUI.consultar_screen import ConsultarNominaScreen
from view.GUI.borrar_screen import BorrarNominaScreen

class NominaApp(App):
    def build(self):
        """Construye la interfaz principal de la aplicación"""
        # Configurar la ventana
        Window.size = (800, 600)
        Window.minimum_width, Window.minimum_height = (800, 600)
        self.title = "Sistema de Liquidación de Nómina"
        
        # Crear el administrador de pantallas
        sm = ScreenManager()
        
        # Agregar todas las pantallas
        sm.add_widget(MainScreen())
        sm.add_widget(CalcularNominaScreen())
        sm.add_widget(ModificarNominaScreen())
        sm.add_widget(ConsultarNominaScreen())
        sm.add_widget(BorrarNominaScreen())
        
        return sm

# Punto de entrada
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    NominaApp().run()
