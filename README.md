# Escale — dépôt compagnon

Application fil rouge du manuel **Docker & Kubernetes — de mon application sur
mon ordinateur à une application observable, sécurisée et déployée en production**.

Escale est une plateforme de suivi d'escales portuaires : des navires émettent
leur position, la plateforme suit leur trajet, prédit leur heure d'arrivée et
signale les anomalies.

> **Aucune source de données externe.** Le trafic est produit par un simulateur
> embarqué (`escale-sim`). Un établissement sans accès Internet doit pouvoir
> exécuter l'intégralité des travaux pratiques.

---

## Démarrage rapide

Sans Docker, pour vérifier que le code fonctionne :

```bash
export PYTHONPATH=services/common:services/api:services/sim
pip install -r services/api/requirements.txt -r services/sim/requirements.txt

python -m uvicorn escale_api.main:app --port 8000     # terminal 1
NAVIRES=15 CADENCE_S=1 python -m escale_sim.main      # terminal 2
curl -s localhost:8000/escales | head
```

Avec Docker, à partir du chapitre 2 :

```bash
docker build -t escale-api:0.2 services/api
docker run -d -p 8080:8000 --name api escale-api:0.2
./scripts/verifier-contrat.sh http://localhost:8080
```

Avec Compose, à partir du chapitre 4 :

```bash
docker compose up --build          # web sur :8081, api sur :8080
```

---

## Structure

```
services/
  common/escale_common/   le contrat de conteneur, implémenté une seule fois
    config.py             règles 1 et 2 — port et configuration par l'environnement
    sante.py              règles 3 et 4 — /healthz, /readyz, /metrics
    logs.py               règle 5      — JSON sur stdout
    arret.py              règle 6      — arrêt propre sur SIGTERM
    chaos.py              les défauts injectables CHAOS_*
  api/                    escale-api — navires, positions, escales
    escale_api/store.py     stockage mémoire (ch. 1-2)
    escale_api/store_pg.py  stockage PostgreSQL (ch. 3+)
    dockerfiles/            les 7 étapes du tableau §2.9.4, une par fichier
  migrate/                escale-migrate — migrations SQL versionnées
  worker/                 escale-worker — consomme la file, écrit en base
  sim/                    escale-sim — générateur de trafic (mode http ou redis)
  web/                    escale-web — carte et tableau de bord
scripts/
  mesures.sh              reproduit le tableau §2.9.4 (corrigé de l'exercice 2.6)
  verifier-contrat.sh     vérifie qu'un service respecte le contrat
  creer-branches.sh       crée les 13 branches d'état
docs/
  etat-par-chapitre.md    ce qui doit fonctionner à la fin de chaque chapitre
CONTRAT.md                le contrat de conteneur et ses variables
```

## Branches

Une branche par chapitre, `ch01` à `ch13`. **Règle d'or : à la fin de chaque
chapitre, Escale est dans un état fonctionnel, versionné et reproductible.**
Jamais de « on verra ça plus tard » qui laisse une application cassée entre
deux séances. Voir `docs/etat-par-chapitre.md`.

Les corrigés des travaux pratiques vivent dans `solutions/`, sur chaque branche,
et sont exclus de l'archive distribuée aux étudiants. Les solutions de
référence des mini-cas notés restent dans l'espace enseignant.

## État d'avancement

| Composant | État |
|---|---|
| `escale_common` — contrat de conteneur | complet, testé |
| `escale-api` — stockage mémoire | complet, testé |
| `escale-api` — stockage PostgreSQL | complet, testé |
| `escale-sim` | complet, testé |
| `escale-web` | complet, build npm **non vérifié** |
| Dockerfiles `api` (7 variantes) | écrits, **builds non vérifiés** |
| `escale-migrate` — migrations SQL | complet, testé |
| `escale-worker` — file Redis vers base | complet, testé |
| Pile Compose complète (7 services) | écrite, **non exécutée faute de Docker** |
| `escale-eta` et son mode `mock` | **à faire, chapitre 9** |
| Branches `ch05` à `ch13` | **à faire** |

Les chiffres cités dans le manuel (1,41 Go au départ, 81 Mo à l'arrivée)
proviennent du tableau §2.9.4 et doivent être **remesurés** avec
`scripts/mesures.sh` sur une machine de référence, puis reportés dans le texte.
Tant que cette mesure n'a pas eu lieu, ces valeurs restent des estimations.

---

## Publier ce dépôt sur GitHub

Le dépôt est prêt : 13 branches, une par chapitre, chacune dans un état
fonctionnel. Il ne reste qu'à l'envoyer sur votre compte — ce que vous faites
vous-même, avec vos propres identifiants :

```bash
gh auth login                                    # authentification par navigateur
./scripts/publier-github.sh mon-compte escale-livre
```

## Générer les QR codes des chapitres

Un QR code par chapitre, pointant vers la branche correspondante. Le lecteur
arrive directement sur l'état d'Escale à la fin du chapitre qu'il lit, sans
avoir besoin des précédents.

```bash
python3 scripts/qr-chapitres.py mon-compte escale-livre
```

Produit `qr/ch01.svg` … `qr/ch13.svg` plus `qr/depot.svg`, en **SVG vectoriel**
à 22 mm de côté, avec correction d'erreur haute. Un QR code destiné à
l'impression ne doit jamais être fourni en image matricielle : il se pixellise
et devient illisible selon la taille de reproduction.
