No gitleaks/trufflehog available, so falling back to grep over full history.

## Secret audit — `<workdir>`

**Tooling:** neither `gitleaks` nor `trufflehog` is installed, so I used the grep fallback over `git log -p --all` plus the sensitive-filename check. No history was rewritten and nothing was force-pushed.

### Findings

| # | Path | Introduced (sha, date, author) | Removed | Still in HEAD? | Type | Value (masked) | Classification |
|---|------|-------------------------------|---------|----------------|------|----------------|----------------|
| 1 | `.env` | `302cde5`, 2026-09-19, fixture ("chore: add env") | `2a9fba8` ("chore: remove env") | No | AWS access key ID (`AWS_ACCESS_KEY_ID`) | `AKIA****LE` | **Only in history (high)** — note: this matches the AWS documentation example access key |
| 2 | `.env` | `302cde5`, 2026-09-19, fixture | `2a9fba8` | No | AWS secret access key (`AWS_SECRET_ACCESS_KEY`) | `wJal****EY` | **Only in history (high)** — note: this matches the AWS documentation example secret key |

Other checks, all clean:
- Working tree / HEAD: only `app.py`, `README.md`, `.gitignore` — no credentials.
- No `*.pem`, `*.p12`, `id_rsa` files ever added.
- No OpenAI/Anthropic, GitHub, Slack, JWT, private-key, or generic `password=`/`token=` matches anywhere in history.
- `.gitignore` already contains `.env` (added in `2a9fba8`).

**Caveat on the notes:** both values are byte-for-byte the well-known AWS docs placeholder pair. If these were pasted from AWS docs as a sample, they are a false positive and steps 1 and 3 below are unnecessary. If you're not certain that's what happened, treat them as real.

### Remediation checklist (rotate first, then purge)

- [ ] **1. Rotate** — if this key pair was ever real, deactivate/delete it in IAM and issue a new one. A credential is compromised once committed, regardless of later deletion from the tree.
- [ ] **2. Remove from HEAD** — already done: `.env` was deleted in `2a9fba8` and `.env` is gitignored. Nothing further needed here.
- [ ] **3. Purge history** (only if the repo is or will be public/shared — requires your explicit approval, I have *not* run this):
  ```bash
  git filter-repo --path .env --invert-paths
  git push --force-with-lease --all && git push --force-with-lease --tags
  ```
  Then tell collaborators to re-clone (existing clones still hold `302cde5`).
- [ ] **4. Prevention**
  - Keep `.env` in `.gitignore` (✅ already present); consider adding `.env.*`, `*.pem`, `*.p12`.
  - Add a pre-commit hook: `gitleaks git --pre-commit --staged .` (install gitleaks first — it isn't on this machine).
  - The Skillkeel `secret-scan` hook is active in this session and will block credential-bearing writes going forward.
