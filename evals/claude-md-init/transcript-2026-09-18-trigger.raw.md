Wrote `CLAUDE.md` (35 lines) at the repo root.

What it's based on:
- **Commands** come straight from `package.json` scripts (`dev`, `build`, `test:ci`, `lint`) and `.github/workflows/ci.yml` (`pnpm i --frozen-lockfile` → `pnpm test:ci`). It lists `pnpm test:ci`, not `npm test`, since that's what CI actually runs and `npm test` doesn't exist.
- **Project** facts: Node 20 from `.nvmrc`, pnpm 9 from `packageManager`.
- **Conventions**: Conventional Commits, inferred from the only commit (`chore: init`).
- **Do not**: `pnpm-lock.yaml` flagged as never hand-edited; no npm/yarn.

Two caveats, stated plainly:
- `pnpm` isn't installed here and there's no `node_modules`, so I could not execute the scripts. I verified each listed command exists by parsing `package.json` with `node` and cross-checking CI; I did not invent any. I skipped `corepack`/installs since those write to the tree.
- The "single test file" example (`pnpm test:ci src/index.test.ts`) uses standard `vitest run <file>` syntax, but no test files exist yet — adjust the path once you have one.

No `tsconfig`, `vite.config`, or ESLint config exists in the repo yet, so I didn't describe any of those. Tell me if you'd like anything changed (e.g. branch naming or PR merge style, which I couldn't detect from a single commit), and it's not committed — say the word if you want it committed.
