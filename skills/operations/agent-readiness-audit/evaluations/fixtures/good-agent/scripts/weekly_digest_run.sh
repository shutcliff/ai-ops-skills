#!/usr/bin/env bash
# Build last week's digests without a person present.
#
# This is a module with a switch. It is off on a fresh install: set
# TICKET_DIGEST_AUTO=on to enable it, and unset it to turn it off again.
# When it is off this script writes nothing and changes no state.
# To see whether it is on:  ./scripts/weekly_digest_run.sh --status
set -euo pipefail

: "${TICKET_DIGEST_AUTO:=off}"
PROJECT_DIR="${TICKET_DIGEST_DIR:-$(cd "$(dirname "$0")/.." && pwd)}"
CLAUDE_BIN="${CLAUDE_BIN:-claude}"

if [[ "${1:-}" == "--status" ]]; then
  echo "automatic weekly run: $TICKET_DIGEST_AUTO (default off)"
  exit 0
fi

if [[ "$TICKET_DIGEST_AUTO" != "on" ]]; then
  echo "automatic weekly run is off (TICKET_DIGEST_AUTO=$TICKET_DIGEST_AUTO); nothing to do"
  exit 0
fi

cd "$PROJECT_DIR"

# One writer at a time: a person running the skill by hand and this run must not
# build the same week together. The lock lives in the state directory, never in git.
STATE_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/ticket-digest"
mkdir -p "$STATE_DIR"
exec 9>"$STATE_DIR/run.lock"
if ! flock -n 9; then
  echo "another run holds the lock ($STATE_DIR/run.lock); nothing to do"
  exit 0
fi

# Ceiling: 20 minutes of wall clock or 40 turns, whichever comes first. On hitting
# either, timeout ends the process before any write and the run entry says incomplete.
timeout 20m "$CLAUDE_BIN" -p "Follow .claude/skills/ticket-digest/SKILL.md for last week. Build one customer at a time with scripts/build_digest.py, which writes the run entry. Do not pass --overwrite. If the ticket system returns no rows, say whether the week was quiet or the query failed, and do not write a digest." \
  --max-turns 40 \
  --permission-mode acceptEdits
