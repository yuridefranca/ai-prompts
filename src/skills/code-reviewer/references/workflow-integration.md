# Workflow Integration

## Overview

The code-reviewer skill is invoked as the **final quality gate** before merge in all three workflows.

## Workflow Artifacts

### Feature Workflow (Phase 8)

**Output File:** `.ai-workflow/[feature-folder]/8-code-review.md`

**Context to Read:**
- `0-startpoint.md` - Original feature requirements
- `0.1-grill-me.md` - Clarifying questions and decisions
- `1-feature-analysis.md` - Feature breakdown
- `2-technical-design.md` - Architectural decisions
- `3-component-mapping.md` - Components affected
- `4-implementation-plan.md` - Implementation approach
- `5-minimal-implementation.md` - Code changes
- `6-test-generation.md` - Test coverage
- `7-refactor.md` - Optimization changes

**Review Focus:**
- Does implementation match design?
- Are all components properly integrated?
- Is test coverage adequate?
- Are there any regressions in existing features?

### Bug Workflow (Phase 7)

**Output File:** Contributes to `.ai-workflow/[feature-folder]/7-post-fix-review.md`

**Note:** Code-reviewer works **alongside** post-fix-reviewer:
- **post-fix-reviewer**: Checks if bug is actually fixed, no new bugs introduced
- **code-reviewer**: Checks code quality, security, performance, maintainability

**Context to Read:**
- `0-startpoint.md` - Bug report
- `0.1-grill-me.md` - Bug investigation
- `1-root-cause-analysis.md` - Root cause identified
- `2-solution-design.md` - Fix approach
- `3-minimal-implementation.md` - Bug fix code
- `4-test-generation.md` - Regression tests
- `5-tradeoff-analysis.md` - Fix tradeoffs
- `6-debug-issue.md` - Verification

**Review Focus:**
- Is the fix minimal and targeted?
- Does it address the root cause?
- Are there defensive safeguards added?
- Will this fix prevent similar bugs?
- Is the fix tested with regression tests?

### Improvement Workflow (Phase 7)

**Output File:** `.ai-workflow/[feature-folder]/7-code-review.md`

**Context to Read:**
- `0-startpoint.md` - Improvement request
- `0.1-grill-me.md` - Scope and goals
- `1-improvement-analysis.md` - Current state vs desired
- `2-technical-design.md` - Refactoring/improvement approach
- `3-component-mapping.md` - Affected components
- `4-implementation-plan.md` - Changes planned
- `5-minimal-implementation.md` - Code changes
- `6-test-generation.md` - Test updates

**Review Focus:**
- Does improvement deliver stated benefits?
- Is backward compatibility preserved?
- Are existing features unaffected?
- Is the improvement worth the complexity?

## Integration Points

### Before Code Review

**Prerequisites:**
1. Implementation complete
2. Tests written and passing
3. (For bugs) Post-fix review confirms bug is fixed
4. (For features) Refactoring phase complete

### During Code Review

**Actions:**
1. Detect tech stack from changed files
2. Load appropriate rule sets
3. Dispatch parallel review agents
4. Synthesize findings
5. Assess regression risks
6. Generate comprehensive report

### After Code Review

**Based on recommendation:**

**✅ APPROVE:**
- Proceed to merge
- May have deferred Low/Medium issues

**⚠️ APPROVE WITH COMMENTS:**
- Merge allowed
- Create follow-up tickets for issues
- Schedule fixes for next sprint

**🔧 REQUEST CHANGES:**
- Block merge
- Developer fixes Critical/High issues
- Re-run code review after fixes

**🛑 REJECT:**
- Significant rework needed
- Return to earlier phase (design/implementation)
- May require architectural changes

## Reading Workflow Context

### Extracting Requirements

From `0-startpoint.md`:
- What problem being solved?
- What are the acceptance criteria?
- What are the constraints?

### Understanding Decisions

From `0.1-grill-me.md`:
- What questions were asked?
- What decisions were made?
- What tradeoffs were considered?

