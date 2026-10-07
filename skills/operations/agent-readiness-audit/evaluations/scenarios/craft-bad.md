# Scenario: a skill written badly for Claude

**Prompt:** Audit `evaluations/fixtures/craft-bad` for the share gate and write the report to the scratch folder.

**Must contain:**
- Verdict NOT READY for gate 1 share.
- A failure under "Started the right way: by a person or by Claude": user-invoked with a trigger list in its description (`SKILL.md:3`).
- A failure under "Nothing said twice, nothing said for nothing" citing the History section.
- A failure under "Each step says when it is done": no step has a "Done when" line.
- A fix plan whose first step is "Tidy the structure" as one line, then behaviour steps each with an "After this" sentence, ending with the count of failures left.
- A "For the fixer" section listing the branches, the size, the structure changes and, per behaviour change, a test; none of it in the chat.
