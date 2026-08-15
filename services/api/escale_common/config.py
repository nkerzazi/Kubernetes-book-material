"""Règle n°1 et n°2 du contrat : le port est configurable, la configuration
vient entièrement de l'environnement. Aucune valeur en dur ailleurs.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from functools import lru_cache


def _bool(nom: str, defaut: bool = False) -> bool:
    return os.environ.get(nom, str(defaut)).strip().lower() in ("1", "true", "yes", "oui")


def _int(nom: str, defaut: int) -> int:
    try:
        return int(os.environ.get(nom, defaut))
    except ValueError:
        return defaut


def _float(nom: str, defaut: float) -> float:
    try:
        return float(os.environ.get(nom, defaut))
    except ValueError:
        return defaut


@dataclass(frozen=True)
class Config:
    service: str
    port: int
    log_level: str
    log_format: str            # json | texte
    delai_arret_s: float       # drainage des connexions sur SIGTERM
    demarrage_lent_s: float    # simule un chargement long (escale-eta)
    database_url: str | None
    redis_url: str | None
    api_url: str
    chaos: dict = field(default_factory=dict)

    @property
    def en_json(self) -> bool:
        return self.log_format == "json"


@lru_cache(maxsize=None)
def get_config(service: str = "escale") -> Config:
    return Config(
        service=os.environ.get("SERVICE_NAME", service),
        port=_int("PORT", 8000),
        log_level=os.environ.get("LOG_LEVEL", "INFO").upper(),
        log_format=os.environ.get("LOG_FORMAT", "json").lower(),
        delai_arret_s=_float("GRACEFUL_TIMEOUT_S", 10.0),
        demarrage_lent_s=_float("STARTUP_DELAY_S", 0.0),
        database_url=os.environ.get("DATABASE_URL"),
        redis_url=os.environ.get("REDIS_URL"),
        api_url=os.environ.get("API_URL", "http://localhost:8000"),
        chaos={
            # fuite mémoire progressive, en Mo par minute
            "memoire_mo_min": _float("CHAOS_MEMORY_LEAK_MB_PER_MIN", 0.0),
            # latence artificielle ajoutée à chaque requête, en millisecondes
            "latence_ms": _float("CHAOS_LATENCY_MS", 0.0),
            # /readyz échoue au bout de N secondes (0 = jamais)
            "readyz_echoue_apres_s": _float("CHAOS_READYZ_FAIL_AFTER_S", 0.0),
            # probabilité de plantage du processus à chaque requête
            "plantage_proba": _float("CHAOS_CRASH_PROBABILITY", 0.0),
            # taux d'erreurs 500 renvoyées
            "erreurs_proba": _float("CHAOS_ERROR_RATE", 0.0),
        },
    )
