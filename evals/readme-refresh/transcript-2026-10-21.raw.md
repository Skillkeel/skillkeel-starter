Two of the README's claims are factually wrong. I'll fix those now and leave the rest as proposals.

I fixed the two wrong claims in `README.md`. Three other gaps are listed below for you to decide on.

## What I checked

| Line | README says | What the repo has | Action |
|---|---|---|---|
| 8 | `npm run start` | `package.json` has no `start` script, only `dev` (`node server.js`) and `test` | **Fixed:** changed to `npm run dev` |
| 13 | Link to [API docs](docs/api.md) | There's no `docs/` folder and no API doc anywhere in the repo | **Fixed:** removed the broken link and added a `<!-- TODO: verify -->` note, keeping the Docs section |
| 17 | License: MIT | No `LICENSE` file, and `package.json` has no `license` field | **Proposed:** add a `LICENSE` file and `"license": "MIT"`, or correct the claim |
| — | No Test section | `npm test` runs `node --test`, which exits cleanly but finds **0 tests** (there are no test files) | **Proposed:** I didn't add a Test section, because it would describe a command that tests nothing |
| — | No Install section | `package.json` has no dependencies | **Proposed:** an Install step isn't needed for now |

## Diff

```diff
-npm run start
+npm run dev
...
-See [API docs](docs/api.md).
+See API docs. <!-- TODO: verify — docs/api.md does not exist in the repo -->
```

Nothing else in the README was changed. The edits aren't committed yet. Tell me if you want any of the proposed changes, such as adding a `LICENSE` file.
