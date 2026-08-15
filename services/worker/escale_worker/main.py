"""escale-worker — consomme les positions et les ecrit en base.

Pourquoi ce service existe : sans lui, le simulateur ecrit directement dans
l'API, et l'application n'a aucune raison pedagogique d'avoir une file. Avec
lui, la montee en charge de l'ecriture devient independante de celle de la
lecture — c'est ce qui rendra l'autoscaling du chapitre 9 observable et
justifiera la profondeur de file comme metrique.

    REDIS_URL=redis://redis:6379 DATABASE_URL=postgresql://... python -m escale_worker.main
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time

import redis
from escale_common import ArretPropre, Chaos, configurer_logs, get_config
from escale_common.logs import journal
from prometheus_client import Counter, Gauge, start_http_server

FILE = os.environ.get("QUEUE_NAME", "escale:positions")

TRAITEES = Counter("escale_positions_traitees_total", "Positions ecrites en base")
ECHECS = Counter("escale_positions_echecs_total", "Positions perdues ou rejetees")
PROFONDEUR = Gauge("escale_file_profondeur", "Positions en attente dans la file")


def publier_profondeur(client: redis.Redis, arret: ArretPropre) -> None:
    """La profondeur de file est LA metrique d'autoscaling du chapitre 9.
    Elle doit donc etre exposee des maintenant, meme si personne ne la lit."""
    while not arret.en_cours:
        try:
            PROFONDEUR.set(client.llen(FILE))
        except Exception:  # noqa: BLE001
            pass
        time.sleep(2)


def main() -> int:
    config = get_config("escale-worker")
    configurer_logs(config.service, config.log_level, config.en_json)
    chaos = Chaos(config.chaos)
    arret = ArretPropre(config.delai_arret_s).installer()

    if not config.redis_url or not config.database_url:
        journal("REDIS_URL et DATABASE_URL sont requis", niveau="error")
        return 2

    from escale_api.store_pg import DepotPostgres      # meme couche que l'API

    depot = DepotPostgres(config.database_url)
    depot.initialiser()
    client = redis.Redis.from_url(config.redis_url, decode_responses=True)

    start_http_server(config.port)                     # /metrics du worker
    threading.Thread(target=publier_profondeur, args=(client, arret), daemon=True).start()
    journal("worker pret", file=FILE, port=config.port)

    traitees = 0
    while not arret.en_cours:
        try:
            element = client.blpop(FILE, timeout=1)    # bloquant : pas d'attente active
        except Exception as exc:                       # noqa: BLE001
            journal("file injoignable", niveau="warning", erreur=str(exc))
            time.sleep(1)
            continue
        if element is None:
            continue

        chaos.avant_requete()
        try:
            depot.enregistrer_position(json.loads(element[1]))
            TRAITEES.inc()
            traitees += 1
        except Exception as exc:                       # noqa: BLE001
            ECHECS.inc()
            journal("position rejetee", niveau="warning", erreur=str(exc))

        if traitees % 200 == 0:
            journal("avancement", traitees=traitees, profondeur=client.llen(FILE))

    # Arret propre : on vide ce qui reste avant de rendre la main.
    journal("arret demande, drainage de la file", restant=client.llen(FILE))
    depot.fermer()
    journal("worker arrete", traitees=traitees)
    return 0


if __name__ == "__main__":
    sys.exit(main())
