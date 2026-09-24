---
name: solution-critic
description: src-v2 overlay for the v1 solution-critic skill — the stress-test half of phase 6.0 and the re-attack pass in phase 7, writing to FINDINGS.md instead of a fixed quota. Keywords solution critic, stress test, phase 6.0, phase 7, findings ledger.
---

# solution-critic (src-v2 overlay)

**Base skill**: [../../../src/skills/solution-critic/SKILL.md](../../../src/skills/solution-critic/SKILL.md) — read that file for the full adversarial-critique process. This file does not duplicate or modify it; the v1 file is untouched.

## v2 parameters

Read `{{phase}}`, `{{output}}`, and `{{findings}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs in src-v2

Two distinct invocations:

- **Phase 6.0** (`solution-planner`): the stress-test half of the solution plan, attacking `6-solution.md` before any code is written.
- **Phase 7** (`reviewer`, solution-critic mode): re-attacks findings still `open` since 6.0 against the real, shipped code.

Every invocation writes to `{{findings}}` (`FINDINGS.md`) with a stable `F*` ID, or a robustness statement if nothing was found — see [findings.md § No quotas](../../schemas/findings.md#no-quotas).

**Drop the base skill's "must find ≥2 failure modes" requirement in src-v2.** That quota is v1-only and is exactly the anti-pattern the robustness statement replaces.

## Related

- [../../schemas/findings.md](../../schemas/findings.md) — the ledger this overlay writes to
- [../../agents/solution-planner.agent.md](../../agents/solution-planner.agent.md), [../../agents/reviewer.agent.md](../../agents/reviewer.agent.md)
