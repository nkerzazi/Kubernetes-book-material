#!/usr/bin/env bash
# Recopie escale_common dans le contexte de build de chaque service.
#
# Pourquoi : un COPY ne peut pas remonter au-dessus du contexte de build, et un
# lien symbolique n'est pas suivi. Deux solutions existent :
#   a) contexte de build a la racine du depot, avec -f services/api/Dockerfile
#   b) le paquet commun est recopie dans chaque contexte  <- retenu ici
# La solution (b) garde la commande du chapitre 2 simple — `docker build .`
# depuis le repertoire du service — au prix de cette synchronisation.
# La source de verite reste services/common/escale_common.
set -euo pipefail
cd "$(dirname "$0")/.."
for s in api sim migrate worker eta; do
  rm -rf "services/$s/escale_common"
  cp -r services/common/escale_common "services/$s/escale_common"
  echo "escale_common -> services/$s/"
done
