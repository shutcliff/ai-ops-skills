# Changelog

## 0.4.0

- Promoted agent-readiness-fix to `operations/` (model-invoked): applies an audit's fix plan. Structure changes go in directly; each behaviour change is shown with one "After this" sentence, written after a yes, then tested by a separate agent on fake data in a scratch copy. At the end it tests again any change a later change touched.
- agent-readiness-audit ends a NOT READY run with "Apply the plan now?"; a yes starts the fixer. A value only the owner knows is asked, never stated as a fact, and every category is checked against the skill's central definition.
- Repo checks: the skill lint now looks for the README in the skill's own folder.

## 0.3.0

- agent-readiness-audit:
  - Two gates instead of three, in the order an agent lives: `share` (a teammate tests it) and `merge` (it goes into a repository anyone can install from). The old handover gate skipped Format and Skill craft, so a skill could pass with its structure broken; both now block at share.
  - New criterion "A teammate can install it" (share). "Built for more than one person to run" keeps the readiness check, roles, symptom table and supported surfaces (merge).
  - `--ci` judges the merge gate from the files and leaves the run evidence to the reviewer.
  - New script checks: text above the H1 title or a second H1, steps written as a numbered list instead of step headings, Never-do and Stop-and-ask lists under 3 lines, "Use at / after / before" trigger wording on a user-invoked skill, and an explicit note when a skill has no reference files.
  - The report lists failures that block merge even at the share gate.
  - New proof case `legacy-layout`; good fixtures brought up to the standard.
  - The fix plan splits structure changes (one "Tidy the structure" step, no change in what the skill does) from behaviour changes (each with an "After this" sentence and a test). A "For the fixer" section at the end of the report holds the skill's anatomy: branches, steps and reference, leading word, legwork, size and no-ops.
  - Criteria: every branch needs a step, legwork needs a forced check, the leading word is defined once, size and no-ops are reported, and a model-invoked skill needs a case that checks it starts.
- Promotion gate in `CLAUDE.md` is now `merge`.

## 0.2.0 (unreleased)

- Repo created: buckets, plugin manifests, rules, docs template, decision records 0001 and 0002. Items being cleaned up wait in `in-progress/`, kept local and not published.
- Promoted agent-readiness-audit to `operations/` (model-invoked):
  - New "Skill craft" block: how a skill starts, what sits in the main file, each step says when it is done, nothing said twice or for nothing.
  - Asks one question, the gate, only when none was named; trigger and touches are read from the files. A check for skills that should be an agent, a subagent, a standing rule, a plugin or a plain script.
  - Reads plugins, marketplaces and .zip or .skill files.
  - Three scenarios in `evaluations/scenarios/` test Claude's report on Haiku, Sonnet and Opus.
  - The standard lives in `references/criteria.md` only; the checklists were removed (the report is the handover record).
- Repo checks: a skill lint for every promoted skill (name, description, length, links, tables of contents, docs page), and the audit skill's own checks run in CI.
