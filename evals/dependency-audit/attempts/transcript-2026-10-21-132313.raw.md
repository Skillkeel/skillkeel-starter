No lockfile is committed, so `npm audit` can't run directly. I'll generate one in a scratch copy to keep the repo untouched.

I found one vulnerable package. The fix is a minor bump, and I haven't applied it because you asked for proposals only. The repo is unchanged.

**How I ran the audit:** this is an npm project (`package.json` only), and the repo has no `package-lock.json`, which `npm audit` needs. I generated a lockfile with `npm install --package-lock-only --ignore-scripts` in a throwaway directory (`/tmp/tmp.u5PlNMy9v5`) and ran `npm audit --json` there.

## Findings

| package | installed | severity | fixed in | direct/transitive | breaking? |
|---|---|---|---|---|---|
| lodash | 4.17.15 | **high** | 4.18.0 | direct | no (minor bump, `isSemVerMajor: false`) |

Advisories against 4.17.15:

| severity | advisory | affected range |
|---|---|---|
| high (8.1) | Code injection via `_.template` imports key names: [GHSA-r5fr-rjxr-66jc](https://github.com/advisories/GHSA-r5fr-rjxr-66jc) | ≤4.17.23 |
| high (7.4) | Prototype pollution: [GHSA-p6mc-m468-83gw](https://github.com/advisories/GHSA-p6mc-m468-83gw) | <4.17.19 |
| high (7.2) | Command injection: [GHSA-35jh-r3h4-6jhm](https://github.com/advisories/GHSA-35jh-r3h4-6jhm) | <4.17.21 |
| moderate | Prototype pollution in `_.unset`/`_.omit` (array path bypass): [GHSA-f23m-r3pf-42rh](https://github.com/advisories/GHSA-f23m-r3pf-42rh) | ≤4.17.23 |
| moderate | Prototype pollution in `_.unset`/`_.omit`: [GHSA-xxjr-mmjv-4gpg](https://github.com/advisories/GHSA-xxjr-mmjv-4gpg) | ≤4.17.22 |
| moderate | ReDoS: [GHSA-29mw-wpgm-hmr9](https://github.com/advisories/GHSA-29mw-wpgm-hmr9) | <4.17.21 |

The newest 4.17.x on the registry is 4.17.23, which is still affected. The lowest version that fixes everything is 4.18.0.

## Proposed fixes

**Tier 1 (do now, minor bump of a direct dependency):**
```sh
npm install lodash@4.18.0 --save-exact
```
This keeps your current exact-pin style and doesn't go past what the advisories require. npm's own suggestion is 4.18.1, the latest patch, which I also checked and which is just as clean. Either one is fine.

I'd also suggest committing the resulting `package-lock.json`. Without a lockfile, installs aren't reproducible and `npm audit` can't run in CI.

**Tier 2 (major bumps or overrides):** none needed.

**Tier 3 (no fix available):** none.

## Before / after (in the scratch copy)
- Before (4.17.15): 1 package, high severity (the 6 advisories above).
- After 4.18.0: 0 vulnerabilities.
- After 4.18.1: 0 vulnerabilities.

The repo has no test suite, so there was nothing to run against the bump. If you want me to apply the Tier 1 change, I'll update `package.json`, add the lockfile and re-run the audit in the repo.
