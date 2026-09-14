#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "$1"
echo "print('app')" > app.py; gi add -A; gi commit -qm "feat: app"
printf 'AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE\nAWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY\n' > .env; gi add .env; gi commit -qm "chore: add env"
echo "# readme" > README.md; gi add -A; gi commit -qm "docs: readme"
gi rm -q .env; echo ".env" > .gitignore; gi add -A; gi commit -qm "chore: remove env"
echo "prompt: Use the secret-audit skill on this repo. Do not rewrite history."
