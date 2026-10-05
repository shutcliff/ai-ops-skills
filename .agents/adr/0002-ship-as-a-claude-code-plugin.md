# 0002. Ship as a Claude Code plugin

Date: 2026-10-04. Status: accepted.

## Context

People need a way to install the skills and get fixes without copying files by hand.

## Decision

The repo is its own plugin marketplace (`.claude-plugin/marketplace.json`) with one plugin (`.claude-plugin/plugin.json`). The plugin lists its skills one by one, so only the promoted set ships. Copying a folder by hand stays possible for people who want to edit their copy.

## Consequences

- Updates arrive with `/plugin marketplace update`, or automatically.
- Every promotion touches `plugin.json`, so `claude plugin validate .` runs after each one (its one warning is expected; see `CLAUDE.md`).
