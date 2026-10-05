# 0001. One public home for shared skills

Date: 2026-10-04. Status: accepted.

## Context

The owner's skills lived in three private places, with copies that had drifted apart. Some of them are useful to business teams.

## Decision

- Skills meant for others live only here. The owner's work system and personal skills stay in private repos.
- An item enters this repo only through a pull request the owner approves, and ships only after the promotion gate in `CLAUDE.md`.
- Structure follows Matt Pocock's `skills` repo (bucket folders, promoted set, changelog, decision records), adapted for non-technical business users: a plain-English docs page per skill.

## Consequences

- One copy of each shared skill. Fixes reach every user through the plugin.
- Promotion takes work: each item needs a cleanup pass before it ships.
