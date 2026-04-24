---
name: post-fix-reviewer
description: Verify bug fix works correctly, handles all edge cases, doesn't introduce regressions, and meets quality standards. Final validation before code review. Always use after patch implementation. Complements code-reviewer skill (which checks broader quality). Keywords post-fix validation, bug fix verification, regression testing, edge case validation, fix quality assurance, testing validation.
---

# Post-Fix Reviewer

**Final validation** that bug fix actually works and doesn't break anything else.

## When to Use

- Immediately after patch implementation
- Before code review
- Before merging fix
- For critical/production bugs

## Workflow Artifact

This skill is invoked as **Phase 7** of the Improvement Workflow (alongside code-reviewer). It MUST produce an output file in the workflow folder.

**Output File**: `.ai-workflow/[feature-folder]/7-post-fix-review.md`

**Context**: Read `0-startpoint.md` for the user's problem description, `2-root-cause-analysis.md` for the root cause, `3-solution-critique.md` for critique feedback, and `6-fix-implementation.md` for what was implemented.

## Core Principle

**Prove It Works**: Don't assume fix works - verify with tests, reproduction, and edge cases.

## Process

### Step 1: Verify Bug Is Fixed

**Re-run original reproduction steps**:

1. Follow exact steps from bug report
2. Use same inputs
3. Check expected behavior occurs

**Manual verification** (if applicable):

- Test in UI
- Check API responses
- Verify database state
- Check logs

**Document**:

```markdown
## Bug Fix Verification

**Original Issue**: [Description]

**Reproduction Steps**:

1. [Step]
2. [Step]

**Result**:

- ✅ Bug no longer occurs
- ✅ Expected behavior observed
- ✅ No error messages

**Evidence**: [Screenshot/log/test output]
```

### Step 2: Run All Tests

**Execute test suite**:

```bash
# Unit tests
npm test

# Integration tests
npm run test:integration

# E2E tests (if applicable)
npm run test:e2e
```

**Check for**:

- All new tests passing
- All existing tests still passing
- No flaky tests introduced
- Coverage maintained/improved

**Document results**:

```markdown
## Test Results

**Unit Tests**: ✅ 152/152 passing
**Integration Tests**: ✅ 43/43 passing
**E2E Tests**: ✅ 12/12 passing

**Coverage**:

- Before: 87.3%
- After: 88.1%
- Delta: +0.8%

**New Tests Added**: 5

- bug-reproduction.spec.ts
- edge-cases.spec.ts (3 tests)
- regression.spec.ts
```

### Step 3: Test Edge Cases

**From solution-critic feedback**, verify each edge case:

```markdown
## Edge Case Validation

### EDGE-1: Null Input

- **Test**: Pass null to function
- **Expected**: Return empty string
- **Actual**: ✅ Returns empty string
- **Test**: `edge-cases.spec.ts:12`

### EDGE-2: Empty Array

- **Test**: Pass [] to function
- **Expected**: Return [] without error
- **Actual**: ✅ Returns []
- **Test**: `edge-cases.spec.ts:18`

### EDGE-3: Concurrent Requests

- **Test**: Send 10 simultaneous requests
- **Expected**: All succeed, no race conditions
- **Actual**: ✅ All succeed
- **Test**: `concurrency.spec.ts:25`
```

### Step 4: Check for Regressions

**Test related features**:

- Features using same components
- Features with similar behavior
- Upstream dependencies
- Downstream consumers

**Manual spot checks**:

```markdown
## Regression Checks

### Feature 1: User Login

- **Status**: ✅ Works normally
- **Tested**: Login flow, session creation

### Feature 2: Password Reset

- **Status**: ✅ Works normally
- **Tested**: Email sending, token validation

### Feature 3: Profile Update

- **Status**: ✅ Works normally
- **Tested**: Form submission, validation
```

### Step 5: Validate Performance

**If performance concerns were raised**:

**Benchmark critical paths**:

```typescript
console.time('operation');
// ... execute operation
console.timeEnd('operation'); // Should be <100ms
```

**Check metrics**:

- Query count (N+1 prevented?)
- Response time (within SLA?)
- Memory usage (no leaks?)
- Database load (indexes used?)

**Document**:

```markdown
## Performance Validation

**PERF-1**: N+1 Query Issue

- **Before**: 50 queries per request
- **After**: 2 queries per request
- **Status**: ✅ Fixed

**Response Time**:

- **Before**: 450ms average
- **After**: 85ms average
- **Target**: <100ms
- **Status**: ✅ Meets target
```

### Step 6: Validate Security

**If security concerns were raised**:

**Test attack vectors**:

```markdown
## Security Validation

**SEC-1**: SQL Injection

- **Attack**: `'; DROP TABLE users--`
- **Result**: ✅ Parameterized query prevents injection
- **Test**: `security.spec.ts:10`

**SEC-2**: XSS

