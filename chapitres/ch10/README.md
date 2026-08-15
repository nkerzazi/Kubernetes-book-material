# Chapitre 10 — Monitoring et observabilité

🔴 **Niveau Production** · branche [`ch10`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch10)

## État d'Escale à la fin de ce chapitre

Métriques, journaux et traces collectés ; tableau de bord et alertes.

## Ce que ce chapitre ajoute au dépôt

- `observabilite/prometheus.yml`, `alertes.yml`, `otel-collector.yaml`
- `observabilite/compose-observabilite.yaml` — la pile, à lancer à côté

## Commandes clés

```bash
kubectl apply -f observabilite/ -n observabilite
kubectl set env deploy/escale-api CHAOS_ERROR_RATE=0.05   # déclencher l'alerte
kubectl set env deploy/escale-api CHAOS_ERROR_RATE-
```

## Points de contrôle

- [ ] Toutes les cibles sont `UP`
- [ ] Le tableau de bord comporte 4 panneaux et répond à une question écrite
- [ ] L'alerte passe par `pending` puis `firing`, et revient au repos

## Récupérer cet état

```bash
git checkout ch10
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch09](../ch09/) · [ch11 →](../ch11/)
