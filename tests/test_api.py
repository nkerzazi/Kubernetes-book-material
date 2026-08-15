"""Tests minimaux — executes par la CI du chapitre 12.

Ils verifient le contrat de conteneur, pas la logique metier : c'est ce
contrat qui doit rester vrai a tous les chapitres.
"""
from fastapi.testclient import TestClient

from escale_api.main import app


def test_healthz_et_readyz_sont_distincts():
    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        assert client.get("/healthz").json() != client.get("/readyz").json()


def test_metriques_au_format_prometheus():
    with TestClient(app) as client:
        assert "# HELP" in client.get("/metrics").text


def test_position_incomplete_est_refusee():
    with TestClient(app) as client:
        assert client.post("/positions", json={"imo": "1"}).status_code == 422


def test_eta_decroit_quand_la_vitesse_augmente():
    with TestClient(app) as client:
        base = {"imo": "9321483", "latitude": 43.9, "longitude": 5.1,
                "destination": "Marseille"}
        client.post("/positions", json={**base, "vitesse_noeuds": 10})
        lent = client.get("/navires/9321483").json()["eta_minutes"]
        client.post("/positions", json={**base, "vitesse_noeuds": 20})
        rapide = client.get("/navires/9321483").json()["eta_minutes"]
        assert rapide < lent
