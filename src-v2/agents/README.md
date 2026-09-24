# Subagent Roster (Slice 3)

17 thin subagents (16 from slice 3 + `task-explainer`, added post-slice-8 — see [../README.md § Amendments](../README.md#amendments-post-slice-8)). Each is stateless, reads an exact file list, applies a skill, writes one artifact, and returns the fixed format: **5-bullet summary + open questions + artifact path + new/updated finding IDs** (deviations from that shape are called out per-agent where the phase needs them — e.g. `implementer`'s task mode reports deviations instead of open questions).

The orchestrator adapters (`orchestrator.agent.md`, `feature-workflow.agent.md`, `debug-workflow.agent.md` — slices 5–6) spawn these; they land in this same directory once built.

| Agent | Role | Skill | Phase |
|---|---|---|---|
| [task-explainer](task-explainer.agent.md) | Living HTML walkthrough — create + 5 deepenings | `explain-task` | 0.5, then 2/6.0/6.x/7/9 |
| [repo-mapper](repo-mapper.agent.md) | Writes/verifies `.ai-rules/project.md` | `project-mapper` | bootstrap |
| [prd-writer](prd-writer.agent.md) | Overview + PRD/mini-PRD + grill | `spec-extractor`, `grill-me` | 1, 2 |
| [architect](architect.agent.md) | Architecture analysis | `system-designer` | 3.1 |
| [data-flow-analyst](data-flow-analyst.agent.md) | Data flow analysis | `component-mapper` | 3.2 |
| [feature-analyst](feature-analyst.agent.md) | Senior SWE perspective | — | 3.3 |
| [synthesizer](synthesizer.agent.md) | ADR — merges 3.1–3.3, surfaces conflicts | `tradeoff-analyzer` | 3.4 |
| [rca-analyst](rca-analyst.agent.md) | Debug root cause (no fixes) | `root-cause-analyzer` | 2.5 (debug) |
| [quiz-master](quiz-master.agent.md) | Decision validation | `grill-me` | 4 |
| [tdd-engineer](tdd-engineer.agent.md) | Behavior contract + failing tests | `test-generator` | 5 |
| [solution-planner](solution-planner.agent.md) | Plan + stress test + pre-mortem | `tradeoff-analyzer`, `solution-critic` | 6.0 |
| [implementer](implementer.agent.md) | Task execution + reconciliation | `minimal-impl-generator`, `patch-implementer` | 6.1..n, 6.x |
| [doc-writer](doc-writer.agent.md) | Real-repo documentation | `documentation-writer` | 6.y |
| [reviewer](reviewer.agent.md) | Code review + solution critic | `code-review`, `solution-critic` | 7 |
| [qa-planner](qa-planner.agent.md) | Adversarial QA plan | — | 8.1 |
| [qa-automator](qa-automator.agent.md) | Playwright execution + UI branch | `design-implementation-validator` | 8.3 |
| [pr-manager](pr-manager.agent.md) | PR + comments + knowledge promotion | `create-pr` | 9, 9.1 |

See [../flows/feature-flow.md](../flows/feature-flow.md) and [../flows/debug-flow.md](../flows/debug-flow.md) for the full phase contracts these agents implement, and [../schemas/](../schemas/) for the conventions (skill-params, artifact status, findings, contract IDs) every agent file assumes.
