# Template: .ai-rules/review.md

**Slice**: 2
**Nature**: normative — "what must this repo's code look like?" (contrast with `.ai-rules/project.md`, descriptive — see [project-md-schema.md](../schemas/project-md-schema.md))
**Written by**: the dev, seeded from real review feedback; grown by the phase 9.5 harvest ([Keeping It Accurate](../PLAN.md#keeping-it-accurate)). Read by phase 7 (`reviewer`).

````markdown
# Review Rules — {Project Name}

## Required Utilities
- Use `{util}()` from `{path}` for {purpose} — never {the thing this replaces}   triggered: 0

## Required Components
- {UI need} → `{Component}` from `{path}` — no {hand-rolled alternative}   triggered: 0

## Banned Patterns
- Never {pattern} — use {alternative} instead   triggered: 0

## Architecture Constraints
- {layer} must not import from {layer} — dependency direction: {A → B → C}   triggered: 0

## Business Invariants
- {domain rule that must always hold, stated so a reviewer can check it mechanically}   triggered: 0
````

## Filling this in

- **Every rule carries a `triggered:` count**, starting at 0. The phase 7 `reviewer` increments it whenever the rule actually catches a real violation — this is the mechanism, not a date field, that keeps the file honest. See [Keeping It Accurate](../PLAN.md#keeping-it-accurate).
- **A rule at `triggered: 0` after 10 flows is proposed for deletion** at the next 9.5 harvest — either it's obsolete or unenforceable as written. Deletion is proposed as a diff for the dev to approve, never automatic.
- New rules are proposed the same way, in reverse: a phase 7 finding that violates a pattern **not yet in this file** is the evidence for adding one (harvest-driven growth).
- If the file doesn't exist at all, phase 7 notes "no project-specific rules found" and proceeds with general code-quality rules only — this is not a hard failure, see [How It Plugs In](../PLAN.md#how-it-plugs-in).

## Related

- [../schemas/project-md-schema.md](../schemas/project-md-schema.md) — the descriptive sibling of this file
- [../PLAN.md § Repository-Specific Review Rules](../PLAN.md#repository-specific-review-rules) — narrative source and a fuller worked example
- [../PLAN.md § Business Logic Awareness in Review](../PLAN.md#business-logic-awareness-in-review) — how phase 7 combines this file with the PRD/contract/ADR
