# Template: 8-qa-plan.md

**Slice**: 2
**Written by**: `qa-planner` (phase 8.1). See [../flows/feature-flow.md § Phase 8](../flows/feature-flow.md#phase-8--qa-three-sub-phases) for the planner's constraints (no selectors, no scenario-count quota).

````markdown
# QA Plan: {Feature Name}

## Manual Test Scenarios

### M1: {name} {✅ happy-path | ⚠️ hostile-user | ...} · covers {C*/AC*}
1. {step}
2. {step}
3. **Verify**: {expected outcome}

## Automated Test Scenarios (intent — 8.3 writes the code)

### A1: {name} {tag} · covers {C*, F*}
- **Precondition**: {state the scenario needs}
- **Steps**: {steps, prose is fine here — 8.3 turns this into a spec}
- **Assert**: {expected outcome}
- **Data**: {what fixtures/seed this needs}

## Coverage Summary

| Category | Manual | Automated | Total |
|---|---|---|---|
| Happy path | | | |
| Edge case | | | |
| Error case | | | |
| Adversarial | | | |
| Hostile user | | | |
| **Total** | | | |

## Open 🔴 Findings Coverage

| Open 🔴 finding | Covered by |
|---|---|
````

## Rules

1. **No selectors, anywhere in this file.** The planner has read the PRD and contract, never the rendered DOM — a locator invented here will not match the implementation. Steps are described in plain terms ("click Confirm"); 8.3 turns them into real Playwright specs with real locators, from `.ai-rules/project.md` §Browser's selector convention.
2. **No minimum scenario count.** Coverage is driven by what the flow actually found: every open 🔴 finding needs a scenario in the coverage table above; if the flow found nothing adversarial, the Adversarial/Hostile-user rows are legitimately zero and the plan says so in one line rather than padding scenarios to hit a quota. See [findings.md § No quotas](../schemas/findings.md#no-quotas).
3. **Non-user-facing features** replace "Manual" with API calls / CLI invocations / DB queries, "Automated" with the repo's integration runner, and drop the Hostile-user row entirely.
4. **Debug flow**: `M1` is always the original repro scenario — see [../flows/debug-flow.md](../flows/debug-flow.md).

## Related

- [../flows/feature-flow.md § Phase 8](../flows/feature-flow.md#phase-8--qa-three-sub-phases) — full phase contract, environment-contract table for 8.3
- [../schemas/findings.md](../schemas/findings.md) — the ledger this plan's coverage table is checked against
