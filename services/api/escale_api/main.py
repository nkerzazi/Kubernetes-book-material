"""escale-api — suivi d'escales portuaires.

Chapitre 2 : stockage en mémoire (les données disparaissent avec le conteneur,
c'est *voulu* et c'est le problème du chapitre 3).
Chapitre 3 : le même code bascule sur PostgreSQL si DATABASE_URL est défini.
"""
from __future__ import annotations

import time
from contextlib import asynccontextmanager

from escale_common import ArretPropre, Chaos, Sante, configurer_logs, get_config, monter_endpoints
from escale_common.logs import journal
from escale_common.sante import LATENCE, REQUETES
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from .store import Depot, creer_depot

config = get_config("escale-api")
configurer_logs(config.service, config.log_level, config.en_json)
chaos = Chaos(config.chaos)
sante = Sante(config.service)
arret = ArretPropre(config.delai_arret_s, au_signal=sante.marquer_non_pret).installer()
depot: Depot | None = None


@asynccontextmanager
async def cycle_de_vie(app: FastAPI):
    global depot
    if config.demarrage_lent_s > 0:
        journal("démarrage lent simulé", secondes=config.demarrage_lent_s)
        time.sleep(config.demarrage_lent_s)
    depot = creer_depot(config.database_url)
    depot.initialiser()
    sante.ajouter_sonde("depot", depot.disponible)
    sante.marquer_pret()
    journal("service prêt", port=config.port, stockage=depot.nom, chaos=chaos.actif)
    yield
    sante.marquer_non_pret()
    journal("arrêt demandé, drainage en cours", delai_s=config.delai_arret_s)
    depot.fermer()


app = FastAPI(title="escale-api", version="0.1.0", lifespan=cycle_de_vie)
monter_endpoints(app, sante, chaos)


@app.middleware("http")
async def instrumenter(request: Request, appeler_suite):
    route = request.url.path
    if route not in ("/metrics",):
        chaos.avant_requete()
    if chaos.doit_echouer() and not route.startswith(("/healthz", "/readyz", "/metrics")):
        REQUETES.labels(config.service, request.method, route, 500).inc()
        return JSONResponse({"detail": "erreur injectée"}, status_code=500)
    debut = time.perf_counter()
    reponse = await appeler_suite(request)
    LATENCE.labels(config.service, route).observe(time.perf_counter() - debut)
    REQUETES.labels(config.service, request.method, route, reponse.status_code).inc()
    return reponse


# ---------------------------------------------------------------- routes


@app.get("/")
def racine():
    return {"service": config.service, "version": app.version, "stockage": depot.nom}


@app.get("/navires")
def lister_navires():
    return {"navires": depot.lister_navires()}


@app.get("/navires/{imo}")
def obtenir_navire(imo: str):
    navire = depot.obtenir_navire(imo)
    if navire is None:
        raise HTTPException(404, f"navire {imo} inconnu")
    return navire


@app.post("/positions", status_code=201)
def enregistrer_position(position: dict):
    for champ in ("imo", "latitude", "longitude"):
        if champ not in position:
            raise HTTPException(422, f"champ obligatoire manquant : {champ}")
    depot.enregistrer_position(position)
    return {"enregistre": True, "imo": position["imo"]}


@app.get("/escales")
def lister_escales():
    """Escales prévues, avec ETA calculée de façon naïve.

    Le calcul sérieux revient à escale-eta, introduit au chapitre 9.
    """
    return {"escales": depot.lister_escales()}
