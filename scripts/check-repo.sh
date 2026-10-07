#!/usr/bin/env bash
# Repo checks, run on every pull request and before any push.
# 1. No em dashes. 2. The promoted set agrees across plugin.json and README.md.
# 3. Skill lint on every promoted skill (frontmatter, size, links, README).
# 4. Scrub check: no employer, colleague or client names.
# 5. Skill self-checks, the same ones CI runs: layers, proof cases, and the
#    readiness audit at the merge gate, for every promoted skill that ships them.
#    Names come from $SCRUB_NAMES (one per line, a GitHub secret in CI)
#    or from "${XDG_CONFIG_HOME:-$HOME/.config}/ai-ops-skills/scrub-names.txt" on the owner's computer.
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0

dash=$(printf '\xe2\x80\x94')
if grep -rIl "$dash" --exclude-dir=.git . >/dev/null; then
  echo "FAIL em dashes in:"; grep -rIl "$dash" --exclude-dir=.git .; fail=1
else echo "PASS no em dashes"; fi

skills=$(python3 -c "import json;print('\n'.join(json.load(open('.claude-plugin/plugin.json'))['skills']))")
for s in $skills; do
  case "$s" in ./skills/operations/*|./skills/productivity/*) ;; *) echo "FAIL $s is not in a promoted bucket"; fail=1;; esac
  [ -f "$s/SKILL.md" ] || { echo "FAIL $s/SKILL.md missing"; fail=1; }
  name=$(basename "$s")
  grep -q "$name" README.md || { echo "FAIL $name missing from README.md"; fail=1; }
done
echo "PASS promoted set checked ($(echo "$skills" | grep -c . || true) skills)"

# Skill lint: one line per failure, prefixed FAIL.
if python3 - $skills <<'PY'
import os, re, sys

def frontmatter(text):
    """Return (fields, body) from a SKILL.md. Simple key: value parsing, stdlib only."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    fields, key = {}, None
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fields[key] = val.strip("'\"") if val not in (">", "|", ">-", "|-") else ""
        elif key and line.startswith((" ", "\t")):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, text[end + 4:].lstrip("\n")

def has_toc(path):
    head = open(path, encoding="utf-8").read().splitlines()[:15]
    if any(l.startswith("#") and "contents" in l.lower() for l in head):
        return True
    return sum(1 for l in head if re.match(r"^\s*[-*\d.]+\s*\[.+\]\(.+\)", l)) >= 2

failed = False
def fail(msg):
    global failed
    failed = True
    print("FAIL " + msg)

for skill in sys.argv[1:]:
    skill = os.path.normpath(skill)
    name = os.path.basename(skill)
    bucket = os.path.basename(os.path.dirname(skill))
    path = os.path.join(skill, "SKILL.md")
    if not os.path.isfile(path):
        continue  # already reported by the promoted set check
    fm, body = frontmatter(open(path, encoding="utf-8").read())
    if fm is None:
        fail(f"{path}: no frontmatter")
        continue
    n = fm.get("name", "")
    if n != name:
        fail(f"{path}: name '{n}' does not match folder '{name}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", n) or len(n) > 64:
        fail(f"{path}: name '{n}' must be lowercase words joined by hyphens, 64 characters at most")
    d = fm.get("description", "")
    if not d:
        fail(f"{path}: description missing")
    elif len(d) > 1024:
        fail(f"{path}: description is {len(d)} characters, the limit is 1024")
    elif d.startswith(("I ", "You ")):
        fail(f"{path}: description starts with 'I ' or 'You '; write it in the third person")
    lines = body.count("\n") + 1
    if lines >= 500:
        fail(f"{path}: body is {lines} lines, keep it under 500")
    refs = set()
    for target in re.findall(r"\]\(([^)\s]+)\)", body):
        if not re.match(r"^(https?:|mailto:|#)", target):
            refs.add(target.split("#")[0])
    refs.update(re.findall(r"`((?:references|scripts|assets)/[^`\s]+)`", body))
    for ref in sorted(r for r in refs if r):
        if "<" in ref or "*" in ref:
            continue  # a placeholder or a pattern, not a file
        if not os.path.exists(os.path.join(skill, ref)):
            fail(f"{path}: link or path '{ref}' does not exist")
    refdir = os.path.join(skill, "references")
    for root, _, files in os.walk(refdir):
        for f in sorted(files):
            p = os.path.join(root, f)
            if f.endswith(".md") and len(open(p, encoding="utf-8").read().splitlines()) > 100 and not has_toc(p):
                fail(f"{p}: over 100 lines with no table of contents in its first 15 lines")
    readme = os.path.join("skills", bucket, "README.md")
    if not os.path.isfile(readme) or name not in open(readme, encoding="utf-8").read():
        fail(f"{name} missing from {readme}")
    if not os.path.isfile(os.path.join(skill, "README.md")):
        fail(f"{name}: README.md missing in the skill folder")

sys.exit(1 if failed else 0)
PY
then echo "PASS skill lint"; else fail=1; fi

list=$(mktemp)
scrub_file="${XDG_CONFIG_HOME:-$HOME/.config}/ai-ops-skills/scrub-names.txt"
if [ -n "${SCRUB_NAMES:-}" ]; then printf '%s\n' "$SCRUB_NAMES" > "$list"
elif [ -f "$scrub_file" ]; then cp "$scrub_file" "$list"
fi
if [ -s "$list" ]; then
  hits=$(grep -rIliwf "$list" --exclude-dir=.git . || true)
  if [ -n "$hits" ]; then echo "FAIL scrub names found in:"; echo "$hits"; fail=1; else echo "PASS scrub check"; fi
else echo "FAIL no scrub list available, so the scrub check could not run"; fail=1; fi
rm -f "$list"

for s in $skills; do
  if [ -f "$s/scripts/check_layers.py" ] && [ -f "$s/scripts/run_evals.py" ] && [ -f "$s/scripts/audit.py" ]; then
    out=$( (cd "$s" && python3 scripts/check_layers.py && python3 scripts/run_evals.py) 2>&1 && python3 "$s/scripts/audit.py" "$s" --gate merge --ci 2>&1 ) \
      && echo "PASS self-checks $(basename "$s")" \
      || { echo "FAIL self-checks $(basename "$s"):"; echo "$out" | grep -E "FAIL|drift|blocks this gate|Result" | head -20; fail=1; }
  fi
done
exit $fail
