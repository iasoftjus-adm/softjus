from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from app.screens.consulta_screen import ConsultaScreen
from app.screens.favoritos_screen import FavoritosScreen
from app.screens.atualizacoes_screen import AtualizacoesScreen
from app.storage.favorites_store import FavoritesStore
from app.api.config import TRIBUNAL_TYPES, TRIBUNAL_URLS, DEFAULT_TRIBUNAL


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.favorites_store = FavoritesStore()
        self.current_tribunal_type = "Justiça Federal"
        self.current_tribunal = DEFAULT_TRIBUNAL
        self.setup_ui()

    def setup_ui(self):
        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))

        # Header
        header = BoxLayout(size_hint=(1, 0.1))
        title = Label(text="Dashboard", font_size='24sp', color=get_color_from_hex('#1976D2'))
        logout_btn = Button(text="Sair", size_hint=(0.2, 1))
        logout_btn.bind(on_press=self.logout)
        header.add_widget(title)
        header.add_widget(logout_btn)

        # Tribunal filter section
        tribunal_layout = BoxLayout(orientation='horizontal', spacing=dp(10), size_hint=(1, 0.08))

        tribunal_label = Label(text="Tribunal:", size_hint=(0.15, 1))

        # Tribunal type dropdown
        self.tribunal_type_spinner = Spinner(
            text=self.current_tribunal_type,
            values=TRIBUNAL_TYPES,
            size_hint=(0.25, 1)
        )
        self.tribunal_type_spinner.bind(text=self.on_tribunal_type_select)

        # Specific tribunal dropdown
        self.tribunal_spinner = Spinner(
            text=self.current_tribunal,
            values=self.get_tribunals_for_type(self.current_tribunal_type),
            size_hint=(0.45, 1)
        )
        self.tribunal_spinner.bind(text=self.on_tribunal_select)

        tribunal_layout.add_widget(tribunal_label)
        tribunal_layout.add_widget(self.tribunal_type_spinner)
        tribunal_layout.add_widget(self.tribunal_spinner)

        # Modo de consulta selector - NOVO
        consulta_mode_layout = BoxLayout(
            orientation='horizontal',
            spacing=dp(10),
            size_hint=(1, 0.08),
            padding=[dp(10), 0, dp(10), 0]
        )

        mode_label = Label(
            text="Tipo de Consulta:",
            size_hint=(0.25, 1),
            font_size='14sp'
        )

        self.mode_toggle = ToggleButton(
            text="Número do Processo",
            group='consulta_mode',
            state='down',
            size_hint=(0.375, 1)
        )
        self.mode_toggle.bind(on_press=lambda x: self.set_consulta_mode("processo"))

        self.oab_toggle = ToggleButton(
            text="Número da OAB",
            group='consulta_mode',
            size_hint=(0.375, 1)
        )
        self.oab_toggle.bind(on_press=lambda x: self.set_consulta_mode("oab"))

        consulta_mode_layout.add_widget(mode_label)
        consulta_mode_layout.add_widget(self.mode_toggle)
        consulta_mode_layout.add_widget(self.oab_toggle)

        # Tab buttons
        tab_layout = BoxLayout(size_hint=(1, 0.08), spacing=dp(5))

        self.consulta_tab = ToggleButton(text="Consulta", group='tabs', state='down')
        self.favoritos_tab = ToggleButton(text="Favoritos", group='tabs')
        self.atualizacoes_tab = ToggleButton(text="Atualizações", group='tabs')

        self.consulta_tab.bind(on_press=self.show_consulta)
        self.favoritos_tab.bind(on_press=self.show_favoritos)
        self.atualizacoes_tab.bind(on_press=self.show_atualizacoes)

        tab_layout.add_widget(self.consulta_tab)
        tab_layout.add_widget(self.favoritos_tab)
        tab_layout.add_widget(self.atualizacoes_tab)

        # Content area
        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 0.66))

        # Initialize screens
        self.consulta_screen = ConsultaScreen(
            favorites_store=self.favorites_store,
            selected_tribunal=self.current_tribunal
        )
        self.favoritos_screen = FavoritosScreen(favorites_store=self.favorites_store)
        self.atualizacoes_screen = AtualizacoesScreen()

        self.content_area.add_widget(self.consulta_screen)

        # Adicionar todos os widgets ao layout principal
        layout.add_widget(header)
        layout.add_widget(tribunal_layout)
        layout.add_widget(consulta_mode_layout)  # Adicionar o seletor de modo
        layout.add_widget(tab_layout)
        layout.add_widget(self.content_area)

        # IMPORTANTE: Adicionar layout ao screen APENAS UMA VEZ
        self.add_widget(layout)

    def get_tribunals_for_type(self, tribunal_type):
        """Get list of tribunals for a given type"""
        if tribunal_type in TRIBUNAL_URLS:
            return list(TRIBUNAL_URLS[tribunal_type].keys())
        return []

    def on_tribunal_type_select(self, spinner, tribunal_type):
        """Handle tribunal type selection"""
        self.current_tribunal_type = tribunal_type
        tribunals = self.get_tribunals_for_type(tribunal_type)

        # Update tribunal spinner values
        self.tribunal_spinner.values = tribunals

        # Select first tribunal in the list
        if tribunals:
            self.tribunal_spinner.text = tribunals[0]
            self.current_tribunal = tribunals[0]

            # Update consulta screen if it's active
            if hasattr(self, 'consulta_screen'):
                self.consulta_screen.update_selected_tribunal(self.current_tribunal)

    def on_tribunal_select(self, spinner, tribunal):
        """Handle specific tribunal selection"""
        self.current_tribunal = tribunal

        # Update consulta screen if it's active
        if hasattr(self, 'consulta_screen'):
            self.consulta_screen.update_selected_tribunal(tribunal)

    def set_consulta_mode(self, mode):
        """Define o modo de consulta (processo ou OAB)"""
        # Atualizar a tela de consulta
        if hasattr(self, 'consulta_screen'):
            self.consulta_screen.set_consulta_mode(mode)

    def show_consulta(self, instance):
        # Ensure consulta screen has current tribunal
        self.consulta_screen.update_selected_tribunal(self.current_tribunal)
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.consulta_screen)

    def show_favoritos(self, instance):
        # Refresh favorites
        self.favoritos_screen.refresh_favorites()
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.favoritos_screen)

    def show_atualizacoes(self, instance):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.atualizacoes_screen)

    def logout(self, instance):
        self.manager.current = 'login'