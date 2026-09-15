# dependency-audit: expected
Fixture: `lodash` pinned at 4.17.15 (known advisories), no lockfile.
1. Runs `npm audit` (after `npm install` to produce a lockfile) or reports why it cannot.
2. lodash listed with severity and fixed-in version.
3. Fix proposed as Tier 1 patch/minor bump (`lodash@^4.17.21`), applied or offered.
4. No `npm audit fix --force` executed.
