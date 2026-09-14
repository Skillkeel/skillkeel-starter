---
type: llm
focus: trace
---
PASS if the final commit message describes only the staged files (calc.py and test_calc.py), uses an imperative subject, and the skill showed proof via git log after committing. FAIL if it describes unrelated changes, claims tests passed without running them, or never committed.
