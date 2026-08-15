# Chapitre 9 — Déploiement avancé et industrialisation

🟠 **Niveau Déploiement** · branche [`ch09`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch09)

## État d'Escale à la fin de ce chapitre

`escale-eta` entre en scène. Ressources, sondes, HPA, chart Helm sur 3 environnements.

## Ce que ce chapitre ajoute au dépôt

- `services/eta/` — 300 Mo de modèle, 30 s de chargement, mode `mock`
- `k8s/prod/deployment-eta.yaml` — les **trois** sondes, dont `startupProbe`
- `k8s/prod/hpa.yaml` — autoscaling sur la profondeur de file
- `helm/escale/` — chart et valeurs par environnement

## Commandes clés

```bash
kubectl apply -f k8s/prod/
kubectl set env deploy/escale-sim NAVIRES=200 CADENCE_S=0.2   # provoquer la charge
helm upgrade --install escale helm/escale -f helm/escale/values-prod.yaml --wait
```

## Points de contrôle

- [ ] `escale-eta` atteint `1/1` **sans aucun redémarrage**
- [ ] L'HPA a effectivement varié, relevé à l'appui
- [ ] Le diff dev/prod tient en moins de 30 lignes

## Récupérer cet état

```bash
git checkout ch09
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch08](../ch08/) · [ch10 →](../ch10/)
