---
name: spec-extractor
description: src-v2 overlay for the v1 spec-extractor skill — backs prd-writer at phase 1 (overview) and phase 2 (PRD), emitting numbered AC* acceptance-criteria IDs instead of a bullet list. Keywords spec extraction, PRD, acceptance criteria, phase 1, phase 2.
---

# spec-extractor (src-v2 overlay)

**Base skill**: [../../../src/skills/spec-extractor/SKILL.md](../../../src/skills/spec-extractor/SKILL.md) — read that file for the full requirements-extraction process. This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs in src-v2

Backs `prd-writer` at both phase 1 (overview mode, no acceptance criteria yet) and phase 2 (PRD mode, output `2-prd.md`).

**Emit acceptance criteria as numbered `AC1..ACn` IDs, not a bullet list.** Phase 7's Business Logic Review checks each ID individually against the implementation — see [PLAN.md § Business Logic Awareness in Review](../../PLAN.md#business-logic-awareness-in-review) — so an unnumbered criterion can't be tracked to a pass/fail.

## Related

- [../../agents/prd-writer.agent.md](../../agents/prd-writer.agent.md)
