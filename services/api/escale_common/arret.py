"""Règle n°6 du contrat : arrêt propre sur SIGTERM.

Le service cesse d'accepter du trafic (/readyz bascule en échec), laisse aux
équilibreurs le temps de le retirer de la rotation, termine les requêtes en
cours, puis s'arrête. Sans cela, chaque mise à jour perd des requêtes.
"""
from __future__ import annotations

import signal
import threading
import time
from typing import Callable


class ArretPropre:
    def __init__(self, delai_s: float = 10.0, au_signal: Callable[[], None] | None = None):
        self.delai_s = delai_s
        self.demande = threading.Event()
        self._au_signal = au_signal
        self._instant: float | None = None

    def installer(self) -> "ArretPropre":
        for sig in (signal.SIGTERM, signal.SIGINT):
            signal.signal(sig, self._recevoir)
        return self

    def _recevoir(self, signum, frame):  # noqa: ARG002
        if self.demande.is_set():
            return
        self.demande.set()
        self._instant = time.monotonic()
        if self._au_signal:
            self._au_signal()

    @property
    def en_cours(self) -> bool:
        return self.demande.is_set()

    def attendre(self) -> None:
        self.demande.wait()
        time.sleep(self.delai_s)
