---
name: patch-implementer
description: Implement minimal bug fixes after critique phase, addressing identified issues and edge cases. Follows TDD approach create failing test then minimal fix, then refactor. Always use after solution-critic provides feedback. Integrates with engineer agents for implementation. Keywords bug fix implementation, patch, minimal fix, TDD, failing test, edge case handling, critique feedback, engineer handoff.
---

# Patch Implementer

Implement **minimal bug fix** that addresses critic feedback. TDD approach: failing test → minimal fix → refactor.

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

### Step 0: CRITICAL - Create/Modify Files

**⚠️ ENGINEER AGENTS MUST MODIFY ACTUAL FILES** - Do NOT just output code in chat.

**When delegating to engineer agents**:

- Explicitly instruct them to use `replace_string_in_file` or `create_file` tools
- Specify exact file paths where fixes should be applied
- Verify files are modified in the workspace after delegation
- Bug fix must be testable

**Why this matters**: Fixes that only exist in chat history don't actually fix the bug.

### Step 1: Review Critique Feedback

**Analyze critic findings**:

- What blocking issues must be addressed?
- What edge cases to handle?
- What performance concerns?
- What security measures needed?

**Prioritize**:

```markdown
## Implementation Checklist

### Must Fix (Blocking)

- [ ] [Issue 1]
- [ ] [Issue 2]

### Should Fix (High Priority)

- [ ] [Issue 3]
- [ ] [Issue 4]

### Can Defer (Low Priority)

- [ ] [Issue 5]
```

### Step 2: Create/Update Failing Tests

**Invoke `tdd-test-generator` skill** to create:

1. **Bug reproduction test** (if not exists):

```typescript
it('should [expected behavior]', () => {
	// Arrange: Setup that triggers bug
	const input = setupBugCondition();

	// Act: Execute buggy code
	const result = buggyFunction(input);

	// Assert: Should pass after fix
	expect(result).toBe(expectedValue);
});
```

2. **Edge case tests** (from critic feedback):

```typescript
it('should handle null input gracefully', () => {
	expect(() => buggyFunction(null)).not.toThrow();
});

it('should handle empty array', () => {
	const result = buggyFunction([]);
	expect(result).toEqual([]);
});
```

