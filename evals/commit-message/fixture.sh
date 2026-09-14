#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "${1:-}"
printf 'def add(a, b):\n    return a + b\n' > calc.py; gi add calc.py; gi commit -qm "feat: add calc"
printf 'def add(a, b):\n    return a + b\n\ndef clamp(x, lo, hi):\n    return max(lo, min(x, hi))\n' > calc.py
printf 'from calc import clamp\n\ndef test_clamp():\n    assert clamp(5, 0, 3) == 3\n' > test_calc.py
gi add calc.py test_calc.py; echo "prompt: Use the commit-message skill to commit the staged changes."
