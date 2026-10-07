# Agent Readiness Standard: the criteria

The one text of the standard, for every Claude Code agent, skill, command or subagent that more than one person will run.

## Contents

- Verdicts, evidence and terms
- What the audit reads, and what it leaves alone
- Before a run and after a run
- The two gates
- The blocks, in order: Purpose, Claude's role, Steps, Safety, Proof, Format, Skill craft, Operability

**What ready means.** Someone who did not build the agent can run it from its documentation, knows what it never does and when it stops to ask, can tell a good run, can switch off anything automatic, and can read what a run did. Ready does not mean fully specified: over-specifying makes instruction-following worse.

## Verdicts, evidence and terms

**Verdicts.** PASS, FAIL, does not apply (with a one-line reason), or NO EVIDENCE YET. No partial marks: a half-met criterion is a FAIL with a note on what would make it pass. NO EVIDENCE YET is only for a criterion that needs a run and has nothing to read; its fix is the run to perform. It blocks the merge gate, and does not block the share gate.

**Evidence.** A file and a line, or a probe check with its date, or the sentence "no file states this". Every verdict, finding and fix carries evidence.

**Terms.**
- The **main instruction file** is the skill or command a person triggers to do the job; when there are several, the one CLAUDE.md lists first.
- A **deny list** is the part of `.claude/settings.json` that names what Claude may never run.
- **Headless** or **unattended** means Claude runs from a scheduled script with no person watching.
- A **check that cannot fail** is a stub (a function that does nothing yet), a function no caller invokes, or a comparison of a value to itself. It fails "Writes are protected" when it guards a write, and "Who decides each number: Claude or code" otherwise; never both.
- A **proof case** is one real input paired with the result someone wrote down before running it.
- A **real system** is anything outside the audited folder and the person's own working folder; a local report or draft the run creates for the person is not a write to a real system.
- A **probe** is a small script in the repository that talks to the live systems and writes a timestamped result file into the operator's state directory, which the audit reads as dated evidence.

## What the audit reads, and what it leaves alone

Decided per file, not per folder.

- **In scope, judged on every criterion:** CLAUDE.md, the readme or setup document, the docs, settings, every skill, command or subagent something in the repository points at, and everything a plugin ships (`skills/`, `commands/`, `agents/`), for each local plugin a marketplace lists.
- **Loaded but nothing uses it:** a skill in `.claude/skills` that no file references. Claude still loads its description, so it can trigger during a run. It gets one line under "The files agree with each other" (delete it or move it out of `.claude/`), plus "Files follow Claude's format".
- **Neither referenced nor loaded, skipped:** vendored tools outside `.claude/`, archives, and this audit's own reports in `docs/readiness/`. The secrets and personal-path scan under "Works on another laptop" still reads every tracked text file except build output and test fixtures, because the whole folder gets handed over.

The audit does not certify safety, judge the architecture, or replace the pull-request reviewer.

## Before a run and after a run

