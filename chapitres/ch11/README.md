# Chapitre 11 — Sécurité des conteneurs et de Kubernetes

🔴 **Niveau Production** · branche [`ch11`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch11)

## État d'Escale à la fin de ce chapitre

Images scannées, conteneurs non privilégiés, RBAC restreint, trafic cloisonné.

## Ce que ce chapitre ajoute au dépôt

- `k8s/securite/securitycontext.yaml` — fragment à fusionner, pas à appliquer
- `k8s/securite/rbac.yaml` — compte de service aux droits minimaux
- `k8s/securite/networkpolicy.yaml` — refus par défaut **et** autorisation du DNS

## Commandes clés

```bash
trivy image escale-api:0.2 --severity HIGH,CRITICAL --ignore-unfixed
kubectl auth can-i get secrets --as=system:serviceaccount:escale:escale-app
kubectl run intrus --rm -it --image=alpine --restart=Never -- nc -zv -w3 postgres 5432
```

## Points de contrôle

- [ ] `auth can-i get secrets` répond `no`
- [ ] **La vérification négative figure au rendu** : l'accès non autorisé échoue
- [ ] Les deux politiques réseau sont appliquées ensemble

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch11
```

📂 **[Parcourir les fichiers de la branche `ch11`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch11)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch10](../ch10/) · [ch12 →](../ch12/)
