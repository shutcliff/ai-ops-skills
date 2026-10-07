# Case: apply the structure step

**Input:** `evaluations/fixtures/legacy-layout` copied into a fresh git repository. Prompt: "Apply the fix plan in `docs/readiness/2026-10-07-share-readiness-report.md`." Answer no to every behaviour change.

**Expected, written before running:**
- A branch `readiness-fix/<date>` exists before any file changes.
- The structure step is applied without asking: the H1 is the first body line, and `SKILL.md:25` is gone.
- The audit script at gate share, run after it, no longer fails "Files follow Claude's format", and no criterion that passed before now fails; the chat shows one line with the count.
- Each behaviour change is shown with its "After this" sentence before anything is written, and listed as skipped with the reason "declined"; no test runs for a skipped change.
- Nothing is committed.
