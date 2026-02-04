from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout as KivyBoxLayout


class OABResultCard(BoxLayout):
    def __init__(self, result=None, favorites_store=None, oab_info=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(200)  # Um pouco menor que o card de processo normal
        self.padding = dp(10)
        self.spacing = dp(5)
        self.result = result
        self.favorites_store = favorites_store
        self.oab_info = oab_info

        self.setup_card()

    def setup_card(self):
        # Header com ícone OAB
        header = BoxLayout(size_hint=(1, 0.2))

        processo_label = Label(
            text=f"[b]Processo:[/b] {self.result['numero_processo']}",
            markup=True,
            size_hint=(0.7, 1),
            halign='left',
            valign='middle',
            font_size='14sp'
        )
        processo_label.bind(size=lambda lbl, size: setattr(processo_label, 'text_size', (lbl.width, None)))

        # Ícone OAB
        oab_icon = Label(
            text="⚖️",
            size_hint=(0.1, 1),
            font_size='16sp'
        )

        # Botões de ação
        action_buttons = BoxLayout(size_hint=(0.2, 1), spacing=dp(5))

        view_btn = Button(
            text="🔍",
            size_hint=(0.5, 1),
            font_size='14sp',
            background_color=(0, 0, 0, 0),
            color=get_color_from_hex('#1976D2')
        )
        view_btn.bind(on_press=self.view_process_details)

        favorite_btn = Button(
            text="☆",
            size_hint=(0.5, 1),
            font_size='16sp',
            background_color=(0, 0, 0, 0),
            color=(0.7, 0.7, 0.7, 1)
        )
        favorite_btn.result_data = self.result
        favorite_btn.bind(on_press=self.toggle_favorite)

        action_buttons.add_widget(view_btn)
        action_buttons.add_widget(favorite_btn)

        header.add_widget(processo_label)
        header.add_widget(oab_icon)
        header.add_widget(action_buttons)

        # Informações do processo
        details = GridLayout(cols=2, size_hint=(1, 0.6), spacing=dp(5))

        # Tribunal
        details.add_widget(Label(text="Tribunal:", size_hint=(0.3, 1), font_size='12sp'))
        details.add_widget(Label(
            text=self.result.get('tribunal', 'N/A'),
            size_hint=(0.7, 1),
            font_size='12sp',
            halign='left',
            color=get_color_from_hex('#1976D2')
        ))

        # Classe
        if self.result.get('classe'):
            details.add_widget(Label(text="Classe:", size_hint=(0.3, 1), font_size='12sp'))
            details.add_widget(Label(
                text=self.result['classe'],
                size_hint=(0.7, 1),
                font_size='12sp',
                halign='left'
            ))

        # Assunto
        if self.result.get('assunto'):
            details.add_widget(Label(text="Assunto:", size_hint=(0.3, 1), font_size='12sp'))
            details.add_widget(Label(
                text=self.result['assunto'],
                size_hint=(0.7, 1),
                font_size='12sp',
                halign='left'
            ))

        # Fonte
        details.add_widget(Label(text="Fonte:", size_hint=(0.3, 1), font_size='12sp'))
        fonte_label = Label(
            text=self.result.get('fonte', 'Consulta OAB'),
            size_hint=(0.7, 1),
            font_size='11sp',
            halign='left',
            color=get_color_from_hex('#666666')
        )
        details.add_widget(fonte_label)

        # Confiabilidade
        if self.result.get('confiabilidade'):
            details.add_widget(Label(text="Confiabilidade:", size_hint=(0.3, 1), font_size='12sp'))
            conf_label = Label(
                text=f"{self.result['confiabilidade']}%",
                size_hint=(0.7, 1),
                font_size='12sp',
                halign='left',
                color=get_color_from_hex('#4CAF50') if self.result['confiabilidade'] > 80 else
                get_color_from_hex('#FF9800') if self.result['confiabilidade'] > 60 else
                get_color_from_hex('#D32F2F')
            )
            details.add_widget(conf_label)

        # Footer com ações
        footer = BoxLayout(size_hint=(1, 0.2), spacing=dp(10))

        # Botão para consultar este processo especificamente
        consult_btn = Button(
            text="Consultar Este Processo",
            size_hint=(0.7, 1),
            background_color=get_color_from_hex('#1976D2'),
            color=(1, 1, 1, 1),
            font_size='12sp'
        )
        consult_btn.bind(on_press=self.consult_this_process)

        # Botão para ver no site original
        if self.result.get('url_detalhes'):
            site_btn = Button(
                text="Ver no Site",
                size_hint=(0.3, 1),
                background_color=get_color_from_hex('#4CAF50'),
                color=(1, 1, 1, 1),
                font_size='12sp'
            )
            site_btn.bind(on_press=lambda x: self.open_external_url(self.result['url_detalhes']))
            footer.add_widget(site_btn)

        footer.add_widget(consult_btn)

        self.add_widget(header)
        self.add_widget(details)
        self.add_widget(footer)

        # Styling
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Fundo mais claro para OAB
            Rectangle(pos=self.pos, size=self.size)
            Color(0.8, 0.8, 0.8, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

    def toggle_favorite(self, instance):
        if not self.favorites_store or not self.result:
            return

        is_favorite = self.favorites_store.is_favorite(self.result['numero_processo'])

        if is_favorite:
            # Remove from favorites
            self.favorites_store.remove_favorite(self.result['numero_processo'])
            instance.text = "☆"
            instance.color = (0.7, 0.7, 0.7, 1)
        else:
            # Add to favorites
            self.favorites_store.add_favorite(self.result)
            instance.text = "★"
            instance.color = get_color_from_hex('#FFD700')

        # Show notification
        from kivy.app import App
        App.get_running_app().show_notification(
            "Favoritos",
            "Adicionado aos favoritos!" if not is_favorite else "Removido dos favoritos!"
        )

    def view_process_details(self, instance):
        """Abre popup com detalhes do processo"""
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))

        # Título
        title = Label(
            text=f"Detalhes do Processo",
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.2),
            color=get_color_from_hex('#1976D2')
        )

        # Detalhes em grid
        details_grid = GridLayout(cols=2, spacing=dp(10), size_hint=(1, 0.6))

        fields = [
            ("Número do Processo", self.result.get('numero_processo', 'N/A')),
            ("Tribunal", self.result.get('tribunal', 'N/A')),
            ("Classe", self.result.get('classe', 'N/A')),
            ("Assunto", self.result.get('assunto', 'N/A')),
            ("Fonte", self.result.get('fonte', 'Consulta OAB')),
            ("Confiabilidade", f"{self.result.get('confiabilidade', 'N/A')}%"),
            ("OAB Consultada", self.oab_info if self.oab_info else 'N/A'),
        ]

        for label, value in fields:
            details_grid.add_widget(Label(
                text=f"{label}:",
                font_size='14sp',
                bold=True,
                size_hint=(0.4, 1),
                halign='right'
            ))
            details_grid.add_widget(Label(
                text=value,
                font_size='14sp',
                size_hint=(0.6, 1),
                halign='left'
            ))

        # Botão de fechar
        close_btn = Button(
            text="Fechar",
            size_hint=(1, 0.2),
            background_color=get_color_from_hex('#1976D2'),
            color=(1, 1, 1, 1)
        )

        content.add_widget(title)
        content.add_widget(details_grid)
        content.add_widget(close_btn)

        popup = Popup(
            title=f"Processo {self.result['numero_processo'][:20]}...",
            content=content,
            size_hint=(0.9, 0.7)
        )

        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    def consult_this_process(self, instance):
        """Abre este processo específico na aba de consulta normal"""
        from kivy.app import App

        # Navegar para a tela de consulta
        app = App.get_running_app()
        if hasattr(app, 'root'):
            # Mudar para modo processo
            dashboard = app.root.get_screen('dashboard')
            if hasattr(dashboard, 'consulta_screen'):
                dashboard.set_consulta_mode("processo")
                dashboard.consulta_screen.process_input.text = self.result['numero_processo']
                dashboard.show_consulta(None)

                # Aguardar um momento e executar a busca
                from kivy.clock import Clock
                Clock.schedule_once(lambda dt: dashboard.consulta_screen.search_process(instance), 0.5)

    def open_external_url(self, url):
        """Abre URL externa no navegador padrão"""
        import webbrowser
        try:
            webbrowser.open(url)
        except Exception as e:
            from kivy.app import App
            App.get_running_app().show_notification("Erro", f"Não foi possível abrir o link: {e}")