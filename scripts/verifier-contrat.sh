#!/usr/bin/env bash
# Verifie qu'un service respecte le contrat de conteneur (CONTRAT.md).
# Utilise comme critere de reussite dans plusieurs TP et pour le projet final.
#
#   ./scripts/verifier-contrat.sh http://localhost:8080
set -uo pipefail
BASE="${1:-http://localhost:8000}"
ok=0; ko=0

verif() {
  local libelle="$1"; shift
  if "$@" >/dev/null 2>&1; then printf "  [ok] %s\n" "$libelle"; ok=$((ok+1))
  else printf "  [KO] %s\n" "$libelle"; ko=$((ko+1)); fi
}

code() { [ "$(curl -s -o /dev/null -w '%{http_code}' "$1")" = "$2" ]; }

echo "Contrat de conteneur — $BASE"
verif "/healthz repond 200"              code "$BASE/healthz" 200
verif "/readyz repond 200"               code "$BASE/readyz" 200
verif "/metrics expose du Prometheus"    bash -c "curl -s $BASE/metrics | grep -q '^# HELP'"
verif "/healthz et /readyz different"    bash -c "[ \"\$(curl -s $BASE/healthz)\" != \"\$(curl -s $BASE/readyz)\" ]"
echo
echo "  $ok conforme(s), $ko ecart(s)"
[ "$ko" -eq 0 ]
