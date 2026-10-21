No scanner installed; grep fallback, masking output.

I scanned the working tree and full git history, and nothing was rewritten or force-pushed. One credential file turned up: a `.env` file that was committed and later deleted. It's no longer in the current files but is still in git history.

Neither gitleaks nor trufflehog is installed, so I used the skill's fallback: a grep over `git log -p --all` with its pattern set, plus a check for sensitive filenames that were ever added.

## Findings

| Path | First commit (sha, date, author) | Still in HEAD? | Type | Classification |
|---|---|---|---|---|
| `.env` → `AWS_ACCESS_KEY_ID=AKIA****LE` | `8f3ac46` (2026-10-21 13:08 +0200, fixture) "chore: add env" | No: removed in `6ea2c47` | AWS access key ID | **Only in history (high)** |
| `.env` → `AWS_SECRET_ACCESS_KEY=wJal****EY` | `8f3ac46` (same) | No: removed in `6ea2c47` | AWS secret access key | **Only in history (high)** |

**Notes**
- The current files are clean, and `.gitignore` now contains `.env`.
- Both values match the **AWS documentation example key pair** (the placeholder ID ending in `…LE` and the secret ending in `…EY`). If that's all they are, they're harmless. Still, a real `.env` was committed, so treat it as a real leak unless you can confirm these were never real credentials.
- Nothing else matched (no private keys, GitHub/Slack/OpenAI-style tokens, JWTs, or `.pem`/`.p12`/`id_rsa` files).

## Remediation checklist
1. [ ] **Rotate first.** In AWS IAM, deactivate and delete the access key ending `…LE` and create a new one, unless you're sure it's only the documentation placeholder. Anything ever committed counts as exposed, even after a purge. Check CloudTrail for use of that key.
2. [x] **Remove from HEAD.** Already done in `6ea2c47`, and `.env` is gitignored. Keep credentials in the environment or a local `.env` only.
3. [ ] **Purge history only if the repo is or will be public or shared.** I did not run this, as you asked:
   ```
   git filter-repo --path .env --invert-paths
   git push --force-with-lease --all
   ```
   After that, collaborators need to re-clone. This needs your explicit go-ahead.
4. [ ] **Prevention.**
   - Install gitleaks and add a pre-commit hook: `gitleaks git --pre-commit --staged .`
   - Keep the `secret-scan` hook enabled.
   - Consider adding `*.pem`, `*.p12` and `id_rsa` to `.gitignore`.
