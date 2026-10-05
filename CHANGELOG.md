# Changelog

## 0.2.0 (unreleased)

- Repo created: buckets, plugin manifests, rules, docs template, decision records 0001 and 0002. Items being cleaned up wait in `in-progress/`, kept local and not published.
- Promoted agent-readiness-audit to `operations/` (model-invoked):
  - New "Skill craft" block: how a skill starts, what sits in the main file, each step says when it is done, nothing said twice or for nothing.
  - Asks one question, the gate, only when none was named; trigger and touches are read from the files. A check for skills that should be an agent, a subagent, a standing rule, a plugin or a plain script.
  - Reads plugins, marketplaces and .zip or .skill files.
  - Three scenarios in `evaluations/scenarios/` test Claude's report on Haiku, Sonnet and Opus.
  - The standard lives in `references/criteria.md` only; the checklists were removed (the report is the handover record).
- Repo checks: a skill lint for every promoted skill (name, description, length, links, tables of contents, docs page), and the audit skill's own checks run in CI.
