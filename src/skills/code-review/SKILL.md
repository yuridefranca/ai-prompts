---
name: code-review
description: >
    Comprehensive code quality review covering security, performance, maintainability,
    anti-patterns, and regression risks. Backs the reviewer subagent at phase 7 of every flow,
    before QA and the PR. Checks SOLID principles, best practices, test coverage, documentation,
    and prevents technical debt. Dispatches parallel review agents for security, performance,
    code quality, business logic, and testing. Keywords: code review, quality assurance,
    security review, performance review, maintainability, SOLID principles, anti-patterns,
    best practices, regression prevention, phase 7, business logic review, review rules.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Code Review

**Comprehensive code quality review** before merging. Final guardian against technical debt, security issues, and poor practices.

## When to Use

- Phase 7 of every flow (feature, debug, improvement, greenfield)
- Pull request review
- Critical/high-impact changes

## Parameters

Read `{{phase}}`, `{{output}}`, and `{{findings}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Two spawns:

- **Phase 7.0**, [`rules-checker`](../../agents/rules-checker.agent.md) (B): only the rules-compliance part — every rule in `.ai-rules/review.md`, writing `7.0-rules.md`.
- **Phase 7**, code-review mode of the [`reviewer`](../../agents/reviewer.agent.md) (S): everything else, taking the rules row from `7.0-rules.md`. Besides the diff, read:

- `.ai-rules/review.md` — project-specific rules. Absent is not a failure: note "no project-specific rules found" and proceed.
- `2-prd.md`, `3.4-tradeoffs.md`, `5-contract.md`, `6-solution.md` — for the Business Logic Review table, which checks every `AC*` ID individually. See [PLAN.md § Business Logic Awareness in Review](../../PLAN.md#business-logic-awareness-in-review).

Every finding goes to `{{findings}}` (`FINDINGS.md`) with a stable `F*` ID. A finding that already exists is **updated**, never re-reported — see [findings.md](../../schemas/findings.md).

## Core Principle

**Prevent Future Problems**: Catch issues now that would cause pain later. Balance thoroughness with pragmatism.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- TypeScript `any` is often hidden in library types - check return types carefully
- `Promise.all()` fails fast - one rejection kills all, use `Promise.allSettled()` for better error handling
- Database transactions in NestJS require explicit `@Transaction()` decorator or manual `queryRunner`
- React `useEffect` cleanup functions must be idempotent - they run on unmount AND before re-run
- JWT tokens without expiry checks are security vulnerabilities even if backend validates
- Soft-deleted records need `WHERE deleted_at IS NULL` in ALL queries or joins return wrong counts
- Frontend validation is UX, backend validation is security - ALWAYS validate on both
- Test mocks that return `Promise.resolve(mockData)` don't test error paths
- Performance issues from N+1 queries are invisible in tests with small datasets
- GraphQL resolvers without `@Authorized()` are publicly accessible even if other resolvers are protected
- HTTP 4xx errors should NOT be logged as errors - they're expected client mistakes
- Async functions without `await` or error handling silently fail

## Tech Stack Detection

Before reviewing, detect the tech stack to load appropriate rules.

See [references/tech-stack-detection.md](references/tech-stack-detection.md) for complete detection patterns and loading strategy.

**Quick Detection:**

1. Check `package.json` dependencies
2. Look for framework-specific files/directories
3. Examine imports and decorators in changed files

**Always Load** (universal):

- [Programming Principles](references/rules-programming-principles.md)
- [Design Patterns](references/rules-design-patterns.md)
- [Security](references/rules-security.md)
- [Performance](references/rules-performance.md)
- [Testing](references/rules-testing.md)
- [Readability](references/rules-readability.md)
- [Data Integrity](references/rules-data-integrity.md)
- [Business Logic](references/rules-business-logic.md)

**Load when detected:**

- **NestJS**: [NestJS Rules](references/rules-backend-nestjs.md)
- **Backend/API**: [Backend Rules](references/rules-backend.md) + [API Design](references/rules-api-design.md)

## Review Process

See [references/review-process.md](references/review-process.md) for the complete detailed process.

### High-Level Overview

**Step 0: Detect Tech Stack & Load Rules**

- Scan package.json, file paths, imports
- Load universal rules + framework-specific rules
- Document what was detected

**Step 1: Dispatch Parallel Review Agents**

- Create specialized agents for each aspect:
    - Security Reviewer
    - Performance Reviewer
    - Code Quality Reviewer
    - Business Logic Reviewer
    - Testing Reviewer
    - (+ conditionally: Backend, API, Framework-specific)
- Each agent focuses on ONE aspect using relevant reference files
- Launch all agents in parallel with `runSubagent`

**Step 2: Synthesize Review Results**

- Collect findings from all agents
- De-duplicate overlapping issues
- Re-prioritize in context of full picture
- Merge different perspectives

**Step 3: Understand Change Context**

- Read the flow artifacts listed under [Where this runs](#where-this-runs)
- Assess scope and complexity
- Document the change summary

**Step 4: Regression Risk Assessment**

- Cross-reference agent findings with affected features
- Identify high-risk changes
- Document testing recommendations

**Step 5: Create Comprehensive Review Report**

- Synthesize all findings into coherent review
- Provide clear recommendation
- Prioritize action items
- Include human reviewer guidance

## Output Format

Generate output as `[phase]-code-review.md` using this structure:

```markdown
# Code Review Report

