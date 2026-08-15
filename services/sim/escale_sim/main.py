"""escale-sim — générateur de trafic maritime.

Aucune source de données externe : les navires sont simulés localement.
C'est la pièce que les manuels omettent, et sans laquelle l'étudiant configure
un autoscaler qui ne se déclenche jamais et une alerte qui ne sonne jamais.

    NAVIRES=25 CADENCE_S=1 API_URL=http://api:8000 python -m escale_sim.main
"""
from __future__ import annotations

import math
import os
import random
import time

import httpx
from escale_common import ArretPropre, configurer_logs, get_config
from escale_common.logs import journal

# Deux modes d'emission, selon le chapitre :
#   http   -> POST direct vers escale-api          (chapitres 1 a 3)
#   redis  -> depot dans la file, lue par le worker (chapitre 4 et suivants)
MODE = os.environ.get("SIM_MODE", "http").lower()
FILE = os.environ.get("QUEUE_NAME", "escale:positions")

PORTS = {"Marseille": (43.30, 5.36), "Fos-sur-Mer": (43.44, 4.94), "Sete": (43.40, 3.70)}
TYPES = ["porte-conteneurs", "vraquier", "petrolier", "roulier", "methanier"]
PREFIXES = ["Mistral", "Sirocco", "Zephyr", "Corail", "Aurore", "Levant", "Ponant", "Alize"]


class Navire:
    def __init__(self, index: int, graine: random.Random):
        self.index = index
        self.imo = f"9{700000 + index:06d}"
        self.nom = f"{graine.choice(PREFIXES)} {index + 1}"
        self.type = graine.choice(TYPES)
        self.destination = graine.choice(list(PORTS))
        cible = PORTS[self.destination]
        angle = graine.uniform(0, 2 * math.pi)
        rayon = graine.uniform(0.4, 2.2)
        self.lat = cible[0] + rayon * math.cos(angle)
        self.lon = cible[1] + rayon * math.sin(angle)
        self.vitesse = graine.uniform(8.0, 20.0)

    def avancer(self, pas_s: float) -> None:
        cible = PORTS[self.destination]
        dlat, dlon = cible[0] - self.lat, cible[1] - self.lon
        norme = math.hypot(dlat, dlon) or 1e-9
        avance = self.vitesse / 60.0 * (pas_s / 3600.0) * 60
        if norme < avance:                      # arrive : on repart au large
            self.__init__(self.index, random.Random(self.imo))
            return
        self.lat += dlat / norme * avance
        self.lon += dlon / norme * avance

    def position(self) -> dict:
        return {
            "imo": self.imo, "nom": self.nom, "destination": self.destination,
            "latitude": round(self.lat, 5), "longitude": round(self.lon, 5),
            "vitesse_noeuds": round(self.vitesse, 1),
        }


def main() -> None:
    config = get_config("escale-sim")
    configurer_logs(config.service, config.log_level, config.en_json)
    arret = ArretPropre(config.delai_arret_s).installer()

    nombre = int(os.environ.get("NAVIRES", 12))
    cadence = float(os.environ.get("CADENCE_S", 2.0))
    graine = random.Random(int(os.environ.get("GRAINE", 42)))   # trafic reproductible
    flotte = [Navire(i, graine) for i in range(nombre)]

    cible = config.redis_url if MODE == "redis" else config.api_url
    journal("simulateur demarre", navires=nombre, cadence_s=cadence, mode=MODE, cible=cible)

    if MODE == "redis":
        import json

        import redis
        emetteur = redis.Redis.from_url(config.redis_url, decode_responses=True)

        def envoyer(position: dict) -> None:
            emetteur.rpush(FILE, json.dumps(position))
    else:
        emetteur = httpx.Client(timeout=5.0)

        def envoyer(position: dict) -> None:
            emetteur.post(f"{config.api_url}/positions", json=position)

    envoyes = erreurs = 0
    try:
        while not arret.en_cours:
            debut = time.monotonic()
            for navire in flotte:
                navire.avancer(cadence)
                try:
                    envoyer(navire.position())
                    envoyes += 1
                except Exception as exc:                       # noqa: BLE001
                    erreurs += 1
                    if erreurs % 20 == 1:
                        journal("envoi impossible", niveau="warning", erreur=str(exc))
            if envoyes % (nombre * 10) < nombre:
                journal("trafic", positions_envoyees=envoyes, erreurs=erreurs)
            time.sleep(max(0.0, cadence - (time.monotonic() - debut)))
    finally:
        if MODE != "redis":
            emetteur.close()
    journal("simulateur arrete", positions_envoyees=envoyes, mode=MODE)


if __name__ == "__main__":
    main()
