---
name: root-cause-analyzer
description: Deeply analyze bugs to identify true root cause through evidence-based investigation. Reproduces issues, traces state/data flow, checks race conditions, and validates assumptions. CRITICAL RULE Never propose fixes in this phase - only analyze. Always use when debugging issues after component mapping. Builds on debug-issue skill methodology. Keywords root cause analysis, debugging, bug investigation, evidence-based analysis, reproduction, state tracing, assumption validation, deep debugging.
---

# Root Cause Analyzer

**CRITICAL RULE**: This skill ONLY analyzes - never proposes fixes. Find the real root cause with evidence, not symptoms.

## When to Use

- After component mapping complete
- Investigating reported bug
- Issue reproduction needed
- Need evidence-based understanding
- Before proposing any solution

## Core Principle

**Evidence Over Assumptions**: Every conclusion must be backed by logs, traces, reproductions, or code analysis.

## Process

### Step 1: Reproduce the Issue

**Create minimal reproduction**:

1. Identify minimal steps to trigger bug
2. Document exact inputs
3. Document expected vs actual behavior
4. Verify reproduction is reliable

**Reproduction format**:

```markdown
## Reproduction Steps

1. [Action 1 with exact parameters]
2. [Action 2 with exact parameters]
3. [Action 3 with exact parameters]

**Expected**: [What should happen]
**Actual**: [What happens instead]
**Frequency**: [Always/Sometimes/Rarely]
```

**If cannot reproduce**:

- Document what was tried
- List potential conditions needed
- Gather more information from reporter

### Step 2: Trace Execution State

**Add logging/breakpoints**:

```typescript
console.log('[TRACE] Function entry', { params });
console.log('[TRACE] State before operation', { state });
// ... operation
console.log('[TRACE] State after operation', { state });
```

**Capture**:

- Variable values at key points
- Function call sequence
- Conditional branch taken
- Exception stack traces

**Analyze state evolution**:

- What state leads to bug?
- When does state become invalid?
- What assumptions about state break?

### Step 3: Trace Data Flow

**Follow data through system**:

1. Where does problematic data originate?
2. How is it transformed at each step?
3. Where does it become incorrect?
4. What validation is missing?

**Check for**:

- Data type mismatches
- Missing null checks
- Incorrect transformations
- Lost data in transit
- Encoding issues

### Step 4: Check for Race Conditions

**Timing issues**:

- Concurrent requests to same resource?
- Async operations completing out-of-order?
- Missing locks/mutexes?
- Event handlers firing unexpectedly?

**Test**:

- Run operations concurrently
- Add artificial delays
- Stress test with high load

### Step 5: Validate Assumptions

**Code assumptions to check**:

- "This will never be null" → Check if it can be
- "This always runs first" → Check order guarantees
- "User always provides X" → Check validation
- "Database has this data" → Check data presence
- "This is always positive" → Check for negative/zero

**Environmental assumptions**:

- Network is reliable?
- External API is available?
- Database is fast?
- Permissions are set correctly?

### Step 6: Review Recent Changes

**Check git history**:

```bash
git log --since="2 weeks ago" -- path/to/affected/file.ts
git blame path/to/affected/file.ts
```

**Questions**:

- When did bug start appearing?
- What changed around that time?
- Was it introduced by specific commit?
- Related to deployment/configuration change?

### Step 7: Formulate Root Cause

**Root cause must**:

- Explain ALL observed symptoms
- Be backed by evidence
- Be specific (not vague)
- Identify underlying mechanism

**Format**:

```markdown
## Root Cause

**Primary Cause** (Confidence: X%):
[Specific description of what's actually wrong]

**Why This Causes the Symptoms**:

1. [Mechanism 1]
2. [Mechanism 2]

**Evidence**:

- [Evidence 1: log excerpt, trace, etc.]
- [Evidence 2: code analysis]
- [Evidence 3: reproduction result]

**Conditions Required**:

- [Condition 1: when does it happen]
- [Condition 2: what state is needed]
```

### Step 8: Consider Alternative Explanations

**List other possible causes**:

```markdown
## Alternative Root Causes

**Alternative 1** (Likelihood: X%):
[Description]
**Why less likely**: [Reasoning]

**Alternative 2** (Likelihood: X%):
[Description]
**Why less likely**: [Reasoning]
```

**Sum of likelihoods should approach 100%**

## Output Format

```markdown
# Root Cause Analysis: [Issue]

## Issue Summary

[Brief description]

## Reproduction

### Steps

1. [Step with exact parameters]
2. [Step]
3. [Step]

### Expected vs Actual

- **Expected**: [Behavior]
- **Actual**: [Behavior]
- **Frequency**: [Always/Sometimes/Rarely]

## Evidence Gathered

### State Trace
```

[Log output or trace]

```

### Data Flow Analysis
[Where data becomes incorrect]

### Race Condition Analysis
[Findings]

### Assumption Violations
- [Assumption that breaks]

## Root Cause

**Primary Cause** (Confidence: 85%):
[Detailed explanation with code references]

**Why This Happens**:
[Underlying mechanism]

**Conditions Required**:
- [Condition 1]
- [Condition 2]

**Evidence Supporting This**:
1. [Evidence item 1]
2. [Evidence item 2]

## Alternative Explanations

**Alt 1** (Likelihood: 10%):
[Description]
**Why less likely**: [Reason]

**Alt 2** (Likelihood: 5%):
[Description]
**Why less likely**: [Reason]

## Assumptions Made
- ASSUMPTION-1: [Assumption]
- ASSUMPTION-2: [Assumption]

## Missing Information
- MISSING-1: [What's   still unclear]

## Confidence Level
**[X]%** - [Justification]

## ⚠️ NO FIX PROPOSED
Analysis complete. Moving to solution stress-test phase.
```

## CRITICAL: Never Propose Fix

**This skill ONLY analyzes**

❌ **DON'T**:

- Suggest how to fix it
- Propose solutions
- Recommend code changes
- Jump to implementation

✅ **DO**:

- Explain what's wrong
- Provide evidence
- Document mechanism
- Identify conditions

**Why**: Premature solutions skip critical stress-testing phase.

## Uncertainty Handling

**If confidence < 70%**:

- 🛑 STOP analysis
- List missing information needed
- Request more details
- DO NOT guess at root cause

## Evals

- [ ] Issue can be reliably reproduced
- [ ] Root cause identified with evidence
- [ ] Alternative causes considered
- [ ] Confidence level ≥70%
- [ ] NO fix proposed (critical)
- [ ] Mechanism fully explained
