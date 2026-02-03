from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp

from app.widgets.favorites_card import FavoriteCard


class FavoritosScreen(BoxLayout):
    def __init__(self, favorites_store=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(10)
        self.padding = dp(10)
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

        self.refresh_favorites()

    def refresh_favorites(self):
        self.favorites_container.clear_widgets()

        favorites = self.favorites_store.get_favorites()

        if not favorites:
            self.favorites_container.add_widget(Label(
                text="Nenhum processo favorito",
                size_hint_y=None,
                height=dp(100),
                font_size='16sp',
                color=(0.5, 0.5, 0.5, 1)
            ))
            return

        for fav in favorites:
            card = FavoriteCard(favorite=fav, favorites_store=self.favorites_store)
            self.favorites_container.add_widget(card)