# Flow Manifest: Greenfield

**Tool-agnostic**, same rules as [feature-flow.md](feature-flow.md): no tool-specific syntax, roles named without `@`.

For a new project or service started from scratch. The core rule is **vision before code**, with planning sized to the project: a weekend prototype needs less process than a production platform. A greenfield run builds **Milestone 1 only** — the smallest usable product. Every later milestone runs as its own [feature flow](feature-flow.md).

Same skeleton as [feature-flow.md](feature-flow.md). This manifest states **only the differences** — every phase not listed below runs exactly as the feature flow defines it, including its Role/Input/Task/Output contract, its templates, and the [Failure Edges](feature-flow.md#failure-edges) table.

## Differences from Feature Flow

| Phase | Feature Flow | Greenfield Flow |
|---|---|---|
| Bootstrap | Check `.ai-rules/project.md` | There's nothing to map yet: `project-mapper` is **deferred to phase 3.5**. See below |
| 0 | Severity gate: small/medium/full | Tiers are **prototype** / **production**. See below |
| 0.5 | Orient — problem, current state, alternatives | Orient — **the vision**: who it's for, what problem it solves, and product-shape alternatives (e.g. CLI vs web app, single service vs several). No "current state" screenshots — there is no product yet; show the problem in the user's world instead |
| 1 | Overview | Overview = the vision: what, why, who, expected outcome, constraints |
| 2 | PRD for one feature | PRD for the **whole project** — every requirement, each with an `AC*` ID |
| 2.1 | — | **Roadmap** (new phase): epics, prioritized stories, milestones. ⛔ gate on Milestone 1's scope. See below |
| 3.0 | Component map of existing code | **Skipped** — no existing code |
| 3.1 | Architecture | Architecture + **tech stack selection** with rationale for each choice |
| 3.x–3.4 | Analysis of the feature | Analysis of **Milestone 1**, informed by the whole roadmap so early choices don't block later milestones |
| 3.5 | — | **Scaffold** (new phase): project structure, tooling, test runner, CI — then `project-mapper map`. See below |
| 5–8 | The feature | **Milestone 1's stories only**, read from `2.1-roadmap.md` |
| 6.y | Update the repo's docs | **Create** them: `README.md` with setup instructions, `AGENTS.md` (via `agents-md-generator`), ADRs from `3.4-tradeoffs.md`, a glossary if the domain needs one |
| 9 | PR | PR if the repo has a remote; otherwise `9-pr-notes.md` alone. Either way it adds a **How to continue** section: remaining milestones, and that each one starts as a new feature flow with `2.1-roadmap.md` as input |

---

## Bootstrap (greenfield)

Same as [bootstrap.md](bootstrap.md) except:

- **No git repo yet** → ask before running `git init`; create `.gitignore` with `.ai-workflow/` in it before any artifact is written.
- **`.ai-rules/project.md` is not checked or offered** here. There are no commands, tests, or conventions to inspect until phase 3.5 creates them. Phases before 3.5 read no project facts.

---

## Phase 0 — Severity Gate (greenfield)

| Tier | Criteria | Phases run | Gates |
|---|---|---|---|
| **Prototype** | Exploration, demo, or personal tool; throwaway acceptable; one runtime | 1, 2, 2.1, 3 (single analyst), 3.4, 3.5, 5, 6, 6.y, 7, 9 | 2, 2.1, 6.0, 9 |
| **Production** | Real users, persisted data, more than one service, or the dev overrides upward | all except 3.0 | 0.5, 2, 2.1, 4, 6.0, 9 |

Evidence for the proposal comes from the request itself (users, data, integrations named), since there's no code to grep.

---

## Phase 2.1 — Roadmap ⛔ GATE (new)

| Field | Value |
|---|---|
| Role | `roadmap-planner` |
| Skill | `product-manager` |
| Input | `1-overview.md`, `2-prd.md` |
| Task | Group requirements into 2–5 epics; split epics into stories of 1–3 days, each citing the `AC*` IDs it delivers; MoSCoW priority (Must Have ≤ 40%); dependencies; S/M/L effort; 2–4 milestones. **Milestone 1 is the smallest usable product**, not "the foundations" |
| Output | `2.1-roadmap.md` `[knowledge]` |
| Gate | ⛔ Dev approves Milestone 1's scope. Phases 3–9 cover only those stories |

**Rejection**: re-spawn `roadmap-planner` with the dev's objection; `2.1-roadmap.md` overwritten wholesale.

---

## Phase 3.5 — Scaffold (new)

| Field | Value |
|---|---|
| Role | `implementer` (scaffold mode), then `repo-mapper` |
| Skill | — (scaffold), `project-mapper` (`map` mode) |
| Input | `3.4-tradeoffs.md` (the stack decision), `3.1-architecture.md` |
| Task | Create the project skeleton the ADR describes: folder structure, package manifest, lint/format, the test runner for every level the contract will need, a dev-server command, CI basics. Run the empty test suite once to prove the runner works. Then `repo-mapper` runs `project-mapper map` against the fresh repo |
| Output | the scaffold in the repo + `.ai-rules/project.md` |

From here on, every phase reads project facts from `.ai-rules/project.md` exactly as in the feature flow. Phase 5 depends on this: `test-generator` reads the test framework from §Test.

---

## Related

- [feature-flow.md](feature-flow.md) — the skeleton this manifest diffs against, and the flow every later milestone runs as
- [bootstrap.md](bootstrap.md) — shared flow-start procedure
- [../skills/product-manager/SKILL.md](../skills/product-manager/SKILL.md) — the roadmap skill
