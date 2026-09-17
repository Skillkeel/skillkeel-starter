No gitleaks or trufflehog installed — falling back to the grep-based scan over full history.

# Secret audit — `secret-audit` repo

**Scanner:** neither `gitleaks` nor `trufflehog` is installed, so I used the fallback grep pattern set over `git log -p --all` plus the sensitive-filename check. 4 commits, 1 branch (`main`), no remotes configured.

## Findings

| # | Path | Introduced | Removed | Still in HEAD? | Type | Value (masked) | Classification |
|---|------|-----------|---------|----------------|------|----------------|----------------|
| 1 | `.env` → `AWS_ACCESS_KEY_ID` | `b153a6d` · 2026-09-17 · fixture <fixture@skillkeel.com> ("chore: add env") | `e37d6fe` ("chore: remove env") | **No** | AWS access key ID (`AKIA…`, 20 chars) | `AKIA…LE` | **Only in history (high)** — note: matches the AWS documentation sample key |
| 2 | `.env` → `AWS_SECRET_ACCESS_KEY` | `b153a6d` (same commit) | `e37d6fe` | **No** | AWS secret access key (40 chars) | `wJal…EY` | **Only in history (high)** — note: matches the AWS documentation sample secret |

Working tree: clean, no hits. `.env` is deleted from HEAD and `.gitignore` now contains `.env` (added in `e37d6fe`). No other patterns (Stripe/Anthropic `sk-*`, GitHub `gh*_`, Slack `xox*`, private keys, JWTs, generic `password=`/`token=`) matched anywhere in history.

**Caveat on classification:** both values are byte-for-byte the well-known AWS docs placeholders, which would normally make this a *false positive / example* note rather than a real leak. I'm reporting it at the history-only severity anyway because (a) the file is a real `.env`, not a doc or test fixture, and (b) the skill's job is to flag what's in history — you know better than I do whether a real key ever sat in that file locally. If these were never real credentials, items 1 and 3 below are no-ops.

## Remediation checklist (rotate first, then purge)

- [ ] **1. Rotate.** If the key pair in `b153a6d` was ever a real IAM credential, deactivate and delete it in IAM (`aws iam update-access-key --status Inactive` → `delete-access-key`) and issue a new one. A committed credential is compromised even after purge. *(Skip if it truly was only the AWS sample key.)*
- [x] **2. Remove from HEAD.** Already done — `.env` deleted and gitignored in `e37d6fe`. Nothing further needed here.
- [ ] **3. Purge history (only if this repo is or will be public/shared).** Not executed, per your instruction and the skill's rules. If you later want it, the command would be:
  ```
  git filter-repo --path .env --invert-paths
  ```
  followed by `git push --force-with-lease` on every remote and telling collaborators to re-clone. This currently has no remote, so there is nothing to force-push; the exposure so far is limited to this local clone and any copies of it.
- [ ] **4. Prevention.**
  - `.gitignore` already covers `.env`; consider adding `.env.*`, `*.pem`, `*.p12` too.
  - Install gitleaks and add a pre-commit hook: `gitleaks git --pre-commit --staged .` (on gitleaks < 8.19: `gitleaks protect --staged`).
  - The Skillkeel `secret-scan` hook is already active in this session and blocks credential-shaped writes going forward.

No history was rewritten and nothing was force-pushed.
