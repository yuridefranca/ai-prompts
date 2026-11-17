---
name: patch-implementer
description: >
    Implement a minimal bug fix for one debug-flow task, addressing the root cause and every open
    finding from the phase 6.0 stress test. Turns the phase 5 failing tests (C1 is always the repro)
    green with the simplest fix that handles all edge cases. Use in the debug flow's task loop
    (phases 6.1..n). Keywords: bug fix implementation, patch, minimal fix, TDD, failing test, edge
    case handling, critique feedback, root cause.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Patch Implementer

Implement a **minimal bug fix** that addresses the root cause and the open findings. TDD approach: failing test (already written at phase 5) → minimal fix → refactor.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- Code that only exists in chat is not a fix — edit the real files
- "Minimal fix" doesn't mean incomplete - must handle all edge cases from critique
- Tests passing locally doesn't mean they run in CI - check test setup in CI config
- Fixing the reported bug without handling edge cases leads to new bug reports
- Implementing fix before writing failing test makes TDD impossible
- Modifying production code to make test pass (instead of minimal fix) is cheating
- "Works on my machine" without testing environment parity is not a fix
- Forgetting to remove debug logs/console statements before commit
- Performance fix without benchmark is just hope - measure before/after
- Security fix without exploit attempt is incomplete - actually try to exploit it
- Deferring low-priority edge cases leads to multiple bug reports for same root issue
- Over-engineering minimal fix adds complexity and new bugs

## When to Use

- After solution critic completed review
- After addressing blocking issues
- Ready to implement bug fix
- Have tests demonstrating bug

## Parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Backs [`implementer`](../../agents/implementer.agent.md) task mode at phases 6.1..n in the **debug flow** — one fix task per spawn. Reads `2.5-root-cause.md`, the `5-contract.md` clauses named for this task (`C1` is always the repro), `6-solution.md` §T{n}, and open findings in `FINDINGS.md` (the 6.0 stress test's findings are the "critique" this skill addresses). Writes code plus an append to `6-solution.md` §T{n}.

## Core Principle

**Minimal Fix First**: Implement simplest solution that fixes bug and handles critique concerns. Don't over-engineer.

## Process

See [references/implementation-patterns.md](references/implementation-patterns.md) for detailed patterns, templates, and code examples.

### Step 0: CRITICAL - Modify the Actual Files

**⚠️ EDIT REAL FILES** - Do NOT just output code in chat. Touch only the files in this task's scope (`6-solution.md` §T{n}), and verify the changes are in the workspace.

### Step 1: Review Critique Feedback

Read the open findings in `FINDINGS.md` (from the 6.0 stress test) that this task must address, and prioritize them. See [references/implementation-patterns.md](references/implementation-patterns.md#implementation-checklist-template) for checklist format.

### Step 2: Confirm the Failing Tests

The repro test (`C1`) and the other contract tests already exist from phase 5 and must still FAIL. Add **one regression test per bug class** this task touches, not just the specific bug instance — citing the clause it covers.

### Step 3: Implement Minimal Fix

**Minimal fix criteria**:

- Fixes the reported bug
- Handles all edge cases from the open findings
- Addresses performance concerns
- Addresses security concerns
- Simplest solution that works

See [references/implementation-patterns.md](references/implementation-patterns.md#common-fix-patterns) for common patterns (input validation, error handling, race conditions, performance).

### Step 4: Verify Tests Pass

Run full test suite. All tests (new and existing) must pass.

### Step 5: Address the Open Findings

Verify each open finding this task owns is addressed, and say so in your return summary:

- Performance: Benchmark if needed
- Security: Test attack vectors
- Edge cases: Verify all handled

### Step 6: Refactor (If Needed)

If code is messy after the fix, apply `refactor-optimizer` within this task's scope, keeping tests green. Don't over-engineer.

### Step 7: Document the Fix

Append to `6-solution.md` §T{n}. See [references/implementation-patterns.md](references/implementation-patterns.md#fix-documentation-template) for the template.

## Output Format

See [references/implementation-patterns.md](references/implementation-patterns.md#fix-documentation-template) for complete template.

**Implementation report structure**:

```markdown
# Fix Implementation: [Issue]

## Fix Summary

[Bug, root cause, solution]

## Changes Made

[Files modified, critique concerns addressed]

## Test Evidence

[Before/after test results]

## Verification

[Checklist of what was verified]

## Deviations from Plan

[Plan said → actually did]
```

## Reference Files

- [Implementation Patterns](references/implementation-patterns.md) - Checklist template, TDD pattern, fix documentation template, common fix patterns
