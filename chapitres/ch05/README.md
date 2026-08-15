# Chapitre 5 — Introduction à Kubernetes

🟠 **Niveau Déploiement** · branche [`ch05`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch05)

## État d'Escale à la fin de ce chapitre

Un premier Pod tourne sur un cluster local.

## Ce que ce chapitre ajoute au dépôt

- `k8s/base/pod-api.yaml` — un Pod **nu**, volontairement sans contrôleur

## Commandes clés

```bash
kind create cluster --name escale
kind load docker-image escale-api:0.2 --name escale
kubectl apply -f k8s/base/pod-api.yaml && kubectl get pod escale-api -w
```

## Points de contrôle

- [ ] Le Pod atteint `Running`
- [ ] `kubectl delete pod` : il **ne revient pas** — c'est le résultat du TP
- [ ] L'étudiant sait montrer la section Events d'un `describe`

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch05
```

📂 **[Parcourir les fichiers de la branche `ch05`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch05)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch04](../ch04/) · [ch06 →](../ch06/)
