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

# Importar todas las pantallas
# Importar todas las pantallas
from main_screen import MainScreen
from calcular_screen import CalcularNominaScreen
from modificar_screen import ModificarNominaScreen
from consultar_screen import ConsultarNominaScreen
from borrar_screen import BorrarNominaScreen

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
    NominaApp().run()
