from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical',
                           spacing=dp(20),
                           padding=[dp(40), dp(100), dp(40), dp(100)])

        # Title
        title = Label(text="IASoftJus",
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
        from app.api.config import ADMIN_USERNAME, ADMIN_PASSWORD

        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.error_label.text = ""
            self.manager.current = 'dashboard'
        else:
            self.error_label.text = "Usuário ou senha incorretos"