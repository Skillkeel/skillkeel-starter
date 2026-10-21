pnpm isn't installed here and there are no `node_modules`, so I can't execute the scripts. I checked them against `package.json` and the CI workflow instead, and I'll note that in the file.

I've written `CLAUDE.md` (37 lines). None of its commands have been run yet: pnpm isn't installed on this machine and there are no `node_modules`. I checked each one against the `package.json` scripts and `.github/workflows/ci.yml` instead.

**What it contains:**
- **Project:** a TypeScript app built with Vite, tested with Vitest and linted with ESLint. Node 20 (from `.nvmrc`), pnpm 9 (from the `packageManager` field).
- **Commands:** install is `pnpm i --frozen-lockfile`, matching CI. The test command is `pnpm test:ci`, which is what CI runs. There is no plain `test` script, so the file warns that `npm test` / `pnpm test` won't work.
- **Do not:** never edit `pnpm-lock.yaml` by hand, and don't create npm or yarn lockfiles.
- **Verification:** `pnpm test:ci` and `pnpm lint` must pass before work counts as done.

**Things to check:**
- The single-test example (`pnpm test:ci src/<file>.test.ts`) is how Vitest normally filters by file. It's unverified, and the repo has no test files yet.
- There's no `pnpm-workspace.yaml`, so this is a single package rather than a monorepo. The file describes it that way.
- The commit-style rule is based on only one commit (`chore: init`).

Once pnpm is installed, run `pnpm i --frozen-lockfile && pnpm test:ci && pnpm lint` to confirm the commands. After that, the note in the file saying they haven't been run can be deleted.

Nothing has been committed. Tell me if you want any corrections.
