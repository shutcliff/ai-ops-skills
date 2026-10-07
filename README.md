# AI Ops Skills

Claude skills to run business operations with AI: practical tools that help business people bring AI into their day-to-day operations.

Built by an AI operations lead. Small, tested, and written in plain English, no coding needed. Each skill passes a readiness audit before it ships.

By Silvana Vasquez Sutcliffe.

## Install

**You need:** Claude Code with a terminal (check with `claude --version`); the readiness skills also need Python 3.9 or newer (check with `python3 --version`).

### As a plugin (recommended)

In Claude Code, run these two commands:

```
/plugin marketplace add shutcliff/ai-ops-skills
/plugin install ai-ops-skills@ai-ops-skills
```

To get new versions, run `/plugin marketplace update ai-ops-skills`, or turn on auto-update for this marketplace in `/plugin`.

### Copied into your project

1. Download the repo (green "Code" button on GitHub, then "Download ZIP").
2. Copy the skill folder you want from `skills/<bucket>/` into your project's `.claude/skills` folder.
3. Restart Claude Code. The copy is yours: it will not update on its own.

### Check it worked

Type `/` in Claude Code. The skills appear in the list.

## First thing to try

Open Claude Code in a folder that holds a skill or an agent and ask: "is this skill ready to share?". A good result: a report in the `docs/readiness` folder, a verdict, a short fix plan in plain words, and the question "Apply the plan now?". Each skill's README says more.

## When something looks wrong

| What you see | What it means | What to do |
|---|---|---|
| The skills do not appear after `/` | The plugin is not installed, or Claude Code was not restarted | Run the two install commands again, then restart Claude Code |
| "Python not found" or a script error | Python 3.9 or newer is missing | Install it, then check with `python3 --version` |
| An old version keeps running | Auto-update is off | Run `/plugin marketplace update ai-ops-skills` |
| A skill misbehaves | Its own symptom table covers it | Open that skill's README, linked below |

**Who to ask:** open an issue on this repository.

## Skills

More skills are being cleaned up and will be published here once they pass the promotion gate.

### User-invoked

You start these yourself, by typing `/` and the name.

(none yet)

### Model-invoked

Claude starts these on its own when your request matches.

- [agent-readiness-audit](./skills/operations/agent-readiness-audit/README.md): a pass or fail report on whether an agent, skill or plugin is ready for someone other than its builder
- [agent-readiness-fix](./skills/operations/agent-readiness-fix/README.md): applies an audit's fix plan; structure is tidied directly, each behaviour change is approved by you and then tested. Starts when you say yes to "Apply the plan now?"

## How this repo is run

- [CLAUDE.md](./CLAUDE.md): the rules for every change
- [CHANGELOG.md](./CHANGELOG.md): what changed, version by version
- [Decisions](./.agents/adr/): why the repo works this way

## What this repo is not

- **Skills tied to one company's tools or data.** Shared skills stay generic. Fork the repo and adapt your copy.
- **Engineering skills** (coding, testing, code review). Better collections exist, for example `mattpocock/skills`.

## License

MIT. See [LICENSE](./LICENSE).
