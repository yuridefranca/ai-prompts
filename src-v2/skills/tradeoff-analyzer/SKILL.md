---
name: tradeoff-analyzer
description: src-v2 overlay for the v1 tradeoff-analyzer skill — backs synthesizer at phase 3.4 (merging independent analyses, surfacing conflicts) and solution-planner at phase 6.0 (evaluating the chosen plan's own tradeoffs). Keywords tradeoff analysis, ADR, phase 3.4, phase 6.0.
---

# tradeoff-analyzer (src-v2 overlay)

**Base skill**: [../../../src/skills/tradeoff-analyzer/SKILL.md](../../../src/skills/tradeoff-analyzer/SKILL.md) — read that file for the full tradeoff-analysis process. This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs in src-v2

Two distinct roles — **not interchangeable**:

- **Phase 3.4** (`synthesizer`): merges `3.1`/`3.2`/`3.3` into `3.4-tradeoffs.md`, explicitly surfacing analyst conflicts (escalated to `FINDINGS.md` if unresolved). Adjudicates between three independent analyses.
- **Phase 6.0** (`solution-planner`): evaluates implementation-approach tradeoffs within `6-solution.md`. Evaluates the chosen plan's own tradeoffs, not competing analyses.

## Related

- [../../agents/synthesizer.agent.md](../../agents/synthesizer.agent.md), [../../agents/solution-planner.agent.md](../../agents/solution-planner.agent.md)
