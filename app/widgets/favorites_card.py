from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle
from datetime import datetime


class FavoriteCard(BoxLayout):
    def __init__(self, favorite=None, favorites_store=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(140)  # Increased height for tribunal info
        self.padding = dp(10)
        self.spacing = dp(5)
        self.favorite = favorite
        self.favorites_store = favorites_store

        self.setup_card()

    def setup_card(self):
        # Process number
        processo_label = Label(
            text=f"[b]{self.favorite.get('processo', 'N/A')}[/b]",
            markup=True,
            size_hint=(1, 0.3),
            font_size='16sp'
        )

        # Tribunal
        tribunal_label = Label(
            text=f"Tribunal: {self.favorite.get('tribunal', 'N/A')}",
            size_hint=(1, 0.2),
            font_size='12sp',
            color=(0.3, 0.3, 0.8, 1)
        )

        # Class
        classe_label = Label(
            text=f"Classe: {self.favorite.get('classe', 'N/A')}",
            size_hint=(1, 0.2)
        )

        # Added date
        data_adicao = self.favorite.get('data_adicao', '')
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

        self.add_widget(processo_label)
        self.add_widget(tribunal_label)
        self.add_widget(classe_label)
        self.add_widget(data_label)

        # Styling
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 0.9, 1)  # Light yellow background for favorites
            Rectangle(pos=self.pos, size=self.size)