#!/usr/bin/env python3
"""Refresh a company's model list (src/contexts/<company>/models.md) against OpenRouter.

Reports models that are new, no longer available, or repriced, and suggests a tier
for new ones. It never assigns a tier on its own: the report is for a person to
review, and --apply asks for confirmation on every change.

See src/schemas/agent-tiers.md for what the tiers mean.

Usage:
  scripts/models_refresh.py duelbits              # report only
  scripts/models_refresh.py clair --top 8         # show more candidates per tier
  scripts/models_refresh.py duelbits --apply      # confirm changes one by one, then write models.md
  scripts/models_refresh.py duelbits --catalog saved.json   # use a saved /models response

Source (set in models.md frontmatter):
  openrouter-key     GET /api/v1/models/user — only the models OPENROUTER_API_KEY can use
  openrouter-public  GET /api/v1/models — the public catalog, filtered by `vendors`

The API key is read from the environment and never written anywhere.
"""
import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

CONTEXTS = Path(__file__).resolve().parent.parent / "contexts"
API = "https://openrouter.ai/api/v1"

# Price-band hint, by output price in USD per million tokens, calibrated to the tiers in use
# (Opus $20 S · Sonnet $10 / Kimi Pro $8.8 A · GLM, MiniMax, Qwen max $1.2–6 B · flash models <$1 C).
# Weak signal on its own: a newer version of a model family already in the list inherits that
# family's tier first.
PRICE_BANDS = [(20.0, "S"), (8.0, "A"), (1.0, "B"), (0.0, "C")]
TIERS = ["S", "A", "B", "C"]


def read_models_md(path):
    text = path.read_text()
    meta = {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.split("#")[0].strip()
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.startswith("| Tier |")), None)
    if start is None:
        sys.exit(f"{path}: no table whose header starts with '| Tier |'")
    header = [c.strip() for c in lines[start].strip("|").split("|")]
    rows, i = [], start + 2
    while i < len(lines) and lines[i].startswith("|"):
        cells = [c.strip() for c in lines[i].strip("|").split("|")]
        rows.append(dict(zip(header, cells)))
        i += 1
    return text, meta, header, rows, (start, i)


def fetch(source, catalog):
    if catalog:
        data = json.loads(Path(catalog).read_text())
        return data.get("data", data)
    url = f"{API}/models/user" if source == "openrouter-key" else f"{API}/models"
    headers = {"User-Agent": "ai-prompts-models-refresh"}
    if source == "openrouter-key":
        key = os.environ.get("OPENROUTER_API_KEY")
        if not key:
            sys.exit("source is openrouter-key: set OPENROUTER_API_KEY (it is never stored)")
        headers["Authorization"] = f"Bearer {key}"
    models = []
    while url:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
            page = json.load(r)
        models += page.get("data", [])
        nxt = (page.get("links") or {}).get("next")
        url = nxt if nxt and nxt.startswith("http") else (f"https://openrouter.ai{nxt}" if nxt else None)
    return models


def per_million(price):
    try:
        return float(price) * 1_000_000
    except (TypeError, ValueError):
        return None


def price_cell(model):
    p = model.get("pricing", {})
    i, o = per_million(p.get("prompt")), per_million(p.get("completion"))
    if i is None or o is None:
        return "?"
    return f"{i:g} / {o:g}"


def usable(model, vendors, min_context):
    """Text-out, tool-calling, long enough context, from an allowed vendor."""
    arch = model.get("architecture", {})
    if "text" not in (arch.get("output_modalities") or ["text"]):
        return False
    if "tools" not in (model.get("supported_parameters") or []):
        return False
    if (model.get("context_length") or 0) < min_context:
        return False
    if vendors and model["id"].split("/")[0] not in vendors:
        return False
    return not model["id"].endswith((":free", ":batch"))  # batch pricing doesn't apply to interactive agents


def family(model_id):
    """'anthropic/claude-sonnet-5.5' -> 'anthropic/claude-sonnet' (drop version-ish parts)."""
    vendor, _, name = model_id.partition("/")
    parts = [p for p in re.split(r"[-:]", name) if not re.match(r"^[\d.]+[a-z]?$|^\d{4}$|^latest$|^preview$|^beta$", p)]
    return vendor + "/" + "-".join(parts)


def listed_sibling(model, rows):
    """The listed row in the same model family, if any."""
    fam = family(model["id"])
    return next((r for r in rows if "/" in r.get("Model", "") and family(r["Model"]) == fam and r.get("Tier") in TIERS), None)


def suggest(model, rows):
    row = listed_sibling(model, rows)
    if row:
        return row["Tier"], f"newer version of {row['Model']} ({row['Tier']})"
    out = per_million(model.get("pricing", {}).get("completion"))
    if out is None:
        return "?", "no price"
    for floor, tier in PRICE_BANDS:
        if out >= floor:
            return tier, f"price hint: ${out:g}/M output"
    return "C", "price hint"


