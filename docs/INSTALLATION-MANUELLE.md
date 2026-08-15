# Installer Escale a la main — chapitre 1

Ce document existe pour etre **penible**. Il decrit l'installation manuelle
d'Escale, telle qu'elle se pratiquait avant la conteneurisation. C'est le
probleme que le reste du livre resout ; il faut l'avoir vecu une fois.

## Prerequis annonces

- Python **3.12 exactement** (3.11 et 3.13 produisent des ecarts de comportement)
- PostgreSQL 16, demarre, avec une base `escale` et un utilisateur dedie
- Redis 7
- Node 22 pour construire l'interface

## Procedure

    python3.12 -m venv .venv && source .venv/bin/activate
    pip install -r services/api/requirements.txt
    createdb escale
    psql escale -f services/migrate/migrations/001_initial.sql
    psql escale -f services/migrate/migrations/002_quais.sql
    export DATABASE_URL=postgresql://...
    PYTHONPATH=services/common:services/api python -m uvicorn escale_api.main:app

## Ce qui va mal se passer, et c'est voulu

1. Votre systeme n'a probablement pas Python 3.12. L'installer a cote de la
   version systeme casse souvent un autre projet.
2. La version de PostgreSQL installee n'est pas la meme que celle du serveur.
3. Le collegue qui recupere le depot n'obtient pas le meme resultat que vous.
4. Rien de tout cela n'est ecrit dans le code : c'est l'**environnement
   d'execution** qui differe, et il n'a pas ete livre.

Notez le temps qu'il vous a fallu. Au chapitre 2, la meme mise en route tiendra
en une commande, sur n'importe quelle machine.
