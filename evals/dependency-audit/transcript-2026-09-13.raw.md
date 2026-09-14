Done. Audit run, one direct dep vulnerable, minor bump applied, audit now clean.

**Findings (before fix)**

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | high (6 advisories, CVSS up to 8.1) | 4.18.0 (min) / 4.18.1 (npm recommended) | direct | no, minor bump |

Advisories rolled up under lodash: GHSA-r5fr-rjxr-66jc code injection via `_.template` (high), GHSA-35jh-r3h4-6jhm command injection (high), GHSA-p6mc-m468-83gw prototype pollution (high), GHSA-f23m-r3pf-42rh and GHSA-xxjr-mmjv-4gpg prototype pollution in `_.unset`/`_.omit` (moderate), GHSA-29mw-wpgm-hmr9 ReDoS (moderate). All fixed at or below 4.18.0.

**Tier 1, applied**
- `lodash` 4.17.15 → 4.18.1, exact pin kept. Chose 4.18.1 over strict minimum 4.18.0 because npm audit recommends it and it shipped one day after 4.18.0 as patch. Revert to 4.18.0 if strict minimum wanted.
- Lockfile: repo had none. Generated `package-lock.json` via `--package-lock-only`, no `node_modules` created. New file, untracked. Commit it or delete it, your call.
- Tests: no `test` script in package.json, so nothing to run.
- No `npm audit fix --force` used.

**Tier 2 / Tier 3**: none. No major bumps needed, no unfixable advisories.

**Before/after counts**

| | high | moderate | total |
|---|---|---|---|
| before | 1 | 0 | 1 |
| after | 0 | 0 | 0 |

Note: npm rewrote `package.json` to compact single-line JSON without trailing newline. Content diff is one line (`lodash` version only).

Nothing committed. Working tree: `package.json` modified, `package-lock.json` new.
