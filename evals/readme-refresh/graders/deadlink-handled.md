---
type: regex
target: {source: file, path: README.md}
pattern: '(?s)\A(?:(?!\]\(docs/api\.md\)).)*\Z|TODO: verify(?:[^\n]*\n){1,3}[^\n]*\]\(docs/api\.md\)|\]\(docs/api\.md\)[^\n]*TODO: verify'
match: contains
---
The dead link `docs/api.md` is handled: removed or retargeted (the link is gone from README.md), or kept under a `<!-- TODO: verify -->` marker within three lines above it or on the same line after it, which the skill's rules allow ("never delete sections you cannot verify; mark them"). Left as a bare claim it fails. 2026-09-18: the trigger run marked it and the old pattern (link must be gone) failed a run that followed the skill text. The 09-18 named run put the marker after the link on the same line.
