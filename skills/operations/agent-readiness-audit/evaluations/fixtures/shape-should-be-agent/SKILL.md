---
name: shape-should-be-agent
description: Adds the new support tickets to the team's tracking sheet each morning. Use when someone asks to set up or change the morning ticket log.
---

# Morning ticket log

This skill runs every morning as a scheduled task under the support team's shared account. It keeps a state file with the last ticket number it logged, so each run adds only the tickets that arrived since the last run.

To pause it, turn off the scheduled task in the app's schedule list.

## Step 1. Read the new tickets

Read the ticket export and keep the tickets numbered above the one in the state file. Done when you hold a list of new ticket numbers.

## Step 2. Log them

Write one row per new ticket to the team's Google Sheet, then save the highest number to the state file. Done when the sheet has a row for each new ticket.
