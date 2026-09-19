Both real scripts work. Applying the factual fixes now.

## README audit — findings

| line | claim | reality | fix |
|---|---|---|---|
| 8 | `npm run start` | No `start` script in `package.json`; only `dev` (`node server.js`) and `test` | Changed to `npm run dev` (verified: runs, prints `hi`) |
| 13 | Link to `docs/api.md` | No `docs/` directory exists | Dead link — kept the section, marked `<!-- TODO: verify -->` (can't invent the doc) |
| — | No Test section | `npm test` (`node --test`) exists and exits 0 | Added a minimal **Test** section |
| 17 | License: MIT | No `LICENSE` file and no `license` field in `package.json` | Left as-is (unverifiable, not provably wrong) — worth adding a `LICENSE` file if MIT is intended |

## Diff applied

```diff
-npm run start
+npm run dev
 ...
 ## Docs
+<!-- TODO: verify -->
 See [API docs](docs/api.md).
+
+## Test
+
+```
+npm test
+```
```

Title, description, and License prose are untouched. Two things you'll need to decide: either create `docs/api.md` or drop the Docs section, and whether to add a `LICENSE` file to back the MIT claim.
