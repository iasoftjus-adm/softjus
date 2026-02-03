from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, Line


class ResultCard(BoxLayout):
    def __init__(self, result=None, favorites_store=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(240)  # Increased height to accommodate tribunal info
        self.padding = dp(10)
        self.spacing = dp(5)
        self.result = result
        self.favorites_store = favorites_store

        self.setup_card()

    def setup_card(self):
        # Header with process number and favorite button
        header = BoxLayout(size_hint=(1, 0.15))

        processo_label = Label(
            text=f"[b]Processo:[/b] {self.result['processo']}",
            markup=True,
            size_hint=(0.8, 1),
            halign='left',
            valign='middle'
        )
        processo_label.bind(size=lambda lbl, size: setattr(processo_label, 'text_size', (lbl.width, None)))

        # Check if already favorite
        is_favorite = self.favorites_store.is_favorite(self.result['processo']) if self.favorites_store else False

        favorite_btn = Button(
            text="★" if is_favorite else "☆",
            size_hint=(0.2, 1),
            font_size='20sp',
            color=get_color_from_hex('#FFD700') if is_favorite else (0.7, 0.7, 0.7, 1)
        )
        favorite_btn.bind(on_press=self.toggle_favorite)

        header.add_widget(processo_label)
        header.add_widget(favorite_btn)

        # Tribunal info (new)
        tribunal_label = Label(
            text=f"[b]Tribunal:[/b] {self.result.get('tribunal', 'N/A')}",
            markup=True,
            size_hint=(1, 0.1),
            font_size='12sp',
            color=get_color_from_hex('#1976D2')
        )
        tribunal_label.bind(size=lambda lbl, size: setattr(tribunal_label, 'text_size', (lbl.width, None)))

        # Details
        details = GridLayout(cols=2, size_hint=(1, 0.75), spacing=dp(5))

        details.add_widget(Label(text="Classe:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=self.result['classe'], size_hint=(0.7, 1), halign='left'))

        details.add_widget(Label(text="Órgão Julgador:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=self.result['orgao'], size_hint=(0.7, 1), halign='left'))

        details.add_widget(Label(text="Data de Ajuizamento:", size_hint=(0.3, 1)))
        details.add_widget(Label(text=self.result['data'], size_hint=(0.7, 1), halign='left'))

        details.add_widget(Label(text="Último Movimento:", size_hint=(0.3, 1)))
        ultimo_mov = Label(text=self.result['ultimo_movimento'],
                           size_hint=(0.7, 1),
                           halign='left',
                           text_size=(Window.width * 0.7 - dp(20), None))
        ultimo_mov.bind(size=lambda lbl, size: setattr(ultimo_mov, 'text_size', (lbl.width, None)))
        details.add_widget(ultimo_mov)

        self.add_widget(header)
        self.add_widget(tribunal_label)
        self.add_widget(details)

        # Styling
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.8, 0.8, 0.8, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

    def toggle_favorite(self, instance):
        if not self.favorites_store or not self.result:
            return

        is_favorite = self.favorites_store.is_favorite(self.result['processo'])

        if is_favorite:
            # Remove from favorites
            self.favorites_store.remove_favorite(self.result['processo'])
            instance.text = "☆"
            instance.color = (0.7, 0.7, 0.7, 1)
        else:
            # Add to favorites
            self.favorites_store.add_favorite(self.result)
            instance.text = "★"
            instance.color = get_color_from_hex('#FFD700')