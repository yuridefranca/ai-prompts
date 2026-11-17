# Agents

**Orchestration**: [orchestrator](orchestrator.agent.md) (entry point — resume or classify, then route) and one adapter per flow: [feature-workflow](feature-workflow.agent.md), [debug-workflow](debug-workflow.agent.md), [improvement-workflow](improvement-workflow.agent.md), [greenfield-workflow](greenfield-workflow.agent.md).

## Subagent roster

18 thin subagents. Each is stateless, reads an exact file list, applies a skill, writes one artifact, and returns the fixed format: **5-bullet summary + open questions + artifact path + new/updated finding IDs** (deviations from that shape are called out per-agent where the phase needs them — e.g. `implementer`'s task mode reports deviations instead of open questions).

The workflow adapters spawn these.

| Agent | Role | Skill | Phase |
|---|---|---|---|
| [task-explainer](task-explainer.agent.md) | Living HTML walkthrough — create + 5 deepenings | `explain-task` | 0.5, then 2/6.0/6.x/7/9 |
| [repo-mapper](repo-mapper.agent.md) | Writes/verifies `.ai-rules/project.md` | `project-mapper` | bootstrap (greenfield: 3.5) |
| [prd-writer](prd-writer.agent.md) | Overview + PRD/mini-PRD + grill | `spec-extractor`, `grill-me` | 1, 2 |
| [roadmap-planner](roadmap-planner.agent.md) | Epics, stories, milestones; scopes Milestone 1 | `product-manager` | 2.1 (greenfield) |
| [architect](architect.agent.md) | Architecture analysis | `system-designer` | 3.1 |
| [data-flow-analyst](data-flow-analyst.agent.md) | Data flow analysis | `component-mapper` | 3.2 |
| [feature-analyst](feature-analyst.agent.md) | Senior SWE perspective | — | 3.3 |
| [synthesizer](synthesizer.agent.md) | ADR — merges 3.1–3.3, surfaces conflicts | `tradeoff-analyzer` | 3.4 |
| [rca-analyst](rca-analyst.agent.md) | Debug root cause (no fixes) | `root-cause-analyzer` | 2.5 (debug) |
| [quiz-master](quiz-master.agent.md) | Decision validation | `grill-me` | 4 |
| [tdd-engineer](tdd-engineer.agent.md) | Behavior contract + failing tests | `test-generator` | 5 |
| [solution-planner](solution-planner.agent.md) | Plan + stress test + pre-mortem | `tradeoff-analyzer`, `solution-critic` | 6.0 |
| [implementer](implementer.agent.md) | Task execution + refactor, reconciliation, greenfield scaffold | `minimal-impl-generator` or `patch-implementer`, then `refactor-optimizer` | 6.1..n, 6.x, 3.5 (greenfield) |
| [doc-writer](doc-writer.agent.md) | Real-repo documentation | `documentation-writer` | 6.y |
| [reviewer](reviewer.agent.md) | Code review + solution critic | `code-review`, `solution-critic` | 7 |
| [qa-planner](qa-planner.agent.md) | Adversarial QA plan | — | 8.1 |
| [qa-automator](qa-automator.agent.md) | Playwright execution + UI branch | `design-implementation-validator` | 8.3 |
| [pr-manager](pr-manager.agent.md) | PR + comments + knowledge promotion | `create-pr` | 9, 9.1 |

See [../flows/](../flows/) for the full phase contracts these agents implement, and [../schemas/](../schemas/) for the conventions (skill-params, artifact status, findings, contract IDs) every agent file assumes.
