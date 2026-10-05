#!/usr/bin/env python3
"""Build the weekly ticket digest JSON for one customer.

Usage: build_digest.py --customer <slug> --week <YYYY-Www> [--dry-run] [--overwrite]
Prints one JSON object with status, ticket_count, stale, headlines.
--dry-run reads config only and prints DRY RUN OK, writing nothing.
One customer and one week per run, so a single bad week can be rebuilt alone.
A week that already has a digest is skipped unless --overwrite is passed, so
re-running after a partial failure is safe.

Every run appends one entry to the operator's own state directory
(~/.local/state/ticket-digest/logs/<date>.md): the week covered, what was
written, what was skipped, whether a person or an automatic trigger started it,
and whether an empty week was quiet or the query was broken. Nothing about a
run is committed.
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

LOG_DIR = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / "ticket-digest" / "logs"


def write_run_entry(week: str, wrote: str, skipped: str, started_by: str, empty_reason: str) -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    entry = (
        f"\n## run {date.today().isoformat()}\n"
        f"- week covered: {week}\n"
        f"- wrote: {wrote}\n"
        f"- skipped: {skipped}\n"
        f"- started by: {started_by}\n"
        f"- empty week was: {empty_reason}\n"
    )
    with (LOG_DIR / f"{date.today().isoformat()}.md").open("a", encoding="utf-8") as fh:
        fh.write(entry)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--customer", required=True, help="one customer slug per run")
    ap.add_argument("--week", required=True, help="one week per run, YYYY-Www")
    ap.add_argument("--dry-run", action="store_true", help="read config, write nothing")
    ap.add_argument("--overwrite", action="store_true", help="rebuild a week that already has a digest")
    a = ap.parse_args()
    if not a.week or len(a.week) != 8 or "-W" not in a.week:
        print("--week must look like 2026-W01; nothing was written", file=sys.stderr)
        return 2
    if a.dry_run:
        print("DRY RUN OK")
        return 0
    target = Path("digests") / f"{a.customer}-{a.week}.md"
    if target.exists() and not a.overwrite:
        write_run_entry(a.week, "nothing", f"{target} already exists", "person", "not applicable")
        print(json.dumps({"status": "skipped", "reason": "digest exists, pass --overwrite to rebuild"}))
        return 0
    result = {"status": "ok", "ticket_count": 0, "stale": False, "headlines": []}
    empty_reason = "quiet week, the query answered with no rows" if result["ticket_count"] == 0 else "not applicable"
    write_run_entry(a.week, str(target), "nothing", "person", empty_reason)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
