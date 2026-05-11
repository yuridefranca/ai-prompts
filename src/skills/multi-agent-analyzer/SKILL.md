---
name: multi-agent-analyzer
description: Orchestrate parallel code analysis from multiple perspectives (quality, edge cases, regression, performance) to validate implementation before testing. Use after implementation to catch issues that a single review angle would miss. Keywords parallel analysis, multi-agent, code validation, robustness check, implementation review.
---

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Bug Workflow Phase 6.1**: Produces `.ai-workflow/[feature-folder]/6.1-parallel-analysis.md`
- **Improvement Workflow Phase 5.1**: Produces `.ai-workflow/[feature-folder]/5.1-parallel-analysis.md`
- **Feature Workflow Phase 5.1**: Produces `.ai-workflow/[feature-folder]/5.1-parallel-analysis.md`

**Context**: Read the implementation file from the prior phase and the solution evaluation / design document before running analysis.

---

# Multi-Agent Parallel Analyzer

Run **3 parallel subagents** against the implementation to catch issues that a single review perspective would miss. Each subagent runs independently and simultaneously, then results are synthesized into a unified report.

This is NOT testing — it's static code analysis from different angles.

## When to Use

After implementation (bug fix, improvement, or feature), before moving to testing phases. This catches issues early when they're cheapest to fix.

## Process

### Step 1: Prepare Analysis Context

Read the following files to build context:

- The implementation output from the prior phase
- The solution evaluation or design document
- The root cause analysis (bug workflow only)

Build a **shared context package** that will be passed to all 3 subagents:

```
Context Package:
- Changed files: [list of files modified]
- What was implemented: [1-2 sentence summary]
- Design/solution approach: [from prior phase document]
- Root cause (bug only): [from Phase 2]
- Key constraints: [from startpoint]
```

### Step 2: Launch 3 Parallel Subagents

Use `runSubagent` to launch all 3 lanes **simultaneously**. Each subagent is an independent analysis that returns its findings.

**⚠️ CRITICAL**: Launch all 3 subagents in parallel (not sequentially). This is the core value of this skill — independent perspectives running at the same time.

---

#### Subagent 1: Code Quality & Maintainability

**Prompt for `runSubagent`**:

```
You are a Code Quality Analyst. Analyze the following implementation for code quality and maintainability issues.

Context:
[Shared context package]

Changed files to analyze:
[List of file paths — the subagent should read these files]

Analyze these specific aspects:
- **Readability**: Can a new team member understand this code in 5 minutes?
- **Naming**: Do variable/function names reveal intent?
- **Complexity**: Are functions too long? Too nested? Cyclomatic complexity?
- **DRY violations**: Is logic duplicated that should be extracted?
- **SOLID violations**: Does code have mixed responsibilities?
- **Dead code**: Are there unused imports, variables, or unreachable paths?
- **Error handling**: Are errors caught and handled properly? Silent catches?
- **Type safety**: Are there `any` types, missing null checks, or unsafe casts?

Return your analysis in this exact format:

### Lane 1: Code Quality & Maintainability

**Overall Grade**: [A/B/C/D/F]

| Issue | Severity | Location | Suggestion |
|-------|----------|----------|------------|
| [Description] | Critical/Major/Minor | [File:Line] | [How to fix] |

**Strengths**: [What's done well]
**Top Priority Fix**: [Most important issue to address]
```

---

#### Subagent 2: Edge Cases & Robustness

**Prompt for `runSubagent`**:

```
You are an Edge Case Analyst. Analyze the following implementation for robustness issues and edge cases that could cause failures in production.

Context:
[Shared context package]

Changed files to analyze:
[List of file paths — the subagent should read these files]

Analyze these specific aspects:
- **Null/undefined inputs**: What if required data is missing?
- **Empty collections**: What if arrays/maps are empty?
- **Boundary values**: What happens at min/max/zero/negative?
- **Concurrent access**: Race conditions? Shared mutable state?
- **Large inputs**: What if data volumes are 10x expected?
- **Invalid formats**: What if input doesn't match expected schema?
- **Partial failures**: What if one step in a multi-step process fails?
- **Idempotency**: Can this be safely retried? What happens on duplicate calls?
- **Time zones / locales**: Date/time handling correct across zones?
- **Character encoding**: Unicode, special characters handled?

Return your analysis in this exact format:

### Lane 2: Edge Cases & Robustness

**Overall Grade**: [A/B/C/D/F]

| Edge Case | Likelihood | Impact | Current Behavior | Expected Behavior |
|-----------|------------|--------|------------------|-------------------|
| [Description] | High/Med/Low | Critical/Major/Minor | [What happens now] | [What should happen] |

**Most Dangerous Edge Case**: [The one most likely to hit production]
**Easiest Win**: [Simplest fix with highest impact]
```

