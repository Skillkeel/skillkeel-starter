# claude-md-init: expected
Fixture: pnpm project, CI runs `pnpm test:ci`, `.nvmrc`=20, `pnpm-lock.yaml` present.
1. CLAUDE.md written, ≤ 100 lines.
2. Test command listed is `pnpm test:ci` (not `npm test`, not `pnpm test`).
3. Node 20 mentioned (from .nvmrc).
4. `pnpm-lock.yaml` listed under do-not-edit-by-hand.
5. No invented commands (every listed script exists in package.json).
