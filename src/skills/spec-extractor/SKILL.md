---
name: spec-extractor
description: Extract complete feature specifications from user descriptions, converting high-level ideas into structured requirements with edge cases and acceptance criteria. Always use this skill when starting new feature work, when users describe what they want to build, or when requirements need clarification. It captures functional requirements, non-functional requirements, constraints, edge cases, and acceptance criteria. Keywords requirements, specification, feature spec, acceptance criteria, edge cases, constraints, functional requirements, requirements extraction, product requirements.
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

**Context**: The workflow folder and `0-startpoint.md` were created in Phase 0. Read `0-startpoint.md` to understand the user's initial requirements before extracting the specification.

## Process

### Step 1: Understand the Feature Goal

Ask clarifying questions to understand:

- **What problem does this solve?** (User need)
- **Who will use this?** (Target users/personas)
- **Why is this needed now?** (Business context)
- **What success looks like?** (Outcomes)

### Step 2: Extract Functional Requirements

Identify explicit and implicit **what the system must do**:

**Questions to answer**:

- What user actions must be supported?
- What data must be created/read/updated/deleted?
- What business rules must be enforced?
- What integrations are required?
- What outputs/responses are expected?

**Format each requirement**:

```
REQ-[N]: [Action] [Object] [Condition]
Example: REQ-1: User can create a new order with valid payment method
```

**Requirements should be**:

- **Specific**: No ambiguous language
- **Measurable**: Can determine if satisfied
- **Testable**: Can write automated test
- **Independent**: Not duplicating other requirements

### Step 3: Extract Non-Functional Requirements (NFRs)

Identify quality attributes and constraints:

**Performance Requirements**:

- Response time targets (e.g., "API responds in <200ms")
- Throughput targets (e.g., "handles 1000 req/sec")
- Resource limits (e.g., "uses <512MB RAM")

**Security Requirements**:

- Authentication needs (who can access?)
- Authorization rules (what can they do?)
- Data sensitivity (PII, financial, etc.)
- Compliance needs (GDPR, HIPAA, etc.)

**Reliability Requirements**:

- Uptime targets (e.g., "99.9% availability")
- Failure handling (what happens when things break?)
- Data integrity (how to prevent data corruption?)

**Scalability Requirements**:

- Expected growth (users, data, traffic)
- Scaling approach (horizontal/vertical)
- Load patterns (steady/spiky)

**Usability Requirements**:

- User experience expectations
- Accessibility standards
- Internationalization needs

### Step 4: Identify Constraints

Document limitations that restrict implementation choices:

**Technical Constraints**:

- Technology stack (must use X framework)
- Existing architecture (must integrate with Y)
- Infrastructure limitations (on-prem, specific cloud)
- Browser/device support requirements

**Business Constraints**:

- Budget limits
- Timeline requirements
- Resource availability (team size, skills)
- Legal/regulatory constraints

**Operational Constraints**:

- Deployment windows
- Maintenance windows
- Support requirements
- Monitoring/observability needs

### Step 5: Identify Edge Cases

Think through **boundary conditions and unusual scenarios**:

**Data Edge Cases**:

- Empty inputs (null, "", [])
- Extreme values (very large, very small, negative)
- Invalid formats (malformed data)
- Special characters (unicode, emojis, SQL injection attempts)
- Missing required fields

**Timing Edge Cases**:

- Race conditions (concurrent requests)
- Timeouts (slow external services)
- Out-of-order events
- Duplicate requests

**State Edge Cases**:

- Resource doesn't exist (404 scenarios)
- Resource already exists (conflict scenarios)
- Unauthorized access attempts
- Expired sessions/tokens

**Volume Edge Cases**:

- Pagination with zero results
- Pagination with millions of results
- Bulk operations (1 item vs 10,000 items)
- Rate limiting scenarios

**Integration Edge Cases**:

- External service down
- External service returns unexpected data
- Network failures
- Partial failures

**Format each edge case**:

```
EDGE-[N]: [Scenario] → [Expected Behavior]
Example: EDGE-1: User submits order with invalid payment → Return 400 error with clear message
```

### Step 6: Define Acceptance Criteria

Create testable criteria for verifying the feature works:

**Each criterion should be**:

- **Observable**: Can see/measure the outcome
- **Binary**: Pass or fail (no ambiguity)
- **Complete**: Covers functional + NFRs + edge cases

**Format using Given-When-Then**:

```
AC-[N]:
Given [precondition/context]
When [action taken]
Then [expected result]

Example:
AC-1:
Given a user has valid authentication credentials
When they submit an order with valid payment method
Then the order is created with status "pending" and user receives confirmation email within 5 seconds
```

**Ensure coverage of**:

- Happy path scenarios (normal use)
- Error scenarios (validation failures, conflicts)
- Edge cases (from Step 5)
- Non-functional requirements (performance, security)

### Step 7: Document Assumptions

List all assumptions you're making:

**Common assumption categories**:

- User behavior assumptions
- Data availability assumptions
- Infrastructure assumptions
- Integration assumptions
- Security assumptions

**Format**:

```
ASSUMPTION-[N]: [Assumption statement]
Example: ASSUMPTION-1: Users have stable internet connection with >1Mbps bandwidth
```

### Step 8: Calculate Confidence Level

Assess how confident you are in the completeness and correctness of the spec:

**Confidence calculation**:

- **90-100%**: All requirements clear, no critical gaps, comprehensive edge cases
- **80-89%**: Most requirements clear, minor gaps, good edge case coverage
- **70-79%**: Core requirements clear, some gaps, basic edge case coverage
- **60-69%**: Requirements somewhat clear, multiple gaps, limited edge cases
- **<60%**: Significant ambiguity, major gaps, insufficient information

**Factors that lower confidence**:

- Ambiguous feature description
- Missing context about users/business goals
- Unclear technical constraints
- No existing similar features for reference
- Complex integrations with unknown systems

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

## Examples

### Good Requirement

✅ REQ-1: User can upload profile image in JPG/PNG format, max 5MB, which is resized to 512x512px and stored in S3

### Poor Requirement

❌ REQ-1: User can upload profile picture

### Good Edge Case

✅ EDGE-1: User uploads 10MB image → Return 400 error: "Image must be under 5MB"

### Poor Edge Case

❌ EDGE-1: User uploads large image → Show error

### Good Acceptance Criterion

✅ AC-1: Given a logged-in user with no profile image, When they upload a 3MB PNG file, Then the image is resized to 512x512px, stored in S3, and profile page displays the image within 2 seconds

### Poor Acceptance Criterion

❌ AC-1: User can upload image and see it on their profile
