# Etat d'Escale, chapitre par chapitre

Regle d'or : a la fin de chaque chapitre, l'application est **fonctionnelle,
versionnee et reproductible**. Chaque ligne correspond a une branche.

| Br. | Etat atteint | Services actifs | Fait |
|---|---|---|---|
| ch01 | installee a la main, dependances en conflit — le probleme est vecu | aucun conteneur | oui |
| ch02 | escale-api dockerisee, image optimisee et publiee | api | oui |
| ch03 | l'API parle a PostgreSQL sur un reseau dedie, donnees persistantes | api, postgres | oui |
| ch04 | pile complete demarree par une seule commande Compose | web, api, worker, sim, postgres, redis, migrate | oui (non execute) |
| ch05 | un premier Pod tourne sur un cluster local | api (Pod isole) | non |
| ch06 | 3 replicas derriere un Service ; update et rollback maitrises | web, api, worker | non |
| ch07 | configuration externalisee, secrets, PVC, migrations en Job | + postgres (PVC), migrate | non |
| ch08 | accessible de l'exterieur via un Ingress, en HTTPS | pile exposee | non |
| ch09 | escale-eta : ressources, probes, HPA, chart Helm sur 3 environnements | + eta | non |
| ch10 | metriques, logs et traces collectes, tableau de bord et alertes | + observabilite | non |
| ch11 | images scannees, non-root, RBAC restreint, trafic cloisonne | pile durcie | non |
| ch12 | un commit declenche test, build, scan, publication et deploiement | pile + pipeline | non |
| ch13 | systeme complet, revu et justifie en revue d'architecture | tout | non |

## Ordonnancement

`escale-eta` n'apparait qu'au chapitre 9, la ou son demarrage lent, son
empreinte memoire et son autoscaling deviennent le sujet. L'introduire plus tot
alourdirait les chapitres 2 a 8 sans benefice. Il est en revanche **mentionne
des le chapitre 4** comme service a venir, ce qui motive le decouplage par file
de messages.

## Ce qui reste a construire, par ordre de priorite

1. Manifestes Kubernetes de base — bloquent les chapitres 5 et 6.
2. Chart Helm et valeurs par environnement — bloquent le chapitre 9.
3. `escale-eta` avec `INFERENCE_MODE=mock|real` — bloque le chapitre 9.
4. Stack d'observabilite (Prometheus, Grafana, Loki) — bloque le chapitre 10.
5. Pipeline CI/CD et variante locale (Gitea + Act) — bloquent le chapitre 12.
6. Environnements degrades des defis (`ch02-defi`, `ch09-defi`, `ch11-defi`).

## Verification a executer sur une machine equipee de Docker

Le socle a ete teste sans Docker : PostgreSQL et Redis en local, les services
lances directement. Restent a verifier une fois Docker disponible :

- les sept Dockerfiles de `services/api/dockerfiles/` et les chiffres du
  tableau 2.9.4, via `scripts/mesures.sh` ;
- le build npm de `escale-web` et le seuil de 40 Mo du TP autonome du ch. 2 ;
- `docker compose up --build` de bout en bout, en particulier la condition
  `service_completed_successfully` sur le service `migrate`.
