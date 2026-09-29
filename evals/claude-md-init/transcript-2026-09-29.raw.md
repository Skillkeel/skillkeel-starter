I wrote `CLAUDE.md` (38 lines), but none of the commands in it have been run. pnpm isn't installed on this machine and there's no `node_modules`. The skill requires running each command first. The only other way to check them was to install dependencies, which would change the repo, so I didn't.

So the commands are taken as written from `package.json` scripts and `.github/workflows/ci.yml`:

- **Commands:** `pnpm i --frozen-lockfile`, `pnpm dev`, `pnpm test:ci`, `pnpm lint`, `pnpm build`. The file also says there's no `test` script, so `pnpm test` or `npm test` will fail; use `pnpm test:ci`, which is what CI runs.
- **Single-test example:** `pnpm test:ci src/path/to/file.test.ts` is a guess based on how Vitest takes file filters. The repo has no test files yet, so this one is the least certain.
- **Do not:** hand-edit `pnpm-lock.yaml`, since CI installs with `--frozen-lockfile`, and don't mix package managers.
- **Verification:** `pnpm lint && pnpm test:ci`.
- **Versions:** Node 20 from `.nvmrc` and pnpm 9.0.0. The Node installed here is v22.23.1, which doesn't match.
- **Conventions:** Conventional Commits and `main` as the default branch. That's thin, because the history is a single `chore: init` commit.

To check the commands, run `corepack enable && pnpm i --frozen-lockfile && pnpm lint && pnpm test:ci` and tell me what to fix. The file isn't committed.

Separately, the Google Drive, HyperFrames by HeyGen and Notion connectors need to be authorized in your claude.ai connector settings before they'll work.
