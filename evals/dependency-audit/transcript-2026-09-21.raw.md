Single ecosystem: npm (`package.json`, no lockfile, no `node_modules`). `npm audit` requires a lockfile, so I'll generate one without installing anything.

`npm install` reformatted `package.json` to one line; restoring the original formatting with just the version changed.

## Dependency audit — `dep-fixture`

**Ecosystem:** npm only (`package.json`; no lockfile or `node_modules` present). Tool: `npm audit` 11.16.0. Since `npm audit` needs a lockfile, I generated one with `npm install --package-lock-only --ignore-scripts` (nothing installed, no scripts run).

### Findings (before)

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** (6 advisories, max CVSS 8.1) | 4.18.1 | direct | no — minor bump (`isSemVerMajor: false`) |

Advisories on 4.17.15:
- [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) high 8.1 — Code injection via `_.template` (≤4.17.23)
- [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) high 7.4 — Prototype pollution (<4.17.19)
- [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) high 7.2 — Command injection (<4.17.21)
- [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) moderate 6.5 — Prototype pollution in `_.unset`/`_.omit` (≤4.17.23)
- [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) moderate 6.5 — Prototype pollution in `_.unset`/`_.omit` (≤4.17.22)
- [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) moderate 5.3 — ReDoS (<4.17.21)

### Fixes

**Tier 1 (applied — minor bump, direct dep):** `lodash 4.17.15 → 4.18.1` (registry `latest`, verified). Pinned exact to match the existing style.
- `package.json`: `"lodash": "4.17.15"` → `"4.18.1"`
- `package-lock.json` (new file): lodash version/resolved/integrity updated; no other entries changed.
- Tests: the project has no `test` script and no test files, so there was nothing to run — treat that as unverified, not passing.

**Tier 2 (ask first):** none — no major bumps or overrides needed.
**Tier 3 (no fix available):** none.

### Before / after

| | info | low | moderate | high | critical | total |
|---|---|---|---|---|---|---|
| before | 0 | 0 | 0 | 1 | 0 | **1** |
| after | 0 | 0 | 0 | 0 | 0 | **0** |

`npm audit fix --force` was not used. Working tree now has `M package.json` and a new untracked `package-lock.json` — nothing committed. If you'd rather keep this proposal-only, `git checkout package.json && rm package-lock.json` reverts it; otherwise I'd suggest committing the lockfile alongside the bump so future audits don't need to regenerate it.
