---
name: solution-critic
description: Adversarially stress-test proposed bug fixes before implementation. Finds failure modes, edge cases, performance issues, and security holes. MUST find at least 2 potential problems with any solution. Always use after root cause analysis and before implementing fix. Prevents premature solutions and incomplete fixes. Keywords solution critique, adversarial review, failure mode analysis, stress testing, edge cases, security review, performance analysis, fix validation.
---

# Solution Critic

**Adversarial stress-testing of proposed bug fixes**. Your job is to find what could go wrong.

## When to Use

- After root cause analysis complete
- Before implementing any fix
- Evaluating proposed solutions
- Critical/high-impact bugs
- Production incident fixes

## Core Principle

**Assume the Fix Will Fail**: Actively search for ways the proposed solution breaks. Better to find problems now than in production.

## Process

### Step 1: Understand the Proposed Solution

**Analyze fix proposal**:

- What does it change?
- What approach does it take?
- What assumptions does it make?
- What's the scope of changes?

**Document understanding**:

```markdown
## Proposed Solution Summary

**Approach**: [High-level strategy]

**Changes**:

1. [Change to component X]
2. [Change to component Y]

**Assumptions**:

- ASSUMPTION-1: [Assumption made]
- ASSUMPTION-2: [Assumption made]
```

### Step 2: Find Failure Modes

**REQUIRED**: Must find at least 2 potential failure modes.

**Categories to check**:

#### Data Failures

- What if input is null/undefined?
- What if data type is unexpected?
- What if array is empty?
- What if string is very long?
- What if number is negative/zero/infinity?

#### Timing Failures

- What if async operation completes out-of-order?
- What if user clicks twice quickly?
- What if operation times out?
- What if race condition occurs?

#### State Failures

- What if component is already in target state?
- What if dependencies aren't initialized?
- What if state becomes invalid mid-operation?
- What if operation is retried?

#### Integration Failures

- What if external API is down?
- What if database query fails?
- What if network is slow/disconnects?
- What if permissions are insufficient?

#### Scale Failures

- What if many users do this simultaneously?
- What if data set is very large?
- What if operation is CPU/memory intensive?
- What if this runs in loop?

**Document failures**:

```markdown
## Potential Failure Modes

### FAILURE-1: [Scenario]

**Trigger**: [How it happens]
**Impact**: [What breaks]
**Likelihood**: [High/Medium/Low]
**Severity**: [Critical/High/Medium/Low]

### FAILURE-2: [Scenario]

...
```

### Step 3: Check Edge Cases

**Boundary conditions**:

- First item / last item
- Empty collection / single item / many items
- Minimum value / maximum value
- Start of day / end of day (time)
- New user / power user

**Unusual but valid inputs**:

- Unicode characters
- Very long strings
- Special characters (', ", <, >, etc.)
- Case sensitivity issues

**Document**:

```markdown
## Edge Cases Not Handled

- EDGE-1: [Scenario] → [What happens]
- EDGE-2: [Scenario] → [What happens]
```

### Step 4: Analyze Performance Impact

**Check for**:

- N+1 query problems
- Missing database indexes
- Inefficient algorithms
- Memory leaks
- Blocking operations

**Questions**:

- Does fix add database queries?
- Does fix iterate large collections?
- Does fix load unnecessary data?
- Does fix block event loop?

**Document**:

```markdown
## Performance Concerns

**PERF-1**: [Issue]

- **Impact**: [How bad could it be]
- **Mitigation**: [How to address]
```

### Step 5: Security Review

**Check for**:

- SQL injection
- XSS vulnerabilities
- Authentication bypass
- Authorization issues
- Data exposure
- CSRF vulnerabilities

**Questions**:

- Does fix trust user input?
- Does fix check permissions?
- Does fix log sensitive data?
- Does fix expose internal errors?

**Document**:

```markdown
## Security Concerns

**SEC-1**: [Vulnerability]

- **Attack Vector**: [How to exploit]
- **Impact**: [Damage potential]
- **Fix Required**: [How to secure]
```

### Step 6: Check Side Effects

**What else might break**:

- Other features using same component
- Existing tests
- API contracts
- Database schema assumptions
- Performance characteristics
- Monitoring/logging

**Document**:

```markdown
## Potential Side Effects

- SIDE-1: [Feature/component affected] - [How]
- SIDE-2: [Feature/component affected] - [How]
```

### Step 7: Validate Against Root Cause

**Critical check**:

- Does fix address the actual root cause?
- Or does it just hide symptoms?

❌ **Symptom fix**: Catches error and silently ignores it
✅ **Root cause fix**: Prevents error from occurring

**Document**:

```markdown
## Root Cause Alignment

**Does fix address root cause?** [Yes/Partially/No]

**Explanation**:
[How fix relates to root cause]

**Concerns**:

- [If symptom fix, explain]
```

### Step 8: Propose Improvements

**For each issue found, suggest**:

- How to prevent it
- What to add/change
- Alternative approach

```markdown
## Recommended Improvements

### For FAILURE-1

- **Add**: [Validation/check needed]
- **Change**: [Modification needed]

### For EDGE-1

- **Handle**: [How to address edge case]
```

## Output Format

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

**FAILURE-1**: [Scenario]

- **Trigger**: [How]
- **Impact**: [What breaks]
- **Likelihood**: High/Medium/Low
- **Severity**: Critical/High/Medium/Low
- **Mitigation**: [How to prevent]

[... more failures ...]

### Edge Cases Not Handled: [N]

**EDGE-1**: [Case] → [What happens]

- **Should**: [Expected behavior]
- **Fix**: [How to handle]

[... more edges ...]

### Performance Concerns

**PERF-1**: [Issue]

- **Impact**: [Performance degradation]
- **Mitigation**: [Optimization needed]

### Security Concerns

**SEC-1**: [Vulnerability]

- **Attack**: [How to exploit]
- **Impact**: [Damage]
- **Fix**: [Security measure]

### Side Effects

- SIDE-1: [Affected area] - [How affected]
- SIDE-2: [Affected area] - [How affected]

### Root Cause Alignment

**Addresses root cause?** [Yes/Partially/No]

**Analysis**:
[Explanation]

## Recommended Improvements

### Must Have (Before implementation)

1. [Improvement 1]
2. [Improvement 2]

### Should Have (Soon after)

1. [Improvement 1]
2. [Improvement 2]

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

## Minimum Requirements

**Must find at least**:

- 2 potential failure modes
- 1 edge case concern
- 1 performance or security consideration

**If can't find issues**:

- Document explicitly that thorough review found none
- Explain why solution is robust
- Still provide at least 2 "what if" scenarios

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

## Evals

- [ ] At least 2 failure modes identified
- [ ] Edge cases analyzed
- [ ] Performance impact assessed
- [ ] Security reviewed
- [ ] Side effects considered
- [ ] Root cause alignment validated
- [ ] Improvements suggested
- [ ] Verdict provided (Approved/With Changes/Needs Revision)
