# Chapitre 3 — Stockage, réseaux et données

🟢 **Niveau Fondations** · branche [`ch03`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch03)

## État d'Escale à la fin de ce chapitre

L'API parle à PostgreSQL sur un réseau dédié, les données survivent.

## Ce que ce chapitre ajoute au dépôt

- `services/api/escale_api/store_pg.py` — la bascule mémoire / PostgreSQL
- `services/migrate/` — migrations SQL versionnées et idempotentes

## Commandes clés

```bash
docker network create escale-net && docker volume create escale-donnees
docker run -d --name postgres --network escale-net -v escale-donnees:/var/lib/postgresql/data postgres:16-alpine
docker run --rm -v escale-donnees:/donnees -v "$PWD":/sauvegarde alpine tar czf /sauvegarde/escale.tar.gz -C /donnees .
```

## Points de contrôle

- [ ] Aucun `-p` sur le conteneur de base
- [ ] Les données survivent à `docker rm -f` des deux conteneurs
- [ ] L'archive de sauvegarde existe et n'est pas vide

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch03
```

📂 **[Parcourir les fichiers de la branche `ch03`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch03)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch02](../ch02/) · [ch04 →](../ch04/)
