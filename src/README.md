# Subagent-Orchestrated Development Flows

Full design: [PLAN.md](PLAN.md). This README indexes what exists.

## What this is

Four flows — **feature**, **debug**, **improvement**, **greenfield** — where a thin orchestrator only orchestrates: stateless subagents do the work, and markdown artifacts in `.ai-workflow/[feature]/` are the contract between them. See [PLAN.md](PLAN.md) for the architecture, the adversarial passes, attention-engineered outputs, and the repository-conventions mechanism (`.ai-rules/project.md`) that keeps flows portable across repos.

## Directory map

```
src/
├── PLAN.md           the design — read this first
├── VERIFICATION.md   dry-run / negative-control protocol + manifest lint status
├── schemas/          conventions every other file is written against
├── flows/            tool-agnostic phase manifests + bootstrap + worktrees
├── templates/        fillable artifact templates (Layer 1/2, INDEX.md, FINDINGS.md, ...)
├── agents/           orchestrator + 4 flow adapters + 18 subagents
├── skills/           every skill the subagents apply, plus 2 standalone ones
├── contexts/         per-company packs: model lists (duelbits/, clair/), Duelbits PR conventions
└── scripts/          manifest-lint.sh (portability check), models_refresh.py (model list refresh)
```

## Status

Everything the plan specifies is written, and the manifest lint passes. **Not yet done**: a real feature or bug going through a flow end to end with a dev in the loop, and the negative-control run on a routine change. See [VERIFICATION.md](VERIFICATION.md) — every "not run" row there is the actual next step. The improvement and greenfield flows were added after the plan was built (ported from the retired v1 workflows) and haven't been dry-run either.

## Flows

| File | Contents |
|---|---|
| [flows/feature-flow.md](flows/feature-flow.md) | The full skeleton: severity gate, phase 0.5 (Orient) + phases 1–9.5, failure edges |
| [flows/debug-flow.md](flows/debug-flow.md) | Diff against feature-flow: mini-PRD, phase 2.5 root cause, repro-first contract |
| [flows/improvement-flow.md](flows/improvement-flow.md) | Diff against feature-flow: measured baseline, impact analysis on every tier, preserve clauses, scope-creep check |
| [flows/greenfield-flow.md](flows/greenfield-flow.md) | Diff against feature-flow: prototype/production tiers, phase 2.1 roadmap, phase 3.5 scaffold, Milestone 1 only |
| [flows/bootstrap.md](flows/bootstrap.md) | Shared flow-start procedure (project.md check, gitignore, folder/branch, overlap stage 1) |
| [flows/worktrees.md](flows/worktrees.md) | Git worktree commands + two-stage overlap detection for parallel flows |

## Schemas

| Schema | Defines |
|---|---|
| [skill-params.md](schemas/skill-params.md) | The `<!-- skill-params -->` block: how an orchestrator parameterizes a skill (`phase`, `output`, `inputs`, `findings`, `context_pack`) without forking it |
| [artifact-lifecycle.md](schemas/artifact-lifecycle.md) | `[knowledge]` vs `[process]` tiers, the per-artifact tier table, and the phase-9 promotion rule |
| [index-frontmatter.md](schemas/index-frontmatter.md) | `INDEX.md`'s YAML state record and the resume procedure |
| [artifact-status.md](schemas/artifact-status.md) | The `draft`/`complete` header every phase artifact carries, and why a `draft` artifact is re-run, never patched |
| [findings.md](schemas/findings.md) | `FINDINGS.md`'s table schema, status enum, update-not-duplicate rule, and robustness statements instead of finding quotas |
| [agent-tiers.md](schemas/agent-tiers.md) | Model tiers S/A/B/C, the default tier per agent, escalation one tier up on rejection, and how a tier resolves to a company's model |
| [contract-ids.md](schemas/contract-ids.md) | `C*` clause IDs, kind→level defaults, red (and preserve-clause green) evidence, the mechanical phase-6.x contract diff |
| [project-md-schema.md](schemas/project-md-schema.md) | `.ai-rules/project.md` — the repo-facts file that retires guessing in test, browser, and PR steps |

## Templates, agents, skills, contexts

- [templates/README.md](templates/README.md) — generic artifact skeleton, gate/task packets, visual standards, and the structured templates (`INDEX.md`, `FINDINGS.md`, `.ai-rules/project.md`, `.ai-rules/review.md`, `8-qa-plan.md`)
- [agents/README.md](agents/README.md) — the orchestrator, flow adapters, and subagent roster
- [skills/README.md](skills/README.md) — which skill backs which subagent and phase
- [contexts/](contexts/) — per-company packs: `models.md` (which model is each tier, per tool) for [duelbits](contexts/duelbits/models.md) and [clair](contexts/clair/models.md), plus Duelbits PR conventions resolved by `create-pr` via `context_pack`

## Proposals (drafted, not wired in)

| Draft | What |
|---|---|
| `scripts/install-agents` | Writes `model:` into agent files per company and tool, and generates the `-up` escalation twins — see [agent-tiers.md § Resolving a tier to a model](schemas/agent-tiers.md#resolving-a-tier-to-a-model). Waits on a Copilot bring-your-own-key test |

## History

This was built as `src-v2/` alongside an earlier set of workflows (v1: one big agent file per workflow, `0-startpoint.md` artifacts, no `INDEX.md`). v1 has been retired: its skills were merged into [skills/](skills/), its improvement and greenfield workflows were ported to [flows/](flows/), and the rest was dropped. It's all still in git history.
