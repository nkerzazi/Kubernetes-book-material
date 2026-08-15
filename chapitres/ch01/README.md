# Chapitre 1 — Pourquoi les conteneurs ?

🟢 **Niveau Fondations** · branche [`ch01`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch01)

## État d'Escale à la fin de ce chapitre

Installée à la main, dépendances en conflit. **Aucun Dockerfile** : c'est le problème.

## Ce que ce chapitre ajoute au dépôt

- `docs/INSTALLATION-MANUELLE.md` — la procédure pénible, à vivre une fois
- `services/api/`, `services/sim/`, `services/web/` — le code, sans conteneurs
- `services/common/escale_common/` — le socle partagé

## Commandes clés

```bash
docker run -d -p 8080:8000 --name escale escale/demo:ch01
docker exec -it escale sh
docker rm -f escale && docker run -d -p 8080:8000 --name escale escale/demo:ch01
```

## Points de contrôle

- [ ] Le conteneur atteint l'état `Up`
- [ ] Le fichier écrit dans `/tmp` a disparu après recréation
- [ ] Deux instances tournent sur deux ports différents

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch01
```

📂 **[Parcourir les fichiers de la branche `ch01`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch01)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← Sommaire](../../README.md) · [ch02 →](../ch02/)
