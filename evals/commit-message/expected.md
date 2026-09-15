# commit-message: expected
Fixture: repo with two new staged Python files (`calc.py`, `calc2.py`), no CLAUDE.md, no git identity.
Assertions:
1. Subject uses a Conventional Commits type matching the diff (`feat`), ≤ 50 chars, imperative, no trailing period.
2. Message describes only staged files.
3. No Co-Authored-By / tool trailer unless asked.
4. Skill shows `git log -1 --stat` (or equivalent proof) after commit.
