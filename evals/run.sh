#!/usr/bin/env bash
# Build all fixtures under $1 (default /tmp/skillkeel-evals) and run each skill via `claude -p`.
# Usage: bash evals/run.sh [outdir] [skill...]
set -u
cd "$(dirname "$0")/.."; ROOT=$PWD; OUT=${1:-/tmp/skillkeel-evals}; shift || true
SK=${@:-"commit-message pr-description claude-md-init changelog readme-refresh dependency-audit secret-audit test-gap-finder"}
mkdir -p "$OUT"; date=$(date +%F)
for s in $SK; do
  prompt=$(bash "evals/$s/fixture.sh" "$OUT/$s" | sed -n 's/^prompt: //p')
  echo "== $s :: $prompt"
  ( cd "$OUT/$s" && timeout 600 claude -p --plugin-dir "$ROOT" --permission-mode bypassPermissions --output-format text "$prompt" ) > "evals/$s/transcript-$date.raw.md" 2>&1
  echo "   exit=$? -> evals/$s/transcript-$date.raw.md ($(wc -l < "evals/$s/transcript-$date.raw.md") lines)"
done
