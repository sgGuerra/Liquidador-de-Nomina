from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Título
        titulo = Label(
            text="SISTEMA DE LIQUIDACIÓN DE NÓMINA",
            font_size=24,
            size_hint=(1, 0.2),
            bold=True
        )
        layout.add_widget(titulo)
        
        # Botones con las diferentes opciones
        opciones = [
            ("Calcular Nueva Nómina", 'calcular', (0.2, 0.6, 0.8, 1)),
            ("Modificar Nómina", 'modificar', (0.8, 0.6, 0.2, 1)),
            ("Consultar Nómina", 'consultar', (0.2, 0.8, 0.6, 1)),
            ("Borrar Nómina", 'borrar', (0.8, 0.2, 0.2, 1))
        ]
        
        for texto, pantalla, color in opciones:
            btn = Button(
                text=texto,
                background_color=color,
                size_hint=(0.8, 0.15),
                pos_hint={'center_x': 0.5}
            )
            btn.bind(on_press=lambda x, screen=pantalla: self.cambiar_pantalla(screen))
            layout.add_widget(btn)
            
        self.add_widget(layout)
    
    def cambiar_pantalla(self, nombre_pantalla):
        self.manager.current = nombre_pantalla
