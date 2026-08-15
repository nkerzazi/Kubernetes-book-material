# Chapitre 12 — CI/CD et déploiement automatisé

🔴 **Niveau Production** · branche [`ch12`](https://github.com/nkerzazi/Kubernetes-book-material/tree/ch12)

## État d'Escale à la fin de ce chapitre

Un commit déclenche test, build, scan, publication, déploiement et vérification.

## Ce que ce chapitre ajoute au dépôt

- `.github/workflows/ci.yml` — tests, build, scan **bloquant**
- `.github/workflows/cd.yml` — déploiement Helm, vérification, retour arrière
- `tests/test_api.py` — vérifient le contrat de conteneur

## Commandes clés

```bash
git commit -am 'sonde cassee' && git push   # faire échouer exprès
kubectl rollout status deploy/escale-api --timeout=5m; echo "code=$?"
./scripts/verifier-contrat.sh https://escale.exemple.fr/api
```

## Points de contrôle

- [ ] Le pipeline échoue au scan, et est rendu vert **sans désactivation**
- [ ] L'image porte l'empreinte du commit
- [ ] Un déploiement raté déclenche un retour arrière, prouvé par l'historique

## Récupérer cet état

```bash
git checkout ch12
```

Chaque branche est **fonctionnelle et autonome** : vous pouvez rejoindre le fil
rouge à n'importe quel chapitre sans avoir fait les précédents.

---

[← ch11](../ch11/) · [ch13 →](../ch13/)
