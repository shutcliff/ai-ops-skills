# agent-readiness-audit

Here an **agent** is any skill, plugin, command or subagent that someone other than its builder will run.

**What it does:** checks whether a Claude Code agent, skill, command or subagent is built well enough for someone other than its builder to run it, against plain-English criteria with a pass or fail each.

**Who runs it:** the builder before sharing an agent with a teammate to test, and the reviewer before it is merged into a repository anyone can install from.

**What it produces:** one report, `docs/readiness/<date>-<gate>-readiness-report.md`, verdict first, with every failure naming a file, a line and a fix. A script checks structure in seconds, and Claude reads the instruction files for meaning. To run the script on every pull request of an agent repository, copy `assets/ci-readiness.yml` into its `.github/workflows/`.

## How it starts

Model-invoked: Claude starts it when someone asks whether an agent or skill is ready to share or merge, or when a pull request changes instruction files, because people ask "is this ready?" without remembering the skill's name, and a pull-request review must reach it every time. You can still start it by typing its name.

# Install

## As a plugin (recommended)

In Claude Code, run these two commands:

```
/plugin marketplace add shutcliff/ai-ops-skills
/plugin install ai-ops-skills@ai-ops-skills
```

To get new versions, run `/plugin marketplace update ai-ops-skills`, or turn on auto-update for this marketplace in `/plugin`.

## Copied into your project

1. Download the repo (green "Code" button on GitHub, then "Download ZIP").
2. Copy the skill folder you want from `skills/<bucket>/` into your project's `.claude/skills/`.
3. Restart Claude Code. The copy is yours: it will not update on its own.

## Check it worked

Type `/` in Claude Code. The skills appear in the list.

## Run these two first

From the skill folder: `skills/operations/agent-readiness-audit` in a downloaded copy of the repository. Installed as a plugin, `find ~/.claude/plugins -type d -name agent-readiness-audit` prints where it is.

```
python3 scripts/check_layers.py
python3 scripts/run_evals.py
```

You need:

- Python 3.9 or newer, standard library only: check with `python3 --version`.
- Read access to the agent repository you audit: ask its owner, or clone it with `git clone <url>`.
- Sonnet or Opus for the audit itself. In the scenario tests, Haiku missed findings that both larger models caught.

Both commands end on a passing line; anything else names the file to fix. Before merging a change to this skill, also run the three scenarios in `evaluations/scenarios/` (they test Claude's report, not only the script). To run the audit script alone: `python3 scripts/audit.py <folder> --gate <share|merge>`. The gates: `share` is giving the agent to a teammate to test (structure, safety, setup; no run needed), `merge` is putting it into a repository anyone can install from (everything in share, plus proof cases, failure plans and run evidence). In CI add `--ci`, which leaves the run evidence to the reviewer.

Then open Claude Code inside the agent repository and ask whether it is ready to `share` (the default) or `merge`. For `merge`, do it on the machine where the teammate's test ran, so the run evidence is there. Without a terminal (the desktop or web app), attach the folder or the .zip: Claude applies the criteria by reading and says the script layer did not run.

## When something looks wrong

| What you see | What it means | What to do |
|---|---|---|
| `NOT AN AGENT REPO` and exit code 2 | The folder holds none of `CLAUDE.md`, `.claude/`, or a `SKILL.md` at its root | Point at the repository root, or at the one skill folder you want audited |
| Run evidence says before-run at the merge gate | No run log or probe result on this machine | Run the agent once here (the teammate's test counts), unless the run-evidence exception under "Before a run and after a run" in `references/criteria.md` applies (nothing writes to a real system and nothing runs by itself) |
| `check_layers.py` fails | A criterion name or gate differs between `scripts/audit.py`, `references/criteria.md` and `references/report-template.md`, a slug in an expected file is wrong, or a criteria count appears in prose | Open the file and line it names and make it match `scripts/audit.py` |
| `run_evals.py` fails | The script no longer gives the expected verdict on a test case | Read the case it names; fix the script, or update the expected file with a one-line reason |

**Who to ask:** the repository's maintainer, through an issue on the repository.
