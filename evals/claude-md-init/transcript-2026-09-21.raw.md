Wrote `CLAUDE.md` (49 lines) at `<workdir>/CLAUDE.md`.

What it's based on:
- `package.json` scripts: `dev`, `build`, `test:ci` (`vitest run`), `lint` (`eslint .`), `packageManager: pnpm@9.0.0`
- `.github/workflows/ci.yml`: `pnpm i --frozen-lockfile` → `pnpm test:ci`
- `.nvmrc`: Node 20; `pnpm-lock.yaml` v9 flagged as do-not-hand-edit
- Git history: single `chore: init` commit → Conventional Commits noted

One caveat: `pnpm` (and `corepack`) aren't installed here and `node_modules` is absent, so I couldn't execute the scripts. I verified them by reading the manifest with `node -e` rather than running `pnpm run`. The single-test example (`pnpm test:ci src/index.test.ts`) uses Vitest's standard file-filter syntax but there's no test file in the repo yet, so it's illustrative. If you want it trimmed further or want a section removed, tell me which.
