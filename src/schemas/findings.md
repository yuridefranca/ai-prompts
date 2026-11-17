# Schema: FINDINGS.md — The Finding Ledger

**Slice**: 0 (Foundations)
**Used by**: the six adversarial passes (3.4 tradeoff digest, 6.0 stress test, 6.0 pre-mortem, 7 code critique, 8.1 adversarial QA plan, 8.2/8.3 hostile-user QA); phase 9 gate; phase 9.5 harvest

## Purpose

Six separate passes look for problems across a flow. Without one shared ledger they re-report the same issue and the dev triages it three times. `FINDINGS.md` is the single append-only file every pass writes to; nothing else does.

## Table schema

````markdown
| ID | Severity | Found at | Summary | Status | Evidence |
|---|---|---|---|---|---|
| F1 | 🔴 | 6.0 stress test | Double-submit creates duplicate wallets | closed @ T3 | wallet.spec.ts:44 |
| F2 | 🔵 | 6.0 pre-mortem | No alert on ledger timeout spike | accepted | out of scope, tracked in OPS-221 |
| F3 | 🔴 | 7 critic | Event emitted outside transaction | open | wallet-service.ts:91 |
````

| Column | Contents |
|---|---|
| `ID` | `F` + sequential integer, assigned once per issue, never reused |
| `Severity` | 🔴 (high) or 🔵 (low) — see [Visual Grammar](../PLAN.md#visual-grammar-consistent-across-all-artifacts) |
| `Found at` | phase/pass that first logged it (e.g. `6.0 stress test`, `7 critic`, `8.1 QA plan`) |
| `Summary` | one line, specific enough to grep for |
| `Status` | see enum below |
| `Evidence` | file:line, test name, or log excerpt — never "trust me" |

## Status enum

| Status | Meaning |
|---|---|
| `open` | Not yet addressed. Blocks phase 9 if 🔴. |
| `closed @ T{n}` | Fixed; `{n}` is the task number (from `6-solution.md`) that fixed it |
| `accepted` | Won't fix, with a mandatory one-line reason in the `Evidence` column |
| `superseded by F{n}` | Merged into a later, more precise finding — kept for audit trail, not deleted |

## Rules

1. **A later pass that finds an already-logged issue updates the existing row** — it never creates a new ID for the same underlying issue. The reporting pass's Layer 1 shows a *delta* (`2 closed · 1 still open · 1 new`), never a re-listing of everything it checked.
2. **Only 🔴 findings block phase 9.** A 🔵 finding needs an `accepted` status with a reason to pass the gate — it does not need to be fixed.
3. **The orchestrator surfaces every `open` finding in every Layer 1** shown to the dev from the point it's opened onward, so nothing silently ages out of view.
4. **`FINDINGS.md` is the only append-only artifact in the flow.** Every other artifact is overwritten wholesale on re-run (see [index-frontmatter.md](index-frontmatter.md#idempotency-rule)); this one only ever grows or has rows updated in place.
5. A loop-back that is the **third** attempt to close the same finding is an escalation, not another silent retry: `"F3 has failed three fix attempts — this looks like a design problem, recommend returning to 3.4."` (see [Failure Edges](../PLAN.md#failure-edges)).

## No quotas

Mandatory finding counts (e.g. "must find ≥2 failure modes", "needs ≥5 scenarios incl. ≥2 adversarial") are **not used**. They manufacture findings on clean work by the same mechanism that makes coverage-% targets produce assertion-free tests.

**Replacement — the robustness statement.** Each adversarial pass either logs findings to this ledger, or writes an explicit statement of what it searched and why nothing was found:

````
No failure modes found. Searched: concurrency on the create path, partial
failure between wallet write and event emit, currency validation bypass.
The transaction boundary at wallet-service.ts:88 covers the first two;
the third is enforced by the enum type.
````

An empty statement is exactly as visible to the orchestrator as an empty findings table — and a vague one ("looks fine") is itself a quality signal the orchestrator can challenge and re-request.

## Related

- [artifact-status.md](artifact-status.md) — `FINDINGS.md` does **not** use the per-artifact draft/complete header; it is append-only and has no single "phase" that owns it
- [index-frontmatter.md](index-frontmatter.md) — `open_findings` mirrors this ledger's `open` rows
- [Adversarial Passes & the Finding Ledger](../PLAN.md#adversarial-passes--the-finding-ledger) — narrative source
