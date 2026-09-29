I checked everything the README claims against the repo and fixed two errors. I also added a Test section because the README didn't have one.

| line | claim | reality | fix |
|---|---|---|---|
| 8 | `npm run start` | `package.json` has no `start` script; the run script is `dev` (`node server.js`) | Changed to `npm run dev` |
| 13 | Links to `docs/api.md` | There is no `docs/` folder | Removed the broken link and left a `<!-- TODO: verify -->` note |
| — | (no Test section) | `npm test` runs `node --test`. It completes, but there are no tests yet (0 tests) | Added a short `## Test` section |
| 17 | License: MIT | There's no `LICENSE` file, and `package.json` has no `license` field | **Left alone, your call:** add a `LICENSE` file and a `"license": "MIT"` field, or change the README |

```diff
@@ -5,12 +5,18 @@ A tiny service.
 ## Run
 
 ```
-npm run start
+npm run dev
+```
+
+## Test
+
+```
+npm test
 ```
 
 ## Docs
 
-See [API docs](docs/api.md).
+API docs are not written yet. <!-- TODO: verify — docs/api.md does not exist -->
 
 ## License
```

The rest of the README is unchanged, and nothing is committed yet.

For the Docs section, I kept the heading and marked it instead of deleting it. If you'd rather not have it, you could remove the section or write `docs/api.md`. Right now `server.js` only prints `hi`, so there's no API to document yet.

The Google Drive, Notion and HyperFrames connectors need to be authorized in your claude.ai connector settings before they can be used. This task didn't need them.
