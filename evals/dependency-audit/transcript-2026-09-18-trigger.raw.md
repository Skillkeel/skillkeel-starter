This matches the `dependency-audit` skill, so I'll invoke it.

## Dependency audit — npm (`package.json`)

Only one ecosystem present (npm, `lodash` as the sole direct dep). The repo had no lockfile, so I generated `package-lock.json` with `npm install --package-lock-only` (no `node_modules` written) to let `npm audit` run.

### Findings (before)

| package | installed | severity | advisory | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** (8.1) | [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) — code injection via `_.template` | >4.17.23 | direct | no (minor) |
| lodash | 4.17.15 | **high** (7.4) | [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) — prototype pollution | ≥4.17.19 | direct | no |
| lodash | 4.17.15 | **high** (7.2) | [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) — command injection | ≥4.17.21 | direct | no |
| lodash | 4.17.15 | moderate (6.5) | [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) — proto pollution in `_.unset`/`_.omit` | >4.17.23 | direct | no |
| lodash | 4.17.15 | moderate (6.5) | [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) — proto pollution in `_.unset`/`_.omit` | ≥4.17.23 | direct | no |
| lodash | 4.17.15 | moderate (5.3) | [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) — ReDoS | ≥4.17.21 | direct | no |

Outdated: `lodash` 4.17.15 → latest 4.18.1.

### Tier 1 (applied) — minor bump, no major

- `lodash` **4.17.15 → 4.18.1** (pinned exact, matching the existing style). Every advisory above is resolved at >4.17.23. 4.18.0 is the strict minimum, but npm marks it deprecated ("Bad release"), so 4.18.1 is the correct target.
- `package.json` diff is the single version-string change; `package-lock.json` is new and resolves `lodash@4.18.1` (`sha512-dMInic…`).
- **Tests: not run** — `package.json` has no `scripts.test` and there is no test suite in the repo, so there was nothing to execute.

### Tier 2 / Tier 3
Nothing — no major bumps needed, no transitive deps, no unfixable advisories.

### Audit before/after
- Before: **1 high** (6 advisories rolled into one package), 0 others
- After: **0 vulnerabilities** (`npm audit` clean, `npm outdated` empty)

### For you to decide
- `package-lock.json` is untracked. I'd recommend committing it alongside the `package.json` change so audits are reproducible; delete it if this repo deliberately goes lockfile-less.
- Nothing has been committed.
