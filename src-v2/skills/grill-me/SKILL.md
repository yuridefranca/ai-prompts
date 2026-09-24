---
name: grill-me
description: src-v2 overlay for the v1 grill-me skill — adversarial spec refinement folded inline into phase 2 (PRD) and phase 4 (decision quiz) instead of producing a standalone artifact. Keywords grill-me, spec refinement, src-v2 overlay.
---

# grill-me (src-v2 overlay)

**Base skill**: [../../../src/skills/grill-me/SKILL.md](../../../src/skills/grill-me/SKILL.md) — read that file for the full interview process. This file does not duplicate or modify it; it states only what's different when this skill runs inside a src-v2 flow. The v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md) — no defaults assumed here, since this skill never runs standalone in src-v2.

## Where this runs in src-v2

Unlike v1 (a standalone `0.1-grill-me.md` artifact), src-v2 folds the interview **inline** into whichever artifact is being produced:

| Caller | Phase | `{{output}}` |
|---|---|---|
| `prd-writer` (PRD mode) | 2 | `2-prd.md` |
| `quiz-master` | 4 | `4-quiz.md` |

No standalone `0.1-grill-me.md` is ever produced by a src-v2 flow — the grilling and its resolution live inside the phase artifact they informed.

## Related

- [../../agents/prd-writer.agent.md](../../agents/prd-writer.agent.md), [../../agents/quiz-master.agent.md](../../agents/quiz-master.agent.md) — the subagents that invoke this overlay
- [../../schemas/skill-params.md](../../schemas/skill-params.md)
