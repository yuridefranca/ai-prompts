---
name: root-cause-analyzer
description: src-v2 overlay for the v1 root-cause-analyzer skill — backs the debug-flow phase 2.5 rca-analyst. No fixes allowed; the deep tier gates on dev confirmation before phase 5 starts. Keywords root cause, RCA, debug flow, phase 2.5.
---

# root-cause-analyzer (src-v2 overlay)

**Base skill**: [../../../src/skills/root-cause-analyzer/SKILL.md](../../../src/skills/root-cause-analyzer/SKILL.md) — read that file for the full evidence-based investigation process. This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md) (v2 default: phase `2.5`, output `2.5-root-cause.md`).

## Where this runs in src-v2

Debug flow only, as `rca-analyst` at phase 2.5, reading the mini-PRD/repro contract (`2-prd.md`) and `3.0-component-map.md`. The base skill's no-fixes rule is unchanged and, if anything, more strictly enforced — the **deep** debug tier gates on this artifact before any solution work begins. See [debug-flow.md](../../flows/debug-flow.md#phase-25--root-cause-analysis-new).

## Related

- [../../agents/rca-analyst.agent.md](../../agents/rca-analyst.agent.md)
- [../../flows/debug-flow.md](../../flows/debug-flow.md)
