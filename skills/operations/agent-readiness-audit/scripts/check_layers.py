#!/usr/bin/env python3
"""Layer consistency check: the criterion names cannot drift apart.

The criteria have plain names and no codes, so the name is the only reference
between the layers. This script checks the names and gates in
references/criteria.md and references/report-template.md against
scripts/audit.py, the slugs in the expected files, and that no prose states a
criteria count.

What it checks:
  1. Every criterion name appears verbatim in the criteria file and the report
     template.
  2. The expected-result files are keyed by the script's own slugs, no more and
     no fewer.
  3. Block names match the script's list in the criteria file and the report
     template.
  4. Gate agreement: each criterion's "Blocks at" line in the criteria file and
     each row of the report template name the same gate as the code.
  5. No layer states how many criteria there are. The count lives only in
     scripts/audit.py, so prose cannot go stale when a criterion is added.

Changing the criteria. Criteria change through a pull request, reviewed by the
team that owns the standard and one builder.
  - Rename: change the name in CRITERIA in scripts/audit.py, then in
    references/criteria.md and references/report-template.md.
  - Add: add it to CRITERIA, write its section in references/criteria.md with a
    "**Blocks at.**" line matching its gate, add its row to
    references/report-template.md, and add its expected result to every file in
    evaluations/expected/.
  - Either way, the change is done when this script and run_evals.py both pass.

Usage:
    python3 check_layers.py

Exit 0 when every layer agrees, 1 otherwise. Standard library only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))

from audit import BLOCKS, CRITERIA  # noqa: E402

# Layers inside the portable skill folder.
LAYER_FILES = [
    SKILL / "SKILL.md",
    SKILL / "README.md",
    SKILL / "references" / "criteria.md",
    SKILL / "references" / "report-template.md",
    SKILL / "references" / "process-agent-patterns.md",
    SKILL / "assets" / "ci-readiness.yml",
    HERE / "audit.py",
    HERE / "run_evals.py",
]

CRITERIA_FILE = SKILL / "references" / "criteria.md"
REPORT_TEMPLATE = SKILL / "references" / "report-template.md"

GATE_WORDS = {"share": "share", "merge": "merge"}

NUMBER_WORDS = ("one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|"
                "sixteen|seventeen|eighteen|nineteen|twenty|thirty")
COUNT_RE = re.compile(r"\b(\d+|(?:twenty|thirty)[- ](?:one|two|three|four|five|six|seven|eight|nine)|" + NUMBER_WORDS + r")\s+criteria\b", re.I)


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def criteria_gates(text: str) -> dict:
    """Map each '### <name>' section of the criteria file to the gate its
    '**Blocks at.**' line names (first word), or None when the line is missing."""
    out = {}
    heads = list(re.finditer(r"^###\s+(.+?)\s*$", text, re.M))
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt = re.search(r"^#{1,2}\s", text[m.end():end], re.M)  # a block heading ends the section
        section = text[m.end():m.end() + nxt.start()] if nxt else text[m.end():end]
        g = re.search(r"\*\*Blocks at\.\*\*\s*(Share|Merge)", section)
        out[m.group(1).strip()] = GATE_WORDS[g.group(1).lower()] if g else None
    return out


def template_rows(text: str) -> dict:
    """Map each criterion row of the report template ('| block | name | ... | gate |')
    to (block, gate), the gate being the cell that holds a gate word."""
    rows = {}
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        gate = next((GATE_WORDS[c.lower()] for c in cells[2:] if c.lower() in GATE_WORDS), None)
        rows[cells[1]] = (cells[0], gate)
    return rows


def main() -> int:
    names = [c.name for c in CRITERIA]
    slugs = {c.slug for c in CRITERIA}
    problems: list[str] = []

    layers = [p for p in LAYER_FILES if p.exists()]
    for p in LAYER_FILES:
        if not p.exists():
            problems.append(f"layer file missing: {p}")

    # 1. every name present in the files that must list all of them
    must_list_all = [CRITERIA_FILE, REPORT_TEMPLATE]
    for p in must_list_all:
        text = read(p)
        for name in names:
            if name not in text:
                problems.append(f"{p.name} does not carry the criterion name '{name}'")

    # 2. expected-result files keyed by the script's slugs
    exp_dir = SKILL / "evaluations" / "expected"
    for p in sorted(exp_dir.glob("*.json")) if exp_dir.exists() else []:
        try:
            data = json.loads(read(p))
        except Exception as e:  # noqa: BLE001
            problems.append(f"{p.name} is not valid JSON ({e})")
            continue
        keys = {k for k in data if not k.startswith('_')}  # _mode and friends are settings, not criteria
        for extra_key in sorted(keys - slugs):
            problems.append(f"{p.name} expects a result for '{extra_key}', which is not a criterion")
        for missing in sorted(slugs - keys):
            problems.append(f"{p.name} has no expected result for '{missing}'")

    # 3. block names, in every file that lists all the criteria
    crit_text = read(CRITERIA_FILE)
    for p in must_list_all:
        text = read(p)
        for block in BLOCKS:
            if block not in text:
                problems.append(f"{p.name} does not carry the block name '{block}'")
    for m in re.finditer(r"^## Block\s+(.+)$", crit_text, re.M):
        if m.group(1).strip() not in BLOCKS:
            problems.append(f"references/criteria.md has an unknown block '{m.group(1).strip()}'")

    # 4. gate agreement: the code is the authority
    code_gate = {c.name: c.gate for c in CRITERIA}
    code_block = {c.name: c.block for c in CRITERIA}
    gates_in_criteria = criteria_gates(crit_text)
    for name in names:
        if name not in gates_in_criteria:
            problems.append(f"criteria.md has no '### {name}' section")
        elif gates_in_criteria[name] is None:
            problems.append(f"criteria.md: '{name}' has no '**Blocks at.**' line naming Share or Merge")
        elif gates_in_criteria[name] != code_gate[name]:
            problems.append(f"criteria.md: '{name}' says it blocks at {gates_in_criteria[name]}, the code says {code_gate[name]}")
    rows = template_rows(read(REPORT_TEMPLATE))
    for name in names:
        if name not in rows:
            problems.append(f"report-template.md has no table row for '{name}'")
            continue
        block, gate = rows[name]
        if gate != code_gate[name]:
            problems.append(f"report-template.md: the row for '{name}' says it blocks at {gate}, the code says {code_gate[name]}")
        if block != code_block[name]:
            problems.append(f"report-template.md: the row for '{name}' sits in block '{block}', the code says '{code_block[name]}'")

    # 5. no layer states how many criteria there are
    for p in layers:
        for i, line in enumerate(read(p).splitlines(), 1):
            m = COUNT_RE.search(line)
            if m:
                problems.append(f"{p.name}:{i} states a count of criteria ('{m.group(0)}'). The count lives only in scripts/audit.py; say 'the criteria'")

    print(f"Layers checked: {len(layers)}")
    if problems:
        print(f"\n{len(problems)} drift problem(s):")
        for pr in problems:
            print(f"  - {pr}")
        print("\nFix: make the layers agree with the criterion names and gates in scripts/audit.py, or change them there first.")
        return 1
    print(f"Every layer agrees on all {len(names)} criterion names and gates, in {len(BLOCKS)} blocks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
