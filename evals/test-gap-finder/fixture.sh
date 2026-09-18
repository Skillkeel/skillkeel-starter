#!/usr/bin/env bash
set -e; . "$(dirname "$0")/../_lib.sh"; newrepo "${1:-}"
mkdir -p pkg tests
printf 'def slugify(s):\n    return s.lower().replace(" ", "-")\n' > pkg/utils.py
printf 'import hashlib\n\ndef hash_password(p, salt):\n    return hashlib.sha256((salt + p).encode()).hexdigest()\n\ndef verify(p, salt, h):\n    return hash_password(p, salt) == h\n' > pkg/auth.py
printf 'def charge(amount_cents, currency="EUR"):\n    if amount_cents <= 0:\n        raise ValueError("amount must be positive")\n    return {"amount": amount_cents, "currency": currency}\n' > pkg/payments.py
printf 'from pkg.utils import slugify\n\ndef test_slugify():\n    assert slugify("A B") == "a-b"\n' > tests/test_utils.py
touch pkg/__init__.py; gi add -A; gi commit -qm "feat: initial"
for i in 1 2 3; do echo "# rev $i" >> pkg/auth.py; gi add -A; gi commit -qm "fix(auth): tweak $i"; done
echo "prompt: Use the test-gap-finder skill. Do not write tests, only propose."; echo "trigger: What should we test next in this repo? Do not write tests, only propose."
