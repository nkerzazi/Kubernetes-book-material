"""Stockage PostgreSQL — introduit au chapitre 3.

Le code applicatif ne change pas : c'est `creer_depot()` qui bascule d'une
implémentation à l'autre selon la présence de `DATABASE_URL`. C'est ce qui
permet au chapitre 3 de porter sur la persistance et non sur du refactoring.
"""
from __future__ import annotations

import threading
import time

import psycopg
from psycopg.rows import dict_row

from .store import QUAIS, Depot


class DepotPostgres(Depot):
    nom = "postgres"

    def __init__(self, url: str):
        self.url = url
        self._verrou = threading.Lock()
        self._connexion: psycopg.Connection | None = None

    # ------------------------------------------------------------ connexion

    def _connecter(self) -> psycopg.Connection:
        """Reconnexion paresseuse.

        Une base peut redémarrer sans que le service ait à redémarrer : c'est
        exactement ce que le chapitre 3 fait constater, et ce que la distinction
        /healthz vs /readyz permet d'exprimer.
        """
        if self._connexion is None or self._connexion.closed:
            self._connexion = psycopg.connect(self.url, row_factory=dict_row, autocommit=True)
        return self._connexion

    def initialiser(self, tentatives: int = 30, delai_s: float = 1.0) -> None:
        """Attend que la base réponde. Sans cette attente, le service démarre
        avant sa base et échoue — le grand classique du chapitre 4."""
        derniere = None
        for _ in range(tentatives):
            try:
                with self._verrou:
                    self._connecter().execute("SELECT 1")
                return
            except Exception as exc:  # noqa: BLE001
                derniere = exc
                time.sleep(delai_s)
        raise RuntimeError(f"base injoignable après {tentatives} tentatives : {derniere}")

    def disponible(self) -> bool:
        try:
            with self._verrou:
                self._connecter().execute("SELECT 1")
            return True
        except Exception:  # noqa: BLE001
            return False

    def fermer(self) -> None:
        with self._verrou:
            if self._connexion and not self._connexion.closed:
                self._connexion.close()

    # ------------------------------------------------------------ lectures

    _DERNIERES = """
        SELECT DISTINCT ON (n.imo)
               n.imo, n.nom, n.type, n.destination,
               p.latitude, p.longitude, p.vitesse_noeuds,
               EXTRACT(EPOCH FROM p.recue_le)::float8 AS maj
        FROM navires n
        LEFT JOIN positions p ON p.imo = n.imo
        ORDER BY n.imo, p.recue_le DESC
    """

    def _ligne_vers_navire(self, ligne: dict) -> dict:
        navire = {
            "imo": ligne["imo"], "nom": ligne["nom"], "type": ligne["type"],
            "destination": ligne["destination"], "maj": ligne["maj"],
            "vitesse_noeuds": ligne["vitesse_noeuds"] or 12.0,
            "position": None,
        }
        if ligne["latitude"] is not None:
            navire["position"] = {"latitude": ligne["latitude"], "longitude": ligne["longitude"]}
        return dict(navire, **self._eta(navire))

    def lister_navires(self) -> list[dict]:
        with self._verrou:
            lignes = self._connecter().execute(self._DERNIERES).fetchall()
        return [self._ligne_vers_navire(l) for l in lignes]

    def obtenir_navire(self, imo: str) -> dict | None:
        with self._verrou:
            ligne = self._connecter().execute(
                self._DERNIERES.replace("ORDER BY", "WHERE n.imo = %s ORDER BY"), (imo,)
            ).fetchone()
        return self._ligne_vers_navire(ligne) if ligne else None

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

    # ------------------------------------------------------------ écritures

    def enregistrer_position(self, position: dict) -> None:
        with self._verrou:
            conn = self._connecter()
            conn.execute(
                """INSERT INTO navires (imo, nom, type, destination)
                   VALUES (%(imo)s, %(nom)s, %(type)s, %(destination)s)
                   ON CONFLICT (imo) DO UPDATE SET destination = EXCLUDED.destination""",
                {"imo": position["imo"], "nom": position.get("nom", "inconnu"),
                 "type": position.get("type", "inconnu"),
                 "destination": position.get("destination", "Marseille")},
            )
            conn.execute(
                """INSERT INTO positions (imo, latitude, longitude, vitesse_noeuds)
                   VALUES (%(imo)s, %(latitude)s, %(longitude)s, %(vitesse_noeuds)s)""",
                {"imo": position["imo"], "latitude": position["latitude"],
                 "longitude": position["longitude"],
                 "vitesse_noeuds": position.get("vitesse_noeuds", 12.0)},
            )

    def compter_positions(self) -> int:
        """Utilisé par les TP du chapitre 3 pour démontrer la persistance."""
        with self._verrou:
            return self._connecter().execute("SELECT count(*) AS n FROM positions").fetchone()["n"]
