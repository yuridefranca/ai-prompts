# Template: FINDINGS.md

**Slice**: 2 · **Schema**: [../schemas/findings.md](../schemas/findings.md)
**Written by**: any of the six adversarial passes (3.4, 6.0 stress test, 6.0 pre-mortem, 7, 8.1, 8.2/8.3). Append-only — see the schema for the one exception to the idempotent-overwrite rule.

````markdown
# Findings — {feature}

| ID | Severity | Found at | Summary | Status | Evidence |
|---|---|---|---|---|---|

## Robustness Statements

Passes that searched for problems and found none log a statement here instead
of a manufactured finding — see [no quotas](../schemas/findings.md#no-quotas).

### {phase} — {pass name}

No failure modes found. Searched: {list what was searched}. {why each is
covered, with a file:line or type-system reference}.
````

## Rules for whoever fills this in

1. Assign a **new** `F{n}` only for an issue not already in the table. If it's the same underlying issue a prior pass found, **update that row**, don't add a new one.
2. `Evidence` is never empty — file:line, test name, or a pasted log excerpt.
3. `accepted` status requires the one-line reason to live in the `Evidence` column, not just in chat.
4. A robustness statement is not optional filler — see [no quotas](../schemas/findings.md#no-quotas) for what makes one acceptable vs. vague.

## Related

- [../schemas/findings.md](../schemas/findings.md) — status enum, ledger rules, the robustness-statement replacement for finding quotas
- [index-template.md](index-template.md) — where `open` rows get mirrored
