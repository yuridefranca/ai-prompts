---
name: spec-extractor
description: >
    Extract complete feature specifications from user descriptions, converting high-level ideas
    into structured requirements with edge cases and acceptance criteria. Always use this skill
    when starting new feature work, when users describe what they want to build, or when requirements
    need clarification. It captures functional requirements, non-functional requirements, constraints,
    edge cases, and acceptance criteria. Keywords: requirements, specification, feature spec,
    acceptance criteria, edge cases, constraints, functional requirements, requirements extraction,
    product requirements.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Specification Extractor

This skill converts a user's high-level feature idea or description into a complete, structured specification document ready for architecture and implementation. It systematically extracts all requirement types, identifies edge cases, and defines clear acceptance criteria.

## When to Use This Skill

- User provides a feature description or idea
- Starting a new feature development cycle
- Requirements are incomplete or ambiguous
- Need to validate understanding before design
- Converting product requests into engineering specs

## Workflow Artifact

This skill is invoked as **Phase 1** of the Feature Workflow. It MUST produce an output file in the workflow folder.

**Output File**: `.ai-workflow/[feature-folder]/1-specification.md`

**Context**: Read `0-startpoint.md` for the user's initial requirements and `0.1-grill-me.md` for refined understanding before extracting the specification.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- "Fast" without a number is useless - always specify response times in milliseconds
- Functional requirements without acceptance criteria can't be tested
- Edge cases with "should handle errors gracefully" are too vague - specify exact error responses
- Missing non-functional requirements lead to performance/security issues in production
- Confidence below 70% means STOP - assumptions lead to rework later
- Acceptance criteria without Given-When-Then structure are hard to verify
- Forgetting to ask "what happens when X fails?" leads to missing error handling requirements
- "Scalable" without numbers (users, TPS, data volume) is not a requirement
- Assumptions not documented become hidden dependencies
- Edge cases for concurrent operations (race conditions) often forgotten
- Missing integration failure scenarios (external API down) cause production incidents
- Requirements like "user-friendly" or "intuitive" are not testable - need specific criteria

## Process

### Step 1: Understand the Feature Goal

Ask clarifying questions to understand:

- **What problem does this solve?** (User need)
- **Who will use this?** (Target users/personas)
- **Why is this needed now?** (Business context)
- **What success looks like?** (Outcomes)

### Step 2: Extract Functional Requirements

