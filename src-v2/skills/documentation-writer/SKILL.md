---
name: documentation-writer
description: src-v2 overlay for the v1 documentation-writer skill — backs doc-writer at phase 6.y, writing straight into the repo's own docs (per .ai-rules/project.md §Docs) instead of a .ai-workflow/ artifact, and running before phase 7 review. Keywords documentation, phase 6.y, real repo docs.
---

# documentation-writer (src-v2 overlay)

**Base skill**: [../../../src/skills/documentation-writer/SKILL.md](../../../src/skills/documentation-writer/SKILL.md) — read that file for the full documentation process (targets, glossary rules, ASCII-art prohibition). This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md). **`{{output}}` defaults to the repo's own docs, not a `.ai-workflow/` artifact** — a hard behavior change from the base skill's v1 defaults.

## Where this runs in src-v2

Backs `doc-writer` at phase 6.y, reading `2-prd.md` + `3.4-tradeoffs.md` + `5-contract.md` + `6-solution.md` + the diff, and writing directly into the paths named by `.ai-rules/project.md` §Docs (README sections, `AGENTS.md`, architecture docs, glossary). It runs *before* phase 7 review, so the reviewer can check the docs match what actually shipped, not just the original plan.

## Related

- [../../agents/doc-writer.agent.md](../../agents/doc-writer.agent.md)
- [../../schemas/project-md-schema.md](../../schemas/project-md-schema.md)
