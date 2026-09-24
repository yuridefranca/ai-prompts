---
name: component-mapper
description: src-v2 overlay for the v1 component-mapper skill — runs standalone at phase 3.0 (feeding all three phase-3 analysts) and again backs data-flow-analyst at phase 3.2. Keywords component map, phase 3.0, phase 3.2, data flow.
---

# component-mapper (src-v2 overlay)

**Base skill**: [../../../src/skills/component-mapper/SKILL.md](../../../src/skills/component-mapper/SKILL.md) — read that file for the full component-mapping process. This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs in src-v2

Two invocations:

- **Phase 3.0**, standalone (both flows): produces `3.0-component-map.md`, feeding all three phase-3 analysts — see [feature-flow.md § Phase 3](../../flows/feature-flow.md#phase-3--analysis-parallel).
- **Phase 3.2**, backing `data-flow-analyst`: the data-flow-specific view (sequence diagrams), reading `3.0-component-map.md` as ground truth.

## Related

- [../../agents/data-flow-analyst.agent.md](../../agents/data-flow-analyst.agent.md)
- [../../flows/feature-flow.md](../../flows/feature-flow.md)
