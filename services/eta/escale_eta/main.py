"""escale-eta — prediction d'heure d'arrivee et detection d'anomalie.

Ce service existe pour une raison pedagogique precise : il est le seul de la
pile a demarrer lentement, a consommer beaucoup de memoire et a justifier un
autoscaling sur metrique personnalisee. C'est pourquoi il n'apparait qu'au
chapitre 9, la ou ces sujets sont traites.

    INFERENCE_MODE=mock  simule chargement, latence et memoire du vrai modele.
                         Symptomes identiques, sans GPU, sur un portable.
    INFERENCE_MODE=real  execute un petit modele ONNX sur CPU.
"""
from __future__ import annotations

import math
import os
import time

from escale_common import ArretPropre, Chaos, Sante, configurer_logs, get_config, monter_endpoints
from escale_common.logs import journal
from fastapi import FastAPI
from prometheus_client import Histogram

MODE = os.environ.get("INFERENCE_MODE", "mock").lower()
TAILLE_MODELE_MO = float(os.environ.get("MODEL_SIZE_MB", 300))
LATENCE_MS = float(os.environ.get("INFERENCE_LATENCY_MS", 45))

INFERENCE = Histogram("escale_inference_secondes", "Duree d'une inference")

config = get_config("escale-eta")
configurer_logs(config.service, config.log_level, config.en_json)
chaos = Chaos(config.chaos)
sante = Sante(config.service)
arret = ArretPropre(config.delai_arret_s, au_signal=sante.marquer_non_pret).installer()
_modele: list[bytes] = []


def charger_modele() -> None:
    """En mode mock, on occupe reellement la memoire et on prend reellement le
    temps annonce : sinon ni la startupProbe ni l'OOMKilled ne sont observables,
    et l'etudiant configure des sondes qu'il ne verra jamais agir."""
    debut = time.monotonic()
    duree = config.demarrage_lent_s or 30.0
    journal("chargement du modele", mode=MODE, taille_mo=TAILLE_MODELE_MO, duree_s=duree)
    if MODE == "mock":
        _modele.append(b"\0" * int(TAILLE_MODELE_MO * 1024 * 1024))
        time.sleep(duree)
    else:                                    # pragma: no cover
        import onnxruntime                   # noqa: F401
        raise NotImplementedError("mode real : brancher ici le modele ONNX")
    journal("modele charge", secondes=round(time.monotonic() - debut, 1))


app = FastAPI(title="escale-eta", version="0.1.0")
monter_endpoints(app, sante, chaos)


@app.on_event("startup")
def demarrer() -> None:
    charger_modele()
    sante.marquer_pret()


@app.post("/predire")
def predire(demande: dict):
    chaos.avant_requete()
    with INFERENCE.time():
        if MODE == "mock":
            time.sleep(LATENCE_MS / 1000.0)
        distance = float(demande.get("distance_nm", 0))
        vitesse = max(float(demande.get("vitesse_noeuds", 12)), 0.1)
        meteo = 1.0 + 0.12 * math.sin(distance)      # correction fictive assumee
    return {
        "eta_minutes": round(distance / vitesse * 60 * meteo, 1),
        "confiance": 0.82,
        "mode": MODE,
    }
