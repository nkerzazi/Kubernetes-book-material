# Contrat de conteneur

Tous les services d'Escale respectent les six memes regles. C'est ce qui permet
d'affirmer au lecteur, a chaque chapitre, que **ce qu'il apprend vaut pour
n'importe quel service**, et ce qui rend la charge utile interchangeable.

Ces regles sont implementees une seule fois, dans `services/common/escale_common`.
Aucun service ne les reimplemente : il les importe.

| # | Regle | Sans quoi |
|---|---|---|
| 1 | Le service ecoute sur `PORT` | impossible de faire cohabiter deux instances — ch. 4 |
| 2 | Configuration entierement par l'environnement, aucune valeur en dur | une image a reconstruire a chaque changement de mot de passe — ch. 7 |
| 3 | `/healthz` (vivant) et `/readyz` (pret) **distincts** | des requetes envoyees a un service qui demarre encore — ch. 9 |
| 4 | `/metrics` au format Prometheus | rien a observer — ch. 10 |
| 5 | Logs JSON sur `stdout`, jamais dans un fichier | des journaux perdus a chaque redemarrage — ch. 10 |
| 6 | Arret propre sur `SIGTERM`, avec drainage | des erreurs a chaque mise a jour — ch. 6 |

## Verification

    ./scripts/verifier-contrat.sh http://localhost:8080

## Variables reconnues

| Variable | Defaut | Role |
|---|---|---|
| `SERVICE_NAME` | `escale` | nom porte dans les logs et les metriques |
| `PORT` | `8000` | port d'ecoute |
| `LOG_LEVEL` | `INFO` | niveau de journalisation |
| `LOG_FORMAT` | `json` | `json` ou `texte` (lisible en salle) |
| `GRACEFUL_TIMEOUT_S` | `10` | duree de drainage sur SIGTERM |
| `STARTUP_DELAY_S` | `0` | demarrage lent simule — utile des le ch. 9 |
| `DATABASE_URL` | — | bascule le stockage sur PostgreSQL (ch. 3) |
| `REDIS_URL` | — | file de messages (ch. 3-4) |
| `API_URL` | `http://localhost:8000` | cible du simulateur |

## Defauts injectables

Aucun effet si la variable n'est pas definie. Ils rendent l'incident
**reproductible a l'identique** pour tous les etudiants, ce qui rend la
notation equitable et le corrige possible.

| Variable | Effet | Utilise par |
|---|---|---|
| `CHAOS_LATENCY_MS` | latence ajoutee a chaque requete | ch. 10 |
| `CHAOS_ERROR_RATE` | proportion de reponses 500 | ch. 10, 12 |
| `CHAOS_READYZ_FAIL_AFTER_S` | `/readyz` echoue au bout de N secondes | ch. 6, 9 |
| `CHAOS_MEMORY_LEAK_MB_PER_MIN` | fuite memoire progressive | ch. 9 (`OOMKilled`) |
| `CHAOS_CRASH_PROBABILITY` | plantage brutal du processus | ch. 5, 6 (`CrashLoopBackOff`) |

Exemple — provoquer un `CrashLoopBackOff` reproductible :

    docker run -e CHAOS_CRASH_PROBABILITY=0.3 -p 8080:8000 escale-api:0.2

## Etat teste

Le socle a ete execute et verifie sans Docker (PostgreSQL et Redis locaux) :

| Verification | Resultat |
|---|---|
| `/healthz` et `/readyz` distincts, `/readyz` a 503 quand la base tombe | ok |
| `/metrics` — 102 series exposees | ok |
| Logs JSON sur stdout | ok |
| `SIGTERM` : `/readyz` bascule avant le drainage | ok |
| Chaine sim -> Redis -> worker -> PostgreSQL, 120 positions | ok |
| Persistance apres redemarrage de l'API | ok |
| Migrations idempotentes (rejouees sans effet) | ok |
| Les cinq variables `CHAOS_*` | ok |
