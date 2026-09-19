Single npm ecosystem, one pinned direct dep (`lodash@4.17.15`), no lockfile. `npm audit` needs a lockfile, so I'll generate one without installing `node_modules`.

All six advisories are patched only in `>=4.18.0`; `4.17.23` is the last 4.17.x and is still vulnerable to two of them. Checking whether 4.18.0 exists so I bump only as far as the advisories require.

npm reflowed the one-line `package.json`; I'll restore the original formatting so the diff is just the version.

## Dependency audit — `dep-fixture` (npm)

**Ecosystem:** npm only (`package.json`, 1 direct dep, no lockfile). Tool: `npm audit` 11.16.0. No other manifests present.

Note: the repo had no lockfile, which `npm audit` requires, so I generated `package-lock.json` with `--package-lock-only` (no `node_modules` installed, no scripts run).

### Findings (before)

| package | installed | severity | advisory | vulnerable range | fixed in | direct? | breaking? |
|---|---|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** 8.1 | [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) Code injection via `_.template` | ≥4.0.0 ≤4.17.23 | 4.18.0 | direct | no (minor) |
| lodash | 4.17.15 | **high** 7.4 | [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) Prototype pollution | ≥3.7.0 <4.17.19 | 4.17.19 | direct | no |
| lodash | 4.17.15 | **high** 7.2 | [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) Command injection | <4.17.21 | 4.17.21 | direct | no |
| lodash | 4.17.15 | moderate 5.3 | [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) ReDoS | ≥4.0.0 <4.17.21 | 4.17.21 | direct | no |
| lodash | 4.17.15 | moderate | [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) Proto pollution `_.unset`/`_.omit` (array path) | ≤4.17.23 | 4.18.0 | direct | no |
| lodash | 4.17.15 | moderate | [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) Proto pollution `_.unset`/`_.omit` | ≥4.0.0 ≤4.17.22 | 4.17.23 | direct | no |

npm rolls these up as **1 high** vulnerability (all in the single `lodash` package).

### Fix tiers

**Tier 1 — applied:** `lodash 4.17.15 → 4.18.1` (minor bump, `isSemVerMajor: false`).
- Why 4.18.1 and not something smaller: the newest advisory (GHSA-r5fr-rjxr-66jc) covers every 4.17.x including 4.17.23, so nothing in the 4.17 line is clean. `4.18.0` is the first patched release but is **deprecated on the registry** ("Bad release. Please use lodash@4.17.21 instead."), so 4.18.1 is the minimal non-deprecated fix — exactly what `npm audit` reports as `fixAvailable`.
- Applied with `npm install --save-exact lodash@4.18.1` to keep the exact-pin style. I restored `package.json`'s original single-line formatting afterwards so the diff is one token.
- Tests: `package.json` has no `scripts` / no test suite, so there was nothing to run. Flagging that as a gap, not a pass.
- Did **not** use `npm audit fix --force`.

**Tier 2 — none needed.** No major bumps or transitive overrides required; lodash has no dependencies of its own.

**Tier 3 — none.** Every advisory has a fix.

### Before / after

| | info | low | moderate | high | critical | total |
|---|---|---|---|---|---|---|
| before | 0 | 0 | 0 | 1 | 0 | **1** |
| after | 0 | 0 | 0 | 0 | 0 | **0** |

### Working-tree changes (uncommitted)

```
 M package.json        lodash "4.17.15" → "4.18.1"
?? package-lock.json   new, 21 lines, 1 package: lodash@4.18.1
                       resolved https://registry.npmjs.org/lodash/-/lodash-4.18.1.tgz
                       integrity sha512-dMInicTPVE8d1e5otfwmmjlxkZoUpiVLwyeTdUsi/Caj/gfzzblBcCE5sRHV/AsjuCmxWrte2TNGSYuCeCq+0Q==
```

Recommend committing the lockfile alongside the bump so future audits are reproducible. Say the word if you want me to commit, or revert if you'd rather keep the fixture pinned.