def report(company, meta, rows, models, args):
    by_id = {m["id"]: m for m in models}
    listed = {r["Model"]: r for r in rows if "/" in r.get("Model", "")}  # rows without a vendor/ slug (e.g. Cursor-only models) are not tracked
    vendors = [v.strip() for v in meta.get("vendors", "").split(",") if v.strip() and v.strip() != "all"]

    removed = [mid for mid in listed if mid not in by_id]
    repriced = [(mid, listed[mid].get("$ in / out per M", ""), price_cell(by_id[mid]))
                for mid in listed if mid in by_id and listed[mid].get("$ in / out per M", "") != price_cell(by_id[mid])]
    def superseded(m):
        """An older version of a family that's already listed — not a candidate."""
        row = listed_sibling(m, rows)
        return row is not None and (m.get("created") or 0) <= (by_id.get(row["Model"], {}).get("created") or 0)

    new = [m for m in models if m["id"] not in listed and usable(m, vendors, args.min_context) and not superseded(m)]
    new.sort(key=lambda m: m.get("created") or 0, reverse=True)

    grouped = {t: [] for t in TIERS + ["?"]}
    for m in new:
        tier, why = suggest(m, rows)
        grouped[tier].append((m, why))

    today = datetime.date.today().isoformat()
    print(f"# Model refresh — {company} — {today}\n")
    print(f"Source: {meta.get('source')} · {len(models)} models fetched · {len(listed)} in models.md\n")
    print(f"## No longer available ({len(removed)})\n")
    for mid in removed:
        print(f"- `{mid}` (was {listed[mid].get('Tier')})")
    print(f"\n## Repriced ({len(repriced)})\n")
    for mid, old, new_p in repriced:
        print(f"- `{mid}`: {old or '—'} → {new_p}")
    print(f"\n## New candidates ({len(new)}; newest {args.top} per suggested tier)\n")
    print("| Suggested | Model | $ in / out per M | Context | Basis |")
    print("|---|---|---|---|---|")
    for tier in TIERS + ["?"]:
        for m, why in grouped[tier][: args.top]:
            print(f"| {tier} | `{m['id']}` | {price_cell(m)} | {m.get('context_length') or '?'} | {why} |")
    print("\nSuggestions are hints. Confirm each tier against what you know of the model (benchmarks, your own runs) before adding it.")
    return removed, repriced, grouped


def apply(path, text, header, rows, span, models, removed, repriced, grouped, top):
    by_id = {m["id"]: m for m in models}
    keep = []
    for row in rows:
        mid = row.get("Model")
        if mid in removed and input(f"Remove `{mid}` ({row.get('Tier')})? [y/N] ").lower() == "y":
            continue
        if mid in dict((r[0], r) for r in repriced) and input(f"Update price of `{mid}` to {price_cell(by_id[mid])}? [Y/n] ").lower() != "n":
            row["$ in / out per M"] = price_cell(by_id[mid])
        keep.append(row)
    today = datetime.date.today().isoformat()
    for tier in TIERS + ["?"]:
        for m, why in grouped[tier][:top]:
            ans = input(f"Add `{m['id']}` ({price_cell(m)}) — suggested {tier} ({why}). Tier [S/A/B/C, Enter=skip]: ").strip().upper()
            if ans in TIERS:
                row = {h: "?" for h in header}
                vision = "image" in (m.get("architecture", {}).get("input_modalities") or [])
                row.update({"Tier": ans, "Model": m["id"], "$ in / out per M": price_cell(m), "Vision": "✅" if vision else "❌",
                            "Context": str(m.get("context_length") or "?"), "Why": f"added {today}, confirmed {ans}"})
                keep.append(row)
    # Stable sort by tier only: the first row of a tier is its default, so existing order is kept
    # and new rows land at the end of their tier.
    keep.sort(key=lambda r: TIERS.index(r["Tier"]) if r.get("Tier") in TIERS else 9)
    lines = text.splitlines()
    table = [lines[span[0]], lines[span[0] + 1]] + ["| " + " | ".join(r.get(h, "") for h in header) + " |" for r in keep]
    path.write_text("\n".join(lines[: span[0]] + table + lines[span[1]:]) + "\n")
    print(f"Wrote {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("company", help="context pack name, e.g. duelbits or clair")
    ap.add_argument("--apply", action="store_true", help="confirm changes interactively, then write models.md")
    ap.add_argument("--top", type=int, default=5, help="new candidates shown per suggested tier (default 5)")
    ap.add_argument("--min-context", type=int, default=64000, help="ignore models with a smaller context (default 64000)")
    ap.add_argument("--catalog", help="read a saved /models JSON response instead of calling the API")
    args = ap.parse_args()

    path = CONTEXTS / args.company / "models.md"
    if not path.exists():
        sys.exit(f"{path} not found")
    text, meta, header, rows, span = read_models_md(path)
    models = fetch(meta.get("source", "openrouter-public"), args.catalog)
    removed, repriced, grouped = report(args.company, meta, rows, models, args)
    if args.apply:
        apply(path, text, header, rows, span, models, removed, repriced, grouped, args.top)


if __name__ == "__main__":
    main()
