#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "${1:-}"
echo "v0" > app.txt; gi add -A; gi commit -qm "feat: initial"; gi tag -a v0.1.0 -m v0.1.0
for m in "feat: add export to CSV (#12)" "fix: handle empty rows in import" "chore: bump eslint" "feat!: drop Node 16 support" "feat(api): add /health endpoint"; do echo "$m" >> app.txt; gi add -A; gi commit -qm "$m"; done
echo "prompt: Use the changelog skill to update CHANGELOG.md with everything since the last tag."; echo "trigger: Update CHANGELOG.md with everything since the last tag."
