# agent-readiness-audit

A pass or fail report on whether an agent, skill or plugin is ready for someone other than its builder to use, for the person handing it over or receiving it.

Model-invoked

## What it does

- Writes one report, verdict first, where every failure names the file, the line and the fix.
- Asks one question, which gate, only when you did not name one. Everything else it reads from the files.
- Checks the files against plain-English criteria: purpose, safety, onboarding, connectors, an off switch for anything automatic, and how well the skill itself is written (how it starts, what sits in the main file, whether each step says when it is done, nothing said twice).
- Runs a script for the mechanical checks, such as leaked keys, personal paths and dead links, then reads every instruction file for meaning.
- Says when something should be a different shape: an agent instead of a skill, or a standing rule instead of a skill.

## When to reach for it

- "Is this skill ready to hand to the support team?"
- "Can I publish this plugin to the whole company?"
- "Review this pull request that changes our CLAUDE.md."
- "I was sent this skill as a zip. Is it safe and usable?"

## Common questions

**Does it run the agent?** No. It reads the files and runs its own checking script. Whether the output is right is the job of test cases and a real run.

**Can I use it without a terminal?** Yes. Claude reads the files and applies the criteria, but the report says the script did not run, and the verdict stays NOT READY until it does, because the leaked-key and personal-path scans need the script.

**Why does it ask me questions first?** Some facts are not in the files: who will use it, and whether it should touch real systems. Your answers are checked against the files, and a mismatch is reported.

**Where does the report go?** Into `docs/readiness/` in the folder you audited. For a GitHub link or a zip, into your current folder. A second audit on the same day and gate replaces that day's report.

**Can it judge whether a skill is well written?** Partly. The script catches hard facts, such as a reference file nothing points to or a sentence repeated word for word. Claude judges the rest by reading, so two audits can disagree on those points.

## It's working if

- Every failure in the report points to a line you can open and find.
- After you apply the fixes, a second audit at the same gate says READY.
- The person receiving the skill gets a first good result from the onboarding alone.
