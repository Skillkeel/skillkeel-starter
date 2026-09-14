---
name: dependency-audit
tags: [starter]
runs: 1
max_turns: 15
timeout_seconds: 600
allowed_tools: [Read, Bash, Glob, Grep, Write, Edit, Skill]
---

Use the dependency-audit skill on this repo. Network is allowed. Apply safe patch or minor bumps; do not apply major bumps.
