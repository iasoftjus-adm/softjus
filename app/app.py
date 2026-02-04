from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from app.screens.login_screen import LoginScreen
from app.screens.dashboard_screen import DashboardScreen


class ProcessoApp(App):
    def build(self):
        self.title = "IASoftJus"
        Window.size = (1000, 700)

        # Create screen manager
        sm = ScreenManager()

        # Add screens
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(DashboardScreen(name='dashboard'))

        return sm