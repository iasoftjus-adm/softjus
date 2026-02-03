from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, Line
import threading
from datetime import datetime

from app.api.api_client import APIClient
from app.api.config import TRIBUNAL_URLS
from app.utils.helpers import format_date, format_datetime


# REMOVED: from app.screens.consulta_screen import ConsultaScreen  # This was the circular import

class ConsultaScreen(BoxLayout):
    def __init__(self, favorites_store=None, selected_tribunal=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.original_results = []
        self.displayed_results = []
        self.favorites_store = favorites_store
        self.selected_tribunal = selected_tribunal or "Tribunal Regional Federal da 1ª Região"
        self.api_client = APIClient()
        self.setup_ui()

    def setup_ui(self):
        # Search section
        search_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.12))

        self.process_input = TextInput(
            hint_text="Número do processo (ex: 00008323520184013202)",
            multiline=False,
            size_hint=(0.7, 1)
        )

        search_btn = Button(text="Buscar", size_hint=(0.15, 1))
        search_btn.bind(on_press=self.search_process)

        clear_btn = Button(text="Limpar", size_hint=(0.15, 1))
        clear_btn.bind(on_press=self.clear_search)

        search_layout.add_widget(self.process_input)
        search_layout.add_widget(search_btn)
        search_layout.add_widget(clear_btn)

        # Tribunal info
        tribunal_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.08))
        tribunal_label = Label(text="Tribunal selecionado:", size_hint=(0.25, 1))
        self.tribunal_info_label = Label(
            text=self.selected_tribunal,
            size_hint=(0.75, 1),
            color=get_color_from_hex('#1976D2'),
            bold=True
        )
        tribunal_layout.add_widget(tribunal_label)
        tribunal_layout.add_widget(self.tribunal_info_label)

        # Filter controls
        filter_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.1))

        filter_label = Label(text="Filtros:", size_hint=(0.15, 1))

        # Filter type dropdown
        self.filter_dropdown = DropDown()
        filter_types = ["Todos", "Processo", "Classe", "Órgão Julgador", "Data", "Último Movimento"]

        for filtro in filter_types:
            btn = Button(text=filtro, size_hint_y=None, height=dp(44))
            btn.bind(on_release=lambda btn, f=filtro: self.select_filter(f))
            self.filter_dropdown.add_widget(btn)

        self.filter_btn = Button(text="Filtrar por", size_hint=(0.3, 1))
        self.filter_btn.bind(on_release=self.filter_dropdown.open)
        self.filter_dropdown.bind(on_select=lambda instance, x: setattr(self.filter_btn, 'text', x))

        self.filter_input = TextInput(
            hint_text="Digite para filtrar...",
            multiline=False,
            size_hint=(0.55, 1)
        )
        self.filter_input.bind(text=self.filter_results)

        filter_layout.add_widget(filter_label)
        filter_layout.add_widget(self.filter_btn)
        filter_layout.add_widget(self.filter_input)

        # Results area
        self.results_container = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.results_container.bind(minimum_height=self.results_container.setter('height'))

        scroll_view = ScrollView(size_hint=(1, 0.7))
        scroll_view.add_widget(self.results_container)

        self.add_widget(search_layout)
        self.add_widget(tribunal_layout)
        self.add_widget(filter_layout)
        self.add_widget(scroll_view)

        self.current_filter = "Todos"

    def update_selected_tribunal(self, tribunal_name):
        """Update the selected tribunal"""
        self.selected_tribunal = tribunal_name
        self.tribunal_info_label.text = tribunal_name

        # Clear any existing results
        self.results_container.clear_widgets()
        self.original_results = []
        self.displayed_results = []

    def select_filter(self, filter_type):
        self.current_filter = filter_type
        self.filter_dropdown.select(filter_type)

    def search_process(self, instance):
        process_number = self.process_input.text.strip()

        if not process_number:
            self.show_popup("Aviso", "Digite um número de processo")
            return

        # Clear previous
        self.results_container.clear_widgets()
        self.original_results = []

        # Show loading
        loading_label = Label(text="Buscando...", font_size='18sp')
        self.results_container.add_widget(loading_label)

        # Start search with selected tribunal
        self.api_client.search_process(
            process_number,
            self.handle_search_response,
            tribunal_name=self.selected_tribunal
        )

    def handle_search_response(self, response, error=None):
        self.results_container.clear_widgets()

        if error:
            self.show_error("Erro", f"Falha na busca: {error}")
            return

        try:
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])

            if not hits:
                self.results_container.add_widget(Label(
                    text="Nenhum processo encontrado",
                    size_hint_y=None,
                    height=dp(50),
                    color=get_color_from_hex('#D32F2F')
                ))
                return

            self.original_results = []

            for hit in hits:
                source = hit.get('_source', {})
                result_data = self.extract_result_data(source)
                self.original_results.append(result_data)

            # Display all results
            self.displayed_results = self.original_results.copy()
            self.update_results_display()

        except Exception as e:
            self.show_error("Erro", f"Resposta inválida da API: {str(e)}")

    def extract_result_data(self, source):
        """Extract and format process data"""
        data = {}

        # Processo
        data['processo'] = source.get('numeroProcesso', 'N/A')

        # Classe
        classe = source.get('classe', {})
        if isinstance(classe, dict):
            data['classe'] = f"{classe.get('codigo', '')} - {classe.get('nome', 'N/A')}"
        else:
            data['classe'] = str(classe)

        # Órgão Julgador
        orgao = source.get('orgaoJulgador', {})
        if isinstance(orgao, dict):
            data['orgao'] = f"{orgao.get('nome', 'N/A')} ({orgao.get('codigoMunicipioIBGE', '')})"
        else:
            data['orgao'] = str(orgao)

        # Data de Ajuizamento
        data_ajuizamento = source.get('dataAjuizamento', '')
        data['data'] = format_date(data_ajuizamento) if data_ajuizamento else "N/A"

        # Último Movimento
        movimentos = source.get('movimentos', [])
        if movimentos:
            ultimo = movimentos[-1]
            data_hora = ultimo.get('dataHora', '')
            nome = ultimo.get('nome', '')
            if data_hora:
                formatted_date = format_datetime(data_hora)
                data['ultimo_movimento'] = f"{formatted_date} - {nome}"
            else:
                data['ultimo_movimento'] = nome
        else:
            data['ultimo_movimento'] = "Nenhum movimento registrado"

        # Tribunal information
        data['tribunal'] = self.selected_tribunal

        # Raw data for filtering
        data['raw'] = source

        return data

    def update_results_display(self):
        self.results_container.clear_widgets()

        if not self.displayed_results:
            self.results_container.add_widget(Label(
                text="Nenhum resultado corresponde ao filtro",
                size_hint_y=None,
                height=dp(50)
            ))
            return

        for result in self.displayed_results:
            self.results_container.add_widget(self.create_result_card(result))

    def create_result_card(self, result):
        from app.widgets.result_card import ResultCard
        return ResultCard(result=result, favorites_store=self.favorites_store)

    def filter_results(self, instance, value):
        filter_text = value.lower().strip()

        if not filter_text:
            self.displayed_results = self.original_results.copy()
        else:
            self.displayed_results = []
            for result in self.original_results:
                if self.matches_filter(result, filter_text):
                    self.displayed_results.append(result)

        self.update_results_display()

    def matches_filter(self, result, filter_text):
        if self.current_filter == "Todos":
            # Search in all fields
            search_fields = [
                result['processo'],
                result['classe'],
                result['orgao'],
                result['data'],
                result['ultimo_movimento']
            ]
            return any(filter_text in field.lower() for field in search_fields)

        elif self.current_filter == "Processo":
            return filter_text in result['processo'].lower()

        elif self.current_filter == "Classe":
            return filter_text in result['classe'].lower()

        elif self.current_filter == "Órgão Julgador":
            return filter_text in result['orgao'].lower()

        elif self.current_filter == "Data":
            return filter_text in result['data'].lower()

        elif self.current_filter == "Último Movimento":
            return filter_text in result['ultimo_movimento'].lower()

        return False

    def clear_search(self, instance):
        self.process_input.text = ""
        self.filter_input.text = ""
        self.results_container.clear_widgets()
        self.original_results = []
        self.displayed_results = []

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.8, 0.4))
        popup.open()

    def show_error(self, title, message):
        self.show_popup(title, message)