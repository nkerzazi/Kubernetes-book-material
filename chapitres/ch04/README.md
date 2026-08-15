# Chapitre 4 — Docker Compose et applications multi-conteneurs

🟢 **Niveau Fondations** · branche [`ch04`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch04)

## État d'Escale à la fin de ce chapitre

Pile complète en une commande. `escale-sim` fait apparaître les navires.

## Ce que ce chapitre ajoute au dépôt

- `compose.yaml` — 7 services, healthchecks, `service_completed_successfully`
- `services/worker/` — consomme la file, écrit en base

## Commandes clés

```bash
docker compose up -d --build
docker compose logs -f sim
docker compose down   # sans -v : les volumes restent
```

## Points de contrôle

- [ ] Dix démarrages consécutifs sans échec, sans aucun `sleep`
- [ ] `migrate` apparaît en état terminé, non en erreur
- [ ] Seuls deux ports sont publiés

## Récupérer cet état

```bash
git checkout ch04
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch03](../ch03/) · [ch05 →](../ch05/)
