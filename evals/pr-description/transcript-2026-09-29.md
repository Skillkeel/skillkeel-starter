# pr-description: run 2026-09-29, Claude Code 2.1.284
Raw output: `transcript-2026-09-29.raw.md` (unedited). Record: `record-2026-09-29.json`. Fixture: `fixture.sh`.
First run of the day FAILED on no-footer, a grader fault: the description had no footer, and the grader matched the words "Generated with" in the model's sentence explaining that it left the footer off. Fix in 0.1.11: the grader matches the footer form (`Generated with [` or the robot line), as commit-message's no-trailer does since 0.1.5.
Rerun on 2.1.284: migration-called-out PASS · no-fake-npm PASS · no-footer PASS (no footer in the markdown; the explanation sentence is outside it) · real-test-command PASS (`make test`) · sections PASS · skill-fired PASS. Verdict: PASS.
