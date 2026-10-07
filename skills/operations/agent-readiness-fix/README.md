# agent-readiness-fix

Here an **agent** is any skill, plugin, command or subagent that someone other than its builder will run.

**What it does:** applies the fix plan an `agent-readiness-audit` report wrote. Structure changes (moving text, layout, merging repeats) are applied directly, because they change nothing the skill does. Each behaviour change is shown with one sentence of what will be different, written only after your yes, and then tested: a separate agent runs the fixed skill on fake data in a scratch copy, and you see the sentence next to what happened.

**Who runs it:** the builder of an agent, right after an audit.

**What it produces:** the fixes, on a new branch `readiness-fix/<date>`, plus a summary in chat of what each step changed and the count it left. Nothing is committed: you review, re-audit, and commit.

## How it starts

Model-invoked, for one moment only: when an audit ends with "Apply the plan now?" and you say yes. You can also type `/agent-readiness-fix <report path>`. It needs a report from the audit first; it never builds its own plan.

## You need

- `agent-readiness-audit` installed next to it (the same plugin installs both).
- Claude Code with a terminal: it edits files, runs Python 3.9 or newer (check with `python3 --version`) and git (check with `git --version`), and starts a helper agent for each test. The desktop and web apps cannot run it.
- Write access to the folder being fixed: ask its owner.

## First thing to type

Ask Claude "is this skill ready to share?" in the skill's folder, which starts the audit. Answer yes to "Apply the plan now?". Or, with a report already written:

```
/agent-readiness-fix docs/readiness/<date>-share-readiness-report.md
```

## What a good result looks like

The structure is tidied in one line, every behaviour change you approved shows "tested: matches", the count falls to 0 failures at the gate (for example 10 → 4 → 1 → 0), and a fresh audit in a new session agrees. A full fix of a small skill takes about 5 minutes of tests.

## When something looks wrong

| What you see | What it means | What to do |
|---|---|---|
| "The report has no Fix plan" | The report comes from an audit version before 0.3.0 | Run `/agent-readiness-audit` again |
| It asks about a quoted line that does not match | The files changed after the audit | Run the audit again, then apply the new plan |
| The count does not fall after a step | The change did not satisfy the criterion, or broke another | Say "undo", then read that criterion in the audit skill's criteria file |
| It stops to ask for a folder, a role or a schedule | Only the owner knows that value | Answer it; the step waits until you do |
| "Tested: does not match" | The fixed skill did something other than the sentence you approved | Choose undo, adjust the change, or keep it if what happened is fine |
| "Not tested, needs a supervised run" | The test needs a real outside system that a fake cannot stand in for | Run that case yourself once, watching it |

**Who to ask:** the repository's maintainer, through an issue on the repository.
