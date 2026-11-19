#!/usr/bin/env python3
"""The phase 6.x contract diff, mechanically.

For every C* clause in 5-contract.md, find the tests that cite it, count the assertions
in each citing test, and check the test sits at the clause's declared level. Prints the
format in src/schemas/contract-ids.md and exits 1 if any clause isn't fully covered.

Usage:
  contract_diff.py .ai-workflow/multi-wallet              # run from the target repo's root
  contract_diff.py .ai-workflow/multi-wallet --json
  contract_diff.py <feature-dir> --repo <path> --project <path/to/project.md>

Levels and test locations come from .ai-rules/project.md §Test (`unit: cmd: … location: <glob>`).
Without project.md, common test-file patterns are scanned and level match is reported as unknown.

Heuristics (stated so a result can be judged): a citation is a comment holding only clause IDs
(`// C2`, `# C2, C3`) or a clause ID inside a test title (`it('C2 rejects …')`). The citing test
runs from the citation to the next test start at the same or lower indent. Assertions counted:
expect(…), assert…, .should, t.is/t.true/…, pytest.raises — zero means uncited.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FALLBACK_GLOBS = ["**/*.spec.*", "**/*.test.*", "**/test_*.py", "**/*_test.py", "**/*_test.go"]
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "coverage", ".ai-workflow", "vendor"}
COMMENT_CITE = re.compile(r"^\s*(?://|#|/\*+|\*)\s*((?:C\d+\s*[,;]?\s*)+)(?:\*/)?\s*$")
TITLE_CITE = re.compile(r"""\b(?:it|test|describe|specify|scenario)(?:\.\w+)?\s*\(\s*(['"`])(.*?)\1""")
TEST_START = re.compile(r"""^(\s*)(?:(?:it|test|describe|specify)(?:\.\w+)?\s*\(|(?:async\s+)?def\s+test_|func\s+Test)""")
ASSERTION = re.compile(r"\bexpect\s*\(|\bassert\w*\b|\.should\b|\bt\.(?:is|not|true|false|deepEqual|throws)\s*\(|\brequire\.\w+\s*\(|\bpytest\.raises\b")
CLAUSE_ID = re.compile(r"\bC\d+\b")
STRING = re.compile(r"""(['"`])(?:\\.|(?!\1).)*\1""")  # string literals, so a title like 'asserts …' isn't counted


def glob_regex(glob):
    """'src/**/*.spec.ts' -> regex matching repo-relative posix paths."""
    out, i = "", 0
    while i < len(glob):
        if glob.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif glob.startswith("**", i):
            out, i = out + ".*", i + 2
        elif glob[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif glob[i] == "?":
            out, i = out + "[^/]", i + 1
        elif glob[i] == "{":
            j = glob.index("}", i)
            out, i = out + "(?:" + "|".join(map(re.escape, glob[i + 1:j].split(","))) + ")", j + 1
        else:
            out, i = out + re.escape(glob[i]), i + 1
    return re.compile(out + "$")


def read_levels(project_md):
    """{'unit': 'src/**/*.spec.ts', ...} from project.md §Test."""
    if not project_md or not project_md.exists():
        return {}
    text = project_md.read_text()
    m = re.search(r"^## Test\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    levels = {}
    for line in (m.group(1) if m else "").splitlines():
        lm = re.match(r"^\s*(unit|integration|e2e):.*?location:\s*(\S+)", line)
        if lm:
            levels[lm.group(1)] = lm.group(2)
    return levels


def read_clauses(contract):
    rows, header = [], None
    for line in contract.read_text().splitlines():
        if not line.startswith("|"):
            header = None if not line.strip() else header
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "ID":
            header = [c.lower() for c in cells]
            continue
        if header and re.fullmatch(r"C\d+", cells[0] or ""):
            row = dict(zip(header, cells))
            rows.append({"id": cells[0], "level": row.get("level", "").split()[0].lower() if row.get("level") else "",
                         "kind": row.get("kind", "")})
    return rows


def test_files(repo, globs):
    regexes = [glob_regex(g) for g in globs]
    for path in repo.rglob("*"):
        if path.is_file() and not (set(path.relative_to(repo).parts[:-1]) & SKIP_DIRS):
            rel = path.relative_to(repo).as_posix()
            if any(r.match(rel) for r in regexes):
                yield path, rel


def citations(path):
    """Yield (clause_id, line_no, assertion_count) for each citation in a test file."""
    try:
        lines = path.read_text(errors="replace").splitlines()
    except OSError:
        return
    for n, line in enumerate(lines):
        ids = []
        cm = COMMENT_CITE.match(line)
        if cm:
            ids = CLAUSE_ID.findall(cm.group(1))
        else:
            for tm in TITLE_CITE.finditer(line):
                ids += CLAUSE_ID.findall(tm.group(2))
        if not ids:
            continue
        # The citing test: from the citation's test start to the next test start at the same or lower indent.
        start = n if TEST_START.match(line) else next((k for k in range(n + 1, min(n + 4, len(lines))) if TEST_START.match(lines[k])), n)
        indent = len(TEST_START.match(lines[start]).group(1)) if TEST_START.match(lines[start]) else len(line) - len(line.lstrip())
        end = len(lines)
        for k in range(start + 1, len(lines)):
            sm = TEST_START.match(lines[k])
            if (sm and len(sm.group(1)) <= indent) or COMMENT_CITE.match(lines[k]):
                end = k
                break
        body = lines[min(n, start):end]
        count = sum(len(ASSERTION.findall(STRING.sub("", l))) for l in body if not COMMENT_CITE.match(l))
        for cid in dict.fromkeys(ids):
            yield cid, n + 1, count


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("feature_dir", help=".ai-workflow/<feature> folder holding 5-contract.md")
    ap.add_argument("--repo", default=".", help="repo root to scan (default: current directory)")
    ap.add_argument("--project", help="path to project.md (default: <repo>/.ai-rules/project.md)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    contract = Path(args.feature_dir) / "5-contract.md"
    if not contract.exists():
        sys.exit(f"{contract} not found")
    levels = read_levels(Path(args.project) if args.project else repo / ".ai-rules" / "project.md")
    clauses = read_clauses(contract)
    if not clauses:
        sys.exit(f"{contract}: no clause table rows (| ID | … with C1, C2, …)")

    level_res = {lvl: glob_regex(g) for lvl, g in levels.items()}
    found = {}
    for path, rel in test_files(repo, list(levels.values()) or FALLBACK_GLOBS):
        actual = next((lvl for lvl, r in level_res.items() if r.match(rel)), None)
        for cid, line, count in citations(path):
            found.setdefault(cid, []).append({"file": rel, "line": line, "assertions": count, "level": actual})

    results, failing = [], 0
    for c in clauses:
        hits = found.get(c["id"], [])
        good = [h for h in hits if h["assertions"] > 0 and (not levels or h["level"] == c["level"])]
        best = good[0] if good else (max(hits, key=lambda h: h["assertions"]) if hits else None)
        if good:
            status, note = "ok", ""
        elif not hits:
            status, note = "uncited", "no citing test"
        elif best["assertions"] == 0:
            status, note = "empty", "0 assertions — counts as uncited"
        else:
            status, note = "level", f"declared {c['level']}, found {best['level'] or 'outside every level location'}"
        failing += status != "ok"
        results.append({"id": c["id"], "level": c["level"], "status": status, "note": note, "best": best, "citations": hits})

    if args.json:
        print(json.dumps({"levels_from_project_md": bool(levels), "clauses": results}, indent=2))
    else:
        if not levels:
            print("⚠️ no .ai-rules/project.md §Test locations — scanned common test patterns; level match unknown\n")
        for r in results:
            b = r["best"]
            icon = {"ok": "✅", "uncited": "❌", "empty": "⚠️", "level": "⚠️"}[r["status"]]
            if not b:
                print(f"{r['id']} {icon} no citing test")
                continue
            lvl = (b["level"] or "?") + (" ✅" if r["status"] == "ok" and levels else " ❌" if r["status"] == "level" else "")
            where = f"{b['file']}:{b['line']}"
            print(f"{r['id']} {icon} {where:<34} · {b['assertions']} assertion{'s' if b['assertions'] != 1 else ''} · {lvl}"
                  + (f" ({r['note']})" if r["note"] else ""))
        print(f"\n{len(results) - failing}/{len(results)} clauses covered")
    sys.exit(1 if failing else 0)


if __name__ == "__main__":
    main()
