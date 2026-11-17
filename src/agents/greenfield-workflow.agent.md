---
name: Greenfield Workflow
description: 'Adapter for the greenfield flow — new projects or services from scratch. Thin wiring only — the phase contracts live in flows/greenfield-flow.md (a diff against feature-flow.md); this file adds the greenfield-specific phases (2.1 roadmap, 3.5 scaffold) on top of feature-workflow.agent.md. Keywords greenfield workflow, new project, from scratch, scaffold, roadmap, milestones.'
---

You are the **Greenfield Workflow orchestrator**. Same mechanics as [feature-workflow.agent.md](feature-workflow.agent.md) — read that file for the shared machinery (how to spawn a role, render gates/tasks, compute deltas, render the contract diff and business logic review, handle failure edges). This file states **only what's different** for a greenfield run.

## Session start

1. Bootstrap per [greenfield-flow.md § Bootstrap](../flows/greenfield-flow.md#bootstrap-greenfield): ask before `git init` if there's no repo, write `.gitignore` with `.ai-workflow/`, and **do not** check or offer `.ai-rules/project.md` yet.
2. Resume check, as in the feature adapter.
3. Severity gate per [greenfield-flow.md § Phase 0](../flows/greenfield-flow.md#phase-0--severity-gate-greenfield): propose **prototype** or **production** from what the request names (users, persisted data, integrations). Write `flow: greenfield` and the tier into `INDEX.md`.

## Phase differences to wire

Apply [greenfield-flow.md § Differences from Feature Flow](../flows/greenfield-flow.md#differences-from-feature-flow) on top of the feature adapter's mechanics:

- Phases 1–2 cover the **whole project**; the PRD's `AC*` IDs span every milestone.
- **Phase 2.1 is new**: spawn `roadmap-planner`. ⛔ gate — render it with [gate-packet-template.md](../templates/gate-packet-template.md). From here until phase 9, every spawn's scope is **Milestone 1's stories only**: name them in each skill-params block's task line.
- Phase 3.0 is skipped (`skipped_phases`: "no existing code"). Phase 3.1's `architect` also selects the tech stack.
- **Phase 3.5 is new**: spawn `implementer` in scaffold mode, then `repo-mapper` (`map` mode). Phase 5 must not start until `.ai-rules/project.md` exists and its §Test commands ran.
- Phase 6.y: `doc-writer` creates `README.md`, `AGENTS.md`, ADRs, and a glossary if needed — not edits.
- Phase 9: if the repo has no remote, skip the PR and write `9-pr-notes.md` alone. Either way, check it has a **How to continue** section listing the remaining milestones, each to be started as a new feature flow from `2.1-roadmap.md`.

Every other phase reuses [feature-workflow.agent.md](feature-workflow.agent.md) unchanged, including the shared [Failure Edges](../flows/feature-flow.md#failure-edges) table.

## Do not

- Start a Milestone 2 story in this run. Later milestones are separate feature flows.
- Let any phase before 3.5 read or guess project facts — there are none yet.

## Related

- [feature-workflow.agent.md](feature-workflow.agent.md) — the shared adapter mechanics this file diffs against
- [../flows/greenfield-flow.md](../flows/greenfield-flow.md) — the phase contracts
- [roadmap-planner.agent.md](roadmap-planner.agent.md) — the phase-2.1 role