Some facts exist only at run time (the access a service account really has, whether last night's run fired), so the audit detects one of two modes.

- **Before-run mode.** Nothing has left a trace on this machine. Criteria that need run evidence report NO EVIDENCE YET instead of failing.
- **After-run mode.** The operator's state directory holds a run log, a probe result, or both. Every criterion gets a verdict.

**The gate rule.** The share gate needs no run: the teammate's test is the run. The merge gate requires after-run mode, because a file-only reading cannot tell whether a real run behaves; the evidence is the teammate's test run, on the machine that ran it. An auditor on a different machine cannot reach it: the verdict is NOT READY, with the reason "no run evidence on this machine" and the state directory the files point at. When nothing writes to a real system and nothing runs by itself, no run evidence is needed: every criterion that needs a run does not apply. In CI (`--ci`), which has no run data, the script judges every merge criterion from the files and the reviewer confirms the run evidence.

**A fact the audit cannot verify resolves one of three ways:** the standard already requires it to be visible in the files, so it is a FAIL on the criterion that needs it; only a live system can settle it, so it becomes a named check in the probe, with the criterion it feeds and the role who adds it, and until the probe carries that check the criterion fails with that one fix; or no criterion depends on it and it is dropped. Reports have no open-questions section.

## The two gates

The gates follow the agent's life, in order. Neither depends on where the repository lives: the same audit applies to a personal repository, a company one, or anyone else's.

- **1, share:** the builder gives the agent to a teammate to test. Question: is it good enough that a test means something? The files must be complete, well structured and safe, and a teammate must be able to install it alone. Blocks: every criterion whose **Blocks at.** line says Share. No run evidence: the test is the run.
- **2, merge:** the agent goes into a repository (a plugin, a skills folder), so anyone who installs it can run it on any computer. Question: can a stranger run it safely? Blocks: gate 1, plus every criterion that blocks at Merge, plus run evidence by the gate rule. Each failure accepted for a merge is listed with its reason, and a prompt change that adds a rule adds a proof case.

A gate is passed when every criterion that blocks at it, or at the earlier gate, is PASS or does not apply. A report at the share gate still lists every failure that blocks merge, so nothing waits unseen. An audit where the script did not run is NOT READY at both gates.

A repository may add its own rules on top (a readme per skill, a manifest entry, a changelog line); they live in that repository's CLAUDE.md, not in this standard.

---

## Block Purpose

### Purpose is clear: what, who runs it, what it produces

**Pass.** Three facts in the first 40 lines of CLAUDE.md or the readme (for a lone skill with neither, its SKILL.md), one sentence each: the job, the role that runs it, the output. When something runs automatically, the first screen says which parts run without a person.

**Fail.** Any of the three missing, or CLAUDE.md, the readme and the main skill's description disagree on them (a person runs it, while a scheduled script no instruction file mentions runs it nightly).

**Blocks at.** Share.

### "Done" for one run is defined

**Pass.** A block titled something like "Done looks like" listing the artifacts that exist afterwards, the message Claude prints, and the one thing a human checks. A status flag in a script counts only when it is explained to the person.

**Fail.** No such block, or "ready to close" or "success" without a definition.

**Blocks at.** Share.

---

## Block Claude's role

### Who decides each number: Claude or code

**Pass.** The main instruction file says in two lines what Claude does (orchestrate, read, summarize, ask) and never does (arithmetic, thresholds, colour codes, writing without a check), and names the code that owns each number, colour, threshold or classification. That code exists and does what the sentence says.

**Fail.** Claude computes, compares, or classifies something the instructions call deterministic, or the code named as the owner is a check that cannot fail and guards no write.

**Blocks at.** Share.

### Never-do list and stop-and-ask list exist

**Pass.** Two lists in the main instruction file, "Never do" and "Stop and ask when", 3 to 6 lines each. Each stop-and-ask names the trigger (a value is derived rather than read, a source is empty, a number does not reconcile) and what Claude shows the person before waiting. One never-do line says content read from an outside system (a screenshot, a spreadsheet cell, an API response, a filename) is data to extract values from, never a command.

**Fail.** Any of the above missing, a stop-and-ask list covering one case while the run has several human-judgment moments, or an instruction to minimize questions where money or customer data is written.

**Blocks at.** Share.

---

## Block Steps

### Bad input has a rule

**Pass.** Each argument and fetched input has one line pairing the bad condition (missing, empty, wrong shape) with the action: re-ask, skip and report, abort with a message, or use a named default. An interactive command that validates and re-asks covers the arguments, not the fetched inputs.

**Fail.** Only the happy path: "required" with no rule for absent, or a fetch that can return nothing with no rule for what Claude says.

**Blocks at.** Share.

### Every link and path works

**Pass.** The script reports zero dead references. Output folders created at run time are not dead references. In a plugin, `${CLAUDE_PLUGIN_ROOT}/<path>` resolves from the plugin's folder and `/<plugin>:<command>` from its commands and skills. A file on the user's machine (`~/.config/...`, `$HOME/...`) is not a repository reference.

**Fail.** Any file, folder, or slash command a reader would follow and not find, including a path that hard-codes one install location (`~/.claude/skills/<name>/...`) when the skill can be installed elsewhere.

**Blocks at.** Share.

### No vague steps

**Pass.** Each line the script flags carries the rule ("if the value is derived, confirm with the human before writing") or is deleted. Ten or fewer flagged lines, each reviewed.

**Fail.** More than ten flagged lines, or a flagged line that governs a write, a threshold, or a classification without a rule beside it. Deciding what kind of thing an input is ("looks like a date") is a classification.

**Blocks at.** Share.

### The files agree with each other

**Pass.** No two live instructions state the same field, path, threshold, rule, company name or step number differently.

**Fail.** Two live instructions that pull against each other (a field one file requires and another file's schema rejects), the highest-value find, since Claude receives both and picks one silently. Across skills, read side by side in a bundle or marketplace: two whose names and descriptions cover near cases, two copies of one skill name (both can trigger), or one that depends on a skill or file shipped in another plugin.

**Blocks at.** Share.

---

## Block Safety

### Each outside system has a failure plan

**Pass.** One line per outside system (a warehouse, a CRM, a spreadsheet, a connector): "If this system is down, empty, or stale: Claude does X and tells the person Y." The three states are distinct, so a quiet day and a broken query never look the same. A connector has a fourth state, not connected: the onboarding says how to connect it or which role adds it, and the skill says what Claude does without it.

**Fail.** A system with no failure line or only "down" covered, code that handles it (a retry, a failed list) while the instructions never tell Claude what to say, or a connector with no "not connected" line. In after-run mode, the probe result says which systems answered.

**Blocks at.** Merge.

### Writes are protected

**Pass.** Every write to a real system (a sheet, a CRM, a ticket, a message channel, a file store) is preceded by a check in code that must pass or a confirmation step that shows the person the values and waits. The check's second value comes from a genuinely separate source: another system, another query, or a value the code fetched itself. Unattended runs use the code check, with Edit, Write and git denied in the settings file.

**Fail.** A write with neither. An unattended run with write permissions and no deny list. A check whose two inputs trace to one extraction event (a number read twice off the same screenshot). A check that cannot fail in front of a write. An instruction to skip a confirmation fails here only when no code check stands in front of that write; otherwise it belongs under "Never-do list and stop-and-ask list exist". A Never-do line, or a draft the person sends themselves, is not a write.

**Blocks at.** Share.

### Works on another laptop, leaks nothing

**Pass.** No credential-shaped strings in tracked files, the environment file ignored by git, no home-directory paths in instructions, scripts, or config, and machine-specific values read from an environment or config file. `.claude/settings.json` lists specific commands rather than wholesale Bash, Write, or Edit, holds no header or key patterns, is not a log of one-off dated commands, carries a deny list when anything runs unattended, and has no rule combining an interpreter flag (`-c`, `-e`, `--eval`, `-m`) with a wildcard or an open suffix. No keys in `.mcp.json`.

**Fail.** Any of the above, even if nothing bad has happened yet. `Bash(python3 -c ' *')` is `Bash(*)` in a form that looks specific. A shared archive with a member whose path leaves its folder.

**Blocks at.** Share.

---

## Block Proof

### Proof cases exist and run

**Pass.** An `evaluations/` (or `evals/`) folder with at least 3 proof cases per skill or product the agent ships, run automatically (CI or a pre-merge command in the pull-request template). A dry-run flag for every step that writes. Before merge, each case has been run 3 times and passed all 3; the report counts cases that passed all three, not once.

A model-invoked skill also has one case where a realistic prompt starts it and one where a near prompt must not.

**Fail.** No cases, cases for one product out of many, cases nothing runs, expected notes in prose the runner skips, or a model-invoked skill with no case that checks it starts.

**Blocks at.** Merge. (Unit tests for the code are welcome and count for nothing here; this criterion is about Claude's output.)

### A teammate can install it

**Pass.** An onboarding (the readme, an ONBOARDING.md, or for a lone skill a setup block in SKILL.md) with four parts: how to get it; what you need first, each prerequisite naming the command that satisfies it or the role who grants it; the first thing to type; what a good result looks like. A configured value (a folder, an ID, a placeholder such as `<memory dir>`) counts as a prerequisite. In a bundle, each skill gets one line.

**Fail.** Any part missing, or a prerequisite that says what you need and not how to get it. At the share gate the teammate installs from the onboarding alone with the builder silent; the report records the result.

**Blocks at.** Share.

### Built for more than one person to run

**Pass.** Four things, readable in the repository.
1. A readiness check the documents tell a new operator to run first: a script, a `check` command, or a first skill step that confirms connectors, access and configured values (for a target with no outside system, a check that the folder and its configured values are in place counts).
2. Roles named everywhere a person is meant, never the people who wrote the instructions.
3. A symptom table for whoever is on call: what you see, what it means, what to do.
4. The docs name the surfaces it supports (Claude Code, the desktop and web apps) and who to ask; anything that needs a terminal, Python or a local file says so.

Before merge, someone who did not build it tries once with one connector disconnected; the report records the result.

**Fail.** Any of the four missing, or a person named where a role belongs (compare `git log` author names with the instruction text). Without a readiness check, a newcomer meets what is missing as an error mid-run.

**Blocks at.** Merge.

---

## Block Format

### Files follow Claude's format

**Pass.** Every `SKILL.md` has a name (lowercase letters, digits, single hyphens, max 64 characters, matching its folder) and a description (1 to 1024 characters, never in the first or second person: no "I" or "you") that says what the skill does; a model-invoked skill's description also says when to use it. SKILL.md body under 500 lines. A reference file over 100 lines starts with a table of contents. Every command has a description, plus an argument hint when it takes arguments. Every subagent has a name, a description, and a tools list. CLAUDE.md under 200 lines. A SKILL.md body opens on its one H1 title, and every section (purpose, done, never do, stop and ask, steps) sits under it.

**Fail.** A field missing or a file over its limit (a command over 500 lines, a CLAUDE.md that embeds a schema and a ten-step procedure). Text above the H1 title, or a second H1: two documents stitched into one file, so Claude reads two sets of rules.

**Blocks at.** Share.

Sources: agentskills.io/specification; platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices; code.claude.com/docs/en/skills, /memory and /sub-agents.

---

## Block Skill craft

How every in-scope skill, command, subagent and CLAUDE.md is written for Claude, after Anthropic's skill authoring best practices (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). "Started the right way: by a person or by Claude" applies to skills and subagents only. The script gathers evidence; reading gives the verdict.
- A **model-invoked** skill has a description Claude reads every session, so Claude can start it on its own.
- A **user-invoked** skill sets `disable-model-invocation: true`, so only a person typing its name starts it.
- A **leading word** is a short, well-known word repeated so that it anchors one behaviour (for example "evidence").
- A **key behaviour** is one a step's "Done when" line depends on.
- A **no-op** is a sentence whose deletion would not change what Claude does.
- A **branch** is one way the skill gets used (a different argument, request or situation). The description, the argument hint and the examples show them.
- **Legwork** is a step Claude tends to rush toward the goal (asking before planning, checking every category before saying "nothing new").

### Started the right way: by a person or by Claude

**Pass.** Model-invoked only when Claude or another skill must reach it on its own; otherwise user-invoked, with a one-line description for people and no trigger list. A model-invoked description puts its leading word first, has one trigger per branch the body handles, and does not repeat identity the body carries. Only when two skills in scope cover near cases, each description says what it is not for. The shape fits the use, by these signs:
- **An agent:** it runs on a schedule or unattended, keeps state between runs, writes to systems repeatedly, or needs its own limited tool set.
- **A subagent:** a long multi-step job that would flood the main conversation, or one that needs fewer permissions than the session.
- **A standing rule** in CLAUDE.md or the organisation's instructions: it is meant to apply always.
- **A user-invoked skill:** it has side effects, or only a person ever starts it.
- **A plugin:** several skills plus connectors handed to a team.
- **A plain script:** every step is fixed and needs no judgment.

**Fail.** Model-invoked when only a person ever starts it, so its description costs context every session. User-invoked while another file tells Claude to run it, which can never work. A description that names one branch twice, or misses a branch. Always-on wording ("every response", "always use", "for all requests"): a skill loads only when Claude picks it, so standing behaviour belongs in CLAUDE.md or the organisation's instructions. A wrong shape, with the right shape as the fix.

**Blocks at.** Share.

### The main file holds only what every use needs

**Pass.** The report lists the skill's branches. Steps, and the reference every branch needs, stay in SKILL.md (or CLAUDE.md). Reference only some branches need sits in its own file, one level deep, behind a pointer line that gives the condition for reading it ("read X before step N"). Each concept's definition, rules and caveats sit together under one heading. Every branch has a step that handles it.

With no reference files, the report says so and states that everything in SKILL.md serves every use.

**Fail.** A branch the steps never handle (an example shows a use no step covers). One concept written in two places (a category list and a file list that map one to one). Reference a step needs that is defined nowhere (the format of the entry the skill writes). A reference file the main file never names, so Claude never reaches it. A pointer with no condition. A reference file that points to another reference file. Material only one branch needs written inline in the main file. Install text, history or a file listing in the file Claude loads.

**Blocks at.** Share.

### Each step says when it is done

**Pass.** A skill that does a job has its steps as headings (`## Step N: <verb> <object>`), each written as an instruction to Claude (read, compare, propose, write) that names its input, and each ending on a "Done when" line Claude can check, demanding where thoroughness matters ("every criterion judged", not "review the files"). A reference-only skill (rules or patterns Claude consults) has no steps and passes on its structure alone. Key behaviours carry a leading word, defined once (the report names the word, or proposes one when the skill's central word is never defined). Legwork has a forced check in its step ("list a candidate or 'none' for every category") or, when it is large, its own skill. Steering states the target behaviour. Prohibitions appear only as hard guardrails in the one short Never-do list, each paired with what to do instead.

**Fail.** A step with no checkable end, which invites Claude to stop early. Legwork with no forced check. A procedure written as a numbered list under a heading such as "What it does": the items describe ("Reviews the session") instead of instruct, and no item can carry a "Done when" line. A step that depends on an input no earlier step reads (a "no duplicates" rule with no step that reads the existing file). A key behaviour steered only by a "never" or "do not" line outside the Never-do list, which puts the unwanted behaviour into Claude's attention.

**Blocks at.** Share.

### Nothing said twice, nothing said for nothing

**Pass.** One meaning lives in one place across SKILL.md, its references, CLAUDE.md, commands and subagents. No dated history, superseded notes, stale names, or time-sensitive facts (a date, price or version that will go stale). No no-ops. No copy of the environment (a config file, a directory listing, a script's help text) unless looking it up is expensive.

The report gives each skill's size (words and lines) and names each no-op by the deletion test: the line, and what Claude would do differently without it ("nothing").

**Fail.** Any of the above, named by file and line. When it is unclear whether a sentence is a no-op, the finding says so and its removal is a behaviour fix for the owner to approve; the auditor does not run it.

**Blocks at.** Share.

---

## Block Operability

### Every automatic behaviour has a switch

**Pass.** Each automatic behaviour reads one setting (an environment variable or a config key) at the top, writes nothing and changes no state when off, and has one command that prints whether it is on; the setup or runbook names the switch, its default, and how to turn it off and check it. A headless invocation has a ceiling (a wall-clock limit or a turn cap) whose value the runbook names, with a stated behaviour on reaching it: abort, no write, logged as incomplete. A fresh install arrives with every automatic behaviour off, and arming one is a setup step after one supervised run. Anything automatic at first contact (a greeting, a setup skill that starts itself) is declared even when it writes nothing. A skill or command that runs on a schedule (daily, cron, a routine) and posts, emails or writes is automatic too: it names the schedule, whose account runs it, and how to pause it.

**Fail.** Any of the above missing for a script that starts Claude headless, a hook, a scheduled skill, or anything naming cron, systemd, launchd, or a login or unlock trigger: an undeclared first-contact behaviour, a behaviour that stops only when the script is edited, a switch no document names, an off state that still writes or marks the day done, or a ceiling missing or with no stated behaviour (logging the duration afterwards is not a ceiling). Does not apply when nothing runs by itself.

**Blocks at.** Share.

### A run can be replayed safely

**Pass.** A flag re-runs one date, source or step alone. A dry-run path for every writing step. One line states what a second run does to values already written: overwrite, skip, or refuse. When a manual and an unattended path can both write, a lock, a claim on the day, or a documented rule keeps them off the same cells at once.

**Fail.** Any of the above missing, including an inline write that bypasses the write helper and its dry run, or a state file that stops a second scheduled run but not a person running the skill by hand. Does not apply when nothing writes to a real system.

**Blocks at.** Merge.

### A run leaves a trace a person reads

**Pass.** In the repository: the code writes one entry per run, the runbook says where it lands, and the entry carries the date the run covers, what it wrote, what it skipped, whether the automatic behaviour was on, and a quiet day told apart from a broken query. On the machine, in the operator's state directory: an entry exists, the newest no older than the schedule the documents claim.

**Fail.** The only record is a raw transcript, an empty result and a broken query look the same in it, the repository does not document the state directory path, or the newest entry on the machine is older than the schedule allows. In before-run mode the machine half is NO EVIDENCE YET, while a failing repository half is still a FAIL. Does not apply when nothing writes to a real system and nothing runs by itself.

**Blocks at.** Merge. Run evidence for the local half is required at merge.
