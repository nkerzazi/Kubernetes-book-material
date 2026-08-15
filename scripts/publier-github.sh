#!/usr/bin/env bash
# Publie le depot Escale et ses 13 branches sur VOTRE compte GitHub.
#
# A executer par vous : ce script n'embarque aucun identifiant, et n'en demande
# aucun. L'authentification passe par `gh auth login`, qui ouvre votre
# navigateur et ne transmet jamais de mot de passe a ce script.
#
#   ./scripts/publier-github.sh mon-compte escale-livre [public|private]
set -euo pipefail

COMPTE="${1:?usage: $0 <compte-github> [depot] [public|private]}"
DEPOT="${2:-escale-livre}"
VISIBILITE="${3:-public}"

command -v gh >/dev/null || {
  echo "GitHub CLI absent. Installation : https://cli.github.com"; exit 1; }
gh auth status >/dev/null 2>&1 || {
  echo "Non authentifie. Lancez d'abord :  gh auth login"; exit 1; }

echo "Creation de $COMPTE/$DEPOT ($VISIBILITE)"
gh repo create "$COMPTE/$DEPOT" "--$VISIBILITE" \
   --description "Escale — application fil rouge du manuel Docker & Kubernetes" \
   --disable-wiki 2>/dev/null || echo "  (le depot existe deja, on continue)"

git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$COMPTE/$DEPOT.git"

echo "Envoi des 13 branches et de main"
git push -u origin main
for n in $(seq -w 1 13); do git push origin "ch$n"; done

echo "Description des branches"
gh repo edit "$COMPTE/$DEPOT" --default-branch main >/dev/null

echo
echo "Depot publie : https://github.com/$COMPTE/$DEPOT"
echo "Generez maintenant les QR codes :"
echo "  python3 scripts/qr-chapitres.py $COMPTE $DEPOT"
