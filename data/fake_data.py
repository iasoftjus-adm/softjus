# Fake data for testing and simulation
import json
from datetime import datetime, timedelta
from typing import Dict, List
import random
from models import Processo


def generate_fake_process(numero: str = None) -> Processo:
    """Generate fake process data for testing"""
    if not numero:
        # Generate a random Brazilian process number
        numero = f"{random.randint(1000000, 9999999)}-{random.randint(10, 99)}.{random.randint(2010, 2024)}.{random.randint(1, 9)}.{random.randint(10, 99)}.{random.randint(1000, 9999)}"

    classes = [
        {"codigo": 436, "nome": "Procedimento do Juizado Especial Cível"},
        {"codigo": 583, "nome": "Execução Fiscal"},
        {"codigo": 1100, "nome": "Ação Civil Pública"},
        {"codigo": 899, "nome": "Mandado de Segurança"},
        {"codigo": 550, "nome": "Ação de Consignação em Pagamento"}
    ]

    orgaos = [
        {"codigoMunicipioIBGE": 5128, "codigo": 16403, "nome": "Tefé"},
        {"codigoMunicipioIBGE": 5300108, "codigo": 1000, "nome": "Brasília"},
        {"codigoMunicipioIBGE": 3550308, "codigo": 2000, "nome": "São Paulo"},
        {"codigoMunicipioIBGE": 3304557, "codigo": 3000, "nome": "Rio de Janeiro"}
    ]

    movimentos = [
        {"dataHora": (datetime.now() - timedelta(days=1)).isoformat() + "Z", "nome": "Distribuição"},
        {"dataHora": (datetime.now() - timedelta(hours=12)).isoformat() + "Z", "nome": "Ato ordinatório"},
        {"dataHora": datetime.now().isoformat() + "Z", "nome": "Juntada de Petição"}
    ]

    partes = [
        {"tipo": "Autor", "nome": "CONDOMÍNIO RESIDENCIAL VILA NOVA"},
        {"tipo": "Réu", "nome": "MUNICÍPIO DE SÃO PAULO"}
    ]

    return Processo(
        numero=numero,
        classe=random.choice(classes),
        orgao_julgador=random.choice(orgaos),
        data_ajuizamento="20181029000000",
        movimentos=movimentos,
        assunto="CONDOMINIO - COBRANCA DE TAXA DE INCENDIO",
        partes=partes,
        raw_data={}
    )


def get_fake_process(process_number: str) -> List[Processo]:
    """Get fake process data for a specific number"""
    processos = []

    # Return 1-3 fake processes
    for i in range(random.randint(1, 3)):
        processo = generate_fake_process(process_number if i == 0 else None)
        processos.append(processo)

    return processos


def generate_fake_favorites(count: int = 5) -> List[Dict]:
    """Generate fake favorite processes"""
    favorites = []
    for i in range(count):
        processo = generate_fake_process()
        favorites.append({
            'processo': processo.numero,
            'classe': processo.classe.get('nome', ''),
            'data_adicao': (datetime.now() - timedelta(days=i)).isoformat()
        })
    return favorites


# Example data for specific process numbers
SAMPLE_PROCESSOS = {
    "00008323520184013202": {
        "numeroProcesso": "00008323520184013202",
        "classe": {"codigo": 436, "nome": "Procedimento do Juizado Especial Cível"},
        "orgaoJulgador": {"codigoMunicipioIBGE": 5128, "codigo": 16403, "nome": "Tefé"},
        "dataAjuizamento": "20181029000000",
        "movimentos": [
            {"dataHora": "2024-07-03T09:05:34.000Z", "nome": "Ato ordinatório"}
        ],
        "assunto": "CONDOMINIO - COBRANCA DE TAXA DE INCENDIO"
    }
}


def get_sample_process(numero: str) -> List[Processo]:
    """Get sample process data from predefined samples"""
    if numero in SAMPLE_PROCESSOS:
        processo = Processo.from_api_data(SAMPLE_PROCESSOS[numero])
        return [processo]
    return []