# Team tools

What it does: two helpers for a support team. report-builder turns a ticket export into a weekly report; notes-digest summarises meeting notes into a short digest. Who runs it: anyone on the support team. Output: a markdown report or digest, shown in the chat.

## How to get it

- Install the team-tools plugin from your organisation's plugin marketplace. If it is not listed, ask the workspace admin.

## What you need first

- Python 3.9 or later, checked with `python3 --version`. Only report-builder needs it.
- Access to the Notion connector: ask the workspace admin to add it to your account.

Settings live in `~/.config/team-tools/config.json` on your own machine; the plugin creates it on first run.

## First thing to type

Run `/team-tools:check` first. It confirms Python and the Notion connector and says what is missing. Then ask "build the weekly report from this export".

## Done looks like: what a good result is

A report with one line per ticket category, and a total that matches the row count of the export.

## Skills in this plugin

- report-builder: the weekly report from a ticket export.
- notes-digest: a short digest of this week's meeting notes.

## Where it works

Claude Code, and the desktop and web apps. report-builder runs a Python script, so it needs Claude Code with a terminal; notes-digest works everywhere.

## Who to ask

The support operations lead owns this plugin.

## When something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| "Notion is not connected" | The connector is missing on your account | Ask the workspace admin to add the Notion connector |
| "Python 3.9 or later is missing" | report-builder cannot run its script | Use Claude Code on a machine with Python 3.9 or later |

## What Claude never does

- Never store an API key in a file or in the chat.
