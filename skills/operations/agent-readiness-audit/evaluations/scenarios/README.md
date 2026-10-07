# Scenarios: the whole skill, run by Claude

`run_evals.py` checks the script alone. These three scenarios check what Claude does with the whole skill: the verdict, the evidence and the report.

**How to run.** Before merging a change to this skill, open a fresh Claude Code session in this skill's folder, once each on Haiku, Sonnet and Opus. Paste a scenario's prompt, then compare the report against its "Must contain" lines. A scenario passes when every line holds. Record the result per model in the pull request.
