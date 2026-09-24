---
name: code-review
description: src-v2 overlay for the v1 code-reviewer skill, invoked under the name "code-review" in src-v2's phase 7 — adds the Business Logic Review table, .ai-rules/review.md rules compliance, and the findings-delta reporting rule. Keywords code review, phase 7, business logic review, review rules.
---

# code-review (src-v2 overlay)

**Base skill**: [../../../src/skills/code-reviewer/SKILL.md](../../../src/skills/code-reviewer/SKILL.md) — read that file for the full review process (security, performance, quality, tech-stack detection, output format). This file does not duplicate or modify it; the v1 file keeps its original name (`code-reviewer`) and is untouched. **In src-v2 this skill is invoked as `code-review`** — see [Repository Conventions naming](../../PLAN.md) and [../../agents/reviewer.agent.md](../../agents/reviewer.agent.md).

## v2 parameters

Read `{{phase}}`, `{{output}}`, and `{{findings}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs in src-v2

Phase 7, code-reviewer mode of the `reviewer` subagent. Additionally reads `.ai-rules/review.md` (project-specific rules — absent is not a hard failure: note "no project-specific rules found" and proceed) plus `2-prd.md`/`3.4-tradeoffs.md`/`5-contract.md`/`6-solution.md` for the Business Logic Review table — see [PLAN.md § Business Logic Awareness in Review](../../PLAN.md#business-logic-awareness-in-review).

Every finding is written to `{{findings}}` (`FINDINGS.md`) with a stable `F*` ID; a finding that already exists is **updated**, never re-reported — see [findings.md](../../schemas/findings.md).

## Related

- [../../schemas/findings.md](../../schemas/findings.md), [../../templates/review-rules-template.md](../../templates/review-rules-template.md)
- [../../agents/reviewer.agent.md](../../agents/reviewer.agent.md)