## Executive Summary

[One paragraph: overall quality, recommendation (approve/needs work/reject), key findings count]

## Tech Stack Detected

[What was detected, which rules were loaded]

## Review Results by Category

### Security [Critical: N | High: N | Medium: N | Low: N]

[Top 3-5 most important findings, or "✅ No issues"]

### Performance [Critical: N | High: N | Medium: N | Low: N]

[Top 3-5 most important findings, or "✅ No issues"]

### Code Quality [Critical: N | High: N | Medium: N | Low: N]

[Top 3-5 most important findings, or "✅ No issues"]

### Business Logic [Critical: N | High: N | Medium: N | Low: N]

[Top 3-5 most important findings, or "✅ No issues"]

### Testing [Critical: N | High: N | Medium: N | Low: N]

[Top 3-5 most important findings, or "✅ No issues"]

### [Additional Categories as detected]

[Findings or "✅ No issues"]

## Regression Risk Assessment

**Risk Level**: [Low / Medium / High / Critical]

**Affected Features**:

- Feature 1: Impact assessment
- Feature 2: ✅ No impact / ⚠️ Needs testing

**Testing Recommendations**:

- Automated test coverage status
- Manual testing areas
- Performance testing needs

## Positive Observations

[What was done well - highlight good patterns, proper implementations]

## Action Items (Prioritized)

**Must Fix Before Merge** (Blocking):

1. [Critical/High issue with location and fix]

**Should Fix** (Non-blocking):

1. [Medium issue with location and fix]

**Consider for Future** (Technical debt):

1. [Low priority improvement]

## Recommendation

**[APPROVE / APPROVE WITH CHANGES / NEEDS WORK / REJECT]**

[2-3 sentence justification referencing key findings and overall code quality]

## Human Reviewer Guidance

[Specific areas to focus on during human review, non-obvious risks, suggestions for testing]
```

### Severity Guidelines

- **Critical**: Security vulnerabilities, data loss risks, crashes, complete feature breakage
- **High**: Performance issues, incorrect business logic, missing validation, poor error handling
- **Medium**: Maintainability issues, readability problems, missing tests, anti-patterns
- **Low**: Naming improvements, documentation, minor optimizations, style consistency

## Reference Files

Load these as needed during the review process:

**Universal Rules** (always load):

- [Programming Principles](references/rules-programming-principles.md)
- [Design Patterns](references/rules-design-patterns.md)
- [Security](references/rules-security.md)
- [Performance](references/rules-performance.md)
- [Testing](references/rules-testing.md)
- [Readability](references/rules-readability.md)
- [Data Integrity](references/rules-data-integrity.md)
- [Business Logic](references/rules-business-logic.md)

**Conditional Rules** (load when detected):

- [Backend Rules](references/rules-backend.md) - when backend framework detected
- [API Design](references/rules-api-design.md) - when REST/GraphQL detected
- [NestJS Rules](references/rules-backend-nestjs.md) - when NestJS detected

**Process Documentation**:

- [Complete Review Process](references/review-process.md) - detailed step-by-step process
- [Tech Stack Detection](references/tech-stack-detection.md) - detection patterns and strategies