- **Attack**: `<script>alert('xss')</script>`
- **Result**: ✅ Input sanitized
- **Test**: `security.spec.ts:20`
```

### Step 7: Review Code Quality

**Quick quality check**:

- Code is readable?
- Follows project conventions?
- No obvious code smells?
- Error handling adequate?
- Comments where needed?

**Issues to flag**:

```markdown
## Code Quality Notes

**✅ Good**:

- Clean variable names
- Proper error handling
- Good test coverage

**⚠️ Minor Concerns**:

- Function could be split (lines 45-80)
- Magic number on line 67 (should be constant)

**🛑 Must Fix**:

- [None]
```

### Step 8: Check Documentation

**Verify documentation updates**:

- Code comments added?
- Commit message descriptive?
- Related docs updated?
- CHANGELOG entry?

**Document**:

```markdown
## Documentation Check

- ✅ Code comments added (lines 45, 67)
- ✅ Commit message follows format
- ✅ AGENTS.md updated (if schema changed)
- ✅ CHANGELOG.md entry added
- ❌ API docs (not needed for internal fix)
```

## Output Format

```markdown
# Post-Fix Review: [Issue]

## Executive Summary

**Fix Status**: ✅ Verified Working / ⚠️ Has Issues / 🛑 Failed

**Confidence**: [X]%

**Recommendation**:

- ✅ Approve for code review
- ⚠️ Approve with minor fixes
- 🛑 Needs more work

## Verification Results

### 1. Bug Fix Verification

- ✅ Original issue resolved
- ✅ Expected behavior observed
- ✅ No errors in logs

**Evidence**: [Link to test output / screenshot]

### 2. Test Suite

- ✅ All tests passing (152/152)
- ✅ New tests added (5)
- ✅ Coverage improved (+0.8%)

**Test Summary**:
```

Test Suites: 15 passed, 15 total
Tests: 152 passed, 152 total
Duration: 12.4s

```

### 3. Edge Cases
- ✅ EDGE-1: Null input handled
- ✅ EDGE-2: Empty array handled
- ✅ EDGE-3: Concurrent requests work

### 4. Regression Check
- ✅ Related features working
- ✅ No unexpected side effects
- ✅ Existing tests passing

**Features Tested**:
1. User Login - ✅ Working
2. Password Reset - ✅ Working
3. Profile Update - ✅ Working

### 5. Performance
- ✅ PERF-1: N+1 query eliminated
- ✅ Response time: 85ms (target <100ms)
- ✅ Database queries: 2 (was 50)

### 6. Security
- ✅ SEC-1: SQL injection prevented
- ✅ Input validation in place
- ✅ Error messages sanitized

### 7. Code Quality

**Strengths**:
- Clean, readable code
- Good error handling
- Adequate comments

**Minor Issues**:
- ⚠️ Function on lines 45-80 could be split
- ⚠️ Magic number on line 67 (LOW priority)

**Must Fix**:
- [None]

### 8. Documentation
- ✅ Code comments added
- ✅ Commit message descriptive
- ✅ CHANGELOG updated
- ✅ Relevant docs updated

## Issues Found

### Critical
[None]

### High Priority
[None]

### Medium Priority
1. **Function too long** (lines 45-80)
   - Consider extracting helper functions
   - Not blocking, can address later

### Low Priority
1. **Magic number** (line 67)
   - Extract to constant
   - Can defer to refactoring phase

## Critique Points Status

**From solution-critic review**:
- ✅ FAILURE-1: Addressed and tested
-  ✅ FAILURE-2: Addressed and tested
- ✅ EDGE-1: Handled and verified
- ✅ EDGE-2: Handled and verified
- ✅ PERF-1: Fixed and benchmarked
- ✅ SEC-1: Secured and tested

## Recommendation

**✅ APPROVED FOR CODE REVIEW**

Fix is working correctly, all tests passing, no regressions detected. Minor code quality issues can be addressed in refactoring phase or future cleanup.

**Confidence**: 95%

**Next Steps**:
1. Invoke `code-reviewer` skill for final quality check
2. Create pull request
3. Address any code review feedback
4. Merge to main branch

## Deferred Items

[Items that can be addressed later, not blocking merge]
1. Function extraction (lines 45-80) - Future refactoring
2. Magic number constant (line 67) - Future cleanup
```

## When to Block Merge

**Block if**:

- ❌ Bug still occurs
- ❌ Tests are failing
- ❌ Regressions detected
- ❌ Security vulnerabilities remain
- ❌ Performance not meeting SLA

**Don't block for**:

- ✅ Minor code style issues
- ✅ Non-critical refactoring opportunities
- ✅ Documentation typos
- ✅ Low-priority improvements

## Evals

- [ ] Original bug verified fixed
- [ ] All tests passing (including existing ones)
- [ ] All edge cases tested and working
- [ ] No regressions detected
- [ ] Performance validated (if applicable)
- [ ] Security validated (if applicable)
- [ ] Code quality acceptable (no critical issues)
- [ ] Documentation updated
- [ ] Clear recommendation provided
