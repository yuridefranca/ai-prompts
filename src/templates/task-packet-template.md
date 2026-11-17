# Template: Task Packet (Phase 6.1..n)

**Slice**: 2
**Used by**: the orchestrator, once per task in the phase 6.1..n loop — the highest-frequency chat surface in the whole flow, so its length budget is enforced hardest

## Shape

````markdown
## Task T{n}: {one-line task name}

{✅ as-planned | ⚠️ N deviations} · covers {C* ids} · {size S/M/L}

| Plan said | Actually did |
|---|---|
| {6-solution.md §T{n} intent} | {what the diff shows} |

**Files touched**: {list}
**New findings**: {F* ids, or "none"}

┌ CHECKS
│ 1. {why/what-happens-if}
│ 2. {why/what-happens-if}
└

Diff: {link/path} · Full record: 6-solution.md §T{n}
````

## Rules

1. **≤20 lines, hard budget.** This is the template [Attention Engineering § Hard length budgets](../PLAN.md#techniques) names explicitly — a task packet that grows past this is a sign the task itself should have been split at 6.0, not that the packet needs more room.
2. **"Plan said → actually did" is mandatory**, even when they match — an empty diff row is itself information (this task went exactly as planned).
3. **No CHECKS enforcement here** — unlike the gate packet, task-loop CHECKS are a reading aid only (see [artifact-template.md § What Layer 1 is not](artifact-template.md)). The dev approves or comments regardless of whether they answer.
4. **Two outcomes only**: dev approves → orchestrator spawns the next task. Dev comments → the **same task** is re-spawned with the feedback, task number unchanged (see [Failure Edges](../flows/feature-flow.md#failure-edges)).
5. Never inline the full diff in the chat surface — link or path it. The packet is a decision aid, not a code review interface.

## Related

- [gate-packet-template.md](gate-packet-template.md) — the enforced-CHECKS sibling, used at gates rather than every task
- [../flows/feature-flow.md § 6.1..n Task Loop](../flows/feature-flow.md#61n--task-loop) — where this packet is spawned from
- [../schemas/contract-ids.md](../schemas/contract-ids.md) — where "covers C* ids" comes from
