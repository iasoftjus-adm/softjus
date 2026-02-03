from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

from app.widgets.update_card import UpdateCard


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
            update_card = UpdateCard(update=update)
            updates_container.add_widget(update_card)

        scroll_view = ScrollView(size_hint=(1, 0.9))
        scroll_view.add_widget(updates_container)

        self.add_widget(title)
        self.add_widget(scroll_view)