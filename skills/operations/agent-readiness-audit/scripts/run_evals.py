#!/usr/bin/env python3
"""Run the audit script against its own fixtures and compare with the expected results.

Usage: python3 run_evals.py          (from anywhere; paths are resolved from this file)
Exit 0 when every case matches, 1 otherwise. Standard library only.

Each case in evaluations/cases/<name>.json names a fixture folder, a gate, the
expected exit code, and optionally a mode and a state directory holding run
evidence. evaluations/expected/<name>.json (optional) holds the expected verdict
per criterion, keyed by the criterion slugs in audit.py. It may also carry
_must_mention: {slug: [text, ...]}, where every text must appear in that
finding's what, fix and evidence, so a case can prove the right reason and not
only the right verdict. A case may name "pack" (a fixture folder) instead of
"fixture": the folder is zipped at run time, with any "pack_extra" members
added (such as a path that climbs out with '..'), and the archive is audited
as a .zip target. A case may also carry "args", a list of extra flags for
audit.py (such as the survey answers --touches read). A mismatch prints the
criterion, the expected verdict, and the actual one, so a change to audit.py
that alters a verdict is visible before it ships.

After editing the skill, run check_layers.py too: it fails when a criterion name
or gate in criteria.md or report-template.md differs from audit.py, an expected
file uses a wrong slug, or prose states a criteria count.
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
EVALS = SKILL / "evaluations"


def load_json(path):
    """(data, None) or (None, a plain message), so one bad file never hides the other cases."""
    try:
        return json.loads(path.read_text()), None
    except Exception as e:  # noqa: BLE001
        return None, f"cannot read {path.relative_to(SKILL)}: {e}"


def pack(folder: Path, out: Path, extra: dict) -> Path:
    """Zip a fixture folder under its own name, plus any extra members as given."""
    with zipfile.ZipFile(out, "w") as z:
        for f in sorted(folder.rglob("*")):
            if f.is_file():
                z.write(f, str(Path(folder.name) / f.relative_to(folder)))
        for name, text in extra.items():
            z.writestr(name, text)
    return out


def main():
    failures = 0
    cases = sorted((EVALS / "cases").glob("*.json"))
    if not cases:
        print("No cases found under evaluations/cases/")
        return 1
    # An expected file with no case never runs, so it would rot unseen.
    case_names = {c.stem for c in cases}
    orphans = sorted(p.name for p in (EVALS / "expected").glob("*.json") if p.stem not in case_names)
    for o in orphans:
        print(f"FAIL  evaluations/expected/{o} has no case in evaluations/cases/")
        failures += 1
    case_failures = 0
    for case_file in cases:
        case, err = load_json(case_file)
        if err:
            print(f"FAIL  {case_file.stem}\n      {err}")
            case_failures += 1
            continue
        scratch = None
        if case.get("pack"):
            scratch = Path(tempfile.mkdtemp(prefix="readiness-evals-"))
            fixture = pack(EVALS / case["pack"], scratch / (Path(case["pack"]).name + ".zip"), case.get("pack_extra", {}))
        else:
            fixture = EVALS / case["fixture"]
        cmd = [sys.executable, str(HERE / "audit.py"), str(fixture), "--gate", case["gate"], "--json"]
        if case.get("mode"):
            cmd += ["--mode", case["mode"]]
        if case.get("state_dir"):
            cmd += ["--state-dir", str(EVALS / case["state_dir"])]
        cmd += [str(a) for a in case.get("args", [])]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if scratch:
            # remove the zip and the folder the audit extracted it into
            try:
                extracted = json.loads(proc.stdout).get("archive", {}).get("extracted_to", "")
            except Exception:  # noqa: BLE001
                extracted = ""
            if extracted and Path(extracted).name.startswith("readiness-audit-"):
                shutil.rmtree(extracted, ignore_errors=True)
            shutil.rmtree(scratch, ignore_errors=True)
        ok = proc.returncode == case["expected_exit"]
        detail = []
        if not ok:
            detail.append(f"exit code: expected {case['expected_exit']}, got {proc.returncode}")
        expected_file = EVALS / "expected" / f"{case['case']}.json"
        if expected_file.exists() and proc.returncode != 2:
            expected, err = load_json(expected_file)
            if err:
                expected = {}
                ok = False
                detail.append(err)
            try:
                payload = json.loads(proc.stdout)
                findings = {f["slug"]: f for f in payload["findings"]}
                actual = {slug: f["result"] for slug, f in findings.items()}
                mode = payload.get("mode")
            except Exception as e:  # noqa: BLE001
                findings, actual, mode = {}, {}, None
                ok = False
                detail.append(f"could not parse JSON output: {e}")
            want_mode = expected.pop("_mode", None)
            must_mention = expected.pop("_must_mention", {})
            for slug, texts in must_mention.items():
                f = findings.get(slug, {})
                haystack = " ".join([f.get("what", ""), f.get("fix", "")] + [str(e) for e in f.get("evidence", [])])
                for t in texts:
                    if t not in haystack:
                        ok = False
                        detail.append(f"{slug}: the finding should mention '{t}' and does not")
            if want_mode and mode != want_mode:
                ok = False
                detail.append(f"run evidence mode: expected {want_mode}, got {mode}")
            for slug, exp in expected.items():
                if actual.get(slug) != exp:
                    ok = False
                    detail.append(f"{slug}: expected {exp}, got {actual.get(slug)}")
        print(f"{'PASS' if ok else 'FAIL'}  {case['case']}  (gate {case['gate']})")
        for d in detail:
            print(f"      {d}")
        case_failures += 0 if ok else 1
    print(f"\n{len(cases) - case_failures} of {len(cases)} cases match.")
    return 1 if (failures or case_failures) else 0


if __name__ == "__main__":
    sys.exit(main())
