import requests
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.storage.jsonstore import JsonStore
from kivy.utils import get_color_from_hex
import threading
from datetime import datetime

# API Configuration
API_URL = "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"
API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw"

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'  # Set name here
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', 
                          spacing=dp(20), 
                          padding=[dp(40), dp(100), dp(40), dp(100)])
        
        # Title
        title = Label(text="Consulta Processos TRF1", 
                     font_size='28sp',
                     color=get_color_from_hex('#1976D2'),
                     bold=True)
        
        # Login form
        form_layout = BoxLayout(orientation='vertical', spacing=dp(15))
        
        # Username field
        self.username_input = TextInput(
            hint_text="Usuário",
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(15), dp(15)],
            font_size='16sp'
        )
        
        # Password field
        self.password_input = TextInput(
            hint_text="Senha",
            password=True,
            multiline=False,
            size_hint=(1, None),
            height=dp(50),
            padding=[dp(15), dp(15)],
            font_size='16sp'
        )
        
        # Login button
        login_btn = Button(
            text="ENTRAR",
            size_hint=(1, None),
            height=dp(50),
            background_color=get_color_from_hex('#1976D2'),
            color=(1, 1, 1, 1),
            bold=True
        )
        login_btn.bind(on_press=self.attempt_login)
        
        # Error label
        self.error_label = Label(
            text="",
            color=get_color_from_hex('#D32F2F'),
            size_hint=(1, None),
            height=dp(30)
        )
        
        form_layout.add_widget(self.username_input)
        form_layout.add_widget(self.password_input)
        form_layout.add_widget(login_btn)
        form_layout.add_widget(self.error_label)
        
        layout.add_widget(title)
        layout.add_widget(form_layout)
        
        self.add_widget(layout)
    
    def attempt_login(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.error_label.text = ""
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = "Usuário ou senha incorretos"

class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dashboard'  # Set name here
        self.favorites_store = JsonStore('favorites.json')
        self.favorite_processes = self.load_favorites()
        self.setup_ui()
    
    def load_favorites(self):
        """Load favorite processes from storage"""
        try:
            favorites = []
            for key in self.favorites_store:
                favorites.append(self.favorites_store.get(key))
            return favorites
        except:
            return []
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        
        # Header
        header = BoxLayout(size_hint=(1, 0.1))
        title = Label(text="Dashboard", font_size='24sp', color=get_color_from_hex('#1976D2'))
        logout_btn = Button(text="Sair", size_hint=(0.2, 1))
        logout_btn.bind(on_press=self.logout)
        header.add_widget(title)
        header.add_widget(logout_btn)
        
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
        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 0.82))
        
        # Initialize screens - Don't pass name parameter to BoxLayout
        self.consulta_screen = ConsultaScreen()
        self.favoritos_screen = FavoritosScreen(favorites=self.favorite_processes,
                                               favorites_store=self.favorites_store)
        self.atualizacoes_screen = AtualizacoesScreen()
        
        self.content_area.add_widget(self.consulta_screen)
        
        layout.add_widget(header)
        layout.add_widget(tab_layout)
        layout.add_widget(self.content_area)
        
        self.add_widget(layout)
    
    def show_consulta(self, instance):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.consulta_screen)
    
    def show_favoritos(self, instance):
        # Refresh favorites
        self.favorite_processes = self.load_favorites()
        self.favoritos_screen.update_favorites(self.favorite_processes)
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.favoritos_screen)
    
    def show_atualizacoes(self, instance):
        self.content_area.clear_widgets()
        self.content_area.add_widget(self.atualizacoes_screen)
    
    def logout(self, instance):
        self.manager.current = 'login'

class ConsultaScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.original_results = []
        self.displayed_results = []
        self.favorites_store = JsonStore('favorites.json')
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
        
        scroll_view = ScrollView(size_hint=(1, 0.78))
        scroll_view.add_widget(self.results_container)
        
        self.add_widget(search_layout)
        self.add_widget(filter_layout)
        self.add_widget(scroll_view)
        
        self.current_filter = "Todos"
    
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
        
        # Start search
        threading.Thread(target=self.perform_search, args=(process_number,), daemon=True).start()
    
    def perform_search(self, process_number):
        try:
            payload = json.dumps({
                "query": {
                    "match": {
                        "numeroProcesso": process_number
                    }
                }
            })
            
            headers = {
                'Authorization': f'ApiKey {API_KEY}',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(API_URL, headers=headers, data=payload, timeout=30)
            Clock.schedule_once(lambda dt: self.display_results(response))
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error("Erro", f"Falha na busca: {str(e)}"))
    
    def display_results(self, response):
        self.results_container.clear_widgets()
        
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
            
        except:
            self.show_error("Erro", "Resposta inválida da API")
    
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
        if data_ajuizamento:
            try:
                dt = datetime.strptime(data_ajuizamento[:8], "%Y%m%d")
                data['data'] = dt.strftime("%d/%m/%Y")
            except:
                data['data'] = data_ajuizamento
        else:
            data['data'] = "N/A"
        
        # Último Movimento
        movimentos = source.get('movimentos', [])
        if movimentos:
            ultimo = movimentos[-1]
            data_hora = ultimo.get('dataHora', '')
            nome = ultimo.get('nome', '')
            if data_hora:
                try:
                    dt = datetime.fromisoformat(data_hora.replace('Z', '+00:00'))
                    data['ultimo_movimento'] = f"{dt.strftime('%d/%m/%Y %H:%M')} - {nome}"
                except:
                    data['ultimo_movimento'] = f"{data_hora} - {nome}"
            else:
                data['ultimo_movimento'] = nome
        else:
            data['ultimo_movimento'] = "Nenhum movimento registrado"
        
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
        card = BoxLayout(orientation='vertical', 
                        size_hint_y=None, 
                        height=dp(220),
                        padding=dp(10),
                        spacing=dp(5))
        
        # Header with process number and favorite button
        header = BoxLayout(size_hint=(1, 0.15))
        
        processo_label = Label(
            text=f"[b]Processo:[/b] {result['processo']}",
            markup=True,
            size_hint=(0.8, 1),
            halign='left',
            valign='middle'
        )
        processo_label.bind(size=lambda lbl, size: setattr(processo_label, 'text_size', (lbl.width, None)))
        
        # Check if already favorite
        is_favorite = False
        try:
            for key in self.favorites_store:
                fav = self.favorites_store.get(key)
                if fav.get('processo') == result['processo']:
                    is_favorite = True
                    break
        except:
            pass
        
        favorite_btn = Button(
            text="★" if is_favorite else "☆",
            size_hint=(0.2, 1),
            font_size='20sp',
            color=get_color_from_hex('#FFD700') if is_favorite else (0.7, 0.7, 0.7, 1)
        )
        favorite_btn.result_data = result
        favorite_btn.bind(on_press=self.toggle_favorite)
        
        header.add_widget(processo_label)
        header.add_widget(favorite_btn)
        
        # Details
        details = GridLayout(cols=2, size_hint=(1, 0.85), spacing=dp(5))
        
        details.add_widget(Label(text="Classe:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=result['classe'], size_hint=(0.7, 1), halign='left'))
        
        details.add_widget(Label(text="Órgão Julgador:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=result['orgao'], size_hint=(0.7, 1), halign='left'))
        
        details.add_widget(Label(text="Data de Ajuizamento:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=result['data'], size_hint=(0.7, 1), halign='left'))
        
        details.add_widget(Label(text="Último Movimento:", size_hint=(0.3, 1)))
        ultimo_mov = Label(text=result['ultimo_movimento'], 
                          size_hint=(0.7, 1), 
                          halign='left',
                          text_size=(Window.width * 0.7 - dp(20), None))
        ultimo_mov.bind(size=lambda lbl, size: setattr(ultimo_mov, 'text_size', (lbl.width, None)))
        details.add_widget(ultimo_mov)
        
        card.add_widget(header)
        card.add_widget(details)
        
        # Styling
        card.canvas.before.clear()
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=card.pos, size=card.size)
            Color(0.8, 0.8, 0.8, 1)
            from kivy.graphics import Line
            Line(rectangle=(card.x, card.y, card.width, card.height), width=1)
        
        return card
    
    def toggle_favorite(self, instance):
        result = instance.result_data
        
        # Check if already favorite
        is_favorite = False
        fav_key = None
        try:
            for key in self.favorites_store:
                fav = self.favorites_store.get(key)
                if fav.get('processo') == result['processo']:
                    is_favorite = True
                    fav_key = key
                    break
        except:
            pass
        
        if is_favorite:
            # Remove from favorites
            self.favorites_store.delete(fav_key)
            instance.text = "☆"
            instance.color = (0.7, 0.7, 0.7, 1)
        else:
            # Add to favorites
            key = f"processo_{len(self.favorites_store) + 1}"
            self.favorites_store.put(key, 
                                   processo=result['processo'],
                                   classe=result['classe'],
                                   data_adicao=datetime.now().isoformat())
            instance.text = "★"
            instance.color = get_color_from_hex('#FFD700')
        
        self.show_popup("Favoritos", 
                       "Adicionado aos favoritos!" if not is_favorite else "Removido dos favoritos!")
    
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

class FavoritosScreen(BoxLayout):
    def __init__(self, favorites=None, favorites_store=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.favorites = favorites or []
        self.favorites_store = favorites_store
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = Label(text="Processos Favoritos", 
                     font_size='20sp',
                     size_hint=(1, 0.1))
        
        # Favorites list
        self.favorites_container = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.favorites_container.bind(minimum_height=self.favorites_container.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 0.9))
        scroll_view.add_widget(self.favorites_container)
        
        self.add_widget(title)
        self.add_widget(scroll_view)
        
        self.update_favorites_display()
    
    def update_favorites(self, favorites):
        self.favorites = favorites
        self.update_favorites_display()
    
    def update_favorites_display(self):
        self.favorites_container.clear_widgets()
        
        if not self.favorites:
            self.favorites_container.add_widget(Label(
                text="Nenhum processo favorito",
                size_hint_y=None,
                height=dp(100),
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1)
            ))
            return
        
        for fav in self.favorites:
            card = self.create_favorite_card(fav)
            self.favorites_container.add_widget(card)
    
    def create_favorite_card(self, favorite):
        card = BoxLayout(orientation='vertical', 
                        size_hint_y=None, 
                        height=dp(120),
                        padding=dp(10),
                        spacing=dp(5))
        
        # Process number
        processo_label = Label(
            text=f"[b]{favorite.get('processo', 'N/A')}[/b]",
            markup=True,
            size_hint=(1, 0.4),
            font_size='16sp'
        )
        
        # Class
        classe_label = Label(
            text=f"Classe: {favorite.get('classe', 'N/A')}",
            size_hint=(1, 0.3)
        )
        
        # Added date
        data_adicao = favorite.get('data_adicao', '')
        if data_adicao:
            try:
                dt = datetime.fromisoformat(data_adicao)
                data_text = f"Adicionado em: {dt.strftime('%d/%m/%Y %H:%M')}"
            except:
                data_text = f"Adicionado em: {data_adicao}"
        else:
            data_text = ""
        
        data_label = Label(
            text=data_text,
            size_hint=(1, 0.3),
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1)
        )
        
        card.add_widget(processo_label)
        card.add_widget(classe_label)
        card.add_widget(data_label)
        
        # Styling
        card.canvas.before.clear()
        with card.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(1, 1, 0.9, 1)  # Light yellow background for favorites
            Rectangle(pos=card.pos, size=card.size)
        
        return card

class AtualizacoesScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title = Label(text="Últimas Atualizações", 
                     font_size='20sp',
                     size_hint=(1, 0.1))
        
        # Updates list
        updates_container = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        updates_container.bind(minimum_height=updates_container.setter('height'))
        
        # Sample updates
        updates = [
            {"date": "15/11/2024", "text": "Sistema atualizado com novo filtro de busca"},
            {"date": "14/11/2024", "text": "Adicionada funcionalidade de favoritos"},
            {"date": "13/11/2024", "text": "Corrigido bug na exibição de datas"},
            {"date": "12/11/2024", "text": "Melhorada performance das consultas"},
            {"date": "10/11/2024", "text": "Lançamento inicial do sistema"}
        ]
        
        for update in updates:
            update_card = self.create_update_card(update)
            updates_container.add_widget(update_card)
        
        scroll_view = ScrollView(size_hint=(1, 0.9))
        scroll_view.add_widget(updates_container)
        
        self.add_widget(title)
        self.add_widget(scroll_view)
    
    def create_update_card(self, update):
        card = BoxLayout(orientation='vertical', 
                        size_hint_y=None, 
                        height=dp(80),
                        padding=dp(10))
        
        date_label = Label(
            text=update['date'],
            size_hint=(1, 0.3),
            font_size='12sp',
            color=get_color_from_hex('#1976D2'),
            bold=True
        )
        
        text_label = Label(
            text=update['text'],
            size_hint=(1, 0.7),
            halign='left',
            valign='middle'
        )
        text_label.bind(size=lambda lbl, size: setattr(text_label, 'text_size', (lbl.width, None)))
        
        card.add_widget(date_label)
        card.add_widget(text_label)
        
        return card

class ProcessoApp(App):
    def build(self):
        Window.size = (1000, 700)
        
        # Create screen manager
        sm = ScreenManager()
        
        # Add screens
        login_screen = LoginScreen()
        dashboard_screen = DashboardScreen()
        
        sm.add_widget(login_screen)
        sm.add_widget(dashboard_screen)
        
        return sm

if __name__ == '__main__':
    ProcessoApp().run()