---
name: create-pr
description: src-v2 overlay for the v1 pr-creator skill, invoked under the name "create-pr" — backs pr-manager at phase 9, reading branch/base/template/checks from .ai-rules/project.md instead of org-detection, with org-specific behavior (e.g. Duelbits) supplied by a context pack instead of a skill fork. Keywords PR creation, phase 9, context pack, knowledge promotion.
---

# create-pr (src-v2 overlay)

**Base skill**: [../../../src/skills/pr-creator/SKILL.md](../../../src/skills/pr-creator/SKILL.md) — read that file for the full PR-creation process (user confirmation, template discovery/filling rules, output format). This file does not duplicate or modify it; the v1 file keeps its original name (`pr-creator`) and is untouched. **In src-v2 this skill is invoked as `create-pr`.**

## v2 parameters

Read `{{phase}}`, `{{output}}`, and `{{context_pack}}` from a [skill-params block](../../schemas/skill-params.md).

## Override — no org detection, project.md + context pack instead

**Skip the base skill's organization-detection step entirely.** Branch pattern, base branch, PR template path, required checks, and merge strategy come from `.ai-rules/project.md` §Git & PR — no heuristics, no git-remote sniffing. Org-specific behavior (e.g. Duelbits' QA handover notes, project detection, Jira integration) is supplied by a [context pack](../../PLAN.md#context-packs) via `{{context_pack}}`, which resolves template overrides (e.g. [contexts/duelbits/pr-template.md](../../contexts/duelbits/pr-template.md)) without forking this skill's logic. See [skill-params.md](../../schemas/skill-params.md).

## Additional src-v2 behavior

Follow `.ai-rules/project.md` §Git & PR directly, using the resolved `{{context_pack}}` template if one was passed. Additionally, promote every `[knowledge]`-tagged artifact into `Docs.features` (stripped of its artifact-status header) and the phase-8.3 Playwright specs into `Test.e2e.location`, both included in the PR diff — see [artifact-lifecycle.md](../../schemas/artifact-lifecycle.md) and [pr-manager.agent.md](../../agents/pr-manager.agent.md). Block PR creation while any 🔴 finding is `open` in `FINDINGS.md`.

## Related

- [../../contexts/duelbits/pr-template.md](../../contexts/duelbits/pr-template.md) — the one context pack built so far
- [../../agents/pr-manager.agent.md](../../agents/pr-manager.agent.md)
