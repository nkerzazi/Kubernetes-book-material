"""Règles n°3 et n°4 du contrat : /healthz et /readyz DISTINCTS, /metrics.

    /healthz  le processus est-il vivant ?        -> liveness probe
    /readyz   est-il prêt à recevoir du trafic ?  -> readiness probe

Confondre les deux est l'erreur qui coûte le plus cher au chapitre 9 : une
liveness probe qui interroge la base de données redémarre le service à chaque
incident de base, et transforme une panne partielle en panne totale.
"""
from __future__ import annotations

import time
from typing import Callable

from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

REQUETES = Counter(
    "escale_requetes_total", "Requêtes HTTP traitées", ["service", "methode", "route", "code"]
)
LATENCE = Histogram(
    "escale_latence_secondes", "Latence des requêtes HTTP", ["service", "route"]
)
PRET = Gauge("escale_pret", "1 si le service accepte du trafic", ["service"])
DEMARRAGE = Gauge("escale_demarrage_secondes", "Durée du démarrage", ["service"])


class Sante:
    """État de santé du service.

    `vivant` reste vrai tant que le processus fonctionne.
    `pret` dépend des dépendances et bascule à faux dès la demande d'arrêt.
    """

    def __init__(self, service: str):
        self.service = service
        self.vivant = True
        self._pret = False
        self._sondes: list[tuple[str, Callable[[], bool]]] = []
        self._debut = time.monotonic()
        PRET.labels(service).set(0)

    def ajouter_sonde(self, nom: str, sonde: Callable[[], bool]) -> None:
        """Une dépendance dont dépend la *readiness* : base, file, modèle…"""
        self._sondes.append((nom, sonde))

    def marquer_pret(self) -> None:
        self._pret = True
        PRET.labels(self.service).set(1)
        DEMARRAGE.labels(self.service).set(time.monotonic() - self._debut)

    def marquer_non_pret(self) -> None:
        self._pret = False
        PRET.labels(self.service).set(0)

    def details(self) -> dict:
        etat = {nom: bool(sonde()) for nom, sonde in self._sondes}
        return {"pret": self._pret and all(etat.values()), "dependances": etat}


def monter_endpoints(app: FastAPI, sante: Sante, chaos=None) -> None:
    """Monte /healthz, /readyz et /metrics sur l'application."""

    @app.get("/healthz", include_in_schema=False)
    def healthz():
        # Volontairement minimal : aucune dépendance externe interrogée ici.
        return {"statut": "ok" if sante.vivant else "ko"}

    @app.get("/readyz", include_in_schema=False)
    def readyz(reponse: Response):
        detail = sante.details()
        if chaos is not None and chaos.readyz_ko():
            detail["pret"] = False
            detail["chaos"] = "readyz_fail_after"
        if not detail["pret"]:
            reponse.status_code = 503
        return detail

    @app.get("/metrics", include_in_schema=False)
    def metrics():
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
