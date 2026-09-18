#!/usr/bin/env bash
# Build all fixtures under $1 (default /tmp/skillkeel-evals) and run each skill via `claude -p`.
# Per case: stream-json output -> evals/<skill>/transcript-<date>.jsonl, run record + mechanical grading
# (evals/record.py) -> record-<date>.json and transcript-<date>.raw.md. At the end evals/cluster.py groups
# the failures by first mechanical mismatch, so transcripts are read only where the record says to.
# --setting-sources project keeps the maintainer's user-level plugins and hooks out of the run (2026-09-17: a user-level
# "be terse" hook turned a bisect report into "Done.").
# --trigger: use each fixture's `trigger:` line instead of `prompt:`, a natural request that never names the skill, so the
# skill-fired grader tests whether the description triggers (the named prompt only tests the invocation path). Records
# are written as record-<date>-trigger.json with mode "trigger"; docs/compat.md lists them in their own column.
# Usage: bash evals/run.sh [--trigger] [outdir] [skill...]
set -u
cd "$(dirname "$0")/.."; ROOT=$PWD
MODE=named; if [ "${1:-}" = "--trigger" ]; then MODE=trigger; shift; fi
OUT=${1:-/tmp/skillkeel-evals}; shift || true
SK=${@:-"commit-message pr-description claude-md-init changelog readme-refresh dependency-audit secret-audit test-gap-finder"}
mkdir -p "$OUT"; date=$(date +%F); tag=$date; [ "$MODE" = trigger ] && tag="$date-trigger"
export SKILLKEEL_EVAL_MODE=$MODE
# The run never sees the maintainer's git identity or global git config: the fixture identity is the only one.
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@skillkeel.com GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@skillkeel.com
for s in $SK; do
  key=prompt; [ "$MODE" = trigger ] && key=trigger
  prompt=$(bash "evals/$s/fixture.sh" "$OUT/$s" | sed -n "s/^$key: //p")
  echo "== $s :: $prompt"
  t0=$(date +%s)
  ( cd "$OUT/$s" && timeout 600 claude -p --plugin-dir "$ROOT" --setting-sources project --permission-mode bypassPermissions --output-format stream-json --verbose "$prompt" ) > "evals/$s/transcript-$tag.jsonl" 2>"evals/$s/stderr-$tag.log"
  code=$?
  python3 evals/record.py "$s" "evals/$s/transcript-$tag.jsonl" "$code" "$(( $(date +%s) - t0 ))" "$OUT/$s" "$tag"
done
python3 evals/cluster.py --date "$tag"
