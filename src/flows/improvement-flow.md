# Flow Manifest: Improvement

**Tool-agnostic**, same rules as [feature-flow.md](feature-flow.md): no tool-specific syntax, roles named without `@`.

For changes to code that **already works**: optimize, refactor, migrate, make faster or cleaner. The core rule is **understand before changing** — the code works today, and the improvement must keep it working while making it measurably better.

Same skeleton as [feature-flow.md](feature-flow.md). This manifest states **only the differences** — every phase not listed below runs exactly as the feature flow defines it, including its Role/Input/Task/Output contract, its templates, and the [Failure Edges](feature-flow.md#failure-edges) table.

## Differences from Feature Flow

| Phase | Feature Flow | Improvement Flow |
|---|---|---|
| 0 | Severity gate: small/medium/full | Same tiers and criteria, but **3.0 runs on every tier**, including small. See below |
| 0.5 | Orient — problem, current state, alternatives | Orient — **what's suboptimal today** (with evidence: a slow trace, a duplicated block, a painful change), and improvement approaches |
| 1 | Overview | Overview + **baseline**: what "better" means, as a metric with today's measured value and the command that measured it. See below |
| 2 | Full PRD | PRD split into **improve** criteria (what gets better) and **preserve** criteria (what must not change). Both use `AC*` IDs; preserve ones are tagged `preserve` |
| 3.0 | Component map | Component map + **impact analysis**: consumers of the current behavior, APIs/data formats/config that would change, blast radius. Runs on every tier |
| 3.4 | ADR | ADR must include **migration strategy** (how to get from current to improved state) and **backward compatibility** (how existing consumers keep working) |
| 5 | Contract, every clause red | Contract adds **preserve clauses** — characterization tests that must **pass** before implementation. See below |
| 6.0 | Task breakdown | Every task leaves the code working (all tests green). Unrelated issues found along the way go to `FINDINGS.md` as 🔵, never fixed in place |
| 7 | Review | Review also flags **scope creep**: any changed file outside 3.0's impact list is a finding unless `6-solution.md` justifies it |
| 8.1 / 8.2 | QA plan / manual QA | Preserve criteria come first in the plan. If phase 1 set a metric, 8.2 **re-measures it** with the same command and records before → after |
| 9 | PR | `9-pr-notes.md` leads with the before → after metric (or "no metric — structural improvement" and why) |

---

## Phase 0 — Severity Gate (improvement)

Same evidence-then-propose mechanism and the same small/medium/full tiers as [feature-flow.md § Phase 0](feature-flow.md#phase-0--bootstrap--severity-gate). One change:

| Tier | Phases run |
|---|---|
| **Small** | 1, 2, **3.0**, 5, 6.0–6.x, 6.y, 7, 9 |
| **Medium** | as feature flow |
| **Full** | as feature flow |

Changing working code without a map of what depends on it is how regressions ship, and 3.0 is cheap.

---

## Phase 1 — Baseline

`1-overview.md` gains a **Baseline** section:

| Field | Example |
|---|---|
| Metric | p95 latency of `GET /wallets` |
| Today's value | 840 ms |
| Measured by | the exact command or query, so 8.2 can re-run it unchanged |
| Target | < 300 ms |

When the improvement is structural (readability, removing duplication, a migration), the metric can be "none" — say what improves instead, in one line. A **guessed** baseline is worse than none: mark it `unmeasured` and measure at phase 5.

---

## Phase 5 — Preserve Clauses

The contract has two kinds of clauses:

| Kind | Before implementation | After implementation | Evidence column |
|---|---|---|---|
| **improve** (`happy`/`error`/`side-effect`/…) | fails | passes | pasted **red** output, as in [contract-ids.md](../schemas/contract-ids.md#red-evidence--mandatory) |
| **preserve** | **passes** | passes | pasted **green** output from the current code |

A preserve clause pins down behavior that must survive the change — a characterization test. One that **fails** before implementation means the characterization is wrong (or the current behavior isn't what anyone thought): fix the test or raise it at the gate, never "fix" the code to match. See [contract-ids.md § Preserve clauses](../schemas/contract-ids.md#preserve-clauses-improvement-flow).

If phase 1 set a metric, phase 5 also adds a **measurable clause** (`C*`, kind `performance` or similar) whose test asserts the target, with today's measurement as its red evidence.

---

## Related

- [feature-flow.md](feature-flow.md) — the skeleton this manifest diffs against
- [bootstrap.md](bootstrap.md) — shared flow-start procedure
- [../schemas/contract-ids.md](../schemas/contract-ids.md) — clause schema, including preserve clauses
