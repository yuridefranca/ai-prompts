# Template: RUNS.md

**Used by**: the orchestrator — one row appended after **every** subagent spawn; read at the 9.5 harvest by `scripts/runs_log.py record`.
**Tier**: `[process]` — dies with the run; the anonymized rows survive in the per-company run log.

## Why

Tiers are set from price and reputation; this is what turns them into evidence. Over a few runs, the log answers "does GLM's code get approved as often as Sonnet's on B tasks?" from your own work, not a benchmark — see [agent-tiers.md](../schemas/agent-tiers.md).

## Shape

````markdown
# Runs — {feature}

| # | Phase | Task | Agent | Tier | Model | Size | Outcome | Note |
|---|---|---|---|---|---|---|---|---|
| 1 | 3.1 | — | architect | A | anthropic/claude-sonnet-5.5 | — | approved | |
| 2 | 6.1 | T1 | implementer | B | z-ai/glm-5.3 | S | approved | |
| 3 | 6.2 | T2 | implementer | B | z-ai/glm-5.3 | M | rejected | missed the null-currency branch |
| 4 | 6.2 | T2 | implementer-up | A | anthropic/claude-sonnet-5.5 | M | approved | escalated from #3 |
| 5 | 6.3 | T3 | implementer | B | z-ai/glm-5.3 | S | spec-gap | §T3 had no path for the DTO |
````

## Columns

| Column | Contents |
|---|---|
| `Model` | the `model:` of the agent file that was spawned — the exact ID, read from the installed agent, not assumed from the tier |
| `Size` | the task's S/M/L from `6-solution.md` (6.1..n only; `—` elsewhere) |
| `Outcome` | `approved` (accepted as is) · `rejected` (dev or gate sent it back) · `spec-gap` (implementer stopped on a gap in §T{n} — counts against the plan, not the model) · `reopened` (a later QA failure or review finding sent this task back — add it as a new row pointing at the original `#`) |
| `Note` | one line; for `rejected`, what was wrong |

## Rules

1. **One row per spawn**, including re-spawns — an escalation is two rows (the rejected one and the `-up` one).
2. **Record the outcome when it's known**: for 6.1..n that's the task review; for gated phases, the gate; for ungated phases, `approved` once the next phase has consumed the artifact without sending it back.
3. **No code, no feature names in `Note`** beyond what the run needs — these notes are not exported, but keep them short anyway.
