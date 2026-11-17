# Flow Manifest: Debug

**Slice**: 1 (skeleton) — the 2.5 root-cause phase is fleshed out here; the `rca-analyst` agent file lands in slice 3, wiring in slice 6.
**Tool-agnostic**, same rules as [feature-flow.md](feature-flow.md): no tool-specific syntax, roles named without `@`.

Same skeleton as [feature-flow.md](feature-flow.md). This manifest states **only the differences** — every phase not listed below runs exactly as the feature flow defines it, with the input substitutions this table implies (e.g. any phase reading "2-prd.md" reads the mini-PRD in a debug run).

## Differences from Feature Flow

| Phase | Feature Flow | Debug Flow |
|---|---|---|
| 0.5 | Orient — problem, current state, solution alternatives | Orient — **the bug**, screenshots of the broken behavior, **fix approaches** (not feature alternatives). Skipped on `trivial` tier instead of `small`. See below |
| 2 | Full PRD | Mini-PRD: current vs expected behavior + repro contract. Same gate, same `2-prd.md` path, smaller content |
| 2.5 | — | **Root cause analysis** (new phase, see below) |
| 5 | Behavior contract, clauses derived from PRD | Contract's first clause (`C1`) is always the repro: "given repro steps, system does X not Y" — every other clause follows [contract-ids.md](../schemas/contract-ids.md) unchanged |
| 8.1 | QA plan | QA plan must include the repro scenario as its first manual test |
| 8.2 | Manual QA | Manual QA must re-run the original repro steps (mandatory, not optional) |

Every other phase (1, 3, 4, 6, 6.y, 7, 8.3, 9, 9.1, 9.5) runs unchanged from [feature-flow.md](feature-flow.md), including its Role/Input/Task/Output contract, its templates, and the [Failure Edges](feature-flow.md#failure-edges) table.

---

## Phase 0.5 — Orient (debug framing)

Same mechanics as [feature-flow.md § Phase 0.5](feature-flow.md#phase-05--orient--mini-gate) — `task-explainer` (create mode), `explain-task` skill, same ⛔ mini-gate, same five later `update`-mode deepenings at phases 2/6.0/6.x/7/9. Two differences:

- **"The problem" is the bug**, sourced from the dev's repro description, not a feature request. **"What it looks like"** shows the broken behavior, not a missing one.
- **"Ways we can solve it"** lists fix approaches, evaluated the same way (what changes, what stays the same, main risk) — this is a lighter, human-readable preview of what phase 2.5's root-cause analysis will later confirm or correct, not a substitute for it. The dev's pick at this gate is provisional; if 2.5 finds a different root cause, `task-explainer` is re-spawned to correct the walkthrough's Clarify stage before Plan.

Skipped on the `trivial` tier (not `small` — debug tiers are named differently, see the tier table below); runs on `standard`/`deep`.

---

## Phase 2.5 — Root Cause Analysis (new)

| Field | Value |
|---|---|
| Role | `rca-analyst` |
| Skill | `root-cause-analyzer` |
| Input | `2-prd.md` (mini-PRD + repro contract), `3.0-component-map.md` |
| Task | Evidence-based investigation of *why* the defect happens. **No fixes allowed** — a root-cause artifact that proposes a fix has failed its job; fixing happens in phase 6 |
| Output | `2.5-root-cause.md` `[knowledge]` |
| Gate | **Deep tier only** — see tier table below. Root cause must be confirmed by the dev before any solution work begins: the "never jump to fix" rule, preserved |

`root-cause-analyzer`'s evidence discipline: stack traces, reproduction confirmation, log analysis — a claimed root cause with no evidence is treated the same as a `C*` clause with no red evidence ([contract-ids.md](../schemas/contract-ids.md#red-evidence--mandatory)): incomplete.

---

## Severity Gate (start)

Same evidence-then-propose mechanism as [feature-flow.md § Phase 0](feature-flow.md#phase-0--bootstrap--severity-gate) — cheap glob/grep evidence, then a proposed tier the dev confirms or overrides.

### Tier → phases → gates

| Tier | Criteria | Phases run | Gates |
|---|---|---|---|
| **Trivial** | Typo, config value, one-line fix, no behavior change beyond the bug | 2 (mini), 5 (repro test), 6.1, 7, 9 | 9 |
| **Standard** | Localized defect with a clear reproduction | 0.5, 1, 2, 2.5, 3.0, 5, 6, 6.y, 7, 8, 9 | 0.5, 2, 6.0, 9 |
| **Deep** | No reliable repro, cross-service, data corruption, or security implication | all + 2.5 extended | 0.5, 2, 2.5, 4, 6.0, 9 |

**Deep tier adds a gate at 2.5** — root cause confirmed by the dev before phase 5 starts. This is the debug-flow analog of feature-flow's phase-4 decision gate, and uses the same miss-handling (re-present Layer 1, ask once more, second miss re-spawns `rca-analyst` with "explain the causal chain more concretely").

---

## Related

- [feature-flow.md](feature-flow.md) — the skeleton this manifest diffs against
- [bootstrap.md](bootstrap.md) — shared flow-start procedure, identical for both flows
- [../schemas/contract-ids.md](../schemas/contract-ids.md) — the `C1`-is-always-the-repro rule
