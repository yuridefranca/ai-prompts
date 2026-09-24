---
name: test-generator
description: src-v2 overlay for the v1 test-generator skill — backs tdd-engineer at phase 5, reading the test framework from .ai-rules/project.md instead of asking, and generating the level a contract clause requires (folding in what v1 called integration-test-generator) instead of unit tests only. Keywords TDD, contract clauses, phase 5, test framework.
---

# test-generator (src-v2 overlay)

**Base skill**: [../../../src/skills/test-generator/SKILL.md](../../../src/skills/test-generator/SKILL.md) — read that file for the base TDD process (edge-cases-first, mocking discipline, red-phase verification). This file does not duplicate or modify it; the v1 file is untouched. **Two behaviors below explicitly override the base skill's v1-only defaults** — everything else in the base skill applies unchanged.

## v2 parameters

Read `{{phase}}`, `{{output}}`, and `{{inputs}}` from a [skill-params block](../../schemas/skill-params.md) (v2 default: phase `5`, output `5-contract.md`).

## Override 1 — framework source

**The base skill's Step 1 says "ASK THE USER" when the framework is unclear.** In src-v2, read the framework, per-level command, file location, and mocking policy from `.ai-rules/project.md` §Test instead — never ask. If project.md was declined for this run, say explicitly that the framework is a guess before proceeding. See [project-md-schema.md](../../schemas/project-md-schema.md).

## Override 2 — output shape and level routing

In the v2 flow this skill produces `5-contract.md` per [contract-ids.md](../../schemas/contract-ids.md), not the v1 unit-test-only doc. When a clause's `Kind` is `side-effect` or a cross-boundary contract, generate the integration-level test directly — the level from the contract table picks the runner, folding in what v1 called `integration-test-generator` as a separate skill (see [that overlay's status note](../integration-test-generator/SKILL.md)). Every clause needs pasted red evidence, and every test cites its `C*` ID.

## Related

- [../../schemas/contract-ids.md](../../schemas/contract-ids.md)
- [../../agents/tdd-engineer.agent.md](../../agents/tdd-engineer.agent.md)
