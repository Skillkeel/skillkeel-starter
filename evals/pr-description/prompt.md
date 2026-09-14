---
name: pr-description
tags: [starter]
runs: 1
max_turns: 12
timeout_seconds: 600
allowed_tools: [Read, Bash, Glob, Grep, Skill]
---

Use the pr-description skill to write the PR description for this branch against main. Do not open a PR, just output the markdown.
