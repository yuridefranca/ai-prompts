# Development Workflows

Comprehensive orchestration system for new features and bug fixes using specialized agents and skills.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Workflows](#workflows)
   - [Feature Workflow](#feature-workflow)
   - [Improvement Workflow](#improvement-workflow)
4. [Skills](#skills)
5. [Usage Examples](#usage-examples)
6. [Key Patterns](#key-patterns)

---

## Overview

This orchestration system implements a **7-phase TDD-based approach** for both new features and bug fixes, coordinating specialized skills to ensure quality, prevent premature solutions, and maintain clean code.

### Core Principles

- **TDD First**: Red (failing test) → Green (minimal implementation) → Refactor (optimize)
- **Never Jump to Solutions**: Especially for bugs - understand root cause first
- **Manual Checkpoints**: Critical decision points require human approval
- **Context Rehydration**: 10-bullet summaries between phases prevent context loss
- **Uncertainty Handling**: Confidence scoring and explicit missing information tracking

### Key Benefits

- Prevents premature fixes that only address symptoms
- Ensures thorough analysis before implementation 
- Maintains code quality through structured reviews
- Provides audit trail of decisions
- Reduces technical debt accumulation

---

## Architecture

### Hybrid Orchestration Model

```
User Request
    ↓
  Type?
    ↓
    ├─→ New Feature → Feature Workflow Agent
    │                      ↓
    │                 Coordinates:
    │                 - Spec Extractor
    │                 - System Designer
    │                 - Tradeoff Analyzer
    │                 - Feature Doc Writer
    │                 - TDD Test Generator
    │                 - Minimal Impl Generator
    │                 - Refactor Optimizer
    │                 - Code Reviewer
    │
    └─→ Bug/Improvement → Improvement Workflow Agent
                               ↓
                          Coordinates:
                          - Component Mapper
                          - Root Cause Analyzer
    IW --> S11[Solution Critic]
    IW --> S4
    IW --> S5
    IW --> S12[Patch Implementer]
    IW --> S13[Post-Fix Reviewer]
    IW --> S8
    
    S6 --> BE[Backend Engineer]
    S6 --> FE[Frontend Engineer]
    S12 --> BE
    S12 --> FE
    S4 --> DW[Doc Writer]
```

### Components

**Orchestrator Agents** (2):
- `feature-workflow` - New feature development
- `improvement-workflow` - Bug fixes and improvements

**Specialized Skills** (13):
- 7 feature skills
- 5 bugfix skills
- 1 shared code review skill

**Engineer Agents** (3):
- `backend-engineer` - Backend implementation
- `frontend-engineer` - Frontend implementation
- `doc-writter` - Documentation

---

## Workflows

### Feature Workflow

**Agent**: [feature-workflow.agent.md](../agents/feature-workflow.agent.md)

**Use When**: Building new functionality, adding capabilities

#### Phases

```
Phase 1: Specification
    ↓
[✓ Checkpoint: Review & Approve Spec]
    ↓
Phase 2: Architecture
    ↓
[✓ Checkpoint: Review & Approve Design]
    ↓
Phase 3: Documentation
    ↓
Phase 4: TDD Tests
    ↓
[✓ Checkpoint: Review Tests]
    ↓
Phase 5: Implementation
    ↓
Phase 6: Refactoring
    ↓
Phase 7: Code Review
```

| Phase | Skill | Purpose | Checkpoint |
|-------|-------|---------|------------|
| **1. Specification** | `spec-extractor` | Extract requirements, edge cases, acceptance criteria | ✅ After |
| **2. Architecture** | `system-designer`<br/>`tradeoff-analyzer` | Design system, evaluate alternatives | ✅ After |
| **3. Documentation** | `feature-doc-writer` | Update project docs | - |
| **4. TDD Tests** | `tdd-test-generator` | Create failing tests | ✅ After |
| **5. Implementation** | `minimal-impl-generator`<br/>+ Engineer agents | Simplest solution to pass tests | - |
| **6. Refactoring** | `refactor-optimizer` | Improve code quality | - |
| **7. Code Review** | `code-reviewer` | Final quality check | - |

#### Context Rehydration

Before **every phase**, the workflow generates a 10-bullet summary:
- What was decided
- What assumptions were made
- What's still unclear
- Why certain choices were made

#### Uncertainty Protocol

If confidence < 70% at any checkpoint:
- ❌ STOP workflow
- 📋 List missing information
- 🤝 Request user input
- 🔄 Resume after clarification

---

### Improvement Workflow

**Agent**: [improvement-workflow.agent.md](../agents/improvement-workflow.agent.md)

**Use When**: Fixing bugs, addressing issues, improving existing code

#### Phases

```
Phase 1: Component Mapping
    ↓
Phase 2: Root Cause Analysis
    ↓
[✓ Checkpoint: Confirm Root Cause]
    ↓
Phase 3: Solution Critique
    ↓
[✓ Checkpoint: Approve Solution]
    ↓
Phase 4: Documentation
    ↓
Phase 5: TDD Tests
    ↓
Phase 6: Patch Implementation
    ↓
Phase 7: Post-Fix Review & Code Review
```

| Phase | Skill | Purpose | Checkpoint |
|-------|-------|---------|------------|
| **1. Component Mapping** | `component-mapper` | Identify affected components, dependencies | - |
| **2. Root Cause** | `root-cause-analyzer` | Find true root cause (NO FIX) | ✅ After |
| **3. Solution Critique** | `solution-critic` | Adversarial stress-test (find 2+ failure modes) | ✅ After |
| **4. Documentation** | `feature-doc-writer` | Update project docs | - |
| **5. TDD Tests** | `tdd-test-generator` | Create failing tests | - |
| **6. Patch** | `patch-implementer`<br/>+ Engineer agents | Minimal fix addressing critique | - |
| **7. Post-Fix Review** | `post-fix-reviewer`<br/>`code-reviewer` | Verify fix works, no regressions | - |

#### Critical Rule: Never Jump to Fix

The workflow **enforces** completing Phases 1-3 before any implementation:

1. **Map components** - Understand what's affected
2. **Root cause analysis** - Find the real problem (evidence-based)
3. **Solution critique** - Stress-test approach (must find ≥2 failure modes)

**Why?** Jumping to fixes leads to:
- Symptom treatment (not root cause)
- Incomplete solutions (edge cases missed)
- New bugs introduced (side effects)
- Technical debt accumulation

#### Context Rehydration

Before **every phase** (more frequently than feature workflow):
- Current understanding of issue
- Evidence gathered
- Assumptions made
- Unknowns remaining

---

## Skills

### Feature Skills (7)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [spec-extractor](../skills/spec-extractor/SKILL.md) | Extract complete requirements | Functional/non-functional requirements, edge cases, acceptance criteria |
| [system-designer](../skills/system-designer/SKILL.md) | Design architecture | Domain model, API contracts, data model, simple text diagrams |
| [tradeoff-analyzer](../skills/tradeoff-analyzer/SKILL.md) | Compare alternatives | Comparison matrix, recommendation, failure scenarios |
| [feature-doc-writer](../skills/feature-doc-writer/SKILL.md) | Update documentation | AGENTS.md, feature docs, architecture docs |
| [tdd-test-generator](../skills/tdd-test-generator/SKILL.md) | Generate failing tests | Unit tests (AAA), integration tests, edge tests |
| [minimal-impl-generator](../skills/minimal-impl-generator/SKILL.md) | Simplest implementation | YAGNI code, happy path first, edge handling |
| [refactor-optimizer](../skills/refactor-optimizer/SKILL.md) | Code quality improvement | SOLID, DRY, performance, all tests still green |

### Bugfix Skills (5)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [component-mapper](../skills/component-mapper/SKILL.md) | Map affected code | Component list, dependency graph, data flow |
| [root-cause-analyzer](../skills/root-cause-analyzer/SKILL.md) | Find true root cause | Evidence-based root cause, alternatives, NO FIX |
| [solution-critic](../skills/solution-critic/SKILL.md) | Adversarial review | ≥2 failure modes, edge cases, security/performance concerns |
| [patch-implementer](../skills/patch-implementer/SKILL.md) | Minimal bug fix | Failing tests → minimal fix → addresses critique |
| [post-fix-reviewer](../skills/post-fix-reviewer/SKILL.md) | Verify fix works | Bug verified fixed, tests pass, no regressions |

### Shared Skills (1)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [code-reviewer](../skills/code-reviewer/SKILL.md) | Comprehensive quality check | Security, performance, maintainability review |

---

## Usage Examples

### Starting Feature Workflow

```
@feature-workflow Add discount code functionality to checkout flow
```

The workflow will:
1. Extract requirements using `spec-extractor`
2. Ask for confirmation at checkpoint
3. Design architecture with `system-designer` and `tradeoff-analyzer`
4. Ask for approval at checkpoint
5. Update documentation
6. Generate failing tests
7. Ask for test approval at checkpoint
8. Hand off to engineer agents for implementation
9. Refactor code
10. Final code review

### Starting Improvement Workflow

```
@improvement-workflow Fix null pointer exception when user has no email
```

The workflow will:
1. Map affected components
2. Analyze root cause (evidence-based, no fix proposed)
3. Ask for confirmation (never skips this)
4. Stress-test proposed solution (find ≥2 problems)
5. Ask for approval (must address blocking issues)
6. Update documentation
7. Generate failing tests
8. Implement minimal fix
9. Verify fix works and no regressions
10. Final code review

### Checkpoint Example

```markdown
## 🛑 CHECKPOINT: Specification Review

### Summary
[10-bullet summary of what was extracted]

### Confidence: 85%

### Missing Information
- MISSING-1: How should system handle expired discount codes?
- MISSING-2: What's the max discount percentage allowed?

### Decision Required
Approve specification and proceed to architecture design?

Options:
1. ✅ Approve - Specification is complete
2. 📝 Clarify - Need more information
3. 🔄 Revise - Specification needs changes
```

---

## Key Patterns

### 1. Context Rehydration

**Problem**: Long workflows lose context between phases

**Solution**: Generate 10-bullet summaries before each phase

```markdown
## Context Rehydration (10-Bullet Summary)

1. **Goal**: Add discount code functionality to checkout
2. **Decided**: Use single-use codes stored in database
3. **Decided**: Apply discount after tax calculation
4. **Assumption**: Codes never expire (confirmed with user)
5. **Assumption**: Only one code per order
6. **Edge Case**: Handle case-insensitive codes
7. **Edge Case**: Prevent negative total if discount > order amount
8. **Unknown**: What happens if code deleted after applied?
9. **Risk**: Race condition if multiple users use same code
10. **Next**: Design database schema and API contracts
```

### 2. Uncertainty Handling

**Problem**: Proceeding with incomplete information leads to rework

**Solution**: Confidence scoring + explicit missing info tracking

```markdown
## Uncertainty Assessment

**Overall Confidence**: 75%

**High Confidence (90-100%)**:
- Core user flow
- Basic validation rules

**Medium Confidence (70-89%)**:
- Error handling approach
- Integration with payment system

**Low Confidence (<70%)**:
- MISSING-1: Discount expiration logic
- MISSING-2: Admin UI requirements
- MISSING-3: Reporting needs

**Action**: 
❌ STOP - Confidence below 70% threshold
📋 Request clarification on MISSING items
```

### 3. Manual Checkpoints

**Problem**: Automated workflows make wrong decisions

**Solution**: Pause at critical points for human approval

```markdown
## 🛑 CHECKPOINT: Architecture Approval

[Summary of design]

**Vote Required**: 
- ✅ Approve and proceed to implementation
- 📝 Needs minor adjustments (what?)
- 🔄 Needs major redesign (why?)
```

**Checkpoint Locations**:
- Feature: After spec, after architecture, after tests
- Bugfix: After root cause, after solution critique

### 4. Never Jump to Fix (Bugfix Only)

**Problem**: Quick fixes address symptoms, not root causes

**Solution**: Enforce 3-phase investigation before any code changes

```
Bug Report
    ↓
Phase 1: Map Components
    ↓
Phase 2: Root Cause Analysis (NO FIX - Analysis Only)
    ↓
Phase 3: Critique Solution
    ↓
Approved?
    ├─→ Yes → Phase 6: Implement Fix
    └─→ No → Back to Phase 2
```

**Phase 2 Rule**: `root-cause-analyzer` skill **never proposes fixes**, only analyzes

### 5. Adversarial Solution Critique

**Problem**: Solutions look good until they break in production

**Solution**: Actively search for failure modes before implementation

```markdown
## Solution Critique Requirements

**Must Find**:
- ≥2 potential failure modes
- ≥1 edge case concern
- ≥1 performance or security issue

**If can't find issues**:
- Document that thorough review found none
- Explain why solution is robust
- Still provide "what if" scenarios
```

### 6. TDD Cycle

**Problem**: Implementation-first leads to untestable code

**Solution**: Always write tests before implementation

```
TDD Cycle:

1. Write Failing Test (RED)
   ↓
2. Run Test → Verify it FAILS
   ↓
3. Write Minimal Code (GREEN)
   ↓
4. Run Test → Verify it PASSES
   ↓
5. Refactor (Keep tests GREEN)
   ↓
6. Run Test → Still PASSES?
   └─→ Yes: Go to next test
   └─→ No: Fix refactoring
```

All tests must:
- ❌ Fail initially (proves they're testing something)
- ✅ Pass after implementation
- ✅ Remain green after refactoring

### 7. Skill Composition

**Problem**: Complex tasks need multiple specialized capabilities

**Solution**: Orchestrator agents coordinate skills at appropriate phases

**Example - Architecture Phase**:
```
1. Invoke `system-designer` skill
   → Produces domain model, API contracts, data model
   
2. Invoke `tradeoff-analyzer` skill  
   → Evaluates alternatives, recommends approach
   
3. Present both to user at checkpoint
   → User approves or requests changes
```

---

## Best Practices

### DO

- ✅ Follow workflows in order (don't skip phases)
- ✅ Stop at checkpoints for approval
- ✅ Write tests before implementation
- ✅ Generate context summaries between phases
- ✅ Track confidence levels explicitly
- ✅ For bugs: find root cause before fixing
- ✅ For bugs: stress-test solution before implementing

### DON'T

- ❌ Skip checkpoints to save time
- ❌ Implement before writing tests
- ❌ Proceed with low confidence (<70%)
- ❌ For bugs: jump straight to fix
- ❌ For bugs: fix symptoms instead of root cause
- ❌ Ignore edge cases raised by skills
- ❌ Skip code review phase

---

## Workflow Selection

| Situation | Use Workflow |
|-----------|--------------|
| New feature/capability | **Feature Workflow** |
| Bug fix | **Improvement Workflow** |
| Performance issue | **Improvement Workflow** |
| Security vulnerability | **Improvement Workflow** |
| Refactoring existing code | **Improvement Workflow** |
| Adding new endpoint/page | **Feature Workflow** |
| Modifying existing behavior | Consider both - if fixing wrong behavior use **Improvement** |

---

## Troubleshooting

### Workflow Stuck at Checkpoint

**Cause**: Missing information or low confidence

**Solution**:
1. Review the uncertainty assessment
2. Provide missing information
3. Ask clarifying questions
4. If still stuck, request to skip checkpoint (justified)

### Tests Won't Pass

**Cause**: Implementation doesn't match tests

**Solution**:
1. Re-read test expectations
2. Verify tests are correct (do they test the right thing?)
3. Fix implementation to match tests
4. If tests are wrong, fix tests first then re-implement

### Root Cause Unclear

**Cause**: Complex issue or insufficient evidence

**Solution**:
1. Gather more evidence (logs, traces, reproductions)
2. List what's known vs unknown
3. Form hypotheses and test them
4. If confidence < 70%, STOP and request help

### Critique Found Too Many Issues

**Cause**: Proposed solution has problems

**Solution**:
1. Address blocking issues first
2. Reconsider approach if many high-priority issues
3. Don't proceed with flawed solution
4. Better to redesign than patch later

---

## Integration with Existing Agents

The workflow agents delegate to existing specialist agents:

- **Backend Implementation** → `backend-engineer` agent
- **Frontend Implementation** → `frontend-engineer` agent  
- **Documentation** → `doc-writter` agent
- **Complex Analysis** → `breakdown-task` agent

**Example Handoff**:
```markdown
@backend-engineer Implement the discount code validation logic

**Context**: [From spec-extractor]
**Architecture**: [From system-designer]
**Tests to Pass**: [From tdd-test-generator]

**Requirements**:
1. Validate code exists in database
2. Check code not already used
3. Apply discount to order total
4. Handle edge cases: null codes, expired codes

**Follow**: TDD approach, keep tests green
```

---

## Related Documentation

- [Skills Directory](../skills/README.md) - Detailed skill documentation
- [Agents Directory](../agents/) - Individual agent files
- [Main README](../../README.md) - Project overview
- [Prompts Registry](../../prompts/registry.yaml) - Versioned templates

---

## Version History

- **v1.0.0** (2024-03-09): Initial implementation
  - 2 orchestrator agents
  - 13 specialized skills
  - 7-phase workflows for features and bugfixes
  - Manual checkpoints and context rehydration
  - Uncertainty handling protocols
