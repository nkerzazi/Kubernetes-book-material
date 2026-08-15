#!/usr/bin/env bash
# Reproduit le tableau de la section 2.9.4 : une modification par ligne,
# trois mesures par ligne. Sert de corrige a l'exercice 2.6.
#
#   ./scripts/mesures.sh            # les sept etapes
#   ./scripts/mesures.sh 01 03 06   # une selection
set -euo pipefail

cd "$(dirname "$0")/.."
CTX=services/api
SORTIE=mesures.csv
ETAPES=("$@")
[ ${#ETAPES[@]} -eq 0 ] && ETAPES=(01 02 03 04 05 06 07)

echo "etape;dockerfile;taille;build_froid_s;build_chaud_s" > "$SORTIE"
printf "%-12s %-10s %-14s %-14s\n" ETAPE TAILLE "FROID (s)" "CHAUD (s)"

for e in "${ETAPES[@]}"; do
  df=$(ls "$CTX"/dockerfiles/Dockerfile."$e"-* 2>/dev/null | head -1)
  [ -z "$df" ] && { echo "etape $e introuvable"; continue; }
  tag="escale-api:$e"

  t0=$(date +%s)
  docker build --no-cache -q -f "$df" -t "$tag" "$CTX" >/dev/null
  froid=$(( $(date +%s) - t0 ))

  taille=$(docker images "$tag" --format "{{.Size}}")

  # meme modification a chaque iteration, sinon les colonnes ne sont pas comparables
  echo "# mesure $(date +%s)" >> "$CTX/escale_api/main.py"
  t0=$(date +%s)
  docker build -q -f "$df" -t "$tag" "$CTX" >/dev/null
  chaud=$(( $(date +%s) - t0 ))
  git checkout -- "$CTX/escale_api/main.py" 2>/dev/null || \
    sed -i '$ d' "$CTX/escale_api/main.py"

  printf "%-12s %-10s %-14s %-14s\n" "$e" "$taille" "$froid" "$chaud"
  echo "$e;$(basename "$df");$taille;$froid;$chaud" >> "$SORTIE"
done

echo
echo "Resultats dans $SORTIE"
echo "Rappel : le changement d'image de base agit sur la TAILLE,"
echo "         le reordonnancement agit sur le TEMPS a chaud. Ne pas confondre."
