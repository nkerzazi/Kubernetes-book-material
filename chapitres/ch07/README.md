# Chapitre 7 — Configuration et données dans Kubernetes

🟠 **Niveau Déploiement** · branche [`ch07`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch07)

## État d'Escale à la fin de ce chapitre

Configuration externalisée, secrets séparés, base persistante, migrations en Job.

## Ce que ce chapitre ajoute au dépôt

- `k8s/config/configmap.yaml`, `secret.yaml` — gabarit, **jamais rempli**
- `k8s/config/postgres.yaml` — StatefulSet et `volumeClaimTemplates`
- `k8s/config/job-migrate.yaml` — la tâche ponctuelle

## Commandes clés

```bash
kubectl apply -f k8s/config/
kubectl wait --for=condition=complete job/escale-migrate --timeout=120s
kubectl get secret escale-secrets -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 -d
```

## Points de contrôle

- [ ] Le PVC est `Bound`
- [ ] Le comptage est identique avant et après suppression de `postgres-0`
- [ ] La dernière commande affiche le mot de passe **en clair** : c'est la démonstration

## Récupérer cet état

```bash
git checkout ch07
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch06](../ch06/) · [ch08 →](../ch08/)
