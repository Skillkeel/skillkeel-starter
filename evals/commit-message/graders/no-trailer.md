---
type: regex
target: trace
pattern: 'Co-Authored-By:|Generated with \['
match: not_contains
---
PASS: no tool attribution trailer was added.
