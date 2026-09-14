#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "$1"
cat > package.json <<'J'
{ "name": "shop", "private": true, "packageManager": "pnpm@9.0.0", "scripts": { "dev": "vite", "build": "vite build", "test:ci": "vitest run", "lint": "eslint ." } }
J
mkdir -p .github/workflows src; printf 'name: ci\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pnpm i --frozen-lockfile\n      - run: pnpm test:ci\n' > .github/workflows/ci.yml
echo "lockfileVersion: '9.0'" > pnpm-lock.yaml; echo "export const x = 1;" > src/index.ts; echo "20" > .nvmrc
gi add -A; gi commit -qm "chore: init"; echo "prompt: Use the claude-md-init skill to create CLAUDE.md for this repo. Write the file."
