# Chapitre 13 — Bonnes pratiques et projet final

🔴 **Niveau Production** · branche [`ch13`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch13)

## État d'Escale à la fin de ce chapitre

Système complet, revu et justifié en revue d'architecture.

## Ce que ce chapitre ajoute au dépôt

- `docs/PROJET-FINAL.md` — cahier des charges, jalons, barème
- `docs/etat-par-chapitre.md` — l'état d'Escale à chaque étape

## Commandes clés

```bash
helm upgrade --install escale helm/escale -f helm/escale/values-prod.yaml --wait
./scripts/verifier-contrat.sh https://escale.exemple.fr/api
```

## Points de contrôle

- [ ] L'application se déploie sur un cluster neuf depuis le seul dépôt
- [ ] Le délai de reprise est **mesuré**, non estimé
- [ ] Chaque décision d'architecture est justifiée et chiffrée

## Récupérer cet état

```bash
git checkout ch13
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch12](../ch12/) · [Sommaire →](../../README.md)
