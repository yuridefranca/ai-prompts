# Verification (Slice 8)

**Slice status**: manifest lint automated and passing. The dry run and negative control require an actual feature/bug going through the flow with a dev in the loop across many gated turns — that has **not** been executed as part of building these flows, and this document says so rather than fabricating a result. Treat the tables below as the protocol to run, not a report of a run that happened.

## Per-slice verification

- Slices 0–2 approved before any agent code was written (see the slice-by-slice approvals in this build's conversation history).
- Slice 4 (`project-mapper`) landed before the orchestrators (slices 5–6), so no adapter was written against guessed repo facts.
- Each slice was presented as a task packet for approval before the next began, per [PLAN.md § Build Slices](PLAN.md#build-slices).

## Manifest lint (portability claim) — automated, passing

```
$ ./src/scripts/manifest-lint.sh
Manifest lint PASSED — flows/*.md contain no tool-specific syntax found by this check.
```

This is what backs the tool-agnostic claim **until a second working adapter exists** — see [PLAN.md § Architecture § Portability status](PLAN.md#three-layer-separation). Only the Copilot-style adapter (`agents/feature-workflow.agent.md`, `agents/debug-workflow.agent.md`) has been built; do not advertise multi-tool support based on the lint alone.

## Dry run (with a baseline) — protocol, not yet executed

Run the flow on a feature that has already shipped (through the retired v1 workflows, or by hand), so there's something to compare against.

| # | Assertion | Kind | Status |
|---|---|---|---|
| 1 | All artifacts produced per templates (Layer 1/2, visual standards, comprehension checks) | presence | ⬜ not run |
| 2 | Gates presented with decision boxes, not buried in prose | presence | ⬜ not run |
| 3 | Contract diff mechanically catches at least one uncited `C*` clause | behavior | ⬜ not run |
| 4 | A comprehension check at a gate is answered by the dev without opening Layer 2 | behavior | ⬜ not run |
| 5 | The finding ledger shows at least one finding *updated* by a later pass rather than duplicated | behavior | ⬜ not run |
| 6 | Hostile-user QA surfaces ≥1 non-obvious issue on a user-facing flow | behavior | ⬜ not run |
| 7 | ≥1 gotcha harvested into a skill's Gotchas section post-merge | presence | ⬜ not run |
| 7a | Every `C*` clause carries real red evidence — pasted failure output, not a claim | behavior | ⬜ not run |
| 7b | The contract diff rejects at least one citing test for zero assertions or wrong level | behavior | ⬜ not run |
| 7c | 8.3 writes Playwright specs from the real DOM into `test.e2e.location`, and they are in the PR diff | behavior | ⬜ not run |
| 7d | `project-mapper check` passes on the target repo, and 8.3 starts the dev server with no hardcoded URL or command | behavior | ⬜ not run |
| 8 | Resume works: kill the session mid-phase, restart, orchestrator resumes at the right phase without re-asking a passed gate | behavior | ⬜ not run |
| 9 | Knowledge-tier artifacts land in project.md's `docs.features` path in the PR diff; process-tier artifacts are absent from git | behavior | ⬜ not run |
| 10 | Phase 0.5's walkthrough gate blocks phase 1 until the dev picks an approach, and the file is actually deepened (not recreated) at each of the five later update spawns | behavior | ⬜ not run — added post-slice-8 |
| 11 | Improvement flow: every `preserve` clause carries green evidence before implementation, and 8.2 re-measures the phase-1 baseline with the same command | behavior | ⬜ not run — added at v1 retirement |
| 12 | Greenfield flow: phase 5 doesn't start until 3.5 has produced `.ai-rules/project.md` with working §Test commands, and the run builds Milestone 1 stories only | behavior | ⬜ not run — added at v1 retirement |

**Baseline comparison** (record, don't pass/fail, once run): artifact count, gate count, wall-clock to PR, and the dev's own answer to "did this catch anything v1 missed, and what did it cost?"

## Negative control — protocol, not yet executed

Run the flow a second time on a genuinely routine change (a copy tweak, a config value).

| Assertion | Status |
|---|---|
| The severity gate proposes **small** tier from evidence, unprompted | ⬜ not run |
| Total gates ≤2 | ⬜ not run |
| Adversarial passes produce robustness statements, not manufactured findings | ⬜ not run |
| Layer 1 outputs are boring | ⬜ not run |

**This is the adoption-critical test.** A flow that's heavyweight on trivial work gets abandoned regardless of how good it is on hard work — see [PLAN.md § Negative control](PLAN.md#negative-control).

## How to actually run this

1. Pick a repo with `.ai-rules/project.md` absent (to also exercise `project-mapper map`) or present (to exercise `check`).
2. Route a real feature request through `orchestrator.agent.md` → `feature-workflow.agent.md`.
3. Work every gate for real — a scripted/faked gate approval invalidates assertions 2 and 4.
4. Fill in the tables above with the actual result (✅/❌ + evidence link), not just a checkmark.
5. Repeat with a routine change for the negative control.
6. File the baseline comparison and any gotchas surfaced into the relevant skill's Gotchas section (phase 9.5) — that's assertion 7, and it's also how this document itself should get its first real update.

## Related

- [PLAN.md § Verification](PLAN.md#verification) — narrative source
- [scripts/manifest-lint.sh](scripts/manifest-lint.sh) — the one automated check in this document
