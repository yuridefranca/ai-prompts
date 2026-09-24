# Schema (Draft): Agent Cost Tiers

> **Status: draft, not wired in.** No flow manifest, template, or agent file references this yet — `feature-flow.md`/`debug-flow.md`'s phase tables have no `Tier` column, `feature-workflow.agent.md`'s "How to spawn a role" doesn't read it, and `project-md-schema.md` doesn't have the `## Agents` section this proposes. This file exists so the design isn't lost, not to be treated as implemented. Wiring it in is future work, not part of any current slice.

## Problem

Once planning/exploration is done (analysis, synthesis, solution design), a lot of what's left is mechanical: implementing a task 6.0 already specified in detail, writing docs from a diff, running a QA spec against a written plan. Those don't obviously need the same reasoning depth as the phases that produced the plan — but the flow manifests are tool-agnostic by design ([Architecture § Three-Layer Separation](../PLAN.md#three-layer-separation)), and *which* cheaper agent/model exists, and under what name, differs per tool and per repo. Hardcoding a model name into a manifest would break portability the same way a hardcoded dev-server URL did before `.ai-rules/project.md` existed.

## Design sketch

### 1. A `Tier` field per phase, default `reasoning`

Every phase in [feature-flow.md](../flows/feature-flow.md) / [debug-flow.md](../flows/debug-flow.md) would carry a `Tier: reasoning | execution` alongside its existing `Role`/`Input`/`Task`/`Output` columns. Default is `reasoning` — a phase is only ever marked `execution` deliberately, never by omission, so a new phase added later doesn't silently get downgraded.

**Proposed defaults**, based on what each phase actually does:

| Phase | Role | Tier | Why |
|---|---|---|---|
| 1 | `prd-writer` (overview) | reasoning | Judgment about business framing |
| 2 | `prd-writer` (PRD) | reasoning | Grilling requires real interrogation |
| 3.0 | `component-mapper` | execution | Mechanical repo inspection |
| 3.1–3.3 | `architect`/`data-flow-analyst`/`feature-analyst` | reasoning | Independent expert judgment |
| 3.4 | `synthesizer` | reasoning | The single most judgment-heavy step in the flow — see [feature-flow.md § Phase 3](../flows/feature-flow.md#phase-3--analysis-parallel) |
| 4 | `quiz-master` | reasoning | Writing a non-mechanical "why" question is itself judgment |
| 5 | `tdd-engineer` | reasoning | Deciding clause kind/level is a judgment call, even though the test *code* is mechanical |
| 6.0 | `solution-planner` | reasoning | Stress test + pre-mortem are adversarial reasoning |
| 6.1..n | `implementer` (task) | **execution, conditionally** | See §2 — only once a task is narrow enough |
| 6.x | `implementer` (reconciliation) | execution | The contract diff is explicitly mechanical — see [contract-ids.md](contract-ids.md#the-contract-diff-phase-6x-mechanical) |
| 6.y | `doc-writer` | execution | Transcribing decisions already made into docs |
| 7 | `reviewer` | reasoning | Business-logic judgment, not a linter |
| 8.1 | `qa-planner` | reasoning | Adversarial scenario design |
| 8.3 | `qa-automator` | execution | Writing specs from a plan + real DOM is mechanical translation |
| 9 | `pr-manager` | execution | Assembling a PR from already-decided content |

### 2. Task-level override for 6.1..n (the ambiguous case)

A single fixed tier for "implementation" doesn't hold — some tasks are truly mechanical (rename a field, wire a already-designed function) and some aren't (a task that turns out to need a design decision `6.0` didn't anticipate). Two options, **undecided**:

- **(a) `solution-planner` classifies each task at 6.0.** It has the most context to judge how mechanical a task will turn out — add an `Execution-safe: yes/no` flag per task in `6-solution.md`, next to size (S/M/L).
- **(b) The orchestrator decides per-spawn**, using task size as a proxy (S → execution, M/L → reasoning) with no upfront classification step.

(a) is more accurate but adds a judgment call to an already-loaded phase; (b) is cheaper to implement but a worse proxy (an S task can still be conceptually hard). Leaning toward (a), not confirmed.

**Escalation, either way**: if an execution-tier spawn produces a bad result, the existing [per-task review rejection](../flows/feature-flow.md#failure-edges) loop applies — same task re-spawned with feedback — with one addition: the re-spawn note may say "escalate to reasoning tier," and that choice is logged in `INDEX.md`'s decision log so a pattern of escalations is visible, not silently repeated.

### 3. Repo-side mapping — proposed `.ai-rules/project.md` §Agents (not yet in [project-md-schema.md](project-md-schema.md))

The schema doesn't know what "cheap" means in a given tool — that's exactly the kind of repo/tool fact `.ai-rules/project.md` already exists to hold (see [project-md-schema.md](project-md-schema.md)). A new, optional section, same `verify:`-where-possible discipline as every other section:

````markdown
## Agents (optional — cost-tier routing)
reasoning: {tool-specific model or agent identifier, e.g. "opus" or "@architect-strong"}
execution: {tool-specific model or agent identifier, e.g. "sonnet" or "@architect-fast"}
```

- **Absent section → every phase runs at `reasoning`.** No section means no downgrading; this key must be opted into, the same way a missing `Browser` section doesn't make phase 8.3 invent a URL.
- The values are opaque strings from the schema's point of view — the tool adapter (`feature-workflow.agent.md`'s "How to spawn a role" step, if this were wired in) is what interprets them into an actual invocation. The schema only says *when* to look the value up, never *how* to use it, keeping the manifest itself tool-agnostic.
- A resolved tier should be visible in the rendered packet (e.g. a task packet footer noting "spawned at execution tier") so a dev reviewing output can tell which tier produced it — auditability, not just cost savings.

## Open questions (why this isn't wired in yet)

1. Per-phase fixed tier vs. per-task dynamic classification for 6.1..n (§2) — undecided, needs a couple of real flows to see which one the 6.0 planner can actually judge well.
2. Should a downgrade ever apply to a ⛔ gate artifact? Current lean: no — gate artifacts (`2-prd.md`, `4-quiz.md`, `6-solution.md`, `9-pr-notes.md`) always run at `reasoning`, full stop, regardless of §Agents. Not yet stated as a hard rule anywhere because the whole mechanism is unconfirmed.
3. Worth tracking tier mix in `INDEX.md` (e.g. "6 tasks at execution tier, 2 at reasoning") as a cost-visibility delta, the way [gate-packet-template.md](../templates/gate-packet-template.md) already tracks findings/deviations? Nice-to-have, not required for a first version.
4. Does a bad `reasoning`/`execution` split just become a `FINDINGS.md`-style gotcha harvested at 9.5 (see [Keeping It Accurate](../PLAN.md#keeping-it-accurate)'s trigger-count pattern), so the default table above self-corrects per repo over time? Plausible, not designed.

## What it would take to actually wire this in

1. Add the `Tier` column to every phase table in `feature-flow.md`/`debug-flow.md`, and to `debug-flow.md`'s phase-2.5 addition.
2. Add the `## Agents` section to [project-md-schema.md](project-md-schema.md) and [templates/project-template.md](../templates/project-template.md).
3. Add a "resolve tier → concrete agent" step to `feature-workflow.agent.md`'s "How to spawn a role" and `debug-workflow.agent.md`.
4. Resolve the open questions above against at least one real dry run (see [VERIFICATION.md](../VERIFICATION.md)) before trusting the default tier table.

None of this has been done. This file is the parking spot for the idea, not a changelog of work completed.

## Related

- [project-md-schema.md](project-md-schema.md) — the schema this proposes extending
- [../flows/feature-flow.md](../flows/feature-flow.md) — the manifest this proposes extending
- [contract-ids.md](contract-ids.md) — the existing mechanical/judgment split (contract diff) this design generalizes
