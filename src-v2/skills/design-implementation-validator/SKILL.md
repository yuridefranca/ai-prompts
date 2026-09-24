---
name: design-implementation-validator
description: src-v2 overlay for the v1 design-implementation-validator skill — backs the UI branch of phase 8.3 (qa-automator), reading the dev-server/URL/selector environment contract from .ai-rules/project.md instead of auto-detection or a hardcoded localhost default. Keywords Figma validation, phase 8.3, environment contract.
---

# design-implementation-validator (src-v2 overlay)

**Base skill**: [../../../src/skills/design-implementation-validator/SKILL.md](../../../src/skills/design-implementation-validator/SKILL.md) — read that file for the full Figma-extraction, design-system-mapping, and Playwright-validation process. This file does not duplicate or modify it; the v1 file (including its `.design-validation.config.js` auto-detection and hardcoded `http://localhost:3000` default) is untouched and still applies to v1 workflows.

## v2 parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Override — environment contract, not auto-detection

In src-v2 (phase 8.3, `qa-automator`), **do not use the base skill's config file or auto-detection** for dev server / URL. Read the environment contract straight from `.ai-rules/project.md` instead:

| Needs | Source |
|---|---|
| Dev server command + ready pattern | `Run.dev`, `Run.ready_pattern` |
| Base URL | `Browser.base_url` |
| Selector convention | `Browser.selectors` (data-testid required, per the base skill's own convention) |
| Viewports/breakpoints | `Browser.viewports` |

If any of these is missing from project.md, **stop and ask** — never fall back to the base skill's `detectDevCommand()`-style heuristics or its `http://localhost:3000` default. See [project-md-schema.md](../../schemas/project-md-schema.md) and [qa-automator.agent.md](../../agents/qa-automator.agent.md).

## Related

- [../../schemas/project-md-schema.md](../../schemas/project-md-schema.md)
- [../../agents/qa-automator.agent.md](../../agents/qa-automator.agent.md)
