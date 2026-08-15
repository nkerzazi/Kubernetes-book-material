"""Socle commun à tous les services Escale.

Ce paquet implémente le *contrat de conteneur* décrit dans CONTRAT.md.
Aucun service ne réimplémente ces règles : il les importe.
"""

from .config import Config, get_config
from .logs import configurer_logs, logger
from .sante import Sante, monter_endpoints
from .arret import ArretPropre
from .chaos import Chaos

__all__ = [
    "Config", "get_config",
    "configurer_logs", "logger",
    "Sante", "monter_endpoints",
    "ArretPropre",
    "Chaos",
]

__version__ = "0.1.0"
