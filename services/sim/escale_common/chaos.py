"""Défauts injectables. Pilotés par les variables CHAOS_*.

Ils rendent les incidents *reproductibles à l'identique* pour tous les
étudiants : c'est ce qui rend la notation équitable et le corrigé possible.
Aucun effet si les variables ne sont pas définies.
"""
from __future__ import annotations

import os
import random
import time
from threading import Thread


class Chaos:
    def __init__(self, config: dict):
        self.config = config
        self._fuite: list[bytes] = []
        self._depart = time.monotonic()
        self._actif = any(v for v in config.values())
        if config.get("memoire_mo_min", 0) > 0:
            Thread(target=self._fuir, daemon=True).start()

    @property
    def actif(self) -> bool:
        return self._actif

    def _fuir(self) -> None:
        mo_min = self.config["memoire_mo_min"]
        while True:
            time.sleep(6)
            self._fuite.append(b"\0" * int(mo_min * 1024 * 1024 / 10))

    def avant_requete(self) -> None:
        """À appeler au début de chaque requête."""
        latence = self.config.get("latence_ms", 0)
        if latence > 0:
            time.sleep(latence / 1000.0)
        proba = self.config.get("plantage_proba", 0)
        if proba > 0 and random.random() < proba:
            os._exit(1)          # plantage brutal, volontairement non rattrapable

    def doit_echouer(self) -> bool:
        proba = self.config.get("erreurs_proba", 0)
        return proba > 0 and random.random() < proba

    def readyz_ko(self) -> bool:
        seuil = self.config.get("readyz_echoue_apres_s", 0)
        return seuil > 0 and (time.monotonic() - self._depart) > seuil