### Checking Design Alignment

From `2-technical-design.md` (or `1-root-cause-analysis.md` for bugs):
- What was the planned approach?
- What components should be affected?
- What patterns should be followed?

### Verifying Implementation

From `5-minimal-implementation.md` (or `3-minimal-implementation.md` for bugs):
- Do code changes match the plan?
- Are there unexpected changes?
- Are changes minimal and focused?

### Assessing Test Coverage

From `6-test-generation.md` (or `4-test-generation.md` for bugs):
- Are all paths tested?
- Are edge cases covered?
- Are error cases tested?
- For bugs: Are regression tests added?

## Cross-Workflow Consistency

### All Workflows Should Check

- **Security**: Input validation, auth/authz, secrets, injection
- **Performance**: Database queries, async ops, caching
- **Code Quality**: SOLID, DRY, KISS, naming, complexity
- **Testing**: Coverage, assertions, edge cases
- **Documentation**: Comments, AGENTS.md updates, CHANGELOG

### Workflow-Specific Checks

**Features:**
- Backward compatibility
- API contract changes
- Migration requirements
- Feature flag integration

**Bugs:**
- Root cause addressed (not symptoms)
- Defensive safeguards added
- Regression tests present
- Similar bugs prevented

**Improvements:**
- Value delivered justifies complexity
- No feature regressions
- Performance actually improved (if perf improvement)
- Metrics to validate improvement

## Communication with Developers

### Tone and Style

✅ **Constructive and educational:**
> "This violates Single Responsibility Principle (SOLID) because the service handles both validation AND persistence. Consider splitting into `ValidatorService` and `RepositoryService` to improve testability and reusability."

❌ **Vague or judgmental:**
> "This code is bad."

### Providing Context

Always explain **why** something is an issue:

✅ **Explains impact:**
> "This N+1 query will execute 50 database calls for a cart with 50 items, causing 500ms+ latency on checkout."

❌ **Just states the rule:**
> "Don't use loops for database queries."

### Suggesting Fixes

Provide **specific, actionable** recommendations:

✅ **Actionable:**
> "Replace lines 45-52 with a single query using JOIN:
> ```sql
> SELECT items.*, discounts.* 
> FROM cart_items items 
> LEFT JOIN discounts ON items.discount_id = discounts.id 
> WHERE cart_id = $1
> ```"

❌ **Generic:**
> "Optimize this."

## Escalation Paths

### Critical Issues Found

**Immediate:**
1. Block merge (REQUEST CHANGES or REJECT)
2. Notify developer with clear explanation
3. Provide specific fix recommendations
4. Offer to pair on fix if needed

### Architectural Concerns

**If review reveals fundamental design issues:**
1. Suggest returning to design phase
2. Document specific concerns
3. Recommend architectural review
4. Don't approve bandaid fixes

### Scope Creep Detected

**If PR includes unrelated changes:**
1. Flag in review
2. Suggest splitting into separate PRs
3. Request focused changes only
4. May approve core changes, defer extras

## Review Metrics

Track for continuous improvement:

- **Issues by Severity**: Critical, High, Medium, Low counts
- **Issues by Category**: Security, Performance, Code Quality, Testing
- **Review Outcome**: Approve, Approve with Comments, Request Changes, Reject
- **Confidence Level**: Reviewer's confidence in assessment
- **Detected Regressions**: Issues that would have caused production problems

## Continuous Improvement

### Learning from Reviews

**After each review:**
- Add new gotchas to [Gotchas section](../SKILL.md#gotchas)
- Update rule references if patterns emerge
- Refine detection patterns for better coverage
- Share learnings with team

### Rule Set Evolution

**When to add new rules:**
- Same issue appears in multiple reviews
- New technology/pattern adopted by team
- Post-incident analysis reveals gap

**When to update rules:**
- Rule causes false positives
- Better detection pattern discovered
- Team consensus on new best practice
