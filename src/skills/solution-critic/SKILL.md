---
name: solution-critic
description: >
    Adversarially stress-test proposed bug fixes before implementation. Finds failure modes,
    edge cases, performance issues, and security holes. MUST find at least 2 potential problems
    with any solution. Always use after root cause analysis and before implementing fix. Prevents
    premature solutions and incomplete fixes. Keywords: solution critique, adversarial review,
    failure mode analysis, stress testing, edge cases, security review, performance analysis,
    fix validation.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Solution Critic

**Adversarial stress-testing of proposed bug fixes**. Your job is to find what could go wrong.

## When to Use

- After root cause analysis complete
- Before implementing any fix
- Evaluating proposed solutions
- Critical/high-impact bugs
- Production incident fixes

## Workflow Artifact

This skill is invoked as **Phase 3** (Part B) of the Bug Workflow. It contributes to the solution evaluation document.

**Output File**: `.ai-workflow/[feature-folder]/3-solution-evaluation.md` (stress test section)

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, `1-component-map.md`, and `2-root-cause-analysis.md` before critiquing solutions.

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

## Minimum Requirements

**Must find at least**:

- 2 potential failure modes
- 1 edge case concern
- 1 performance or security consideration

**If can't find issues**: Document explicitly that thorough review found none, explain why solution is robust, still provide at least 2 "what if" scenarios.

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
