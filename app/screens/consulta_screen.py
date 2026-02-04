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
from kivy.animation import Animation
import threading
from datetime import datetime

from app.api.api_client import APIClient
from app.api.config import TRIBUNAL_URLS
from app.utils.helpers import format_date, format_datetime

# Tente importar OABScraper, mas não falhe se não existir
try:
    from app.scrapers.advanced_oab_scraper import AdvancedOABScraper
    SCRAPER_DISPONIVEL = 'advanced'
    print("✓ AdvancedOABScraper corrigido carregado")
except ImportError as e:
    print(f"✗ AdvancedOABScraper corrigido não disponível: {e}")
    SCRAPER_DISPONIVEL = 'none'


class ConsultaScreen(BoxLayout):
    # app/screens/consulta_screen.py - DENTRO DO __init__ DA CLASSE ConsultaScreen

    def __init__(self, favorites_store=None, selected_tribunal=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.original_results = []
        self.displayed_results = []
        self.favorites_store = favorites_store
        self.selected_tribunal = selected_tribunal or "Tribunal Regional Federal da 1ª Região"
        self.consulta_mode = "processo"  # "processo" ou "oab"
        self.api_client = APIClient()

        # Inicializar scraper
        self.scraper = None
        if SCRAPER_DISPONIVEL == 'advanced':
            try:
                self.scraper = AdvancedOABScraper()
                print("✓ AdvancedOABScraper inicializado com sucesso")
            except Exception as e:
                print(f"✗ Erro ao inicializar scraper: {e}")
                self.scraper = None

        self.setup_ui()
    def setup_ui(self):
        # Search section - Dinâmica baseada no modo
        self.search_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.12))

        self.process_input = TextInput(
            hint_text="Número do processo (ex: 00008323520184013202)",
            multiline=False,
            size_hint=(0.7, 1)
        )

        self.search_btn = Button(text="Buscar", size_hint=(0.15, 1))
        self.search_btn.bind(on_press=self.search)

        clear_btn = Button(text="Limpar", size_hint=(0.15, 1))
        clear_btn.bind(on_press=self.clear_search)

        self.search_layout.add_widget(self.process_input)
        self.search_layout.add_widget(self.search_btn)
        self.search_layout.add_widget(clear_btn)

        # OAB-specific fields (hidden by default)
        self.oab_fields_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.08))
        self.oab_fields_layout.opacity = 0
        self.oab_fields_layout.disabled = True

        oab_label = Label(text="Número OAB:", size_hint=(0.25, 1))

        self.oab_input = TextInput(
            hint_text="Ex: 123456/SP ou SP123456",
            multiline=False,
            size_hint=(0.45, 1)
        )

        self.uf_input = TextInput(
            hint_text="UF",
            multiline=False,
            size_hint=(0.15, 1),
            text="SP"
        )

        self.oab_fields_layout.add_widget(oab_label)
        self.oab_fields_layout.add_widget(self.oab_input)
        self.oab_fields_layout.add_widget(self.uf_input)

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

        self.add_widget(self.search_layout)
        self.add_widget(self.oab_fields_layout)
        self.add_widget(tribunal_layout)
        self.add_widget(filter_layout)
        self.add_widget(scroll_view)

        self.current_filter = "Todos"

    def set_consulta_mode(self, mode):
        """Alternar entre modo processo e OAB"""
        self.consulta_mode = mode

        if mode == "processo":
            # Mostrar campo de processo, esconder OAB
            self.process_input.hint_text = "Número do processo (ex: 00008323520184013202)"
            self.search_btn.text = "Buscar Processo"

            # Animar transição
            Animation(opacity=0, duration=0.3).start(self.oab_fields_layout)
            Clock.schedule_once(lambda dt: setattr(self.oab_fields_layout, 'disabled', True), 0.3)

        else:  # modo OAB
            # Mostrar campos OAB
            self.process_input.hint_text = "Nome do Advogado (opcional)"
            self.search_btn.text = "Buscar por OAB"

            # Animar transição
            self.oab_fields_layout.disabled = False
            Animation(opacity=1, duration=0.3).start(self.oab_fields_layout)

    def search(self, instance):
        """Executa busca baseada no modo selecionado"""
        if self.consulta_mode == "processo":
            self.search_process(instance)
        else:
            self.search_by_oab(instance)

    def search_process(self, instance):
        """Busca tradicional por número de processo"""
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

    def search_by_oab(self, instance):
        """Busca por número da OAB"""
        oab_numero = self.oab_input.text.strip()
        oab_uf = self.uf_input.text.strip().upper()

        if not oab_numero or not oab_uf:
            self.show_popup("Aviso", "Digite o número e UF da OAB")
            return

        # Limpar resultados anteriores
        self.results_container.clear_widgets()
        self.original_results = []

        # Mostrar loading
        loading_label = Label(text="Consultando processos do advogado...", font_size='18sp')
        self.results_container.add_widget(loading_label)

        # Executar consulta OAB em thread separada
        threading.Thread(
            target=self.perform_oab_search,
            args=(oab_numero, oab_uf),
            daemon=True
        ).start()

    # No consulta_screen.py, atualize o método perform_oab_search:

    # app/screens/consulta_screen.py - MÉTODO perform_oab_search

    def perform_oab_search(self, oab_numero, oab_uf):
        """Executa busca por OAB em background"""
        try:
            import re

            # Limpar OAB - apenas números
            oab_limpo = re.sub(r'\D', '', oab_numero)
            oab_uf_limpo = oab_uf.upper()[:2]

            if self.scraper:
                print(f"Usando scraper para OAB {oab_limpo}/{oab_uf_limpo}")

                # Usar método correto baseado no tipo de scraper
                if hasattr(self.scraper, 'consultar_oab_detalhado'):
                    resultados = self.scraper.consultar_oab_detalhado(oab_limpo, oab_uf_limpo)
                elif hasattr(self.scraper, 'consultar_por_oab'):
                    resultados = self.scraper.consultar_por_oab(oab_limpo, oab_uf_limpo)
                else:
                    resultados = {
                        'numero_oab': f"{oab_limpo}/{oab_uf_limpo}",
                        'processos_encontrados': [],
                        'erro': 'Scraper não tem método de consulta válido'
                    }
            else:
                resultados = {
                    'numero_oab': f"{oab_limpo}/{oab_uf_limpo}",
                    'processos_encontrados': [],
                    'erro': 'Nenhum scraper disponível. Instale beautifulsoup4 e requests.'
                }

            # Atualizar interface
            Clock.schedule_once(lambda dt: self.display_oab_results(resultados))

        except Exception as e:
            error_msg = f"Falha na busca OAB: {str(e)}"
            print(f"Erro no perform_oab_search: {e}")
            Clock.schedule_once(lambda dt: self.show_error("Erro", error_msg))

    # E no display_oab_results, use o novo card detalhado:
    def display_oab_results(self, resultados):
        """Exibe resultados da busca por OAB com informações detalhadas"""
        self.results_container.clear_widgets()

        if not resultados or 'processos_encontrados' not in resultados:
            self.results_container.add_widget(Label(
                text="Nenhum processo encontrado para esta OAB",
                size_hint_y=None,
                height=dp(50),
                color=get_color_from_hex('#D32F2F')
            ))
            return

        processos = resultados['processos_encontrados']

        if not processos:
            self.results_container.add_widget(Label(
                text=f"Nenhum processo encontrado para OAB {resultados.get('numero_oab', '')}",
                size_hint_y=None,
                height=dp(50),
                color=get_color_from_hex('#666666')
            ))
            return

        # Estatísticas
        stats = resultados.get('estatisticas', {})
        stats_text = (
            f"⚖️ OAB: {resultados.get('numero_oab', '')} | "
            f"Processos: {stats.get('total_processos', len(processos))} | "
            f"Detalhados: {stats.get('processos_com_detalhes', 0)} | "
            f"Tempo: {stats.get('tempo_consulta', 0)}s"
        )

        stats_label = Label(
            text=stats_text,
            size_hint_y=None,
            height=dp(40),
            font_size='13sp',
            bold=True,
            color=get_color_from_hex('#1976D2')
        )
        self.results_container.add_widget(stats_label)

        # Adicionar cada processo com card detalhado
        for processo in processos:
            if processo.get('detalhes_completos', False):
                # Usar card detalhado
                from app.widgets.detailed_process_card import DetailedProcessCard
                card = DetailedProcessCard(processo)
                card.size_hint_y = None
                card.height = dp(300)  # Altura inicial
            else:
                # Usar card básico
                card = self.create_oab_result_card(processo)

            self.results_container.add_widget(card)

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

    def create_oab_result_card(self, processo):
        """Cria card simples para resultado de busca por OAB"""
        card = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=dp(10),
            spacing=dp(5)
        )

        # Processo number
        processo_label = Label(
            text=f"[b]Processo:[/b] {processo['numero_processo']}",
            markup=True,
            size_hint=(1, 0.3),
            font_size='14sp',
            color=get_color_from_hex('#1976D2')
        )

        # Tribunal
        tribunal_label = Label(
            text=f"Tribunal: {processo.get('tribunal', 'N/A')}",
            size_hint=(1, 0.2),
            font_size='12sp'
        )

        # Classe (se disponível)
        if processo.get('classe'):
            classe_label = Label(
                text=f"Classe: {processo['classe']}",
                size_hint=(1, 0.2),
                font_size='12sp'
            )
            card.add_widget(classe_label)

        # Fonte
        fonte_label = Label(
            text=f"Fonte: {processo.get('fonte', 'Consulta OAB')}",
            size_hint=(1, 0.2),
            font_size='11sp',
            color=get_color_from_hex('#666666')
        )

        # Botão para ver detalhes
        details_btn = Button(
            text="Ver Detalhes",
            size_hint=(1, 0.3),
            background_color=get_color_from_hex('#1976D2'),
            color=(1, 1, 1, 1),
            font_size='12sp'
        )
        details_btn.bind(on_press=lambda x: self.show_process_details(processo))

        card.add_widget(processo_label)
        card.add_widget(tribunal_label)
        card.add_widget(fonte_label)
        card.add_widget(details_btn)

        # Estilo
        card.canvas.before.clear()
        with card.canvas.before:
            Color(0.98, 0.98, 0.98, 1)
            Rectangle(pos=card.pos, size=card.size)
            Color(0.8, 0.8, 0.8, 1)
            Line(rectangle=(card.x, card.y, card.width, card.height), width=1)

        return card

    def show_process_details(self, processo):
        """Mostra detalhes do processo em um popup"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        title = Label(
            text=f"Detalhes do Processo",
            font_size='18sp',
            bold=True,
            color=get_color_from_hex('#1976D2')
        )

        details = f"""
        Número: {processo['numero_processo']}
        Tribunal: {processo.get('tribunal', 'N/A')}
        Classe: {processo.get('classe', 'N/A')}
        Assunto: {processo.get('assunto', 'N/A')}
        Fonte: {processo.get('fonte', 'Consulta OAB')}
        Data Consulta: {processo.get('data_consulta', 'N/A')}
        """

        details_label = Label(
            text=details,
            font_size='14sp',
            halign='left',
            valign='top'
        )
        details_label.bind(size=lambda lbl, size: setattr(details_label, 'text_size', (lbl.width, None)))

        close_btn = Button(
            text="Fechar",
            size_hint=(1, 0.2),
            background_color=get_color_from_hex('#1976D2'),
            color=(1, 1, 1, 1)
        )

        content.add_widget(title)
        content.add_widget(details_label)
        content.add_widget(close_btn)

        popup = Popup(
            title=f"Processo {processo['numero_processo'][:20]}...",
            content=content,
            size_hint=(0.8, 0.6)
        )

        close_btn.bind(on_press=popup.dismiss)
        popup.open()

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

    def select_filter(self, filter_type):
        self.current_filter = filter_type
        self.filter_dropdown.select(filter_type)

    def clear_search(self, instance):
        self.process_input.text = ""
        self.oab_input.text = ""
        self.uf_input.text = "SP"
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

    def update_selected_tribunal(self, tribunal_name):
        """Update the selected tribunal"""
        self.selected_tribunal = tribunal_name
        self.tribunal_info_label.text = tribunal_name

        # Clear any existing results
        self.results_container.clear_widgets()
        self.original_results = []
        self.displayed_results = []