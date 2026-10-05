# Weekly ticket digest agent

What it does: builds a weekly support ticket digest for one customer. Who runs it: the Support team lead. Output: one markdown file per customer per week under `digests/`.

## Before you start: what you need and who gives it to you

1. A read-only ticket-system token: ask your Jira administrator, then copy `.env.example` to `.env` and fill `JIRA_TOKEN`.
2. Python 3.11 and the dependencies: `pip install -r requirements.txt` inside a virtual environment.
3. Read access to the customer list: `config/customers.json` ships with the repository, no access request needed.

## Step one, always: is this machine ready?

```
python3 scripts/check_ready.py --report
```

It checks the token, the dependencies, and that the ticket system answers, then writes what it found to `~/.local/state/ticket-digest/probe/<date>.json`. Any failed line is the first thing to fix; every other error in a run is usually this error in disguise.

## Running it

```
python3 scripts/build_digest.py --customer <slug> --week <YYYY-Www> --dry-run
```

A dry run prints `DRY RUN OK` and writes nothing. Drop `--dry-run` for the real thing. One customer and one week at a time, so a single bad week can be rebuilt on its own. Re-running a week that already has a digest skips it unless you pass `--overwrite`, so a repeat run is safe.

## The automatic weekly run, and how to turn it off

`scripts/weekly_digest_run.sh` can build last week's digests with nobody watching. It is off by default: it only runs when `TICKET_DIGEST_AUTO=on` is set in the environment that starts it, and with the switch off it writes nothing and changes no state. To turn it off again, unset that variable. To see the current state:

```
./scripts/weekly_digest_run.sh --status
```

During an automatic run the settings file denies Edit, Write, and git, so the run cannot change the agent itself. Every write still goes through `scripts/build_digest.py`.

Arming it is a deliberate step: install, run one week by hand with a person watching, then set `TICKET_DIGEST_AUTO=on`. The run has a ceiling of 20 minutes or 40 turns; on hitting either it stops before writing and the run entry says `incomplete`. It also takes a lock file, `~/.local/state/ticket-digest/run.lock`, before it starts, so if a person is building a week at the same moment the automatic run exits with "another run holds the lock" and tries again next week.

## Where the run trace lands

Each run appends one entry to `~/.local/state/ticket-digest/logs/<date>.md`: the week the run covers, what it wrote, what it skipped, whether it ran from a person or automatically, and whether an empty week was quiet or the query was broken. Nothing about a run is committed: this repository is a template, the run data belongs to whoever runs it.

## When something looks wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `DIGEST WRITTEN` says 0 tickets | The week really was quiet, or the query broke | Open the run entry: a quiet week says `quiet`, a broken query says `error` with the message |
| The readiness check fails on the token | The token expired or was never filled in | Ask the Jira administrator for a new read-only token and refill `.env` |
| A digest exists but looks stale | The week was rebuilt without `--overwrite` | Re-run that week with `--overwrite` |
| Nothing writes and no error appears | You left `--dry-run` on | Re-run without the flag |

## Who to ask

Questions about a digest's content: the Support team lead. Questions about the ticket system's access: the Jira administrator. Questions about the code: the agent owner named in the repository settings.
