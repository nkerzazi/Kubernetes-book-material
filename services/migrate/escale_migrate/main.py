"""escale-migrate — application des migrations de schema.

Chapitre 3 : lance a la main avant l'API.
Chapitre 4 : service Compose dont l'API depend.
Chapitre 7 : Job Kubernetes, puis initContainer.

Ce service s'arrete apres avoir travaille : c'est une tache ponctuelle, pas un
serveur. Son code de sortie 0 est ce sur quoi l'orchestrateur s'appuie pour
autoriser le demarrage des autres services.
"""
from __future__ import annotations

import pathlib
import sys
import time

import psycopg
from escale_common import configurer_logs, get_config
from escale_common.logs import journal

DOSSIER = pathlib.Path(__file__).resolve().parent.parent / "migrations"


def attendre_base(url: str, tentatives: int = 30) -> psycopg.Connection:
    """La base n'est pas prete quand le conteneur demarre : elle est prete
    quand elle accepte des connexions. Les deux instants different de plusieurs
    secondes, et c'est le sujet du chapitre 4."""
    derniere = None
    for essai in range(1, tentatives + 1):
        try:
            return psycopg.connect(url, autocommit=True)
        except Exception as exc:  # noqa: BLE001
            derniere = exc
            if essai % 5 == 1:
                journal("base pas encore prete", niveau="warning", essai=essai)
            time.sleep(1.0)
    raise RuntimeError(f"base injoignable apres {tentatives} tentatives : {derniere}")


def main() -> int:
    config = get_config("escale-migrate")
    configurer_logs(config.service, config.log_level, config.en_json)
    if not config.database_url:
        journal("DATABASE_URL absent", niveau="error")
        return 2

    conn = attendre_base(config.database_url)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS schema_migrations (
               version     TEXT PRIMARY KEY,
               applique_le TIMESTAMPTZ NOT NULL DEFAULT now())"""
    )
    deja = {ligne[0] for ligne in conn.execute("SELECT version FROM schema_migrations").fetchall()}

    appliquees = 0
    for fichier in sorted(DOSSIER.glob("*.sql")):
        version = fichier.stem
        if version in deja:
            journal("deja appliquee", version=version)
            continue
        journal("application", version=version)
        with conn.transaction():          # tout ou rien, migration par migration
            conn.execute(fichier.read_text())
            conn.execute("INSERT INTO schema_migrations (version) VALUES (%s)", (version,))
        appliquees += 1

    journal("migrations terminees", appliquees=appliquees, total=len(deja) + appliquees)
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
