from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


class UpdateCard(BoxLayout):
    def __init__(self, update=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(80)
        self.padding = dp(10)
        self.update = update

        self.setup_card()

    def setup_card(self):
        date_label = Label(
            text=self.update['date'],
            size_hint=(1, 0.3),
            font_size='12sp',
            color=get_color_from_hex('#1976D2'),
            bold=True
        )

        text_label = Label(
            text=self.update['text'],
            size_hint=(1, 0.7),
            halign='left',
            valign='middle'
        )
        text_label.bind(size=lambda lbl, size: setattr(text_label, 'text_size', (lbl.width, None)))

        self.add_widget(date_label)
        self.add_widget(text_label)