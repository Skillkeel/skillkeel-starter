#!/usr/bin/env bash
# Build all fixtures under $1 (default /tmp/skillkeel-evals) and run each skill via `claude -p`.
# Per case: stream-json output -> evals/<skill>/transcript-<date>.jsonl, run record + mechanical grading
# (evals/record.py) -> record-<date>.json and transcript-<date>.raw.md. At the end evals/cluster.py groups
# the failures by first mechanical mismatch, so transcripts are read only where the record says to.
# Usage: bash evals/run.sh [outdir] [skill...]
set -u
cd "$(dirname "$0")/.."; ROOT=$PWD; OUT=${1:-/tmp/skillkeel-evals}; shift || true
SK=${@:-"commit-message pr-description claude-md-init changelog readme-refresh dependency-audit secret-audit test-gap-finder"}
mkdir -p "$OUT"; date=$(date +%F)
for s in $SK; do
  prompt=$(bash "evals/$s/fixture.sh" "$OUT/$s" | sed -n 's/^prompt: //p')
  echo "== $s :: $prompt"
  t0=$(date +%s)
  ( cd "$OUT/$s" && timeout 600 claude -p --plugin-dir "$ROOT" --permission-mode bypassPermissions --output-format stream-json --verbose "$prompt" ) > "evals/$s/transcript-$date.jsonl" 2>"evals/$s/stderr-$date.log"
  code=$?
  python3 evals/record.py "$s" "evals/$s/transcript-$date.jsonl" "$code" "$(( $(date +%s) - t0 ))" "$OUT/$s" "$date"
done
python3 evals/cluster.py --date "$date"
