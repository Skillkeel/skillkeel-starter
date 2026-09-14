#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "${1:-}"
printf 'test:\n\tpython -m pytest -q\n' > Makefile; echo "# app" > README.md; gi add -A; gi commit -qm "chore: init"
gi checkout -qb feat/orders
mkdir -p migrations; echo "ALTER TABLE orders ADD COLUMN note TEXT;" > migrations/0002_note.sql; printf 'def create_order(note=None):\n    return {"note": note}\n' > orders.py; gi add -A; gi commit -qm "feat(orders): add note field"
printf 'def create_order(note=None):\n    if note and len(note) > 500:\n        raise ValueError("note too long")\n    return {"note": note}\n' > orders.py; gi add -A; gi commit -qm "fix(orders): cap note length"
echo "Orders support notes." >> README.md; gi add -A; gi commit -qm "docs: mention notes"
echo "prompt: Use the pr-description skill to write the PR description for this branch against main. Do not open a PR, just output the markdown."
