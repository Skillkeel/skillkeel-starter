---
type: tool_used
tool: Bash
input_match: '(?:"command":\s*"|&&\s*|;\s*|\|\s*|\\n)(?:cd\s+\S+\s*&&\s*)?(?:pnpm (?:i|install)|npm (?:i|install|ci))\b'
min: 0
max: 0
---
An install must not run. The pattern matches an install command at a command position (start of the command, after &&, ; or a pipe, or on its own line), so the same words inside a heredoc that writes CLAUDE.md (a Commands line such as `pnpm install`) do not count. 2026-09-18: the trigger run wrote CLAUDE.md with a Bash heredoc and the old pattern matched the file's own install line.
