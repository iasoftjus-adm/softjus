# app/scrapers/config.py
"""
Configurações do sistema de scraping
"""

# Timeouts e limites
SCRAPER_CONFIG = {
    'request_timeout': 30,
    'max_retries': 3,
    'delay_between_requests': 1.5,
    'max_concurrent_requests': 5,
    'cache_duration_hours': 24,
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    ]
}

# Mapeamento de tribunais suportados
SUPPORTED_TRIBUNALS = {
    'TJSP': {
        'name': 'Tribunal de Justiça de São Paulo',
        'scraper_class': 'TJSPScraper',
        'enabled': True,
        'priority': 1
    },
    'TJRJ': {
        'name': 'Tribunal de Justiça do Rio de Janeiro',
        'scraper_class': 'TJRJScraper',
        'enabled': False,  # Em desenvolvimento
        'priority': 2
    },
    'TJMG': {
        'name': 'Tribunal de Justiça de Minas Gerais',
        'scraper_class': 'TJMGScraper',
        'enabled': False,
        'priority': 3
    }
}

# Status mapping para exibição
STATUS_MAPPING = {
    'julgado': {
        'label': 'Julgado',
        'color': '#4CAF50',
        'icon': '✅'
    },
    'arquivado': {
        'label': 'Arquivado',
        'color': '#9E9E9E',
        'icon': '📁'
    },
    'em_andamento': {
        'label': 'Em Andamento',
        'color': '#2196F3',
        'icon': '⚖️'
    },
    'em_tramite': {
        'label': 'Em Trâmite',
        'color': '#FF9800',
        'icon': '📄'
    },
    'desconhecido': {
        'label': 'Status Desconhecido',
        'color': '#F44336',
        'icon': '❓'
    }
}