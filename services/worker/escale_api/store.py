"""Stockage des navires et des positions.

Deux implémentations volontairement interchangeables :

  DepotMemoire   chapitres 1 et 2 — tout disparaît avec le conteneur
  DepotPostgres  chapitre 3 et suivants — activé dès que DATABASE_URL existe

Le fait que le *même* code applicatif fonctionne dans les deux cas est ce qui
permet au chapitre 3 de porter sur la persistance, et non sur du refactoring.
"""
from __future__ import annotations

import math
import threading
import time

QUAIS = ["A1", "A2", "B1", "B2", "C1"]

# Flotte de départ : aucune source externe, tout est embarqué.
FLOTTE = [
    {"imo": "9321483", "nom": "Marguerite", "type": "porte-conteneurs", "destination": "Fos-sur-Mer"},
    {"imo": "9403967", "nom": "Sirocco", "type": "vraquier", "destination": "Marseille"},
    {"imo": "9511234", "nom": "Aïcha", "type": "pétrolier", "destination": "Fos-sur-Mer"},
    {"imo": "9600021", "nom": "Zéphyr", "type": "roulier", "destination": "Sète"},
    {"imo": "9712045", "nom": "Corail", "type": "porte-conteneurs", "destination": "Marseille"},
]

PORTS = {
    "Marseille": (43.30, 5.36),
    "Fos-sur-Mer": (43.44, 4.94),
    "Sète": (43.40, 3.70),
}


def distance_nm(a: tuple[float, float], b: tuple[float, float]) -> float:
    """Distance orthodromique approchée, en milles nautiques."""
    r = 3440.065
    lat1, lon1, lat2, lon2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


class Depot:
    nom = "abstrait"

    def initialiser(self) -> None: ...
    def fermer(self) -> None: ...
    def disponible(self) -> bool: return True
    def lister_navires(self) -> list[dict]: raise NotImplementedError
    def obtenir_navire(self, imo: str) -> dict | None: raise NotImplementedError
    def enregistrer_position(self, position: dict) -> None: raise NotImplementedError
    def lister_escales(self) -> list[dict]: raise NotImplementedError

    def _eta(self, navire: dict) -> dict:
        port = PORTS.get(navire.get("destination"))
        pos = navire.get("position")
        if not port or not pos:
            return {"eta_minutes": None, "distance_nm": None}
        d = distance_nm((pos["latitude"], pos["longitude"]), port)
        vitesse = max(navire.get("vitesse_noeuds", 12.0), 0.1)
        return {"eta_minutes": round(d / vitesse * 60, 1), "distance_nm": round(d, 1)}


class DepotMemoire(Depot):
    nom = "memoire"

    def __init__(self):
        self._verrou = threading.Lock()
        self._navires: dict[str, dict] = {}

    def initialiser(self) -> None:
        with self._verrou:
            for n in FLOTTE:
                self._navires[n["imo"]] = dict(n, position=None, vitesse_noeuds=12.0, maj=None)

    def lister_navires(self) -> list[dict]:
        with self._verrou:
            return [dict(n, **self._eta(n)) for n in self._navires.values()]

    def obtenir_navire(self, imo: str) -> dict | None:
        with self._verrou:
            n = self._navires.get(imo)
            return dict(n, **self._eta(n)) if n else None

    def enregistrer_position(self, position: dict) -> None:
        with self._verrou:
            navire = self._navires.setdefault(
                position["imo"],
                {"imo": position["imo"], "nom": position.get("nom", "inconnu"),
                 "type": "inconnu", "destination": position.get("destination", "Marseille")},
            )
            navire["position"] = {"latitude": position["latitude"], "longitude": position["longitude"]}
            navire["vitesse_noeuds"] = position.get("vitesse_noeuds", 12.0)
            navire["maj"] = time.time()

    def lister_escales(self) -> list[dict]:
        escales = []
        for i, navire in enumerate(self.lister_navires()):
            if navire.get("eta_minutes") is None:
                continue
            escales.append({
                "imo": navire["imo"], "nom": navire["nom"],
                "port": navire["destination"], "quai": QUAIS[i % len(QUAIS)],
                "eta_minutes": navire["eta_minutes"],
            })
        return sorted(escales, key=lambda e: e["eta_minutes"])


def creer_depot(database_url: str | None) -> Depot:
    """Bascule mémoire / PostgreSQL selon l'environnement.

    L'import de psycopg est volontairement paresseux : aux chapitres 1 et 2,
    le pilote n'est pas installé et n'a aucune raison de l'être.
    """
    if not database_url:
        return DepotMemoire()
    from .store_pg import DepotPostgres
    return DepotPostgres(database_url)
