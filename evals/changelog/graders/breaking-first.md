---
type: regex
target: {source: file, path: CHANGELOG.md}
pattern: '### Added\s*\n- \*\*BREAKING'
match: contains
weight: 2
---
