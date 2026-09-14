---
type: regex
target: trace
pattern: '(?:feat|fix|refactor|perf|docs|test|build|ci|chore)(?:\([\w./-]+\))?: [^\n"]{1,50}'
match: contains
weight: 2
---
PASS: a Conventional Commits subject (type, optional scope, ≤50 chars) appears in the run.