See [references/requirement-types.md](references/requirement-types.md#functional-requirements) for detailed guidance.

**Quick guide**: Identify what the system must do - user actions, data operations, business rules, integrations, expected outputs.

### Step 3: Extract Non-Functional Requirements (NFRs)

See [references/requirement-types.md](references/requirement-types.md#non-functional-requirements-nfrs) for detailed guidance.

**Categories**: Performance, Security, Reliability, Scalability, Usability

### Step 4: Identify Constraints

See [references/requirement-types.md](references/requirement-types.md#constraints) for detailed guidance.

**Categories**: Technical, Business, Operational

### Step 5: Identify Edge Cases

See [references/edge-case-guide.md](references/edge-case-guide.md) for complete edge case categories.

**Quick checklist**: Data, Timing, State, Volume, Integration edge cases

### Step 6: Define Acceptance Criteria

Create testable criteria for verifying the feature works.

**Format using Given-When-Then**:

```
AC-[N]:
Given [precondition/context]
When [action taken]
Then [expected result]
```

**Each criterion should be**:

- **Observable**: Can see/measure the outcome
- **Binary**: Pass or fail (no ambiguity)
- **Complete**: Covers functional + NFRs + edge cases

See [references/examples.md](references/examples.md#acceptance-criteria) for good vs poor examples.

### Step 7: Document Assumptions

List all assumptions you're making:

**Format**:

```
ASSUMPTION-[N]: [Assumption statement]
Example: ASSUMPTION-1: Users have stable internet connection with >1Mbps bandwidth
```

### Step 8: Calculate Confidence Level

Assess how confident you are in the completeness and correctness of the spec:

**Confidence levels**:

- **90-100%**: All requirements clear, no critical gaps, comprehensive edge cases
- **80-89%**: Most requirements clear, minor gaps, good edge case coverage
- **70-79%**: Core requirements clear, some gaps, basic edge case coverage
- **<70%**: 🛑 **STOP** - Insufficient information to proceed

### Step 9: Identify Missing Information

Explicitly list what information is missing or unclear:

**Format**:

```
MISSING-[N]: [Question that needs answering]
Example: MISSING-1: What happens when user attempts to modify order after it's been shipped?
```

**If confidence < 70%**: STOP and present missing information to user for clarification.

## Output Format

Produce a structured specification document:

```markdown
# Feature Specification: [Feature Name]

## Summary

[1-2 sentence description of feature]

## Goals & Context

- **Problem**: [What problem this solves]
- **Users**: [Who will use this]
- **Success Criteria**: [High-level outcomes]

## Functional Requirements

- REQ-1: [Requirement description]
- REQ-2: [Requirement description]
- ...

## Non-Functional Requirements

### Performance

- NFR-1: [Performance target]
- ...

### Security

- NFR-2: [Security requirement]
- ...

### Reliability

- NFR-3: [Reliability requirement]
- ...

### Scalability

- NFR-4: [Scalability requirement]
- ...

## Constraints

### Technical

- [Constraint 1]
- [Constraint 2]

### Business

- [Constraint 1]
- [Constraint 2]

### Operational

- [Constraint 1]
- [Constraint 2]

## Edge Cases

- EDGE-1: [Scenario] → [Expected behavior]
- EDGE-2: [Scenario] → [Expected behavior]
- ...

## Acceptance Criteria

- AC-1:
  Given [precondition]
  When [action]
  Then [result]
- AC-2:
  Given [precondition]
  When [action]
  Then [result]
- ...

## Assumptions & Confidence

### Assumptions

- ASSUMPTION-1: [Assumption]
- ASSUMPTION-2: [Assumption]
- ...

### Confidence Level

**[X]%** - [Brief justification]

### Missing Information

- MISSING-1: [Question]
- MISSING-2: [Question]
- ...

## Next Steps

[If confidence ≥70%: Proceed to architecture]
[If confidence <70%: Request clarification on missing information]
```

## Uncertainty Handling Protocol

**If confidence ≥ 80%**:

- ✅ Proceed to next phase
- Document assumptions for awareness

**If confidence 70-79%**:

- ⚠️ Proceed with caution
- Highlight assumptions explicitly
- Recommend user validation

**If confidence < 70%**:

- 🛑 **STOP immediately**
- Present missing information list
- Request clarification from user
- Do NOT proceed with assumptions

**Clarification request format**:

```markdown
## ⚠️ Insufficient Information to Proceed

**Current Confidence**: [X]%

**To proceed, I need clarification on**:

1. [Specific question about requirement]
2. [Specific question about constraint]
3. [Specific question about edge case]

**Impact of not clarifying**:

- [Risk 1: What could go wrong]
- [Risk 2: What assumptions would be made]

**Recommended next step**: Please provide answers to questions 1-3 above so I can complete the specification with confidence.
```

## Evals

Evaluate specification quality using these criteria:

### Completeness (40% weight)

- [ ] All functional requirements captured
- [ ] Non-functional requirements for perf/security/reliability/scalability
- [ ] Technical, business, and operational constraints identified
- [ ] Comprehensive edge case list (at least 5 categories)
- [ ] Acceptance criteria for all requirements

### Clarity (25% weight)

- [ ] Requirements are specific and unambiguous
- [ ] No vague terms ("fast", "easy", "flexible")
- [ ] Technical terms defined or obvious from context
- [ ] Acceptance criteria are testable (Given-When-Then)

### Testability (20% weight)

- [ ] Each requirement has corresponding acceptance criterion
- [ ] Edge cases have expected behaviors defined
- [ ] Success/failure conditions are binary (no subjectivity)
- [ ] Can be automated (not requires manual judgment)

### Risk Management (15% weight)

- [ ] Assumptions explicitly documented
- [ ] Confidence level calculated honestly
- [ ] Missing information identified
- [ ] Stops if confidence < 70%

**Scoring**:

- 90-100%: Excellent spec, ready for architecture
- 80-89%: Good spec, minor refinements may be needed
- 70-79%: Acceptable spec, proceed with caution
- <70%: Inadequate spec, requires more information

## Common Pitfalls to Avoid

❌ **Assuming requirements without asking**: Ask questions, don't guess
❌ **Vague requirements**: "Fast", "scalable", "user-friendly" mean nothing without numbers
❌ **Missing edge cases**: Think through data/timing/state/volume/integration edge cases
❌ **Untestable acceptance criteria**: Must be objective and automatable
❌ **Ignoring non-functional requirements**: Performance/security/reliability matter
❌ **High confidence with low information**: Be honest about what you don't know
❌ **Proceeding below 70% confidence**: Stop and request clarification

See [references/examples.md](references/examples.md) for detailed good vs poor examples.

## Reference Files

- [Requirement Types](references/requirement-types.md) - Detailed guidance on functional, non-functional requirements and constraints
- [Edge Case Guide](references/edge-case-guide.md) - Comprehensive edge case categories (data, timing, state, volume, integration)
- [Examples](references/examples.md) - Good vs poor requirements, edge cases, and acceptance criteria
