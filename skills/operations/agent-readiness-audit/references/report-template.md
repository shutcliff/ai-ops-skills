# Report template

Replace every `<...>`. Keep the order: the reader decides in five lines whether to read on.

```markdown
# Readiness report: <repository name>

**Verdict: <READY | NOT READY> for gate <1 share | 2 merge> <(default), when nobody chose>.**
<How many criteria that block at this gate or an earlier one fail, and the main reason; "no run evidence on this machine" when the gate rule in `criteria.md` applies.>

**Shape:** trigger <answer>, touches <answers>, both inferred from the files. <The right shape, or the shape it should be, by "Started the right way" in `references/criteria.md`.>

**Audited:** <commit>, branch <name>, <YYYY-MM-DD>, by reading; the agent was not run. Run evidence: <before-run | after-run, read from `<state directory>`>. Script layer: <ran | did not run (no terminal), so facts only the script checks are marked "checked by reading"; so the verdict is NOT READY by "The three gates" in `criteria.md`>.

**Scope:** <judged on every criterion; unreferenced skills, format only; skipped.>

## Fix plan

<The order to work in. Or "Nothing blocks this gate.">

1. **Tidy the structure** (closes: <criterion names>). <N> changes; the skill does the same thing afterwards. The list is under "For the fixer".
2. **<Behaviour change, in plain words>** (closes: <criterion names>). After this: <one sentence a person can check, "when X, the skill does Y">. <"This closes the risk below." on the step that fixes the pre-mortem.>

After the plan: <N> of <M> failures at this gate closed<; what is left, and why it waits>. <At share: what merge still needs, in one line.>

## Also fails at merge

<At the share gate only: every criterion that passes share but fails merge, one line each with `file:line` and the fix, so nothing waits unseen. At the merge gate, or when nothing fails there, delete this section.>

## If this misbehaves in someone else's hands next month, the most likely reason is

<One sentence, from a finding above.>

## All criteria

| Block | Criterion | Result | Blocks at | Evidence |
|---|---|---|---|---|
| Purpose | Purpose is clear: what, who runs it, what it produces | <verdict> | share | `file:line` |
| Purpose | "Done" for one run is defined | | share | |
| Claude's role | Who decides each number: Claude or code | | share | |
| Claude's role | Never-do list and stop-and-ask list exist | | share | |
| Steps | Bad input has a rule | | share | |
| Steps | Every link and path works | | share | |
| Steps | No vague steps | | share | |
| Steps | The files agree with each other | | share | |
| Safety | Each outside system has a failure plan | | merge | |
| Safety | Writes are protected | | share | |
| Safety | Works on another laptop, leaks nothing | | share | |
| Proof | Proof cases exist and run | | merge | |
| Proof | A teammate can install it | | share | |
| Proof | Built for more than one person to run | | merge | |
| Format | Files follow Claude's format | | share | |
| Skill craft | Started the right way: by a person or by Claude | | share | |
| Skill craft | The main file holds only what every use needs | | share | |
| Skill craft | Each step says when it is done | | share | |
| Skill craft | Nothing said twice, nothing said for nothing | | share | |
| Operability | Every automatic behaviour has a switch | | share | |
| Operability | A run can be replayed safely | | merge | |
| Operability | A run leaves a trace a person reads | | merge | |

## Details per failing criterion

### <Criterion name><, skill name when several skills are in scope>
Found: <file:line, quoted if short>. Why it matters here: <this agent, not a principle>. Fix: <in which file>.

## For the fixer

<One block per skill in scope. Written for the agent-readiness-fix skill and for a curious reader; the chat never shows it.>

### <skill name>

- **Trigger:** <person or Claude, and why that fits>.
- **Branches:** <each use, with its evidence `file:line`, and the step that handles it or "no step">.
- **Steps and reference:** <each piece of reference, the branches that use it, and its place: stays in SKILL.md, or moves to `references/<name>.md` behind the pointer line "<exact line>">.
- **Leading word:** <the word and its one definition, or the one to adopt>.
- **Legwork:** <the step Claude will rush, and its forced check, or "none">.
- **Size:** <words> words, <lines> lines. No-ops: <`file:line` and what changes without it, or "none">.
- **Structure changes:** <numbered; each moves text, changes the layout, or merges two copies of one instruction that survives in one place, with `file:line`>.
- **Behaviour changes:** <numbered, matching the fix plan; each with the text to write, the "After this" sentence, and the test: an input on fake data and what the skill must do>.

## Checks to add to the probe

<Per fact on the probe branch of the three-way rule in `criteria.md`, else delete:> <live fact> feeds <criterion>: add the check <name>, by <role>.
```

Rules:

- **Structure or behaviour.** A **structure change** only moves text, changes the layout (title, headings, sections), moves text for people to a readme, or merges two copies of one instruction so that it survives in one place. Everything else is a **behaviour change**: a new or changed rule, step, stop-and-ask line, definition or value, a branch the steps now handle, and the removal of a no-op. When unsure, it is a behaviour change.
- **Fix plan.** All structure changes are one step, "Tidy the structure", always first: every other fix lands inside it. Then one step per behaviour change, never one per criterion, in this order:
  1. The change that closes the pre-mortem risk, then any failure of Writes are protected, Works on another laptop, or Never-do list and stop-and-ask list exist: safety outranks clarity.
  2. Changes for branches the steps do not handle, and for legwork.
  3. One-line changes (a contradiction, a trigger phrase, a definition).
  4. Setup and documents for people (onboarding, readme, symptom table).
  At most five behaviour steps; a failure that fits none goes in Details. A value only the owner knows (where it runs, a folder, a schedule, a role, which of two rules wins) is never written as a fact: the step asks it as a question, with the recommended answer and why. Each behaviour step ends on its "After this" sentence, which the person approves and the fixer tests. On a tie, prefer the file a newcomer reads first: CLAUDE.md, the readme, the main skill.
- **Evidence.** One or two `file:line` per row, the rest in Details; a probe-settled criterion cites the probe line and date.
- **Gate names.** The filename and the verdict line use the gate name (share, merge). At merge the pre-mortem has an owner and a date.
- **Plain English.** No em dashes (in a quote, use a colon). A technical term gets its meaning in parentheses once. An adjective such as "fragile" needs a quoted line or is cut. One sentence of finding, one of fix naming the file and what to add or delete.
