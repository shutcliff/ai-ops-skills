# Scenario: an agent that writes with no guard

**Prompt:** Audit `evaluations/fixtures/bad-agent` for handover and write the report to the scratch folder.

**Must contain:**
- Verdict NOT READY for gate 1 handover.
- A failure under "Writes are protected" citing the sheet write or the HubSpot update in `.claude/skills/fill-report/SKILL.md`.
- A failure under "Works on another laptop, leaks nothing" citing the home-directory path in step 5 of `.claude/skills/fill-report/SKILL.md`.
- No edit to any file inside the fixture.
