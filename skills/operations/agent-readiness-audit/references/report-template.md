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

<The order to work in. One step per change, and each step closes every failure that change fixes. Or "Nothing blocks this gate.">

1. **<Verb and object, in which file>** (closes: <criterion names>). <What to write or delete, with `file:line`.> <"This closes the risk below." on the step that fixes the pre-mortem.>

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

## Checks to add to the probe

<Per fact on the probe branch of the three-way rule in `criteria.md`, else delete:> <live fact> feeds <criterion>: add the check <name>, by <role>.
```

Rules:

- **Fix plan.** Group the failures by the change that fixes them: one step per change, never one step per criterion. Order the steps:
  1. A rewrite of the layout or the steps, when Format or Skill craft fails: every other fix lands inside it, so doing it later means writing those fixes twice.
  2. The step that closes the pre-mortem risk, then any failure of Writes are protected, Works on another laptop, or Never-do list and stop-and-ask list exist: safety outranks clarity.
  3. One-line fixes (a contradiction, a trigger phrase).
  4. Setup and documents for people (onboarding, readme, symptom table).
  At most five steps; a failure that fits none goes in Details. Each step says what to write, not only what is missing. On a tie, prefer the file a newcomer reads first: CLAUDE.md, the readme, the main skill.
- **Evidence.** One or two `file:line` per row, the rest in Details; a probe-settled criterion cites the probe line and date.
- **Gate names.** The filename and the verdict line use the gate name (share, merge). At merge the pre-mortem has an owner and a date.
- **Plain English.** No em dashes (in a quote, use a colon). A technical term gets its meaning in parentheses once. An adjective such as "fragile" needs a quoted line or is cut. One sentence of finding, one of fix naming the file and what to add or delete.
