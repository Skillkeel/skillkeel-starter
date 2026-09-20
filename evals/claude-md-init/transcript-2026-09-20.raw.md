Wrote `CLAUDE.md` (38 lines).

**What it captures**
- Stack: Vite + TypeScript, Node 20, pnpm 9.0.0 — from `.nvmrc` and `package.json`.
- Commands: `pnpm i --frozen-lockfile`, `pnpm dev`, `pnpm test:ci`, `pnpm lint`, `pnpm build`, plus an explicit note that there is no `test` script so `pnpm test` won't work — CI runs `pnpm test:ci`.
- Layout: `src/` and the CI workflow.
- Do-not list: hand-editing `pnpm-lock.yaml`, unfrozen installs, changing `packageManager`/`.nvmrc`.
- Verification: `pnpm lint` and `pnpm test:ci`.

**One caveat:** the skill asks that every listed command be executed or dry-run, but `pnpm` isn't on this machine's PATH and there's no `node_modules`, so I couldn't run `pnpm run` to list scripts. I sourced every command by reading `package.json` and `ci.yml` instead. If you want them exercised, install pnpm (`corepack enable`) and run `pnpm i --frozen-lockfile && pnpm lint && pnpm test:ci` — if any of those fail, tell me and I'll drop or fix the entry.
