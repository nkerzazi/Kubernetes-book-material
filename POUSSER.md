# Envoyer ce dépôt sur GitHub

L'historique de ce dossier **se greffe sur le commit initial** déjà présent sur
`nkerzazi/Kubernetes-book-material`. Aucun forçage n'est donc nécessaire, et
le `LICENSE` du dépôt est conservé.

## Envoi

```bash
tar xzf escale-depot.tar.gz && cd escale-final
git push -u origin main
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13; do git push origin "ch$n"; done
```

Si `git push` demande une authentification, utilisez un jeton d'accès personnel
ou `gh auth login` — ce dépôt n'en contient aucun, et n'en demande aucun.

## Vérification

```bash
git ls-remote --heads origin | wc -l     # doit afficher 14
```

Puis, sur github.com : la page d'accueil doit renvoyer vers `chapitres/`, et le
sélecteur de branches doit lister `ch01` … `ch13`.

## Ce qui a été vérifié avant l'envoi

| Contrôle | Résultat |
|---|---|
| L'historique se greffe sur le commit initial, sans forçage | ok |
| `LICENSE` conservé | ok |
| 14 branches, un commit par chapitre | ok |
| `ch01` ne contient **aucun** fichier Docker | ok |
| `ch01` démarre et sert l'API | ok |
| `main` passe les 4 tests | ok |
| 13 manifestes Kubernetes syntaxiquement valides | ok |
| Chaîne sim → Redis → worker → PostgreSQL | ok |
| Builds Docker, build npm, pile Compose, manifestes appliqués | **non vérifiés** — Docker absent de l'environnement de rédaction |

## Après l'envoi

1. Générer les QR codes définitifs :
   `python3 scripts/qr-chapitres.py nkerzazi Kubernetes-book-material`
2. Scanner deux ou trois codes : ils mènent en 404 tant que les branches ne
   sont pas publiées.
3. Exécuter `./scripts/mesures.sh` sur une machine équipée de Docker, et
   reporter les chiffres obtenus dans le tableau §2.9.4 du manuel.
