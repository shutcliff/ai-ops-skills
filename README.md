# AI Ops Skills

Claude skills to run business operations with AI: practical tools that help business people bring AI into their day-to-day operations.

Built by an AI operations lead. Small, tested, and written in plain English, no coding needed. Each skill passes a readiness audit before it ships.

By Silvana Vasquez Sutcliffe.

## Install

See [install steps](./.agents/install-block.md). Two ways:

1. **As a plugin** (recommended): updates reach you automatically.
2. **Copied into your project**: the files are yours to change.

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
