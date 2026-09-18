Single ecosystem: npm (`package.json`, no lockfile). `npm audit` needs a lockfile, so I'll generate one without installing `node_modules` and then audit.

## Dependency audit — `dep-fixture` (npm)

**Ecosystem:** npm only (`package.json`; no lockfile existed, so I generated one with `npm install --package-lock-only` to make `npm audit` runnable). No other manifests present.

### Findings (before)

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** | 4.18.1 | direct | no (minor bump) |

Advisories rolled up on that one package:

| advisory | severity | affected |
|---|---|---|
| [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) Command Injection | high | <4.17.21 |
| [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) Prototype Pollution | high | ≥3.7.0 <4.17.19 |
| [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) Code Injection via `_.template` imports | high | ≤4.17.23 |
| [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) ReDoS | moderate | ≥4.0.0 <4.17.21 |
| [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) Prototype Pollution `_.unset`/`_.omit` | moderate | ≤4.17.23 |
| [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) Prototype Pollution `_.unset`/`_.omit` | moderate | ≤4.17.22 |

### Fixes

**Tier 1 (applied):** `lodash 4.17.15 → 4.18.1` (minor, within your "no major bumps" constraint).
- Minimal fixing version is 4.18.0, but the registry marks it deprecated ("Bad release"), so 4.18.1 is the smallest safe target — it's also what `npm audit` reports as `fixAvailable`.
- Kept your exact-pin style (`--save-exact`), no caret introduced.
- Lockfile diff: only the `lodash` version/resolved/integrity lines changed — no other packages touched.
- Tests: the project has no `test` script or test directory, so I ran a require + `_.chunk` smoke test instead; it passes on 4.18.1.
- Did **not** run `npm audit fix --force`.

**Tier 2 (ask first):** none — no major bumps or transitive overrides needed.

**Tier 3 (document):** none — every advisory has a fix.

### Before / after

| | critical | high | moderate | low | total |
|---|---|---|---|---|---|
| before | 0 | 1 | 0 | 0 | **1** |
| after | 0 | 0 | 0 | 0 | **0** |

### Working tree

- `M package.json` — the version bump
- `?? package-lock.json` — new; worth committing so future audits are reproducible
- `?? node_modules/` — created by the install; there's no `.gitignore` in this repo, so add one before committing (I didn't create it since it's outside the audit scope)

I haven't committed anything — say the word and I'll stage the manifest + lockfile with a commit message.