---

#### Subagent 3: Regression & Performance

**Prompt for `runSubagent`**:

```
You are a Regression & Performance Analyst. Analyze the following implementation for regression risks and performance concerns.

Context:
[Shared context package]

Changed files to analyze:
[List of file paths — the subagent should read these files]

Analyze these specific aspects:
- **API contract changes**: Are existing endpoints/interfaces modified?
- **Data format changes**: Are existing data structures altered?
- **Behavior changes**: Does existing functionality work differently?
- **Consumer impact**: Which callers/consumers are affected?
- **Database queries**: New queries? N+1? Missing indexes?
- **Memory usage**: New allocations? Potential leaks? Large object retention?
- **CPU usage**: Expensive loops? Recursive calls? Unnecessary computations?
- **Network calls**: Additional API calls? Larger payloads? Missing caching?
- **Startup time**: New initialization? Heavy imports?
- **Bundle size** (frontend): New dependencies? Tree-shaking issues?

Return your analysis in this exact format:

### Lane 3: Regression & Performance

**Overall Grade**: [A/B/C/D/F]

**Regression Risks**:

| Change | Affected Consumers | Risk Level | Mitigation |
|--------|-------------------|------------|------------|
| [What changed] | [Who depends on it] | High/Med/Low | [How to prevent breakage] |

**Performance Assessment**:

| Area | Before | After | Impact | Concern? |
|------|--------|-------|--------|----------|
| [Metric] | [Baseline] | [Estimated] | [Delta] | Yes/No |

**Critical Regression Risk**: [Most likely thing to break in production]
**Performance Bottleneck**: [Biggest performance concern, if any]
```

---

### Step 3: Synthesize Findings

Once all 3 subagents return their results, combine them into a unified report:

```markdown
# Parallel Analysis Report: [Feature/Bug Name]

**Date**: [Current date]
**Implementation Phase**: [Which phase produced the code]
**Analysis Method**: 3 parallel subagents

## Summary

| Lane              | Grade | Critical | Major | Minor |
| ----------------- | ----- | -------- | ----- | ----- |
| Code Quality      | [X]   | [N]      | [N]   | [N]   |
| Edge Cases        | [X]   | [N]      | [N]   | [N]   |
| Regression & Perf | [X]   | [N]      | [N]   | [N]   |

## Critical Issues (MUST fix before proceeding)

1. **[Lane N]**: [Issue description]
    - **Why critical**: [Impact if not fixed]
    - **Fix**: [How to address]

## Major Issues (SHOULD fix)

1. **[Lane N]**: [Issue description]
    - **Fix**: [How to address]

## Minor Issues (NICE to fix)

1. **[Lane N]**: [Issue description]

## Cross-Lane Patterns

[Note any issues that appeared in multiple lanes — these are highest priority]

## Recommended Next Steps

1. [Fix critical issues]
2. [Fix major issues if time permits]
3. [Proceed to testing phase]

## Confidence Assessment

**Implementation Confidence**: [High/Medium/Low]
**Regression Risk**: [High/Medium/Low]
**Ready for Testing**: [Yes/No - with conditions]
```

### Step 4: Fix Critical Issues

If any critical issues are found:

1. Fix them immediately
2. Re-run the affected subagent lane(s)
3. Update the report

If no critical issues: proceed to the next workflow phase.

## Important Rules

- **Use `runSubagent` for true parallelism**: All 3 lanes must run simultaneously, not sequentially. This is the core value of this skill.
- **Each subagent is independent**: Subagents don't share state. Pass all needed context in the prompt.
- **This is NOT testing**: No test execution. This is static code analysis from multiple perspectives.
- **Be specific**: Every issue must have a file location and suggestion.
- **Be honest about grades**: Don't inflate grades. A "C" with honest fixes is better than an "A" with hidden issues.
- **Prioritize ruthlessly**: Not all issues are equal. Critical = blocks progress. Major = should fix. Minor = nice to have.
- **Don't repeat the code review**: This focuses on quality, edge cases, and regression. The dedicated code-reviewer skill handles security, architecture, and final quality later.
- **Cross-lane patterns are gold**: If the same issue appears in multiple lanes, it's almost certainly a real problem. Highlight these in the synthesis.
