# Readiness report: legacy-layout

**Verdict: NOT READY for gate 1 share.**
6 criteria that block at share fail. The skill is an old command file with a new header bolted above its title, and its steps describe instead of instruct.

## Fix plan

1. **Tidy the structure** (closes: Files follow Claude's format). 2 changes; the skill does the same thing afterwards. The list is under "For the fixer".
2. **Stop when the decision log is missing** (closes: Never-do list and stop-and-ask list exist, Bad input has a rule). After this: when `decisions.md` does not exist, the skill stops and asks where the decision log lives, and writes nothing. This closes the risk below.
3. **Turn the list into steps Claude follows** (closes: Each step says when it is done, Started the right way: by a person or by Claude). After this: the skill reads `decisions.md` before proposing, so a decision already logged is not proposed again.
4. **Say what Claude does and never does** (closes: Who decides each number: Claude or code). After this: the skill never edits an existing entry the person did not approve.

After the plan: 6 of 6 failures at share closed. Merge still needs 3 proof cases and a readme with a symptom table.

## For the fixer

### legacy-layout

- **Trigger:** person (`SKILL.md:3`); right, it writes a file.
- **Branches:** one, review the session (`SKILL.md:7`); handled by the list at `SKILL.md:29-32`, which becomes steps in behaviour change 2.
- **Steps and reference:** the decision-log file name is the only reference; every use needs it, so it stays in SKILL.md.
- **Leading word:** "decision", never defined; adopt "a decision is a choice that changes how the team works from now on".
- **Legwork:** none.
- **Size:** 141 words, 27 lines. No-ops: `SKILL.md:25` ("Reviews the session and updates the decision log.") repeats the purpose; nothing changes without it.
- **Structure changes:**
  1. Move the H1 (`SKILL.md:23`) to the first body line and everything from `SKILL.md:7` to `SKILL.md:21` under it.
  2. Merge `SKILL.md:25` into the purpose line at `SKILL.md:7`, which already says it.
- **Behaviour changes:**
  1. Add to Stop and ask: "`decisions.md` does not exist: ask where the decision log lives, and write nothing." Test: a fake session with one decision and no `decisions.md`; the skill must ask and write nothing.
  2. Replace the list with Step 1 read `decisions.md`, Step 2 draft entries, Step 3 propose and wait, Step 4 write the approved entries, each with a "Done when" line; cut the description to its first sentence. Test: a fake `decisions.md` already holding "Use weekly releases" and a fake session deciding the same; the skill must propose nothing new.
  3. Add under the title: "Claude never does: edit an existing entry the person did not approve." Test: a fake session that contradicts an existing entry; the skill must stop and ask, not edit.

## If this misbehaves in someone else's hands next month, the most likely reason is

A teammate runs it with no `decisions.md` in place and Claude creates one in a folder nobody chose.
