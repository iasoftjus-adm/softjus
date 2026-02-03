import requests
import json
import threading
from kivy.clock import Clock

from .config import API_KEY, TRIBUNAL_URLS


class APIClient:
    def __init__(self):
        self.api_key = API_KEY

    def get_tribunal_url(self, tribunal_name):
        """Get API URL for a specific tribunal"""
        for tribunal_type, tribunals in TRIBUNAL_URLS.items():
            if tribunal_name in tribunals:
                return tribunals[tribunal_name]
        # Default to TRF1 if not found
        return "https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search"

    def search_process(self, process_number, callback, tribunal_name=None):
        """Search for a process by number in specific tribunal"""

        def perform_search():
            try:
                # Get URL for the selected tribunal
                api_url = self.get_tribunal_url(tribunal_name) if tribunal_name else self.get_tribunal_url(
                    "Tribunal Regional Federal da 1ª Região")

                headers = {
                    'Authorization': f'ApiKey {self.api_key}',
                    'Content-Type': 'application/json'
                }

                payload = json.dumps({
                    "query": {
                        "match": {
                            "numeroProcesso": process_number
                        }
                    }
                })

                response = requests.post(
                    api_url,
                    headers=headers,
                    data=payload,
                    timeout=30
                )

                Clock.schedule_once(lambda dt: callback(response, None))

            except Exception as e:
                Clock.schedule_once(lambda dt: callback(None, str(e)))

        threading.Thread(target=perform_search, daemon=True).start()

    def search_by_criteria(self, criteria, callback, tribunal_name=None):
        """Search processes by various criteria in specific tribunal"""

        def perform_search():
            try:
                # Get URL for the selected tribunal
                api_url = self.get_tribunal_url(tribunal_name) if tribunal_name else self.get_tribunal_url(
                    "Tribunal Regional Federal da 1ª Região")

                headers = {
                    'Authorization': f'ApiKey {self.api_key}',
                    'Content-Type': 'application/json'
                }

                payload = json.dumps({
                    "query": {
                        "multi_match": {
                            "query": criteria,
                            "fields": ["numeroProcesso", "classe.nome", "orgaoJulgador.nome"]
                        }
                    }
                })

                response = requests.post(
                    api_url,
                    headers=headers,
                    data=payload,
                    timeout=30
                )

                Clock.schedule_once(lambda dt: callback(response, None))

            except Exception as e:
                Clock.schedule_once(lambda dt: callback(None, str(e)))

        threading.Thread(target=perform_search, daemon=True).start()