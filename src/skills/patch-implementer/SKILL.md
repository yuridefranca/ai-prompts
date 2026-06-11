---
name: patch-implementer
description: >
    Implement minimal bug fixes after critique phase, addressing identified issues and edge cases.
    Follows TDD approach: create failing test then minimal fix, then refactor. Always use after
    solution-critic provides feedback. Integrates with engineer agents for implementation. Keywords:
    bug fix implementation, patch, minimal fix, TDD, failing test, edge case handling, critique
    feedback, engineer handoff.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Patch Implementer

Implement **minimal bug fix** that addresses critic feedback. TDD approach: failing test → minimal fix → refactor.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- Engineers agents don't create/modify files unless explicitly told to use `replace_string_in_file` or `create_file`
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

## Workflow Artifact

This skill is invoked as **Phase 6** of the Bug Workflow. It MUST produce an output file in the workflow folder.

**Output File**: `.ai-workflow/[feature-folder]/6-fix-implementation.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, `2-root-cause-analysis.md`, `3-solution-evaluation.md`, and `5-tdd-tests.md` before implementing the fix.

## Core Principle

**Minimal Fix First**: Implement simplest solution that fixes bug and handles critique concerns. Don't over-engineer.

## Process

See [references/implementation-patterns.md](references/implementation-patterns.md) for detailed patterns, templates, and code examples.

### Step 0: CRITICAL - Create/Modify Files

**⚠️ ENGINEER AGENTS MUST MODIFY ACTUAL FILES** - Do NOT just output code in chat.

When delegating to engineer agents:

- Explicitly instruct them to use `replace_string_in_file` or `create_file` tools
- Specify exact file paths where fixes should be applied
- Verify files are modified in the workspace after delegation

### Step 1: Review Critique Feedback

Analyze solution-critic findings and prioritize. See [references/implementation-patterns.md](references/implementation-patterns.md#implementation-checklist-template) for checklist format.

### Step 2: Create/Update Failing Tests

Invoke `test-generator` skill to create bug reproduction test, edge case tests, and regression tests. All tests should FAIL before fix.

### Step 3: Implement Minimal Fix

Delegate to engineer agent (backend-engineer or frontend-engineer) with explicit file modification instructions.

**Minimal fix criteria**:

- Fixes the reported bug
- Handles all edge cases from critique
- Addresses performance concerns
- Addresses security concerns
- Simplest solution that works

See [references/implementation-patterns.md](references/implementation-patterns.md#common-fix-patterns) for common patterns (input validation, error handling, race conditions, performance).

### Step 4: Verify Tests Pass

Run full test suite. All tests (new and existing) must pass.

### Step 5: Address Critique Concerns

Verify each concern from solution-critic is addressed:

- Performance: Benchmark if needed
- Security: Test attack vectors
- Edge cases: Verify all handled

### Step 6: Minimal Refactoring (If Needed)

If code is messy after fix, refactor while keeping tests green. Don't over-engineer.

### Step 7: Document the Fix

See [references/implementation-patterns.md](references/implementation-patterns.md#fix-documentation-template) for documentation template.

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

## Next Steps

1. Post-fix review (invoke `post-fix-reviewer` skill)
2. Code review (invoke `code-reviewer` skill)
```

## Reference Files

- [Implementation Patterns](references/implementation-patterns.md) - Checklist template, TDD pattern, fix documentation template, common fix patterns
