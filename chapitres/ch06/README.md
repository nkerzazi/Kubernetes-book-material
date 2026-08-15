# Chapitre 6 — Déployer une application sur Kubernetes

🟠 **Niveau Déploiement** · branche [`ch06`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch06)

## État d'Escale à la fin de ce chapitre

3 réplicas derrière un Service ; mise à jour et rollback maîtrisés.

## Ce que ce chapitre ajoute au dépôt

- `k8s/base/deployment.yaml` — selector et labels cohérents, `maxUnavailable: 0`
- `k8s/base/service.yaml` — sélection par labels

## Commandes clés

```bash
kubectl apply -f k8s/base/ && kubectl get endpoints escale-api
kubectl set image deployment/escale-api api=escale-api:0.3
kubectl rollout undo deployment/escale-api
```

## Points de contrôle

- [ ] **Trois endpoints listés** — le critère central du chapitre
- [ ] Un Pod supprimé est remplacé sous 15 s, avec un nom différent
- [ ] `rollout undo` ramène l'ancienne image, prouvé par `describe`

## Récupérer cet état

```bash
git checkout ch06
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch05](../ch05/) · [ch07 →](../ch07/)
