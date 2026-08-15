# Chapitre 2 — Construire des images Docker

🟢 **Niveau Fondations** · branche [`ch02`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch02)

## État d'Escale à la fin de ce chapitre

`escale-api` dockerisée, image optimisée et publiée.

## Ce que ce chapitre ajoute au dépôt

- `CONTRAT.md` — le contrat de conteneur, référence de tout le livre
- `services/api/dockerfiles/` — **les 7 étapes du tableau §2.9.4**, une par fichier
- `services/*/.dockerignore`, `scripts/mesures.sh`

## Commandes clés

```bash
docker build -t escale-api:0.2 services/api
docker history escale-api:0.2
./scripts/mesures.sh
```

## Points de contrôle

- [ ] `mesures.csv` comporte 7 lignes cohérentes
- [ ] Le build à chaud passe sous 10 s après réordonnancement
- [ ] L'image publiée est retéléchargeable après suppression locale

## Récupérer cet état

```bash
git clone https://github.com/nkerzazi/Kubernetes-book-material.git
cd Kubernetes-book-material
git checkout ch02
```

📂 **[Parcourir les fichiers de la branche `ch02`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch02)**

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch01](../ch01/) · [ch03 →](../ch03/)
