# Schema: Contract IDs & Test Levels

**Slice**: 0 (Foundations)
**Used by**: phase 5 (`tdd-engineer`), phase 6.1..n (`implementer`), phase 6.x (contract diff), phase 7 (`reviewer`), phase 8.1 (`qa-planner`)

## Purpose

This is what makes the phase 6.x contract diff **mechanical rather than inferential** — a grep, not a judgment call. Every behavior the feature must exhibit gets a stable, citable ID at phase 5, and every test that asserts it must cite that ID back.

## Clause table schema (`5-contract.md`)

````markdown
| ID | Clause | Kind | Level | Test intent | Red evidence |
|---|---|---|---|---|---|
| C1 | `createWallet(userId, "USD")` returns a Wallet with balance 0.00 | happy | unit | `src/wallet/wallet.spec.ts` · "creates with zero balance" · call with a fresh user · `balance` is `0.00` | `AssertionError: expected undefined to be 0.00` |
| C2 | Duplicate currency for same user → 409, no wallet created | error | integration | `test/integration/wallet.int.spec.ts` · seed a USD wallet · POST another USD · 409 and wallet count still 1 | `Expected 409, got 500` |
| C3 | Wallet mutation emits `WalletUpdated` within the same transaction | side-effect | integration | same file · capture events · update a wallet · exactly one `WalletUpdated`, inside the txn | `0 events captured, expected 1` |
| C4 | Upstream ledger timeout (>5s) → 503, wallet not persisted | error | integration | same file · ledger stub delays 6s · POST · 503 and no row | `Timeout stub not wired — TypeError` |
| C5 | User sees the new wallet in the list without refreshing | happy | e2e | `e2e/wallet.spec.ts` · create via the form · `[data-testid=wallet-row]` appears | `locator not found: [data-testid=wallet-row]` |
````

| Column | Contents |
|---|---|
| `ID` | `C` + sequential integer, assigned once per behavior, stable for the life of the feature — future changes add new IDs, they don't renumber |
| `Clause` | one sentence, specific enough that a test can assert it directly |
| `Kind` | `happy` \| `error` \| `side-effect` \| cross-boundary contract \| user-visible flow — drives the default `Level` below |
| `Level` | `unit` \| `integration` \| `e2e` — see the default table |
| `Test intent` | file path, test name, setup, action, and assertion — exact enough that `test-writer` (tier B) writes the test without deciding anything |
| `Red evidence` | the **actual pasted failure output** from running the test before implementation exists — `pending` until `test-writer` runs it |

## Clause kind → default level

| Clause kind | Default level | Why |
|---|---|---|
| Pure logic, calculation, validation | unit | No I/O to get wrong |
| Error mapping | unit | |
| Side effect (event emitted, row written, cache invalidated) | **integration** | Mocking the effect means testing the mock |
| Cross-boundary contract (status code, response shape, wire format) | integration (API) | |
| User-visible flow | e2e | |

The `tdd-engineer` may override a default, but must say why in one line on the clause. A level the target repo has no runner for (per `.ai-rules/project.md` §Test) is **downgraded with a note**, never silently dropped — see [project-md-schema.md](project-md-schema.md).

## Red evidence — mandatory

`test-writer` runs the suite and pastes the *actual* failure output per clause, not a description of what it expects to fail. **A clause with no red evidence means phase 5 did not complete.** This is the single most common LLM-TDD failure mode: writing a test that already passes, or a tautology, and never noticing because nobody ran it. See assertion 7a in [Verification](../PLAN.md#dry-run-slice-8--with-a-baseline).

## Preserve clauses (improvement flow)

The [improvement flow](../flows/improvement-flow.md#phase-5--preserve-clauses) adds a clause kind for behavior that must **survive** the change:

| Kind | Default level | Evidence column |
|---|---|---|
| `preserve` | the level the current behavior is observable at — usually integration | pasted **green** output from the current code, before any change |

A preserve clause is a characterization test: it passes before implementation and must still pass after. One that fails before implementation means the characterization is wrong — fix the test or raise it at the gate, never change the code to match. The 6.x contract diff treats preserve clauses exactly like the others (citation, assertion count, level match).

## Test citation convention

Every test must cite the clause it asserts, in the test name or a leading comment:

```ts
// C2
it('rejects duplicate currency with 409', async () => { ... });
```

## The contract diff (phase 6.x, mechanical)

At reconciliation the `implementer` runs `$AI_PROMPTS/src/scripts/contract_diff.py .ai-workflow/[feature]` — no model does this by reading files. For each `C*` ID it finds the citing tests and reports three things — citation, assertion count, and level match — and exits non-zero if any clause isn't covered:

```
C1 ✅ wallet.spec.ts:12        · 2 assertions · unit ✅
C2 ✅ wallet.int.spec.ts:40    · 3 assertions · integration ✅
C3 ⚠️ wallet.spec.ts:88        · 1 assertion  · unit ❌ (declared integration)
C4 ❌ no citing test
C5 ⚠️ e2e/wallet.spec.ts:9     · 0 assertions · e2e ❌ empty test body
```

- **Assertion count is what makes the citation meaningful.** A test tagged `// C4` whose body is `expect(true).toBe(true)` passes a naive grep; zero assertions in the citing block counts as **uncited**. Same failure mode coverage-% targets produce, caught mechanically here.
- **Level match** compares the citing test's path against `.ai-rules/project.md`'s per-level `location` globs (§Test). A side-effect clause "covered" by a unit test with a mocked emitter is a **finding**, not a pass — log it to `FINDINGS.md`.
- An uncited clause (`❌`) opens a new task at 6.1 (`T{n+1}: cover C4`) rather than silently amending the contract — see [Failure Edges](../PLAN.md#failure-edges).

## Related

- [project-md-schema.md](project-md-schema.md) — where per-level command/location/mocking policy come from
- [findings.md](findings.md) — where a level-mismatch or uncited clause gets logged
- [Phase 5 — TDD](../PLAN.md#phase-5--tdd) — narrative source
