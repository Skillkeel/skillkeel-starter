CLAUDE.md written. 64 lines. Uncommitted.

**What verified:**
- `pnpm run` listing (via `npx pnpm@9.0.0`): dev, build, test:ci, lint. pnpm not on PATH here.
- `pnpm i --frozen-lockfile` exit 0. But it rewrote `pnpm-lock.yaml` (added empty `importers`). Reverted with git checkout.
- `pnpm test:ci` and `pnpm lint` fail: `vitest: command not found`, `eslint: command not found`. Reason: `package.json` has zero dependencies declared. Documented as known gap, not hidden.

**File contents:**
- Project: Node 20, pnpm 9.0.0, Vite + TS stub.
- Commands table, pnpm only, `npx pnpm@9.0.0` fallback.
- CI section mirrors `ci.yml`: install frozen, then `pnpm test:ci` (not `npm test`).
- Do-not: hand-edit lockfile, run `npm install`.
- Verification: `pnpm i --frozen-lockfile && pnpm test:ci`.

**Next:** add `vite`, `vitest`, `eslint` to `devDependencies` and commit regenerated lockfile, else CI red. Review CLAUDE.md, commit when happy.
