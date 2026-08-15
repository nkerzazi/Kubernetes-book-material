# Chapitre 8 — Exposition des applications et trafic réseau

🟠 **Niveau Déploiement** · branche [`ch08`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch08)

## État d'Escale à la fin de ce chapitre

Accessible de l'extérieur via un Ingress unique, en HTTPS.

## Ce que ce chapitre ajoute au dépôt

- `k8s/reseau/ingress.yaml` — routage par hôte et par chemin, TLS, repli `nip.io`

## Commandes clés

```bash
kubectl apply -f k8s/reseau/ingress.yaml
kubectl get ingress   # colonne ADDRESS vide = personne ne le traite
curl -skI https://escale.127.0.0.1.nip.io/
```

## Points de contrôle

- [ ] Les deux chemins répondent par la même adresse
- [ ] **Tous les Services applicatifs restent en `ClusterIP`**
- [ ] Le certificat est `READY: True`

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch08
```

📂 **[Parcourir les fichiers de la branche `ch08`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch08)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch07](../ch07/) · [ch09 →](../ch09/)
