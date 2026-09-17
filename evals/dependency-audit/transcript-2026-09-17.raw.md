No lockfile is present, so `npm audit` can't run yet. I'll generate one without touching `node_modules` (`--package-lock-only`), then audit.

## Dependency audit — `dep-fixture` (npm)

**Ecosystem:** npm only (`package.json`, 1 direct dep). No lockfile existed, so I generated one with `npm install --package-lock-only` (no `node_modules` written) so `npm audit` could run.

### Findings (before)

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** (4 high, 2 moderate advisories) | 4.18.1 | direct | no — minor bump |

Advisories:
- high — Command Injection (`<4.17.21`) [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm)
- high — Prototype Pollution (`<4.17.19`) [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw)
- high — Code Injection via `_.template` imports (`<=4.17.23`) [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc)
- moderate — ReDoS (`<4.17.21`) [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9)
- moderate — Prototype Pollution in `_.unset`/`_.omit` (`<=4.17.23`) [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh)
- moderate — Prototype Pollution in `_.unset`/`_.omit` (`<=4.17.22`) [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg)

### Fixes

**Tier 1 (applied):** `lodash 4.17.15 → 4.18.1` via `npm install lodash@4.18.1 --save-exact` (kept the manifest's exact-pin style; no `--force`). Lockfile diff is just the lodash `version`/`resolved`/`integrity` lines — no other packages changed.

**Tier 2 (ask first):** none — no major bumps or overrides needed.

**Tier 3 (unfixable):** none.

### Before / after
- Before: `high: 1, total: 1`
- After: `total: 0` — `npm audit` reports **0 vulnerabilities**

### Caveats
- **Tests:** `package.json` has no `test` script, so I couldn't run a suite to validate the bump. 4.18.x is a minor release and the lodash changelog is security/bug fixes, but if this fixture stands in for real code, a smoke test before merging is worth doing.
- `package-lock.json` is new and untracked — commit it alongside the `package.json` change if you want the audit to be reproducible in CI.

Working tree: `M package.json`, `?? package-lock.json`. Nothing committed.
