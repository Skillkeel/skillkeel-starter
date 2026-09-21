Range is `v0.1.0..HEAD`, five commits, no existing CHANGELOG.md. Creating it with the Keep a Changelog header.

Created `CHANGELOG.md` (none existed) with entries for `v0.1.0..HEAD`:

- **Added**: `feat!: drop Node 16 support` → first, with **BREAKING:** prefix; `/health` endpoint; CSV export (#12)
- **Fixed**: empty rows in import
- Omitted `chore: bump eslint` (not user-visible)

One assumption to flag: I wrote "Node 18 or later is now required" for the breaking change, but the commit only says Node 16 was dropped — if the new minimum is different, adjust that line. The file is uncommitted; no version was cut or tagged.
