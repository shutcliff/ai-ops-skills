# ai-ops-skills

Claude skills to run business operations with AI: practical tools that help business people bring AI into their day-to-day operations. Written in plain English for people who do not code. Public. Owner: Silvana Vasquez Sutcliffe.

## Buckets

Skills live in bucket folders under `skills/`:

- `operations/`: running operations with AI (auditing agents and skills, sizing projects, designing AI pipelines)
- `productivity/`: everyday work tools (decks, Notion, session reviews)
- `in-progress/`: being cleaned up, kept local only. Git ignores everything in it except its README, so nothing in it is published or shipped. Agents waiting here sit in `in-progress/_agents/`.

`operations/` and `productivity/` are the **promoted** buckets. The plugin ships exactly the promoted set.

## Rules for every change

1. **Promoted means listed in three places:** the `skills` array in `.claude-plugin/plugin.json`, the top-level `README.md`, and the bucket's `README.md`. Anything outside the promoted buckets appears in none of them. Run `claude plugin validate .` after touching a manifest. Its one warning, that this CLAUDE.md is not shipped to plugin users, is expected: this file is for people editing the repo.
2. **Promotion gate.** An item leaves `in-progress/` only when it passes:
    - the readiness audit (`agent-readiness-audit`, gate `merge`; `share` first when a teammate tests it), whose Format and Skill craft blocks apply Anthropic's skill authoring best practices (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
    - at least 3 proof cases in the skill's `evaluations/`
    - the repo checks (`scripts/check-repo.sh`), which lint every promoted skill
    - generic content: no names of people, employers or clients, no personal paths. "The user", never the owner's name.
3. **Trigger on purpose.** Every `SKILL.md` is either user-invoked (`disable-model-invocation: true`) or model-invoked, and its docs page says which. The README groups skills under **User-invoked** and **Model-invoked**.
4. **README.** Every promoted skill has a `README.md` in its folder, for people: what it does, who runs it, what it produces, how to install and check it, and a symptom table. It travels with every install.
5. **Changelog and version.** Every promotion, rename, removal or behaviour change adds a line to `CHANGELOG.md` and bumps `version` in `plugin.json` (new skill or behaviour: minor; fix: patch).
6. **Decisions.** A choice that shapes the repo gets a numbered record in `.agents/adr/`. A request we say no to gets one line under "What this repo is not" in `README.md`.
7. **Plain English, no em dashes,** in every file. Rewrite the sentence, never swap the character blindly.
8. **Never in this repo:** names of employers, colleagues or clients, company data, credentials, personal paths. The scrub check on every pull request enforces it.

## How work arrives

- Edits happen here only, through a pull request, from any computer. Commits use the owner's personal email.
- New items come from the owner's private work repo, by a pull request she approves. Nothing arrives automatically.
- Install commands are copied word for word from `.agents/install-block.md`.

Terms used here: `GLOSSARY.md`.
