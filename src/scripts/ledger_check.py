#!/usr/bin/env python3
"""Check a flow's FINDINGS.md against src/schemas/findings.md, and INDEX.md against it.

The orchestrator runs this at every gate and on resume instead of re-reading the ledger
itself. Exits 1 on any error; warnings don't fail. With --gate 9, an open 🔴 finding is an
error (phase 9 blocks on it).

Usage:
  ledger_check.py .ai-workflow/multi-wallet
  ledger_check.py .ai-workflow/multi-wallet --gate 9
  ledger_check.py .ai-workflow/multi-wallet --json
"""
import argparse
import json
import re
import sys
from pathlib import Path

SEVERITIES = {"🔴", "🔵"}
STATUS = re.compile(r"^(open|accepted|closed @ T\d+|superseded by F\d+)$")


def table_rows(text, first_col):
    header, rows = None, []
    for line in text.splitlines():
        if not line.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == first_col:
            header = cells
        elif header and not set(cells[0]) <= {"-", ":", ""}:
            rows.append(dict(zip(header, cells)))
    return rows


def frontmatter_list(text, key):
    m = re.search(rf"^{key}:\s*\[(.*?)\]", text, re.M)
    return None if m is None else [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("feature_dir")
    ap.add_argument("--gate", help="the gate being presented, e.g. 9 (blocks on open 🔴)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    d = Path(args.feature_dir)
    findings, index, solution = d / "FINDINGS.md", d / "INDEX.md", d / "6-solution.md"
    errors, warnings = [], []
    if not findings.exists():
        sys.exit(f"{findings} not found")

    rows = table_rows(findings.read_text(), "ID")
    ids = [r.get("ID", "") for r in rows]
    tasks = set(re.findall(r"^#+\s*T(\d+)\b", solution.read_text(), re.M)) if solution.exists() else None

    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"{dup}: ID used more than once — update the existing row instead")
    for r in rows:
        fid, sev, status, ev = r.get("ID", ""), r.get("Severity", ""), r.get("Status", ""), r.get("Evidence", "")
        if not re.fullmatch(r"F\d+", fid):
            errors.append(f"row {fid or '?'}: ID must be F<number>")
        if sev not in SEVERITIES:
            errors.append(f"{fid}: severity '{sev}' must be 🔴 or 🔵")
        if not STATUS.match(status):
            errors.append(f"{fid}: status '{status}' isn't one of open / accepted / closed @ T<n> / superseded by F<n>")
        if not ev or ev in {"—", "-"}:
            errors.append(f"{fid}: evidence is empty" + (" — `accepted` needs its one-line reason here" if status == "accepted" else ""))
        sup = re.match(r"superseded by (F\d+)", status)
        if sup and sup.group(1) not in ids:
            errors.append(f"{fid}: superseded by {sup.group(1)}, which doesn't exist")
        closed = re.match(r"closed @ T(\d+)", status)
        if closed and tasks is not None and closed.group(1) not in tasks:
            warnings.append(f"{fid}: closed @ T{closed.group(1)}, but 6-solution.md has no T{closed.group(1)}")

    open_ids = [r["ID"] for r in rows if r.get("Status") == "open"]
    open_red = [r["ID"] for r in rows if r.get("Status") == "open" and r.get("Severity") == "🔴"]
    if index.exists():
        mirrored = frontmatter_list(index.read_text(), "open_findings")
        if mirrored is None:
            warnings.append("INDEX.md has no open_findings list")
        elif set(mirrored) != set(open_ids):
            errors.append(f"INDEX.md open_findings {sorted(mirrored)} ≠ open rows in FINDINGS.md {sorted(open_ids)}")
    if args.gate == "9" and open_red:
        errors.append(f"gate 9 blocked: open 🔴 {', '.join(open_red)}")

    if args.json:
        print(json.dumps({"errors": errors, "warnings": warnings, "open": open_ids, "open_red": open_red}, indent=2))
    else:
        for e in errors:
            print(f"❌ {e}")
        for w in warnings:
            print(f"⚠️ {w}")
        print(f"{len(rows)} findings · {len(open_ids)} open ({len(open_red)} 🔴) · {len(errors)} errors · {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
