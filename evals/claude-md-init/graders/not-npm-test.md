---
type: regex
target: {source: file, path: CLAUDE.md}
pattern: '(?:^|\n)(?![^\n]*\b(?:[Nn]o|[Nn]ot|[Nn]ever|[Dd]on.t|[Ii]nstead of|[Aa]void)\b)[^\n]*\bnpm test\b'
match: not_contains
---
CLAUDE.md must not offer `npm test` as a command. A line that names it only to rule it out ("There is no `test` script, so `npm test` will not work") passes; any other line with `npm test` fails. 2026-09-29 on Claude Code 2.1.284: the file listed `pnpm test:ci` and warned against `npm test` on its own line, and the old pattern (any `npm test`) failed it.
