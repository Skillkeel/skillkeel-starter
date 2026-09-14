---
type: llm
focus: {source: file, path: CLAUDE.md}
---
PASS if the file is under 100 lines, mentions Node 20 or .nvmrc, and lists pnpm-lock.yaml as something not to edit by hand. FAIL otherwise.
