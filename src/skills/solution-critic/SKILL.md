---
name: solution-critic
description: >
    Adversarially stress-test a proposed solution or fix before implementation, and re-attack
    open findings against shipped code. Finds failure modes, edge cases, performance issues, and
    security holes, and records them in FINDINGS.md — or states why the solution is robust. Use at
    phase 6.0 (solution plan) and phase 7 (review). Prevents premature solutions and incomplete fixes. Keywords: solution critique, adversarial review,
    failure mode analysis, stress testing, edge cases, security review, performance analysis,
    fix validation.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Solution Critic

**Adversarial stress-testing of proposed solutions and fixes**. Your job is to find what could go wrong.

## When to Use

- Phase 6.0: before any code is written
- Phase 7: against the real, shipped code
- Critical/high-impact bugs and production incident fixes

## Parameters

Read `{{phase}}`, `{{output}}`, and `{{findings}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Two distinct invocations:

- **Phase 6.0** ([`plan-critic`](../../agents/plan-critic.agent.md), on a different vendor than the planner): stress test and pre-mortem of `6-solution.md` before any code is written.
- **Phase 7** ([`reviewer`](../../agents/reviewer.agent.md), solution-critic mode): re-attacks findings still `open` since 6.0 against the real, shipped code.

Every invocation writes to `{{findings}}` (`FINDINGS.md`) with a stable `F*` ID, or a robustness statement if nothing was found — see [findings.md § No quotas](../../schemas/findings.md#no-quotas).

## Core Principle

**Assume the Fix Will Fail**: Actively search for ways the proposed solution breaks. Better to find problems now than in production.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- "Fix works for happy path" doesn't mean it handles edge cases - always test boundary conditions
- Performance fix without benchmark is just hope - measure before claiming improvement
- Security fix that blocks one attack vector may open another - think like an attacker
- Fixing symptoms instead of root cause means the bug will resurface differently
- "No side effects" assumption is dangerous - check all consumers of changed code
- Concurrent access patterns often missed in review - think about race conditions
- Error handling that catches and ignores is worse than no error handling
- Adding a lock fixes race conditions but can introduce deadlocks
- Caching fix may cause stale data issues - consider cache invalidation
- Input validation on frontend only is not validation - backend must validate too
- Fix that works for single user may fail under concurrent load
- Minimum 2 failure modes required - if you can't find them, you're not looking hard enough

## Process

See [references/critique-templates.md](references/critique-templates.md) for all detailed templates and output format.

### Step 1: Understand the Proposed Solution

Analyze fix proposal: what it changes, approach, assumptions, scope. See [references/critique-templates.md](references/critique-templates.md#proposed-solution-summary-template) for template.

### Step 2: Find Failure Modes

Systematically search for how the fix could fail. See [references/critique-templates.md](references/critique-templates.md#failure-mode-categories) for complete categories.

**Categories**: Data failures, Timing failures, State failures, Integration failures, Scale failures

### Step 3: Check Edge Cases

Identify boundary conditions and unusual scenarios the fix doesn't handle. See [references/critique-templates.md](references/critique-templates.md#edge-case-template) for template.

### Step 4: Analyze Performance Impact

Assess if fix introduces performance problems (N+1 queries, memory leaks, slow operations). See [references/critique-templates.md](references/critique-templates.md#performance-concern-template) for template.

### Step 5: Security Review

Check for vulnerabilities the fix might introduce or not address. See [references/critique-templates.md](references/critique-templates.md#security-concern-template) for template.

### Step 6: Check Side Effects

What else might break? Other features, API contracts, database schema, monitoring. See [references/critique-templates.md](references/critique-templates.md#side-effects-template) for template.

### Step 7: Validate Against Root Cause

Does fix address the actual root cause, or just hide symptoms? See [references/critique-templates.md](references/critique-templates.md#root-cause-alignment-template) for template.

### Step 8: Propose Improvements

For each issue found, suggest how to prevent it, what to add/change, or alternative approaches.

## No quotas

There is **no minimum number of findings**. A quota pushes the critic to manufacture weak findings that bury the real ones.

**Cover every step above.** For each step that turns up nothing, say what you checked. If the whole review finds nothing, write a **robustness statement** instead: what you attacked, and why the solution holds. See [findings.md § No quotas](../../schemas/findings.md#no-quotas).

## Mindset

**Be adversarial, not destructive**:

- Goal: Make fix better, not block progress
- Frame issues constructively
- Suggest mitigations
- Prioritize findings

**Think like an attacker/tester**:

- How would I break this?
- What did developer assume?
- Where are the weak points?

## Output Format

See [references/critique-templates.md](references/critique-templates.md#full-output-format-template) for complete template.

**Structure**:

```markdown
# Solution Critique: [Issue]

## Proposed Solution Summary

[Brief description]

## Critical Findings

### 🛑 BLOCKING ISSUES (Must fix before implementation)

### ⚠️ HIGH PRIORITY (Should fix)

## Detailed Analysis

[Failure modes, edge cases, performance, security, side effects, root cause alignment]

## Recommended Improvements

[Must have, should have, nice to have]

## Critique Summary

**Verdict**: ✅ APPROVED / ⚠️ APPROVED WITH CHANGES / 🛑 NEEDS REVISION
**Confidence**: [X]%
```

## Reference Files

- [Critique Templates](references/critique-templates.md) - All failure mode categories, templates, and full output format