3. **Regression tests** (ensure fix doesn't break existing behavior):

```typescript
it('should still work for normal case', () => {
	const result = buggyFunction(normalInput);
	expect(result).toBe(normalOutput);
});
```

**Run tests - ALL MUST FAIL**:

```bash
npm test -- path/to/test.spec.ts
```

### Step 3: Implement Minimal Fix

**Hand off to engineer agent**:

- Backend bug → `backend-engineer` agent
- Frontend bug → `frontend-engineer` agent

**Instructions to engineer**:

```markdown
⚠️ USE FILE EDITING TOOLS - Create/modify actual files, don't just show code.

Implement minimal bug fix:

**Root Cause**: [From root-cause-analyzer]

**Fix Strategy**: [Specific approach]

**Must Address**:

- [Critique point 1]
- [Critique point 2]
- [Edge case 1]
- [Edge case 2]

**Tests to Pass**:

- `test/path/bug.spec.ts` - Main bug test
- `test/path/edges.spec.ts` - Edge cases

**Files to Modify**:

- Use `replace_string_in_file` for: [specific files]
- Use `create_file` if new files needed

**Constraints**:

- Minimal changes only
- Follow existing patterns
- No refactoring yet (next phase)
- Security: [Specific requirements]
- Performance: [Specific requirements]
```

**Engineer implements**:

- Changes only what's necessary
- Handles identified edge cases
- Adds validation/checks from critique
- Keeps style consistent

### Step 4: Verify Tests Pass

**Run all tests**:

```bash
# Run bug-specific tests
npm test -- path/to/affected

# Run full suite (check for regressions)
npm test
```

**All tests must**:

- ✅ Bug reproduction test passes
- ✅ Edge case tests pass
- ✅ Regression tests pass
- ✅ Existing tests still pass

**If tests fail**:

- Analyze failure
- Adjust implementation
- Re-run tests
- Repeat until green

### Step 5: Address Critique Concerns

**Check each critic point**:

#### Performance Concerns

```markdown
**PERF-1**: N+1 query problem

- ✅ Added: Database index on user_id
- ✅ Changed: Single query with JOIN
```

#### Security Concerns

```markdown
**SEC-1**: SQL injection risk

- ✅ Added: Parameterized query
- ✅ Added: Input validation
```

#### Edge Cases

```markdown
**EDGE-1**: Null input handling

- ✅ Added: Early return for null
- ✅ Added: Test coverage
```

### Step 6: Minimal Refactoring (If Needed)

**Only if fix is messy**:

- Extract duplicated code
- Rename for clarity
- Add comments for complex logic

**Keep tests green**:

- Run tests after each refactoring
- If test fails, revert immediately

**Don't**:

- Optimize prematurely
- Restructure architecture
- Add features
- Fix unrelated issues

### Step 7: Document the Fix

**In code comments**:

```typescript
/**
 * Fixes ISSUE-123: Null pointer when user has no email
 *
 * Root cause: Missing null check before email.toLowerCase()
 * Solution: Early return for null emails
 *
 * Handles edge cases:
 * - Null email
 * - Undefined email
 * - Empty string email
 */
function processEmail(email: string | null): string {
	if (!email) return '';
	return email.toLowerCase().trim();
}
```

**In commit message**:

```
fix: handle null email in processEmail function

Fixes ISSUE-123

Root cause: Missing null check caused crash when users
had no email address in profile.

Changes:
- Add null/undefined/empty check
- Return empty string for invalid emails
- Add tests for edge cases

Addresses security concern SEC-1 from solution critique
```

## Output Format

````markdown
# Bug Fix Implementation: [Issue]

## Fix Summary

[1-2 sentence description]

## Root Cause Addressed

[From root-cause-analyzer output]

## Changes Made

### Primary Fix

**File**: `path/to/file.ts`
**Lines**: [Line range]
**Change**: [What was changed]

```diff
- old code
+ new code
```
````

### Edge Case Handling

1. **Null input**: Added early return
2. **Empty array**: Return empty array immediately
3. **Concurrent requests**: Added locking mechanism

### Security Measures

- ✅ Input validation added
- ✅ Parameterized queries used
- ✅ Error messages sanitized

### Performance Optimizations

- ✅ Database index added
- ✅ N+1 query eliminated
- ✅ Caching layer added

## Tests

### Tests Added

- `bug-reproduction.spec.ts` - Main bug test (✅ passing)
- `edge-cases.spec.ts` - Edge case coverage (✅ passing)
- `regression.spec.ts` - Existing behavior (✅ passing)

### Test Results

```
✅ Bug reproduction: PASS
✅ Null input: PASS
✅ Empty array: PASS
✅ Concurrent requests: PASS
✅ Regression suite: PASS (42/42)
```

## Critique Points Addressed

### Blocking Issues

- ✅ FAILURE-1: [How addressed]
- ✅ FAILURE-2: [How addressed]

### High Priority

- ✅ EDGE-1: [How addressed]
- ✅ PERF-1: [How addressed]

### Deferred

- ❌ LOW-1: [Why deferred and when to address]

## Code Changes

**Files Modified**:

1. `src/service/user.service.ts` (+12, -3 lines)
2. `test/service/user.service.spec.ts` (+45 lines)

**Complexity**: [Low/Medium/High]

**Breaking Changes**: [None / List if any]

## What Was NOT Changed

[Explicitly list what was not modified to avoid confusion]

## Next Steps

1. Post-fix review (invoke `post-fix-reviewer` skill)
2. Code review (invoke `code-reviewer` skill)
3. [Any follow-up tasks]

````

## Engineer Handoff Pattern

**When to delegate**:
- Implementation requires domain expertise
- Multiple files affected
- Complex business logic

**Handoff format**:
```markdown
@backend-engineer Please implement this bug fix:

**Context**: [From component-mapper]
**Root Cause**: [From root-cause-analyzer]
**Critique Feedback**: [From solution-critic]

**Implementation Requirements**:
1. [Specific requirement]
2. [Specific requirement]

**Tests to pass**: [List test files]

**Constraints**: [Minimal fix, no refactoring, follow patterns]
````

## Evals

- [ ] All critique blocking issues addressed
- [ ] Failing tests created (reproduction + edges)
- [ ] Implementation is minimal (no over-engineering)
- [ ] All tests passing (bug + edge + regression)
- [ ] Security measures implemented
- [ ] Performance concerns addressed
- [ ] Code documented (comments + commit)
- [ ] No unnecessary changes made
