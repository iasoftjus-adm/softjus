# app/widgets/detailed_process_card.py
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle, Line
from datetime import datetime


class DetailedProcessCard(Accordion):
    """Card expansível com informações detalhadas do processo"""

    def __init__(self, process_data, **kwargs):
        super().__init__(**kwargs)
        self.process_data = process_data
        self.orientation = 'vertical'
        self.setup_card()

    def setup_card(self):
        # Item 1: Informações Básicas
        basic_info = AccordionItem(title='📋 Informações Básicas')
        basic_content = self.create_basic_info_section()
        basic_info.add_widget(basic_content)
        self.add_widget(basic_info)

        # Item 2: Partes Envolvidas
        if self.process_data.get('partes'):
            partes_item = AccordionItem(title='👥 Partes Envolvidas')
            partes_content = self.create_partes_section()
            partes_item.add_widget(partes_content)
            self.add_widget(partes_item)

        # Item 3: Movimentações
        if self.process_data.get('movimentacoes'):
            mov_item = AccordionItem(title='📈 Movimentações')
            mov_content = self.create_movimentacoes_section()
            mov_item.add_widget(mov_content)
            self.add_widget(mov_item)

        # Item 4: Status e Andamento
        status_item = AccordionItem(title='⚖️ Status e Andamento')
        status_content = self.create_status_section()
        status_item.add_widget(status_content)
        self.add_widget(status_item)

        # Item 5: Informações Complementares
        if self.process_data.get('informacoes_complementares'):
            info_item = AccordionItem(title='📊 Detalhes Técnicos')
            info_content = self.create_info_complementar_section()
            info_item.add_widget(info_content)
            self.add_widget(info_item)

    def create_basic_info_section(self):
        """Cria seção de informações básicas"""
        layout = GridLayout(cols=2, spacing=dp(5), padding=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        fields = [
            ("Número do Processo", self.process_data.get('numero_processo', 'N/A')),
            ("Tribunal", self.process_data.get('tribunal', 'N/A')),
            ("Classe", self.process_data.get('classe', 'N/A')),
            ("Assunto", self.process_data.get('assunto', 'N/A')),
            ("Foro", self.process_data.get('foro', 'N/A')),
            ("Vara", self.process_data.get('vara', 'N/A')),
            ("Data Distribuição", self.format_date(self.process_data.get('data_distribuicao'))),
            ("Valor da Causa", self.process_data.get('valor_causa', 'N/A')),
            ("Situação", self.process_data.get('situacao_atual', 'N/A')),
            ("Fonte", self.process_data.get('fonte', 'Consulta OAB')),
            ("Data Coleta", self.format_date(self.process_data.get('data_coleta'))),
            ("Confiabilidade", f"{self.process_data.get('confiabilidade', 0)}%"),
        ]

        for label, value in fields:
            if value and value != 'N/A':
                # Label
                label_widget = Label(
                    text=f"{label}:",
                    font_size='12sp',
                    bold=True,
                    size_hint=(0.4, 1),
                    halign='right',
                    color=get_color_from_hex('#666666')
                )

                # Value
                value_widget = Label(
                    text=str(value),
                    font_size='12sp',
                    size_hint=(0.6, 1),
                    halign='left',
                    text_size=(dp(200), None)
                )

                layout.add_widget(label_widget)
                layout.add_widget(value_widget)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        return scroll

    def create_partes_section(self):
        """Cria seção de partes envolvidas"""
        layout = GridLayout(cols=1, spacing=dp(10), padding=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        partes = self.process_data.get('partes', [])

        for parte in partes[:10]:  # Limitar a 10 partes
            parte_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(80),
                padding=dp(5),
                spacing=dp(2)
            )

            # Tipo da parte
            tipo_label = Label(
                text=f"[b]{parte.get('tipo', 'Parte')}:[/b]",
                markup=True,
                size_hint=(1, 0.3),
                font_size='12sp',
                color=get_color_from_hex('#1976D2')
            )

            # Nome da parte
            nome_label = Label(
                text=parte.get('nome', 'N/A'),
                size_hint=(1, 0.4),
                font_size='11sp',
                text_size=(dp(300), None)
            )

            # Advogados
            advogados = parte.get('advogados', [])
            if advogados:
                adv_text = "Advogados: " + ", ".join(advogados[:3])  # Limitar a 3
                if len(advogados) > 3:
                    adv_text += f" (+{len(advogados) - 3})"

                adv_label = Label(
                    text=adv_text,
                    size_hint=(1, 0.3),
                    font_size='10sp',
                    color=get_color_from_hex('#666666'),
                    text_size=(dp(300), None)
                )
                parte_card.add_widget(adv_label)

            parte_card.add_widget(tipo_label)
            parte_card.add_widget(nome_label)

            # Estilo do card
            with parte_card.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                Rectangle(pos=parte_card.pos, size=parte_card.size)
                Color(0.8, 0.8, 0.8, 1)
                Line(rectangle=(parte_card.x, parte_card.y, parte_card.width, parte_card.height), width=0.5)

            layout.add_widget(parte_card)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        return scroll

    def create_movimentacoes_section(self):
        """Cria seção de movimentações"""
        layout = GridLayout(cols=1, spacing=dp(5), padding=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        movimentacoes = self.process_data.get('movimentacoes', [])[:20]  # Limitar a 20

        for mov in movimentacoes:
            mov_card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=dp(70),
                padding=dp(5),
                spacing=dp(2)
            )

            # Data e descrição
            data_label = Label(
                text=f"[b]{self.format_date(mov.get('data'))}[/b]",
                markup=True,
                size_hint=(1, 0.3),
                font_size='11sp',
                color=get_color_from_hex('#1976D2')
            )

            desc_label = Label(
                text=mov.get('descricao', ''),
                size_hint=(1, 0.5),
                font_size='10sp',
                text_size=(dp(350), None)
            )

            # Complemento (se houver)
            if mov.get('complemento'):
                comp_label = Label(
                    text=f"📌 {mov['complemento'][:100]}",
                    size_hint=(1, 0.2),
                    font_size='9sp',
                    color=get_color_from_hex('#666666'),
                    text_size=(dp(350), None)
                )
                mov_card.add_widget(comp_label)

            mov_card.add_widget(data_label)
            mov_card.add_widget(desc_label)

            # Estilo alternado
            with mov_card.canvas.before:
                if len(movimentacoes) % 2 == 0:
                    Color(0.98, 0.98, 0.98, 1)
                else:
                    Color(0.95, 0.95, 0.95, 1)
                Rectangle(pos=mov_card.pos, size=mov_card.size)

            layout.add_widget(mov_card)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        return scroll

    def create_status_section(self):
        """Cria seção de status analisado"""
        layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))

        status_info = self.process_data.get('status_analisado', {})

        # Status principal
        status_color = self.get_status_color(status_info.get('status', 'desconhecido'))

        status_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        status_label = Label(
            text=f"Status: [b]{status_info.get('status', 'Desconhecido').upper()}[/b]",
            markup=True,
            font_size='16sp',
            color=status_color
        )
        prob_label = Label(
            text=f"Confiança: {status_info.get('probabilidade', 0)}%",
            font_size='12sp',
            color=get_color_from_hex('#666666')
        )
        status_box.add_widget(status_label)
        status_box.add_widget(prob_label)

        layout.add_widget(status_box)

        # Última movimentação
        if status_info.get('ultima_movimentacao'):
            ultima_mov = status_info['ultima_movimentacao']
            mov_box = BoxLayout(orientation='vertical', size_hint=(1, 0.3))

            mov_box.add_widget(Label(
                text="[b]Última Movimentação:[/b]",
                markup=True,
                font_size='14sp',
                size_hint=(1, 0.3)
            ))

            mov_box.add_widget(Label(
                text=f"Data: {self.format_date(ultima_mov.get('data'))}",
                font_size='12sp',
                size_hint=(1, 0.2)
            ))

            mov_box.add_widget(Label(
                text=f"Descrição: {ultima_mov.get('descricao', '')}",
                font_size='11sp',
                size_hint=(1, 0.5),
                text_size=(dp(400), None)
            ))

            layout.add_widget(mov_box)

        # Tempo de andamento
        if status_info.get('tempo_andamento'):
            tempo_box = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
            tempo_box.add_widget(Label(
                text=f"Tempo desde última movimentação: {status_info['tempo_andamento']}",
                font_size='12sp'
            ))
            layout.add_widget(tempo_box)

        # Indicadores
        if status_info.get('indicadores'):
            indicadores_box = BoxLayout(orientation='vertical', size_hint=(1, 0.35))
            indicadores_box.add_widget(Label(
                text="[b]Indicadores:[/b]",
                markup=True,
                font_size='14sp',
                size_hint=(1, 0.3)
            ))

            indic_grid = GridLayout(cols=2, size_hint=(1, 0.7))
            for indicador in status_info['indicadores']:
                indic_label = Label(
                    text=f"• {self.translate_indicator(indicador)}",
                    font_size='11sp',
                    color=get_color_from_hex('#666666')
                )
                indic_grid.add_widget(indic_label)

            indicadores_box.add_widget(indic_grid)
            layout.add_widget(indicadores_box)

        return layout

    def create_info_complementar_section(self):
        """Cria seção de informações complementares"""
        layout = GridLayout(cols=2, spacing=dp(5), padding=dp(10), size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        infos = self.process_data.get('informacoes_complementares', {})

        for key, value in list(infos.items())[:20]:  # Limitar a 20 itens
            if value and len(str(value)) < 100:  # Ignorar valores muito longos
                # Label
                label_widget = Label(
                    text=f"{key}:",
                    font_size='11sp',
                    bold=True,
                    size_hint=(0.4, 1),
                    halign='right',
                    color=get_color_from_hex('#666666')
                )

                # Value
                value_widget = Label(
                    text=str(value),
                    font_size='11sp',
                    size_hint=(0.6, 1),
                    halign='left',
                    text_size=(dp(200), None)
                )

                layout.add_widget(label_widget)
                layout.add_widget(value_widget)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        return scroll

    def format_date(self, date_value):
        """Formata data para exibição"""
        if not date_value:
            return "N/A"

        if isinstance(date_value, datetime):
            return date_value.strftime('%d/%m/%Y')

        if isinstance(date_value, str):
            # Tentar parsear a string
            try:
                dt = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
                return dt.strftime('%d/%m/%Y')
            except:
                return date_value

        return str(date_value)

    def get_status_color(self, status):
        """Retorna cor baseada no status"""
        colors = {
            'julgado': get_color_from_hex('#4CAF50'),  # Verde
            'arquivado': get_color_from_hex('#9E9E9E'),  # Cinza
            'em_andamento': get_color_from_hex('#2196F3'),  # Azul
            'em_tramite': get_color_from_hex('#FF9800'),  # Laranja
            'desconhecido': get_color_from_hex('#F44336')  # Vermelho
        }
        return colors.get(status.lower(), get_color_from_hex('#666666'))

    def translate_indicator(self, indicator):
        """Traduz indicadores para português"""
        translations = {
            'processo_antigo': 'Processo antigo (>1 ano)',
            'pouco_movimento': 'Pouco movimento (6+ meses)',
            'recente': 'Movimentação recente (<30 dias)',
            'decisao_proferida': 'Decisão/julgamento proferido',
            'processo_finalizado': 'Processo finalizado/arquivado',
            'atuacao_judicial': 'Atuação judicial em andamento',
            'movimentacao_partes': 'Movimentação das partes'
        }
        return translations.get(indicator, indicator)