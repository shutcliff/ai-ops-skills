# Writing a docs page

Every promoted skill has one page at `docs/<bucket>/<skill-name>.md`. The reader is a business user, not technical, who has never seen the skill. Plain English, short sentences, no em dashes.

## Template

```
# <skill-name>

<One sentence: what it produces, for whom.>

User-invoked | Model-invoked

## What it does
<3 to 5 bullets. The output first, then the steps the user will notice.>

## When to reach for it
<2 to 4 real situations, in the user's words.>

## Common questions
<3 to 5 questions people actually asked, each with a short answer. Find them in issues, pull requests and the skill's stop-and-ask list.>

## It's working if
<2 or 3 things the user can check, ideally a number.>
```

## When a page changes

- New, renamed or changed skill: create or re-sync its page in the same pull request.
- Skill removed from a promoted bucket: the page stays, with "Archived on <date>: <why>" as its first line.
