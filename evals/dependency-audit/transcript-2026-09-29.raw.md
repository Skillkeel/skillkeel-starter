No lockfile exists, so I'll generate one to run the audit, without installing anything.

I've applied one fix: lodash `4.17.15` → `4.18.1`. It's a minor bump, not a major one. There was 1 high-severity finding before and 0 after. There's no test suite, so nothing checked that the app still works.

The repo has one ecosystem (npm) and one dependency, lodash. There was no lockfile, so I made one with `npm install --package-lock-only --ignore-scripts` so the audit could run. Nothing was installed and no install scripts ran.

**Audit results**

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** (6 advisories: 3 high, 3 moderate) | >4.17.23 → 4.18.0 / 4.18.1 | direct | no (minor bump) |

The advisories:
- **High:** Code Injection via `_.template` imports ([GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc), ≤4.17.23)
- **High:** Command Injection ([GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm), <4.17.21)
- **High:** Prototype Pollution ([GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw), <4.17.19)
- **Moderate:** Prototype Pollution in `_.unset` / `_.omit` ([GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh), [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg))
- **Moderate:** ReDoS ([GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9))

**What I changed**
- **Why 4.18.1 and not the minimum:** the lowest version that fixes all six is 4.18.0, but npm marks it deprecated ("Bad release"). 4.18.1 is the next version, is not deprecated, and also clears the audit.
- **Pin style:** I kept the exact pin, as the original had.
- **Files:** `package.json` now says `4.18.1`, and `package-lock.json` is new. npm also collapsed the spacing in `package.json`, so the diff is noisier than the actual change.
- **Before/after:** `npm audit` went from high 1, total 1 to 0 vulnerabilities.

**Held back**
- **Major bumps or overrides:** none were needed.
- **Unfixable findings:** none, so nothing needs documenting in `SECURITY.md`.

**Needs your attention**
- **Behaviour check:** 4.18 is a new minor line after years of 4.17.x, so I'd try the code paths that use lodash before shipping.
- **Not committed:** to undo, run `git checkout package.json && rm package-lock.json`.
