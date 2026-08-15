"""Règle n°5 du contrat : journaux structurés en JSON sur stdout, jamais
dans un fichier. Un conteneur ne conserve rien ; c'est l'hôte qui collecte.
"""
from __future__ import annotations

import json
import logging
import sys
import time

logger = logging.getLogger("escale")


class FormatJSON(logging.Formatter):
    def __init__(self, service: str):
        super().__init__()
        self.service = service

    def format(self, record: logging.LogRecord) -> str:
        charge = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(record.created)),
            "niveau": record.levelname,
            "service": self.service,
            "message": record.getMessage(),
        }
        for cle, valeur in getattr(record, "extra_champs", {}).items():
            charge[cle] = valeur
        if record.exc_info:
            charge["exception"] = self.formatException(record.exc_info)
        return json.dumps(charge, ensure_ascii=False)


def configurer_logs(service: str, niveau: str = "INFO", json_actif: bool = True) -> logging.Logger:
    logger.handlers.clear()
    sortie = logging.StreamHandler(sys.stdout)   # stdout, jamais un fichier
    if json_actif:
        sortie.setFormatter(FormatJSON(service))
    else:
        sortie.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-7s %(message)s"))
    logger.addHandler(sortie)
    logger.setLevel(niveau)
    logger.propagate = False
    return logger


def journal(message: str, niveau: str = "info", **champs):
    fn = getattr(logger, niveau)
    fn(message, extra={"extra_champs": champs})
