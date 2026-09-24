# src-v2 — Subagent-Orchestrated Development Flows

Full design: [PLAN.md](PLAN.md). This README tracks build status and indexes what exists so far.

## What this is

Two flows (feature, debug) where a thin orchestrator only orchestrates — stateless subagents do the work, markdown artifacts in `.ai-workflow/[feature]/` are the contract between them. See [PLAN.md](PLAN.md) for the full architecture, the six adversarial passes, attention-engineered outputs, and the repository-conventions mechanism that keeps flows portable across repos.

Built in 9 reviewable slices ([Build Slices](PLAN.md#build-slices)); each slice was presented for approval before the next started.

## Directory map

```
src-v2/
├── PLAN.md              the design — read this first
├── README.md            this file
├── VERIFICATION.md       [slice 8] dry-run / negative-control protocol + manifest lint status
├── schemas/              [slice 0] foundational conventions — the vocabulary every other slice writes in
├── flows/                [slice 1, 7] tool-agnostic phase manifests + bootstrap + worktrees
├── templates/            [slice 2] fillable artifact templates (Layer 1/2, INDEX.md, FINDINGS.md, ...)
├── agents/               [slice 3, 5, 6 + amendment] 17 subagents + the v2 orchestrator + feature/debug adapters
├── skills/               [slice 3, 4 + amendment] thin v2 overlays over v1 skills (never edits src/skills/) + project-mapper, explain-task (new, no proper v1 base)
├── contexts/             [slice 7] per-repo template overrides (duelbits/)
└── scripts/              [slice 8] manifest-lint.sh — the automated portability check
```

## Slice status — all 9 done

| Slice | Contents | Status |
|---|---|---|
| **0** | Foundations (`schemas/`) | ✅ done |
| **1** | Flow manifests (`flows/feature-flow.md`, `flows/debug-flow.md`, `flows/bootstrap.md`) | ✅ done |
| **2** | Artifact templates (`templates/`) | ✅ done |
| **3** | Subagent roster (16 `.agent.md` files) + their `skills/` overlays | ✅ done |
| **4** | Repository conventions (`skills/project-mapper` + `repo-mapper` agent + bootstrap) | ✅ done |
| **5** | Copilot orchestrators (`agents/orchestrator.agent.md` router + `agents/feature-workflow.agent.md` adapter) | ✅ done |
| **6** | Debug adapter (`agents/debug-workflow.agent.md`) | ✅ done |
| **7** | Context packs (`contexts/duelbits/`) + worktree management + overlap detection (`flows/worktrees.md`) | ✅ done |
| **8** | Manifest lint (automated, passing) + dry-run/negative-control protocol (`VERIFICATION.md`) | ✅ protocol built — **dry run itself not yet executed**, see below |

See [Amendments (post-slice-8)](#amendments-post-slice-8) below for what's landed since all 9 slices were marked done.

Cross-cutting skill refactors ([PLAN.md §Cross-Cutting Skill Refactor](PLAN.md#cross-cutting-skill-refactor)) landed inside whichever slice first used each skill, not as a separate slice. **All 12 skills in that table have a `src-v2/skills/<name>/SKILL.md` overlay** (`{{phase}}`/`{{output}}`/`{{inputs}}`/`{{findings}}`/`{{context_pack}}` support, v1 defaults preserved) — the v1 files under `../src/skills/` are **untouched**; see [skills/README.md](skills/README.md) for the index. `project-mapper` (new skill, slice 4) has no v1 base and lives entirely at [`skills/project-mapper/SKILL.md`](skills/project-mapper/SKILL.md).

## What "done" means here vs. what's still open

Every artifact the plan specifies has been written: schemas, manifests, templates, the subagent roster, the three v2 `.agent.md` orchestrator files, the context pack, worktree docs, and an automated manifest lint (passing). **What has not happened**: a real feature or bug going through the flow end to end with a dev in the loop, and the negative-control run on a routine change. See [VERIFICATION.md](VERIFICATION.md) for the exact assertion checklist and how to run it — treat every "not yet executed" row there as the actual next step, not a formality.

## Amendments (post-slice-8)

Changes made after all 9 slices were marked done, so the slice table above doesn't silently go stale.

### Phase 0.5 — Orient, + `task-explainer`, + `explain-task` skill

Added a new phase at the very start of both flows: a living, mobile-first HTML walkthrough (the problem, screenshots, plain-language solution alternatives, Watch outs) that gates on the dev picking an approach *before* the formal PRD is written, then gets deepened — without a gate — five more times as the flow progresses (after phases 2, 6.0, 6.x, 7, 9).

Adapted from a WIP skill the dev had already built for a different, non-portable workflow (`src-duelbits/skills/explain-task` — Cursor-slash-command-based, hardcoded to one specific client's terminology and tooling). The src-v2 version at [skills/explain-task/SKILL.md](skills/explain-task/SKILL.md) keeps the actual design (stages, watch-out cards, quiz, mobile-first HTML spec) and retargets every repo-specific assumption onto `.ai-rules/project.md` / the v2 phase model. The original is untouched — see [src-v2/skills/README.md § Why two skills kept their v1 name](skills/README.md) for the same "don't edit the source, overlay instead" reasoning applied here, one step further (this skill has no proper v1 base to overlay, so it's a fresh adaptation, not a thin pointer).

**Touched by this amendment**: `flows/feature-flow.md`, `flows/debug-flow.md` (new phase 0.5 + 5 hook notes + failure-edge row), `agents/task-explainer.agent.md` (new), `skills/explain-task/{SKILL.md,FORMAT.md}` (new), `schemas/artifact-lifecycle.md` (new artifact row), `schemas/artifact-status.md` (new non-markdown-artifact section), `templates/index-template.md` (phase row + Mermaid node), `PLAN.md` (phase count, tier tables, roster table, INDEX.md example — all updated to match).

**Not yet done**: `templates/gate-packet-template.md` and `templates/task-packet-template.md` need no changes (phase 0.5 reuses the existing mini-gate packet shape verbatim), but this amendment hasn't been through its own dry run — see assertion 10 in [VERIFICATION.md](VERIFICATION.md), added alongside this amendment.

## Schemas (Slice 0)

The vocabulary that everything downstream — flow manifests, templates, agents — is written against.

| Schema | Defines |
|---|---|
| [skill-params.md](schemas/skill-params.md) | The `<!-- skill-params -->` block: how an orchestrator parameterizes a shared skill (`phase`, `output`, `inputs`, `findings`, `context_pack`) without forking it |
| [artifact-lifecycle.md](schemas/artifact-lifecycle.md) | `[knowledge]` vs `[process]` tiers, the canonical per-artifact tier table, and the phase-9 promotion rule |
| [index-frontmatter.md](schemas/index-frontmatter.md) | `INDEX.md`'s YAML state record and the 5-step resume procedure the orchestrator runs at the start of every session |
| [artifact-status.md](schemas/artifact-status.md) | The `draft`/`complete` header every phase artifact carries, and why a `draft` artifact is re-run, never patched |
| [findings.md](schemas/findings.md) | `FINDINGS.md`'s table schema, status enum, update-not-duplicate rule, and the no-quotas / robustness-statement replacement for mandatory finding counts |
| [contract-ids.md](schemas/contract-ids.md) | `C*` clause IDs, kind→level defaults, the mandatory red-evidence rule, and the mechanical phase-6.x contract diff |
| [project-md-schema.md](schemas/project-md-schema.md) | `.ai-rules/project.md` — the repo-facts file that retires guessing in `test-generator`, `design-implementation-validator`, and `create-pr` |

## Flows (Slice 1, 7)

| File | Contents |
|---|---|
| [flows/feature-flow.md](flows/feature-flow.md) | Full feature-flow manifest: severity gate, phase 0.5 (Orient) + all 9 numbered phases (21 execution stops, 20 on the `small` tier which skips 0.5), failure edges |
| [flows/debug-flow.md](flows/debug-flow.md) | Debug flow as a diff against feature-flow, plus the new phase 2.5 root-cause contract |
| [flows/bootstrap.md](flows/bootstrap.md) | Shared flow-start procedure (project.md check, gitignore, folder/branch, overlap stage 1) |
| [flows/worktrees.md](flows/worktrees.md) | Git worktree commands + two-stage overlap detection for parallel flows |

## Templates (Slice 2)

See [templates/README.md](templates/README.md) for the full index (generic artifact skeleton, gate/task packets, visual standards, and the five structured templates: `INDEX.md`, `FINDINGS.md`, `.ai-rules/project.md`, `.ai-rules/review.md`, `8-qa-plan.md`).

## Agents (Slice 3, 5, 6)

See [agents/README.md](agents/README.md) for the 17-role subagent roster. The three orchestration files sit alongside them: [agents/orchestrator.agent.md](agents/orchestrator.agent.md) (v1/v2 router + resume), [agents/feature-workflow.agent.md](agents/feature-workflow.agent.md), [agents/debug-workflow.agent.md](agents/debug-workflow.agent.md).

## Skills (Slice 3, 4)

See [skills/README.md](skills/README.md) for the overlay index. Every file under `src-v2/skills/` either (a) overlays a v1 skill — points at the untouched `src/skills/<name>/SKILL.md` and states only the src-v2-specific delta, or (b) is new to v2 with no proper v1 equivalent (`project-mapper`, `explain-task` — the latter adapted from a WIP client-specific skill, see [Amendments](#amendments-post-slice-8)). **No file under `src/skills/` is ever edited for v2** — see [PLAN.md § Architecture](PLAN.md#three-layer-separation).

## Context packs (Slice 7)

[contexts/duelbits/pr-template.md](contexts/duelbits/pr-template.md) — the one context pack built so far, resolved by `create-pr` via `context_pack` in its skill-params block.

## Proposals (drafted, not wired in)

Ideas captured for later so they aren't lost, but **not** part of any flow, template, or agent file yet — don't assume these are live.

| Draft | What |
|---|---|
| [schemas/agent-tiers.md](schemas/agent-tiers.md) | Per-phase cost tiers (`reasoning`/`execution`) so mechanical post-planning phases can hand off to a cheaper agent/model, with the actual mapping left to a per-repo `.ai-rules/project.md` section (tool-specific, never hardcoded in the manifest). Open questions listed in the file; not yet applied to `feature-flow.md`/`debug-flow.md`. |

## Relationship to v1

src-v2 depends on `../src/skills/` for base skill content — v1 is not deleted, both are installed in the same repos, and **v2 never edits a v1 skill file**; any v2-specific behavior lives in a `src-v2/skills/` overlay instead. See [v1 / v2 Coexistence](PLAN.md#v1--v2-coexistence) for the routing and folder-identification rules (`INDEX.md` presence is what marks a v2 folder).
