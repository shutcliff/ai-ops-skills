---
name: sheet-sync
description: Copy the weekly totals into the team sheet. Use when someone asks to sync the weekly totals.
---

# Sheet sync

Run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/missing.py` to build the totals.
Then run `/guard-tools:verify` to compare them.
The column rules live in `~/.claude/skills/sheet-sync/rules.md`.
Write the draft email for the user.
Write the totals to the sheet.

## Never do

- Never delete rows in the sheet.
