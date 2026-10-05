# Report template

Replace every `<...>`. Keep the order: the reader decides in five lines whether to read on.

```markdown
# Readiness report: <repository name>

**Verdict: <READY | NOT READY> for gate <1 handover | 2 pull request | 3 release> <(default), when nobody chose>.**
<How many criteria that block at this gate or an earlier one fail, and the main reason; "no run evidence on this machine" when the gate rule in `criteria.md` applies.>

**Shape:** trigger <answer>, touches <answers>, both inferred from the files. <The right shape, or the shape it should be, by "Started the right way" in `references/criteria.md`.>

**Audited:** <commit>, branch <name>, <YYYY-MM-DD>, by reading; the agent was not run. Run evidence: <before-run | after-run, read from `<state directory>`>. Script layer: <ran | did not run (no terminal), so facts only the script checks are marked "checked by reading"; so the verdict is NOT READY by "The three gates" in `criteria.md`>.

**Scope:** <judged on every criterion; unreferenced skills, format only; skipped.>

## Fix these first

1. **<Criterion name>.** <What is wrong, `file:line`.> Fix: <what to add or delete, in which file.>

<Up to three, or "Nothing blocks this gate.">

## If this misbehaves in someone else's hands next month, the most likely reason is

<One sentence, from a finding above.>

## All criteria

| Block | Criterion | Result | Blocks at | Evidence |
|---|---|---|---|---|
| Purpose | Purpose is clear: what, who runs it, what it produces | <verdict> | handover | `file:line` |
| Purpose | "Done" for one run is defined | | handover | |
| Claude's role | Who decides each number: Claude or code | | handover | |
| Claude's role | Never-do list and stop-and-ask list exist | | handover | |
| Steps | Bad input has a rule | | pull request | |
| Steps | Every link and path works | | handover | |
| Steps | No vague steps | | pull request | |
| Steps | The files agree with each other | | pull request | |
| Safety | Each outside system has a failure plan | | pull request | |
| Safety | Writes are protected | | handover | |
| Safety | Works on another laptop, leaks nothing | | handover | |
| Proof | Proof cases exist and run | | release | |
| Proof | Built for more than one person to run | | handover | |
| Format | Files follow Claude's format | | pull request | |
| Skill craft | Started the right way: by a person or by Claude | | pull request | |
| Skill craft | The main file holds only what every use needs | | pull request | |
| Skill craft | Each step says when it is done | | pull request | |
| Skill craft | Nothing said twice, nothing said for nothing | | pull request | |
| Operability | Every automatic behaviour has a switch | | handover | |
| Operability | A run can be replayed safely | | pull request | |
| Operability | A run leaves a trace a person reads | | pull request | |

## Details per failing criterion

### <Criterion name><, skill name when several skills are in scope>
Found: <file:line, quoted if short>. Why it matters here: <this agent, not a principle>. Fix: <in which file>.

## Checks to add to the probe

<Per fact on the probe branch of the three-way rule in `criteria.md`, else delete:> <live fact> feeds <criterion>: add the check <name>, by <role>.
```

Rules:

- **Ranking.** "Fix these first" ranks by harm in someone else's hands; safety outranks clarity. On a tie, prefer the file a newcomer reads first: CLAUDE.md, the readme, the main skill.
- **Evidence.** One or two `file:line` per row, the rest in Details; a probe-settled criterion cites the probe line and date.
- **Gate names.** The filename uses the short gate form (handover, pr, release), the verdict line the long form. At release the pre-mortem has an owner and a date.
- **Plain English.** No em dashes (in a quote, use a colon). A technical term gets its meaning in parentheses once. An adjective such as "fragile" needs a quoted line or is cut. One sentence of finding, one of fix naming the file and what to add or delete.
