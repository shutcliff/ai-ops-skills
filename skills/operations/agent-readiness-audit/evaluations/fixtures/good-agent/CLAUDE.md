# Weekly ticket digest agent

## Purpose

This agent produces a weekly digest of support tickets for one customer. It is run by the Support team lead every Monday. One run produces one markdown file, `digests/<customer>-<week>.md`, and prints a summary line in chat.

## What runs by itself

One behaviour is automatic: `scripts/weekly_digest_run.sh` builds last week's digests with nobody watching. It is off on a fresh install and reads one setting, `TICKET_DIGEST_AUTO`. Off means it writes nothing and changes no state. `./scripts/weekly_digest_run.sh --status` prints whether it is on.

## Who runs it

The Support team lead, or any operator the lead names. The builder is not needed for a run.

## Done looks like

A run is complete when:
1. `digests/<customer>-<week>.md` exists and opens.
2. Claude has printed `DIGEST WRITTEN <customer> <week> (<n> tickets)`.
3. The human opens the file and checks the ticket count against the ticket system's own count for the week.

## Rules

- Secrets in `.env` (see `.env.example`), never in config or instructions.
- The agent reads the ticket system; it never writes to it.
- Claude never counts or classifies tickets itself: `scripts/build_digest.py` does that.

## Run

```
python3 scripts/build_digest.py --customer <slug> --week <YYYY-Www> --dry-run
```

Then use the `ticket-digest` skill for the full run.
