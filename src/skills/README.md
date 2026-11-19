# Skills

Each skill follows the [Agent Skills spec](https://agentskills.io/) (see the repo-root [AGENTS.md](../../AGENTS.md) for authoring rules). Skills that a flow phase invokes take a [skill-params block](../schemas/skill-params.md) and open with `## Parameters` and `## Where this runs` sections.

## Used by the flows

| Skill | Subagent | Phase |
|---|---|---|
| [project-mapper](project-mapper/SKILL.md) | `repo-mapper` | bootstrap (greenfield: 3.5) |
| [explain-task](explain-task/SKILL.md) | `task-explainer` | 0.5, then updates at 2/6.0/6.x/7/9 |
| [spec-extractor](spec-extractor/SKILL.md) | `prd-writer` | 1, 2 |
| [grill-me](grill-me/SKILL.md) | `prd-writer`, `quiz-master` | 2, 4 (inline, no standalone artifact) |
| [product-manager](product-manager/SKILL.md) | `roadmap-planner` | 2.1 (greenfield) |
| [root-cause-analyzer](root-cause-analyzer/SKILL.md) | `rca-analyst` | 2.5 (debug) |
| [component-mapper](component-mapper/SKILL.md) | standalone, `data-flow-analyst` | 3.0, 3.2 |
| [system-designer](system-designer/SKILL.md) | `architect` | 3.1 |
| [tradeoff-analyzer](tradeoff-analyzer/SKILL.md) | `synthesizer`, `solution-planner` | 3.4, 6.0 |
| [test-generator](test-generator/SKILL.md) | `tdd-engineer` (contract), `test-writer` (tests) | 5 (all test levels — absorbed the old `integration-test-generator`) |
| [solution-critic](solution-critic/SKILL.md) | `solution-planner`, `reviewer` | 6.0, 7 |
| [minimal-impl-generator](minimal-impl-generator/SKILL.md) | `implementer` | 6.1..n (feature, improvement, greenfield) |
| [patch-implementer](patch-implementer/SKILL.md) | `implementer` | 6.1..n (debug) |
| [refactor-optimizer](refactor-optimizer/SKILL.md) | `implementer` | end of each 6.1..n task |
| [documentation-writer](documentation-writer/SKILL.md) | `doc-writer` | 6.y |
| [code-review](code-review/SKILL.md) | `rules-checker` (written rules), `reviewer` | 7.0, 7 |
| [design-implementation-validator](design-implementation-validator/SKILL.md) | `qa-automator` | 8.3 (UI branch) |
| [create-pr](create-pr/SKILL.md) | `pr-manager` | 9, 9.1 |

## Standalone

| Skill | Use | Tier |
|---|---|---|
| [btw](btw/SKILL.md) | Side questions that stay out of the flow's artifacts and state | C |
| [agents-md-generator](agents-md-generator/SKILL.md) | Create or update a repo's `AGENTS.md`; also used by `documentation-writer` | A |

Skills inside the flows carry no tier — the agent applying them does. Standalone skills do; only Claude Code honors it (see [agent-tiers.md § Standalone skills](../schemas/agent-tiers.md#standalone-skills)).

## Related

- [../schemas/skill-params.md](../schemas/skill-params.md) — the block every flow skill accepts
- [../agents/README.md](../agents/README.md) — the subagents that invoke these skills
