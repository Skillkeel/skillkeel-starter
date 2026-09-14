#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "${1:-}"
cat > package.json <<'J'
{ "name": "dep-fixture", "version": "1.0.0", "private": true, "dependencies": { "lodash": "4.17.15" } }
J
gi add -A; gi commit -qm "chore: init"; echo "prompt: Use the dependency-audit skill on this repo. Network is allowed. Propose fixes; do not apply major bumps."
