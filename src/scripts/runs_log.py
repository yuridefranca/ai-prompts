#!/usr/bin/env python3
"""Keep a per-company log of which model did which job, and how it went.

  record  — at the 9.5 harvest: append a flow's RUNS.md rows to the company's log, anonymized
            (no feature name, no notes — only date, phase, agent, tier, model, size, outcome)
  stats   — per model: spawns, first-pass approval rate, rejections, escalations, spec gaps

The log lives at $AI_PROMPTS/data/runs/<company>.jsonl and is gitignored: it describes work
done for a company, so it stays on the machine unless you choose to commit it.

Usage:
  runs_log.py record .ai-workflow/multi-wallet --company duelbits
  runs_log.py stats --company duelbits
  runs_log.py stats --company duelbits --tier B
"""
import argparse
import datetime
import hashlib
import json

import sys
from collections import defaultdict
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent.parent / "data" / "runs"
OUTCOMES = {"approved", "rejected", "spec-gap", "reopened"}


def log_path(company):
    return DATA / f"{company}.jsonl"


def read_runs_md(path):
    rows, header = [], None
    for line in path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[0] == "#":
            header = [c.lower() for c in cells]
        elif header and cells[0].isdigit():
            rows.append(dict(zip(header, cells)))
    return rows


def load(company):
    p = log_path(company)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def record(args):
    runs = Path(args.feature_dir) / "RUNS.md"
    if not runs.exists():
        sys.exit(f"{runs} not found")
    # A stable, non-reversible run id, so recording the same flow twice doesn't duplicate rows.
    run_id = hashlib.sha256(str(Path(args.feature_dir).resolve()).encode()).hexdigest()[:12]
    existing = {(e["run"], e["n"]) for e in load(args.company)}
    today = datetime.date.today().isoformat()
    new, skipped = [], []
    for r in read_runs_md(runs):
        outcome = r.get("outcome", "")
        if outcome not in OUTCOMES:
            skipped.append(f"#{r.get('#')}: outcome '{outcome}' not one of {sorted(OUTCOMES)}")
            continue
        if (run_id, int(r["#"])) in existing:
            continue
        new.append({"run": run_id, "n": int(r["#"]), "date": today, "phase": r.get("phase", ""),
                    "agent": r.get("agent", ""), "tier": r.get("tier", ""), "model": r.get("model", ""),
                    "size": r.get("size", "—"), "outcome": outcome})
    log_path(args.company).parent.mkdir(parents=True, exist_ok=True)
    with log_path(args.company).open("a") as f:
        for e in new:
            f.write(json.dumps(e) + "\n")
    for s in skipped:
        print(f"⚠️ skipped {s}")
    print(f"recorded {len(new)} rows → {log_path(args.company)}")


def stats(company, tier=None):
    """{model: {spawns, approved, rejected, spec_gap, reopened, first_pass}} — tasks only count spec gaps separately."""
    out = defaultdict(lambda: defaultdict(int))
    for e in load(company):
        if tier and e.get("tier") != tier:
            continue
        s = out[e["model"]]
        s["spawns"] += 1
        s[e["outcome"].replace("-", "_")] += 1
        if e["agent"].endswith("-up"):
            s["as_escalation"] += 1
    return out


def print_stats(args):
    rows = stats(args.company, args.tier)
    if not rows:
        print(f"no runs logged for {args.company}" + (f" at tier {args.tier}" if args.tier else ""))
        return
    print("| Model | Spawns | Approved | Rejected | Spec gaps | Reopened | Approval (excl. spec gaps) |")
    print("|---|---|---|---|---|---|---|")
    for model, s in sorted(rows.items(), key=lambda kv: -kv[1]["spawns"]):
        judged = s["spawns"] - s["spec_gap"]
        rate = f"{100 * s['approved'] / judged:.0f}%" if judged else "—"
        print(f"| {model} | {s['spawns']} | {s['approved']} | {s['rejected']} | {s['spec_gap']} | {s['reopened']} | {rate} |")
    print("\nSpec gaps count against the plan (6.0), not the model. Read rates with their sample size: 3 spawns prove nothing.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("record", help="append a flow's RUNS.md to the company log")
    r.add_argument("feature_dir")
    r.add_argument("--company", required=True)
    s = sub.add_parser("stats", help="per-model outcomes")
    s.add_argument("--company", required=True)
    s.add_argument("--tier", choices=["S", "A", "B", "C"])
    args = ap.parse_args()
    record(args) if args.cmd == "record" else print_stats(args)


if __name__ == "__main__":
    main()
