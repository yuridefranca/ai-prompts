# Schema: INDEX.md Frontmatter & Resume Procedure

**Slice**: 0 (Foundations)
**Used by**: the orchestrator/adapter at the start of every session; every gate; phase 9.5

## Why this exists

Subagents are stateless and a full flow does not fit in one context window. `INDEX.md` is how the orchestrator answers "where am I?" from files alone, without relying on conversation memory.

## Frontmatter schema

`INDEX.md` opens with YAML frontmatter — the machine-readable state record. A human-readable body (Mermaid flow diagram, phase table, decision log — see the [INDEX.md example](../PLAN.md#indexmd-example)) follows below it.

````yaml
---
flow: feature                # feature | debug | improvement | greenfield
feature: multi-wallet         # kebab-case feature slug; also the folder name and branch suffix
branch: feat/multi-wallet
tier: full                    # small | medium | full  (feature, improvement)  ·  trivial | standard | deep  (debug)  ·  prototype | production  (greenfield)
started: 2026-01-14
current_phase: "3.1"          # phase currently in progress or last attempted
last_completed: "3.0"         # last phase whose artifact status is `complete`
gates_passed: [2]
gates_pending: ["4", "6.0", "9"]
open_findings: [F2, F5]        # mirrors FINDINGS.md `open` rows — see findings.md
skipped_phases: []             # [{phase: "4", reason: "..."}] per severity gate
---
````

| Field | Type | Notes |
|---|---|---|
| `flow` | enum | `feature` or `debug` — selects which tier table and phase list apply |
| `feature` | string | kebab-case; used to derive the `.ai-workflow/[feature]/` folder and default branch name |
| `branch` | string | actual git branch for this run |
| `tier` | enum | see the tier tables in the [Feature Flow](../PLAN.md#feature-flow) / [Debug Flow](../PLAN.md#debug-flow) sections. Can move up mid-flow, never down after a gate passes |
| `started` | date | `YYYY-MM-DD` |
| `current_phase` | string | phase ID as a string (`"3.1"`, not `3.1`, so `3.10` isn't misread as `3.1`) |
| `last_completed` | string | last phase with `status: complete` on its artifact |
| `gates_passed` | list of strings | phase IDs whose gate the dev has approved |
| `gates_pending` | list of strings | gates still ahead in this tier's plan |
| `open_findings` | list of strings | `F*` IDs currently `open` in `FINDINGS.md` |
| `skipped_phases` | list of `{phase, reason}` | phases the tier didn't run, and why — always populated for `small`/`medium`/`trivial`/`standard` tiers |

## Resume procedure

Run this at the start of **every** session, before anything else:

1. Read `.ai-workflow/[feature]/INDEX.md` frontmatter → get `current_phase`, `gates_pending`.
2. Read the artifact named by `current_phase`. If its status header (see [artifact-status.md](artifact-status.md)) says `status: draft`, or the file is missing, re-spawn that phase's subagent with the original contract — **never resume or patch a draft**.
3. If `current_phase` is `complete` but its gate ID is still in `gates_pending`, **re-present the gate packet**. Never assume a gate was approved off-record just because the artifact is complete.
4. Run `$AI_PROMPTS/src/scripts/ledger_check.py .ai-workflow/[feature]` → it validates `FINDINGS.md` and checks `INDEX.md`'s `open_findings` matches it. Fix any mismatch before continuing, then surface every `open` finding in the next Layer 1 shown to the dev.
5. Announce, verbatim shape: `Resuming [feature] at phase N (tier: X) · N gates passed · N open findings`.

## Idempotency rule

Re-running any phase **overwrites its artifact wholesale**. No phase appends to another phase's output file. The only append-only file in the whole flow is `FINDINGS.md` (see [findings.md](findings.md)).

## Related

- [artifact-status.md](artifact-status.md) — per-artifact draft/complete header this procedure depends on
- [findings.md](findings.md) — the ledger `open_findings` mirrors
- [State & Resumption](../PLAN.md#state--resumption) — narrative source
- [Failure Edges](../PLAN.md#failure-edges) — what updates `current_phase`/`gates_pending` on rejection
