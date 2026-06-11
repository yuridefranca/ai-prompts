---
name: post-fix-reviewer
description: >
    Verify bug fix works correctly, handles all edge cases, doesn't introduce regressions,
    and meets quality standards. Final validation before code review. Always use after patch
    implementation. Complements code-reviewer skill (which checks broader quality). Keywords:
    post-fix validation, bug fix verification, regression testing, edge case validation,
    fix quality assurance, testing validation.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Post-Fix Reviewer

**Final validation** that bug fix actually works and doesn't break anything else.

## When to Use

- Immediately after patch implementation
- Before code review
- Before merging fix
- For critical/production bugs

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- Passing tests don't guarantee the bug is fixed - always re-run original reproduction steps
- Edge case tests passing doesn't mean you tested the RIGHT edge cases - verify against solution-critic feedback
- Zero regression test failures can hide regressions - manually test related features
- Test coverage increase doesn't mean quality tests - check tests actually assert the fix
- "All tests passing" in PR doesn't mean local tests were run - always run full suite locally
- Performance fix not benchmarked is just hope - measure before/after with real data
- Security fix without attack vector testing is incomplete - try to exploit the vulnerability
- Code looking good doesn't mean it works - verify with actual reproduction
- Fix works in dev doesn't mean it works in prod - check environment differences
- Manual testing once doesn't catch race conditions - test concurrent scenarios
- Documentation update without code change review is incomplete - ensure docs match implementation
- Blocking merge for minor style issues wastes time - distinguish critical from cleanup

## Workflow Artifact

This skill is invoked as **Phase 7** of the Bug Workflow (alongside code-reviewer). It MUST produce an output file in the workflow folder.

**Output File**: `.ai-workflow/[feature-folder]/7-post-fix-review.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, `2-root-cause-analysis.md`, `3-solution-evaluation.md`, and `6-fix-implementation.md` before reviewing the fix.

## Core Principle

**Prove It Works**: Don't assume fix works - verify with tests, reproduction, and edge cases.

## Process

### Step 1: Verify Bug Is Fixed

**Re-run original reproduction steps** from bug report. See [references/verification-templates.md](references/verification-templates.md#bug-fix-verification-template) for documentation format.

### Step 2: Run All Tests

Execute full test suite (unit, integration, E2E). See [references/verification-templates.md](references/verification-templates.md#test-results-template) for results format.

**Commands**:

```bash
npm test                    # Unit tests
npm run test:integration   # Integration tests
npm run test:e2e          # E2E tests
```

### Step 3: Test Edge Cases

From solution-critic feedback, verify each edge case. See [references/verification-templates.md](references/verification-templates.md#edge-case-validation-template) for format.

### Step 4: Check for Regressions

Test related features manually and verify existing tests still pass. See [references/verification-templates.md](references/verification-templates.md#regression-checks-template) for format.

### Step 5: Validate Performance

If performance concerns were raised, benchmark critical paths. See [references/verification-templates.md](references/verification-templates.md#performance-validation-template) for format.

### Step 6: Validate Security

If security concerns were raised, test attack vectors. See [references/verification-templates.md](references/verification-templates.md#security-validation-template) for format.

### Step 7: Review Code Quality

Quick quality check (readability, conventions, error handling). See [references/verification-templates.md](references/verification-templates.md#code-quality-notes-template) for format.

### Step 8: Check Documentation

Verify code comments, commit message, docs updates, CHANGELOG entry. See [references/verification-templates.md](references/verification-templates.md#documentation-check-template) for format.

## Output Format

See [references/verification-templates.md](references/verification-templates.md) for all detailed templates.

**Post-fix review structure**:

```markdown
# Post-Fix Review: [Issue]

## Executive Summary

**Fix Status**: ✅ Verified Working / ⚠️ Has Issues / 🛑 Failed
**Confidence**: [X]%
**Recommendation**: ✅ Approve / ⚠️ Minor fixes / 🛑 Needs work

## Verification Results

[Use templates from references/verification-templates.md]

## Issues Found

**Critical**: [List or None]
**High Priority**: [List or None]
**Medium Priority**: [List or None]
**Low Priority**: [List or None]

## Critique Points Status

[Check off all points from solution-critic]

## Recommendation

**[APPROVED / NEEDS WORK]**
[Justification]

**Next Steps**: [What to do next]

## Deferred Items

[Items for future, not blocking merge]
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

## Reference Files

- [Verification Templates](references/verification-templates.md) - All verification step templates (bug fix, tests, edge cases, regressions, performance, security, code quality, documentation)

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
