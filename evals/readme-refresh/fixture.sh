#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "$1"
cat > package.json <<'J'
{ "name": "svc", "scripts": { "dev": "node server.js", "test": "node --test" } }
J
echo "console.log('hi')" > server.js
printf '# svc\n\nA tiny service.\n\n## Run\n\n```\nnpm run start\n```\n\n## Docs\n\nSee [API docs](docs/api.md).\n\n## License\n\nMIT\n' > README.md
gi add -A; gi commit -qm "chore: init"; echo "prompt: Use the readme-refresh skill to audit and fix README.md."
