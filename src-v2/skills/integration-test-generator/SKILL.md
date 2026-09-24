---
name: integration-test-generator
description: 'Status note: this skill is NOT used in src-v2 — folded into test-generator via contract-clause levels. Kept only as a pointer so nothing accidentally references it from a v2 flow. Keywords integration tests, folded, not used in src-v2.'
---

# integration-test-generator — not used in src-v2

**This skill is not invoked in any src-v2 flow.** The v1 base skill remains at [../../../src/skills/integration-test-generator/SKILL.md](../../../src/skills/integration-test-generator/SKILL.md), untouched, for v1 workflows.

## Why

Each `C*` clause in `5-contract.md` declares a `Kind` (happy/error/side-effect/cross-boundary/user-visible) which maps to a default `Level` (unit/integration/e2e) per [contract-ids.md](../../schemas/contract-ids.md). [test-generator (src-v2 overlay)](../test-generator/SKILL.md) generates the correct level directly from that table, rather than a separate skill re-detecting the framework and level per repo — see that overlay's "Override 2." A separate skill per level didn't scale across the `.ai-rules/project.md`-driven repo model; one level-aware skill does.

## Related

- [../test-generator/SKILL.md](../test-generator/SKILL.md) — where this behavior actually lives in src-v2
- [../../schemas/contract-ids.md](../../schemas/contract-ids.md)
