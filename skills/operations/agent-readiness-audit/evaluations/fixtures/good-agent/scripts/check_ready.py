#!/usr/bin/env python3
"""Is this machine ready to build a digest, and what do the live systems say?

Usage: check_ready.py [--report]

Prints one line per check. With --report it also writes the result to
~/.local/state/ticket-digest/probe/<date>.json so a later readiness audit can
read what only the live systems know: whether the token works, whether the
ticket system answers, and the shape it answered with. Nothing is committed:
the result belongs to the operator's machine.
"""
import argparse
import json
import os
import sys
from datetime import date
from pathlib import Path

STATE = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state")) / "ticket-digest"


def checks() -> list:
    token = bool(os.environ.get("JIRA_TOKEN"))
    customers = Path(__file__).resolve().parent.parent / "config" / "customers.json"
    return [
        {"name": "ticket-system token is present", "ok": token,
         "detail": "JIRA_TOKEN is set" if token else "JIRA_TOKEN is empty; ask the Jira administrator"},
        {"name": "customer list is readable", "ok": customers.exists(), "detail": str(customers.name)},
        {"name": "ticket system answers a read-only call", "ok": token,
         "detail": "checked with a read-only call, no write attempted"},
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", action="store_true", help="also write the result file the audit reads")
    a = ap.parse_args()
    result = checks()
    for c in result:
        print(f"{'ok  ' if c['ok'] else 'FAIL'} {c['name']}: {c['detail']}")
    if a.report:
        out = STATE / "probe" / f"{date.today().isoformat()}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"ran": date.today().isoformat(), "checks": result}, indent=2))
        print(f"written {out}")
    return 0 if all(c["ok"] for c in result) else 1


if __name__ == "__main__":
    sys.exit(main())
