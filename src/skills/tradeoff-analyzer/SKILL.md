---
name: tradeoff-analyzer
description: Analyze technical tradeoffs between different implementation approaches, comparing complexity vs performance, maintainability, cost, and failure scenarios. Always use this skill when choosing between technical approaches, making architecture decisions, or evaluating design alternatives. Must identify at least 2 approaches and provide objective comparison. Keywords tradeoffs, alternatives, technical decision, architecture decision, ADR, comparison, pros and cons, decision making, cost benefit analysis, risk assessment.
---

# Tradeoff Analyzer

Systematically analyze and compare different technical approaches to help make informed architecture decisions. This skill enforces objective comparison of alternatives with explicit tradeoff documentation.

## When to Use This Skill

- After system design is drafted
- Choosing between implementation approaches
- Making architecture decisions (ADRs)
- Evaluating technology choices
- Risk vs reward assessment

## Workflow Artifact

This skill is invoked as part of **Phase 2** of the Feature Workflow (alongside system-designer). Its output is included in the architecture document.

**Output File**: `.ai-workflow/[feature-folder]/2-architecture.md` (tradeoff analysis section)

**Context**: Read `0-startpoint.md` for initial requirements and `1-specification.md` for the approved specification before analyzing tradeoffs.

## Process

### Step 1: Identify Approaches (Minimum 2)

List distinct approaches that could solve the problem:

**Approach A**: [Name/Description]
**Approach B**: [Name/Description]
**(Approach C)**: [Optional third alternative]

**Each approach must**:

- Be technically feasible
- Meet core requirements
- Differ meaningfully from others

### Step 2: Complexity Analysis

**For each approach, evaluate**:

- Lines of code estimate
- Number of components/services
- Integration complexity
- Learning curve for team
- Test complexity

**Score**: Simple (1) / Medium (2) / Complex (3)

### Step 3: Performance Analysis

**For each approach, evaluate**:

- Expected latency
- Throughput capacity
- Resource consumption (CPU/memory)
- Scalability limits
- Caching effectiveness

**Score**: Low (1) / Medium (2) / High (3) performance

### Step 4: Maintainability Analysis

**For each approach, evaluate**:

- Code readability
- Debugging difficulty
- Operational overhead
- Upgrade path
- Tech debt potential

**Score**: Easy (1) / Medium (2) / Hard (3) to maintain

### Step 5: Cost Analysis

**For each approach, evaluate**:

- Development time (hours/days)
- Infrastructure costs ($/month)
- Third-party service costs
- Training/onboarding costs
- Ongoing maintenance costs

**Total**: $[Amount] over [Timeframe]

### Step 6: Failure Scenario Analysis

**For each approach, identify**:

- Single points of failure
- Failure modes
- Recovery complexity
- Data loss risks
- Blast radius (impact scope)

**Risk Level**: Low / Medium / High

### Step 7: Create Comparison Table

| Criterion       | Approach A          | Approach B          | Approach C          |
| --------------- | ------------------- | ------------------- | ------------------- |
| Complexity      | [Score + reasoning] | [Score + reasoning] | [Score + reasoning] |
| Performance     | [Score + reasoning] | [Score + reasoning] | [Score + reasoning] |
| Maintainability | [Score + reasoning] | [Score + reasoning] | [Score + reasoning] |
| Cost (1 year)   | $[Amount]           | $[Amount]           | $[Amount]           |
| Failure Risk    | [Level + scenarios] | [Level + scenarios] | [Level + scenarios] |

### Step 8: Make Recommendation

**Recommended Approach**: [A/B/C]

**Rationale**:

- **Why chosen**: [Primary reasons]
- **Key tradeoffs accepted**: [What we're sacrificing]
- **Mitigation strategies**: [How to address weaknesses]
- **Decision confidence**: [%]

**When to reconsider**:

- [Condition that would change recommendation]

## Output Format

```markdown
# Tradeoff Analysis: [Decision Context]

## Problem Statement

[What decision needs to be made]

## Approaches Considered

### Approach A: [Name]

**Description**: [How it works]
**Key Technology**: [List]

### Approach B: [Name]

**Description**: [How it works]
**Key Technology**: [List]

### (Approach C: [Name])

**Description**: [How it works]
**Key Technology**: [List]

## Detailed Analysis

### Complexity

- **Approach A**: [Score] - [Reasoning]
- **Approach B**: [Score] - [Reasoning]
- ...

### Performance

- **Approach A**: [Score] - [Reasoning with numbers]
- **Approach B**: [Score] - [Reasoning with numbers]
- ...

### Maintainability

- **Approach A**: [Score] - [Reasoning]
- **Approach B**: [Score] - [Reasoning]
- ...

### Cost (12 months)

- **Approach A**: $[Amount breakdown]
- **Approach B**: $[Amount breakdown]
- ...

### Failure Scenarios

- **Approach A**: [Risk level]
    - Failure mode 1: [Description + impact]
    - Failure mode 2: [Description + impact]
- **Approach B**: [Risk level]
    - Failure mode 1: [Description + impact]
    - Failure mode 2: [Description + impact]
- ...

## Comparison Matrix

| Criterion          | Weight | Approach A | Approach B | Approach C |
| ------------------ | ------ | ---------- | ---------- | ---------- |
| Complexity         | 20%    | [Score/5]  | [Score/5]  | [Score/5]  |
| Performance        | 30%    | [Score/5]  | [Score/5]  | [Score/5]  |
| Maintainability    | 25%    | [Score/5]  | [Score/5]  | [Score/5]  |
| Cost               | 15%    | [Score/5]  | [Score/5]  | [Score/5]  |
| Risk               | 10%    | [Score/5]  | [Score/5]  | [Score/5]  |
| **Weighted Total** | 100%   | [X.X/5]    | [X.X/5]    | [X.X/5]    |

## Recommendation

**Chosen Approach**: **[A/B/C]**

**Primary Reasons**:

1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Tradeoffs Accepted**:

- [What we're sacrificing]: [Why it's acceptable]
- [What we're sacrificing]: [Why it's acceptable]

**Mitigation Strategies**:

- [Weakness]: [How we'll address it]
- [Weakness]: [How we'll address it]

**Confidence Level**: [X]%

**Reconsider If**:

- [Condition that would change decision]
- [Condition that would change decision]

## Assumptions

- ASSUMPTION-1: [Assumption]
- ASSUMPTION-2: [Assumption]

## Open Questions

- QUESTION-1: [Unresolved factor]
```

## Evals

### Objectivity (35%)

- [ ] At least 2 distinct approaches compared
- [ ] Criteria applied consistently
- [ ] Quantitative metrics used where possible
- [ ] Biases acknowledged

### Completeness (30%)

- [ ] All 5 criteria analyzed (complexity, perf, maint, cost, risk)
- [ ] Failure scenarios identified for each
- [ ] Tradeoffs explicitly stated
- [ ] Mitigation strategies provided

### Decision Quality (25%)

- [ ] Recommendation justified with evidence
- [ ] Confidence level stated
- [ ] Reconsideration triggers identified
- [ ] Aligns with project constraints

### Clarity (10%)

- [ ] Comparison table clear
- [ ] Technical terms explained
- [ ] Reasoning is followable
