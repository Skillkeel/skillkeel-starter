Wrote `<workdir>/CLAUDE.md` (41 lines).

What it's based on:
- `package.json` scripts: `dev`, `build`, `test:ci` (`vitest run`), `lint` — pnpm 9 via `packageManager`, Node 20 from `.nvmrc`
- `.github/workflows/ci.yml`: `pnpm i --frozen-lockfile` → `pnpm test:ci`, so the file uses `pnpm test:ci` (there is no `npm test`/`test` script)
- `pnpm-lock.yaml` listed under **Do not** hand-edit
- Layout is just `src/index.ts`; conventions note Conventional Commits from the single `chore: init` commit

One caveat, also noted inside the file: `pnpm` (and `corepack`) isn't installed on this machine, so I couldn't execute `pnpm run` to list scripts live — I verified them by reading `package.json` and the CI workflow instead. If you install pnpm and want that note removed, say so and I'll drop it. The "single test" line and "colocate `*.test.ts`" convention are inferred from Vitest defaults since no tests exist yet — correct them if your layout differs.
