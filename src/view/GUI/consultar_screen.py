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
        """Muestra un popup con un mensaje informativo o de error.

        Este método crea y muestra una ventana emergente (popup) con un título
        y un mensaje. Se usa principalmente para mostrar errores al usuario.

        Args:
            titulo (str): El título que aparecerá en la barra superior del popup.
            mensaje (str): El mensaje que se mostrará en el cuerpo del popup.

        Note:
            El popup se cierra automáticamente al hacer clic en cualquier parte
            fuera de él o al presionar la tecla Escape.
        """
        Popup(title=titulo, content=Label(text=mensaje), size_hint=(0.8, 0.3)).open()
    
    def volver_menu_principal(self):
        """Navega de vuelta a la pantalla principal de la aplicación.

        Este método cambia la pantalla actual a la pantalla principal ('main')
        utilizando el ScreenManager de Kivy.

        Note:
            Este método es llamado cuando el usuario presiona el botón
            'Volver al Menú Principal'.
        """
        self.manager.current = 'main'
    
    def buscar_nomina(self, instance):
        """Busca y muestra la información de la nómina de un empleado.

        Este método consulta la información completa de un empleado usando su número de cédula
        y muestra los resultados en la interfaz gráfica.

        Args:
            instance: Instancia del botón que triggerea el evento (requerido por Kivy)

        Raises:
            EmpleadoNoExistenteError: Si no se encuentra un empleado con la cédula proporcionada.
            CedulaInvalidaError: Si el formato de la cédula no es válido (debe ser numérico y tener entre 8-10 dígitos).
            psycopg2.Error: Si ocurre un error en la conexión o consulta a la base de datos.
            psycopg2.InterfaceError: Si hay un problema con la interfaz de la base de datos.
            psycopg2.OperationalError: Si hay un error operacional en la base de datos (ej: conexión perdida).
            Exception: Para cualquier otro error no esperado durante la consulta.

        Note:
            El resultado se muestra en el Label self.resultado_label y los errores
            se muestran en un popup.
        """
        cedula = self.cedula_input.text.strip()
        if not cedula:
            self.mostrar_popup("Error", "Ingrese una cédula para consultar")
            return
        
        try:
            empleado = NominaController.ObtenerEmpleadoPorCedula(cedula)
            if empleado:
                # Formatear las horas extras
                horas_extras_info = "No tiene horas extras registradas"
                if empleado['horas_extras']:
                    horas_extras_info = "\n".join([
                        f"- {he['numero_de_horas']} horas {he['tipo_hora_extra']}"
                        for he in empleado['horas_extras']
                    ])
                
                # Formatear el préstamo
                prestamo_info = "No tiene préstamo activo"
                if empleado['prestamo']:
                    prestamo_info = (
                        f"Monto: ${empleado['prestamo']['monto']:,.2f}\n"
                        f"Cuotas: {empleado['prestamo']['numero_de_cuotas']}\n"
                        f"Tasa de interés: {empleado['prestamo']['tasa_interes']}%\n"
                        f"Fecha inicio: {empleado['prestamo']['fecha_inicio']}"
                    )

                # Obtener historial de nóminas
                historial = NominaController.ObtenerHistorialNomina(cedula)
                historial_info = "No hay historial de nóminas calculadas"
                if historial:
                    historial_info = "[b]Historial de Nóminas:[/b]\n"
                    for h in historial:
                        historial_info += (
                            f"[color=333333]Fecha: {h['fecha'].strftime('%Y-%m-%d %H:%M')}[/color]\n"
                            f"Salario Bruto: ${h['salario_bruto']:,.2f}\n"
                            f"Deducciones: ${h['deducciones']:,.2f}\n"
                            f"Impuestos: ${h['impuestos']:,.2f}\n"
                            f"Auxilio Transporte: ${h['auxilio_transporte']:,.2f}\n"
                            f"[color=00aa00]Neto: ${h['neto']:,.2f}[/color]\n\n"
                        )
                
                resultado = (
                    f"[b]Cédula:[/b] {empleado['cedula']}\n"
                    f"[b]Nombres:[/b] {empleado['nombres']}\n"
                    f"[b]Apellidos:[/b] {empleado['apellidos']}\n"
                    f"[b]Cargo:[/b] {empleado['cargo']}\n"
                    f"[b]Salario Base:[/b] ${empleado['salario_base']:,.2f}\n\n"
                    f"[b]Horas Extras:[/b]\n{horas_extras_info}\n\n"
                    f"[b]Préstamo:[/b]\n{prestamo_info}\n\n"
                    f"{historial_info}"
                )
                self.resultado_label.text = resultado
            else:
                self.resultado_label.text = "No se encontró un empleado con esa cédula."

        except Exception as e:
            self.mostrar_popup("Error", str(e))
