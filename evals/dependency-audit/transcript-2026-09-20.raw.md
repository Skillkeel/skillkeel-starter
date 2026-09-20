Single npm ecosystem, no lockfile. `npm audit` needs one, so I'll generate a lockfile without installing (`--package-lock-only`) and audit.

4.18.0 is deprecated as a bad release, so 4.18.1 is the minimum clean fix. It's a minor bump (4.17 → 4.18, not major), so it's Tier 1 — applying it now.

npm rewrote the spec to `^4.18.1` and collapsed the JSON formatting; the original was an exact pin on one line. Restoring that style so the diff stays minimal.

## Dependency audit — `dep-fixture`

**Ecosystem:** npm only (`package.json`; no lockfile was committed, so I generated one with `npm install --package-lock-only` to make `npm audit` runnable). No Python/Rust/Go/Ruby/PHP manifests.

### Findings (before)

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** (6 advisories) | 4.18.1 | direct | no (minor bump) |

Advisories rolled up into that one entry:

| advisory | title | severity | CVSS | vulnerable range |
|---|---|---|---|---|
| [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) | Code injection via `_.template` import key names | high | 8.1 | ≤4.17.23 |
| [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) | Prototype pollution | high | 7.4 | <4.17.19 |
| [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) | Command injection | high | 7.2 | <4.17.21 |
| [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) | Prototype pollution via array path in `_.unset`/`_.omit` | moderate | 6.5 | ≤4.17.23 |
| [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) | Prototype pollution in `_.unset`/`_.omit` | moderate | 6.5 | ≤4.17.22 |
| [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) | ReDoS | moderate | 5.3 | <4.17.21 |

### Fix tiers

**Tier 1 (applied):** `lodash 4.17.15 → 4.18.1`, a minor bump.
- Why 4.18.1 and not something smaller: every 4.17.x release (through 4.17.23) is still inside the ≤4.17.23 ranges above, and `4.18.0` is deprecated on the registry ("Bad release. Please use lodash@4.17.21 instead."). 4.18.1 is therefore the lowest clean version that clears all six advisories.
- Kept your exact-pin style (`"4.18.1"`, not `^4.18.1`) and the original one-line `package.json` formatting; npm had rewritten both, so I reverted that.
- Lockfile diff: only the `lodash` entry changed (version, `resolved`, `integrity`). No transitive deps — lodash has none.
- Tests: `package.json` has no `scripts`, so there was no test suite to run. Nothing to verify beyond the audit.
- No `npm audit fix --force` used.

**Tier 2 (major bumps / overrides):** none needed — nothing here requires a major bump, so nothing to ask about.

**Tier 3 (no fix available):** none.

### Before / after

| | critical | high | moderate | low | total |
|---|---|---|---|---|---|
| before | 0 | 1 | 0 | 0 | **1** |
| after | 0 | 0 | 0 | 0 | **0** |

### Working tree

- `M package.json` — the one-line version change
- `?? package-lock.json` — newly generated; worth committing so future audits and installs are reproducible

Nothing is committed. Say the word if you want me to commit these two files.
