---
name: Hook report
about: A guard blocked something it should not have, or let something through
title: "[guard-bash|secret-scan] "
labels: bug
---

**Command or file write** (exact text):

**What the hook said** (the message Claude showed, or "nothing, it ran"):

**Expected** (blocked / allowed, and why):

**Versions**: Claude Code (`claude --version`), plugin (`.claude-plugin/plugin.json`)

**Reproduction** (optional, copy the output):
```
printf '{"tool_name":"Bash","tool_input":{"command":"..."}}' | bash hooks/guard-bash; echo "exit=$?"
```
