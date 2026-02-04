"""
Módulo de scrapers para o SoftJus
"""

# Tente importar o scraper avançado
try:
    from .advanced_oab_scraper import AdvancedOABScraper
    __all__ = ['AdvancedOABScraper']
except ImportError:
    # Se não existir, tente o básico
    try:
        from .oab_scraper import OABScraper
        __all__ = ['OABScraper']
    except ImportError:
        __all__ = []