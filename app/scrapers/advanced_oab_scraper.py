"""
AdvancedOABScraper corrigido - sem métodos faltando
"""
import requests
from bs4 import BeautifulSoup
import re
import json
import logging
from datetime import datetime
from typing import List, Dict, Optional
import time
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class AdvancedOABScraper:
    """Scraper avançado corrigido para consulta por OAB"""

    def __init__(self, max_retries=3, delay_between_requests=1):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9',
        })
        self.max_retries = max_retries
        self.delay = delay_between_requests

    def consultar_oab_detalhado(self, oab_numero: str, oab_uf: str = "SP",
                                coletar_detalhes: bool = False) -> Dict:
        """
        Consulta OAB - versão simplificada
        """
        try:
            # Normalizar entrada
            oab_limpo = re.sub(r'\D', '', oab_numero)
            uf_limpo = oab_uf.upper()[:2]

            print(f"Consultando OAB {oab_limpo}/{uf_limpo}...")

            # Consultar TJSP apenas (para começar)
            processos = self._consultar_tjsp_simplificado(oab_limpo, uf_limpo)

            # Retornar resultados
            return {
                'numero_oab': f"{oab_limpo}/{uf_limpo}",
                'processos_encontrados': processos,
                'estatisticas': {
                    'total_processos': len(processos),
                    'tempo_consulta': 0,
                    'tribunais_consultados': ['TJSP'] if processos else []
                },
                'fonte': 'TJSP Scraping',
                'data_consulta': datetime.now().isoformat(),
                'versao_scraper': '1.0.0-corrigido'
            }

        except Exception as e:
            logger.error(f"Erro na consulta OAB: {e}")
            return {
                'numero_oab': f"{oab_numero}/{oab_uf}",
                'processos_encontrados': [],
                'erro': str(e),
                'data_consulta': datetime.now().isoformat()
            }

    def _consultar_tjsp_simplificado(self, oab_numero: str, oab_uf: str) -> List[Dict]:
        """Consulta simplificada no TJSP"""
        try:
            url = "https://esaj.tjsp.jus.br/cpopg/search.do"

            # Códigos de foro do TJSP
            foro_codes = {
                'SP': '0', 'AC': '1', 'AL': '2', 'AM': '3', 'AP': '4',
                'BA': '5', 'CE': '6', 'DF': '7', 'ES': '8', 'GO': '9',
                'MA': '10', 'MG': '11', 'MS': '12', 'MT': '13', 'PA': '14',
                'PB': '15', 'PE': '16', 'PI': '17', 'PR': '18', 'RJ': '19',
                'RN': '20', 'RO': '21', 'RR': '22', 'RS': '23', 'SC': '24',
                'SE': '25', 'TO': '26'
            }

            foro_code = foro_codes.get(oab_uf, '0')

            # Parâmetros da busca
            params = {
                'conversationId': '',
                'cbPesquisa': 'NUMOAB',
                'dadosConsulta.valorConsulta': oab_numero,
                'cdForo': '-1',
                'dadosConsulta.localPesquisa.cdLocal': foro_code
            }

            print(f"Fazendo requisição para TJSP com parâmetros: {params}")

            # Fazer requisição
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()

            # Parsear resultados
            return self._parse_tjsp_response_simplificada(response.text)

        except Exception as e:
            print(f"Erro ao consultar TJSP: {e}")
            return []

    def _parse_tjsp_response_simplificada(self, html: str) -> List[Dict]:
        """Parseia resposta do TJSP de forma simplificada"""
        processos = []

        try:
            # Método 1: Buscar por padrão de número de processo
            padrao = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
            numeros_processo = re.findall(padrao, html)

            for num in set(numeros_processo):  # Remover duplicatas
                processo = {
                    'numero_processo': num,
                    'tribunal': 'TJSP',
                    'tribunal_codigo': 'TJSP',
                    'fonte': 'TJSP Scraping',
                    'confiabilidade': 80,
                    'data_coleta': datetime.now().isoformat(),
                    'detalhes_completos': False,
                    'status_analisado': {
                        'status': 'em_andamento',
                        'probabilidade': 70,
                        'indicadores': ['processo_encontrado']
                    }
                }

                # Tentar extrair mais informações com BeautifulSoup
                try:
                    soup = BeautifulSoup(html, 'html.parser')

                    # Procurar por informações próximas ao número do processo
                    texto_processo = self._encontrar_texto_processo(soup, num)

                    if texto_processo:
                        # Extrair classe se possível
                        classe_match = re.search(r'Classe[:\s]+([^\n<]+)', texto_processo, re.IGNORECASE)
                        if classe_match:
                            processo['classe'] = classe_match.group(1).strip()

                        # Extrair assunto se possível
                        assunto_match = re.search(r'Assunto[:\s]+([^\n<]+)', texto_processo, re.IGNORECASE)
                        if assunto_match:
                            processo['assunto'] = assunto_match.group(1).strip()

                        # Extrair foro se possível
                        foro_match = re.search(r'Foro[:\s]+([^\n<]+)', texto_processo, re.IGNORECASE)
                        if foro_match:
                            processo['foro'] = foro_match.group(1).strip()

                        processo['confiabilidade'] = 85  # Aumentar confiabilidade se encontrou mais info

                except Exception as e:
                    print(f"Erro ao parsear detalhes do processo {num}: {e}")

                processos.append(processo)

            # Se não encontrou com regex, tentar método alternativo
            if not processos:
                processos = self._buscar_processos_alternativo(html)

        except Exception as e:
            print(f"Erro ao parsear resposta TJSP: {e}")

        return processos

    def _encontrar_texto_processo(self, soup, numero_processo):
        """Encontra o texto relacionado a um processo específico"""
        try:
            # Procurar por tabelas
            tabelas = soup.find_all('table')

            for tabela in tabelas:
                texto_tabela = tabela.get_text()
                if numero_processo in texto_tabela:
                    # Encontrar a linha específica
                    linhas = tabela.find_all('tr')
                    for linha in linhas:
                        if numero_processo in linha.get_text():
                            return linha.get_text()

            # Procurar por divs
            divs = soup.find_all('div')
            for div in divs:
                if numero_processo in div.get_text():
                    return div.get_text()

        except Exception as e:
            print(f"Erro ao buscar texto do processo: {e}")

        return None

    def _buscar_processos_alternativo(self, html):
        """Método alternativo para buscar processos"""
        processos = []

        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Procurar por links que possam ser de processos
            links = soup.find_all('a', href=True)

            for link in links:
                href = link.get('href', '')
                texto = link.get_text(strip=True)

                # Verificar se é link de processo do TJSP
                if ('processo.codigo' in href or 'consultarProcesso' in href) and texto:
                    # Tentar extrair número do processo
                    padrao = r'\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}'
                    match = re.search(padrao, texto)

                    if match:
                        processos.append({
                            'numero_processo': match.group(),
                            'tribunal': 'TJSP',
                            'tribunal_codigo': 'TJSP',
                            'fonte': 'TJSP Link Scraping',
                            'confiabilidade': 75,
                            'data_coleta': datetime.now().isoformat(),
                            'detalhes_completos': False,
                            'url_detalhes': f"https://esaj.tjsp.jus.br{href}" if href.startswith('/') else href
                        })

        except Exception as e:
            print(f"Erro no método alternativo: {e}")

        return processos

    def _make_request(self, url: str, method: str = 'GET',
                      params: Dict = None, data: Dict = None) -> Optional[requests.Response]:
        """Faz requisição HTTP com retry"""
        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, params=params, timeout=30)
                else:
                    response = self.session.post(url, data=data, timeout=30)

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                print(f"Tentativa {attempt + 1} falhou para {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.delay * (attempt + 1))

        print(f"Todas as tentativas falharam para {url}")
        return None