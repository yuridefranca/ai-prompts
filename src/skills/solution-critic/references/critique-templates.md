# Failure Mode Categories and Templates

## Failure Mode Categories

### Data Failures

- Null/undefined inputs
- Empty collections
- Invalid formats
- Special characters
- Missing required fields
- Boundary values (max int, min int, overflow)

### Timing Failures

- Race conditions (concurrent access)
- Timeouts (slow dependencies)
- Out-of-order events
- Duplicate requests
- Stale data reads

### State Failures

- Resource doesn't exist
- Resource already exists
- Unauthorized access
- Expired sessions/tokens
- Invalid state transitions
- Partial state updates

### Integration Failures

- External service down
- External service returns unexpected data
- Network failures
- Partial failures (some succeed, some fail)
- API contract changes
- Authentication failures with external systems

### Scale Failures

- Large datasets (pagination, memory)
- High concurrency (locking, deadlocks)
- Bulk operations (batch size limits)
- Rate limiting
- Storage limits

## Failure Mode Template

```markdown
## Potential Failure Modes

### FAILURE-1: [Scenario]
- **Trigger**: [What causes it]
- **Impact**: [What breaks]
- **Likelihood**: High/Medium/Low
- **Severity**: Critical/High/Medium/Low
- **Mitigation**: [How to prevent]

### FAILURE-2: [Scenario]
- **Trigger**: [What causes it]
- **Impact**: [What breaks]
- **Likelihood**: High/Medium/Low
- **Severity**: Critical/High/Medium/Low
- **Mitigation**: [How to prevent]
```

## Edge Case Template

```markdown
## Edge Cases Not Handled

### EDGE-1: [Case] → [What happens]
- **Should**: [Expected behavior]
- **Fix**: [How to handle]

### EDGE-2: [Case] → [What happens]
- **Should**: [Expected behavior]
- **Fix**: [How to handle]
```

## Performance Concern Template

```markdown
## Performance Concerns

### PERF-1: [Issue]
- **Impact**: [Performance degradation]
- **Mitigation**: [Optimization needed]

### PERF-2: [Issue]
- **Impact**: [Performance degradation]
- **Mitigation**: [Optimization needed]
```

## Security Concern Template

```markdown
## Security Concerns

### SEC-1: [Vulnerability]
- **Attack Vector**: [How to exploit]
- **Impact**: [Damage potential]
- **Fix Required**: [How to secure]
```

## Side Effects Template

```markdown
## Potential Side Effects

- SIDE-1: [Feature/component affected] - [How]
- SIDE-2: [Feature/component affected] - [How]
```

## Root Cause Alignment Template

```markdown
## Root Cause Alignment

**Does fix address root cause?** [Yes/Partially/No]

**Explanation**:
[How fix relates to root cause]

**Concerns**:
- [If symptom fix, explain]
```

## Proposed Solution Summary Template

```markdown
## Proposed Solution Summary

**Approach**: [High-level strategy]

**Changes**:
1. [Change to component X]
2. [Change to component Y]

**Assumptions**:
1. [Assumption being made]
2. [Assumption being made]

**Scope**: [What's included and excluded]
```

## Full Output Format Template

```markdown
# Solution Critique: [Issue]

## Proposed Solution Summary
[Brief description of fix]

## Critical Findings

### 🛑 BLOCKING ISSUES (Must fix before implementation)
1. **[Issue]** - [Description]
   - Impact: [What breaks]
   - Fix: [How to address]

### ⚠️ HIGH PRIORITY (Should fix)
1. **[Issue]** - [Description]
   - Impact: [Potential problem]
   - Fix: [How to address]

## Detailed Analysis

### Failure Modes Found: [N]
[Use FAILURE template from above]

### Edge Cases Not Handled: [N]
[Use EDGE template from above]

### Performance Concerns
[Use PERF template from above]

### Security Concerns
[Use SEC template from above]

### Side Effects
[Use SIDE template from above]

### Root Cause Alignment
[Use alignment template from above]

## Recommended Improvements

### Must Have (Before implementation)
1. [Improvement 1]
2. [Improvement 2]

### Should Have (Soon after)
1. [Improvement 1]

### Nice to Have (Future)
1. [Improvement 1]

## Alternative Approaches

**ALT-1**: [Different approach]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]
- **Recommendation**: [Consider/Skip]

## Critique Summary

**Total Issues Found**: [N]
- Blocking: [N]
- High Priority: [N]
- Medium Priority: [N]
- Low Priority: [N]

**Verdict**:
- ✅ **APPROVED** (minor issues only)
- ⚠️ **APPROVED WITH CHANGES** (address high priority items)
- 🛑 **NEEDS REVISION** (blocking issues found)

**Confidence in Analysis**: [X]%
```
