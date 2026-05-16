# Development Workflows

Comprehensive orchestration system for new features, bug fixes, and improvements using specialized agents and skills.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Orchestrator](#orchestrator)
4. [Workflows](#workflows)
   - [Debug Workflow](#debug-workflow)
   - [Improvement Workflow](#improvement-workflow)
   - [Feature Workflow](#feature-workflow)
5. [Skills](#skills)
6. [Usage Examples](#usage-examples)
7. [Key Patterns](#key-patterns)

---

## Overview

This orchestration system implements **three specialized workflows**, each with a distinct philosophy and phase sequence, coordinated through a router agent for automatic classification.

### Core Principles

- **TDD First**: Red (failing test) → Green (minimal implementation) → Refactor (optimize)
- **Never Jump to Solutions**: Especially for bugs — understand root cause first
- **Understand Before Changing**: Especially for improvements — evaluate tradeoffs before modifying working code
- **Design Before Code**: Especially for features — complete specification and architecture first
- **Manual Checkpoints**: Critical decision points require human approval
- **Context Rehydration**: 10-bullet summaries between phases prevent context loss
- **Uncertainty Handling**: Confidence scoring and explicit missing information tracking
- **Workflow Artifacts**: Every phase produces a numbered file in `.ai-workflow/[feature-folder]/`

### Key Benefits

- Prevents premature fixes that only address symptoms
- Ensures thorough analysis before implementation
- Maintains code quality through structured reviews
- Provides audit trail of decisions via workflow artifacts
- Reduces technical debt accumulation
- Each workflow optimized for its task type

---

## Architecture

### Hybrid Orchestration Model

```
User Request
    ↓
@orchestrator (classifies task type)
    ↓
    ├─→ Bug → @debug-workflow
    │              ↓
    │         Coordinates:
    │         - grill-me (Phase 0.1)
    │         - component-mapper
    │         - root-cause-analyzer
    │         - tradeoff-analyzer + solution-critic
    │         - documentation-writer
    │         - test-generator
    │         - patch-implementer
    │         - post-fix-reviewer + code-reviewer
    │
    ├─→ Improvement → @improvement-workflow
    │                     ↓
    │                Coordinates:
    │                - grill-me (Phase 0.1)
    │                - component-mapper
    │                - tradeoff-analyzer + system-designer
    │                - documentation-writer
    │                - test-generator
    │                - minimal-impl-generator
    │                - integration-test-generator
    │                - code-reviewer
    │
    └─→ Feature → @feature-workflow
                      ↓
                 Coordinates:
                 - grill-me (Phase 0.1)
                 - spec-extractor
                 - system-designer + tradeoff-analyzer
                 - documentation-writer
                 - test-generator
                 - minimal-impl-generator
                 - integration-test-generator
                 - refactor-optimizer
                 - code-reviewer

    └─→ Greenfield → @greenfield-workflow
                         ↓
                    Coordinates:
                    - grill-me (Phase 0.1)
                    - spec-extractor
                    - product-manager
                    - system-designer + tradeoff-analyzer
                    - documentation-writer
                    - test-generator
                    - minimal-impl-generator
                    - integration-test-generator
                    - refactor-optimizer
                    - code-reviewer
```

### Components

**Orchestrator Agents** (5):
- `orchestrator` - Task classification and delegation
- `debug-workflow` - Bug fix workflow
- `improvement-workflow` - Code improvement workflow
- `feature-workflow` - New feature development
- `greenfield-workflow` - New project from scratch

**Specialized Skills** (18):
- 7 feature skills
- 5 bug skills
- 2 improvement skills
- 1 greenfield skill
- 5 shared skills
- 1 deployment skill (standalone)

**Engineer Agents** (3):
- `backend-engineer` - Backend implementation
- `frontend-engineer` - Frontend implementation
- `documentation-writer` - Documentation

---

## Orchestrator

**Agent**: [orchestrator.agent.md](../agents/orchestrator.agent.md)

**Use When**: Any task — the router classifies and delegates automatically.

### Classification Table

| Signal Keywords | Workflow | Philosophy |
|----------------|----------|------------|
| broken, error, crash, null pointer, unexpected, failing, bug | Bug | Never jump to fix |
| optimize, refactor, improve, enhance, migrate, performance | Improvement | Understand before changing |
| new, add, create, build, implement, feature | Feature | Design before code |
| new project, from scratch, greenfield, scaffold, new app, new service | Greenfield | Vision before code |

### Ambiguous Cases

| Request | Classification | Reason |
|---------|---------------|--------|
| "Fix the slow query" | Improvement | Working but suboptimal |
| "Fix the crash on login" | Bug | Something is broken |
| "Add caching to improve performance" | Improvement | Enhancement to working code |
| "Add user profile page" | Feature | New functionality |
| "Build a new SaaS app" | Greenfield | Entirely new project |
| "Start a new microservice" | Greenfield | New standalone service |

### Hybrid Requests

If a request contains both bug and improvement signals (e.g., "Fix the login bug and improve the error messages"), the router splits it into separate tasks and runs the appropriate workflow for each.

---

## Workflows

### Debug Workflow

**Agent**: [debug-workflow.agent.md](../agents/debug-workflow.agent.md)

**Use When**: Something is broken, errors occur, behavior is unexpected.

**Philosophy**: **Never Jump to Fix** — thorough evidence-based analysis before implementation.

#### Phases

```
Phase 0: Starting Point
    ↓
Phase 0.1: Grill Me (spec refinement)
    ↓
Phase 1: Component Mapping
    ↓
Phase 2: Root Cause Analysis
    ↓
[✓ Checkpoint: Confirm Root Cause]
    ↓
Phase 3: Solution Evaluation (tradeoff + critique)
    ↓
[✓ Checkpoint: Approve Solution]
    ↓
Phase 4: Documentation
    ↓
Phase 5: TDD Tests
    ↓
Phase 6: Patch Implementation
    ↓
Phase 7: Post-Fix Review
    ↓
Phase 8: PR Creation (optional)
```

| Phase | Skill | Purpose | Checkpoint | Output File |
|-------|-------|---------|------------|-------------|
| **0. Starting Point** | — | Capture bug description | ✅ After | `0-startpoint.md` |
| **0.1. Grill Me** | `grill-me` | Adversarial spec refinement | - | `0.1-grill-me.md` |
| **1. Component Mapping** | `component-mapper` | Identify affected components, dependencies | - | `1-component-map.md` |
| **2. Root Cause** | `root-cause-analyzer` | Find true root cause (NO FIX) | ✅ After | `2-root-cause-analysis.md` |
| **3. Solution Evaluation** | `tradeoff-analyzer`<br/>`solution-critic` | Evaluate approaches + adversarial stress-test | ✅ After | `3-solution-evaluation.md` |
| **4. Documentation** | `documentation-writer` | Update project docs | - | `4-solution-documentation.md` |
| **5. TDD Tests** | `test-generator` | Create failing tests | - | `5-tdd-tests.md` |
| **6. Patch** | `patch-implementer`<br/>+ Engineer agents | Minimal fix addressing critique | - | `6-fix-implementation.md` |
| **6.1. Analysis** | `multi-agent-analyzer` | Parallel code validation (quality, edge cases, regression) | - | `6.1-parallel-analysis.md` |
| **7. Post-Fix Review** | `post-fix-reviewer`<br/>`code-reviewer` | Verify fix works, no regressions | - | `7-post-fix-review.md` |
| **8. PR Creation** | `pr-creator` | Create pull request | Optional | `8-pr-creation.md` |

#### Critical Rule: Never Jump to Fix

The workflow **enforces** completing Phases 0-3 before any implementation:

1. **Map components** - Understand what's affected
2. **Root cause analysis** - Find the real problem (evidence-based)
3. **Solution evaluation** - Compare approaches + stress-test (must find ≥2 failure modes)

**Why?** Jumping to fixes leads to:
- Symptom treatment (not root cause)
- Incomplete solutions (edge cases missed)
- New bugs introduced (side effects)
- Technical debt accumulation

---

### Improvement Workflow

**Agent**: [improvement-workflow.agent.md](../agents/improvement-workflow.agent.md)

**Use When**: Improving, optimizing, refactoring, or enhancing existing working code.

**Philosophy**: **Understand Before Changing** — evaluate tradeoffs and impact before modifying working code.

#### Phases

```
Phase 0: Starting Point
    ↓
Phase 0.1: Grill Me (spec refinement)
    ↓
Phase 1: Component Mapping & Impact Analysis
    ↓
Phase 2: Tradeoff Analysis & Design
    ↓
[✓ Checkpoint: Approve Design]
    ↓
Phase 3: Documentation
    ↓
Phase 4: TDD Tests
    ↓
Phase 5: Implementation
    ↓
Phase 6: Integration Tests
    ↓
Phase 7: Code Review
    ↓
Phase 8: PR Creation (optional)
```

| Phase | Skill | Purpose | Checkpoint | Output File |
|-------|-------|---------|------------|-------------|
| **0. Starting Point** | — | Capture improvement description | ✅ After | `0-startpoint.md` |
| **0.1. Grill Me** | `grill-me` | Adversarial spec refinement | - | `0.1-grill-me.md` |
| **1. Component Mapping** | `component-mapper` | Identify affected components + impact analysis | - | `1-component-map.md` |
| **2. Tradeoff & Design** | `tradeoff-analyzer`<br/>`system-designer` | Evaluate approaches + design chosen approach | ✅ After | `2-tradeoff-and-design.md` |
| **3. Documentation** | `documentation-writer` | Update project docs | - | `3-improvement-documentation.md` |
| **4. TDD Tests** | `test-generator` | Create tests for improvement + regression tests | - | `4-tdd-tests.md` |
| **5. Implementation** | `minimal-impl-generator`<br/>+ Engineer agents | Full implementation following design | - | `5-implementation.md` |
| **5.1. Analysis** | `multi-agent-analyzer` | Parallel code validation (quality, edge cases, regression) | - | `5.1-parallel-analysis.md` |
| **6. Integration Tests** | `integration-test-generator` | Integration & E2E tests | - | `6-integration-tests.md` |
| **7. Code Review** | `code-reviewer` | Comprehensive quality check | - | `7-code-review.md` |
| **8. PR Creation** | `pr-creator` | Create pull request | Optional | `8-pr-creation.md` |

#### Critical Rule: Understand Before Changing

The workflow **enforces** completing Phases 0-2 before any implementation:

1. **Map components & assess impact** - What depends on current behavior?
2. **Tradeoff analysis** - What are the costs of each approach?
3. **Design with migration** - How do we transition safely?

**Why?** Modifying working code without understanding leads to:
- Regressions in existing behavior
- Breaking changes for consumers
- Incomplete migration paths
- Unnecessary complexity

---

### Feature Workflow

**Agent**: [feature-workflow.agent.md](../agents/feature-workflow.agent.md)

**Use When**: Building new functionality, adding capabilities.

**Philosophy**: **Design Before Code** — complete specification and architecture before implementation.

#### Phases

```
Phase 0: Starting Point
    ↓
Phase 0.1: Grill Me (spec refinement)
    ↓
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
Phase 6: Integration & E2E
    ↓
Phase 7: Refactor & Optimize
    ↓
Phase 8: Code Review
    ↓
Phase 9: PR Creation (optional)
```

| Phase | Skill | Purpose | Checkpoint | Output File |
|-------|-------|---------|------------|-------------|
| **0. Starting Point** | — | Capture feature description | ✅ After | `0-startpoint.md` |
| **0.1. Grill Me** | `grill-me` | Adversarial spec refinement | - | `0.1-grill-me.md` |
| **1. Specification** | `spec-extractor` | Extract requirements, edge cases, acceptance criteria | ✅ After | `1-specification.md` |
| **2. Architecture** | `system-designer`<br/>`tradeoff-analyzer` | Design system, evaluate alternatives | ✅ After | `2-architecture.md` |
| **3. Documentation** | `documentation-writer` | Update project docs | - | `3-feature-documentation.md` |
| **4. TDD Tests** | `test-generator` | Create failing tests | ✅ After | `4-unit-tests.md` |
| **5. Implementation** | `minimal-impl-generator`<br/>+ Engineer agents | Simplest solution to pass tests | - | `5-implementation.md` |
| **5.1. Analysis** | `multi-agent-analyzer` | Parallel code validation (quality, edge cases, regression) | - | `5.1-parallel-analysis.md` |
| **6. Integration & E2E** | `integration-test-generator` | Integration & E2E tests | - | `6-integration-tests.md` |
| **7. Refactor** | `refactor-optimizer` | Improve code quality | - | `7-refactoring.md` |
| **8. Code Review** | `code-reviewer` | Final quality check | - | `8-code-review.md` |
| **9. PR Creation** | `pr-creator` | Create pull request | Optional | `9-pr-creation.md` |

#### Context Rehydration

Before **every phase**, the workflow generates a 10-bullet summary:
- What was decided
- What assumptions were made
- What's still unclear
- Why certain choices were made

---

### Greenfield Workflow

**Agent**: [greenfield-workflow.agent.md](../agents/greenfield-workflow.agent.md)

**Use When**: Starting a new project from scratch, building a new application or service.

**Philosophy**: **Vision Before Code** — invest in understanding what you're building and break it into deliverable milestones before writing any code.

#### Phases

```
Phase 0: Starting Point & Vision
    ↓
Phase 0.1: Grill Me (vision refinement)
    ↓
Phase 1: Specification
    ↓
[✓ Checkpoint: Review & Approve Spec]
    ↓
Phase 2: Task Breakdown & Prioritization
    ↓
[✓ Checkpoint: Approve Milestones]
    ↓
Phase 3: Architecture & Design
    ↓
[✓ Checkpoint: Approve Architecture]
    ↓
Phase 4: Documentation
    ↓
Phase 5: Implementation (Milestone 1)
    ↓
[✓ Checkpoint: Demo Milestone 1]
    ↓
Phase 6: Validation & Refinement
    ↓
Phase 7: Code Review
    ↓
Phase 8: Next Steps & Handoff
```

| Phase | Skill | Purpose | Checkpoint | Output File |
|-------|-------|---------|------------|-------------|
| **0. Starting Point** | — | Capture project vision | ✅ After | `0-startpoint.md` |
| **0.1. Grill Me** | `grill-me` | Adversarial vision refinement | - | `0.1-grill-me.md` |
| **1. Specification** | `spec-extractor` | Extract requirements, edge cases, acceptance criteria | ✅ After | `1-specification.md` |
| **2. Task Breakdown** | `product-manager` | Epics, stories, MoSCoW prioritization, milestones | ✅ After | `2-task-breakdown.md` |
| **3. Architecture** | `system-designer`<br/>`tradeoff-analyzer` | Design system, evaluate alternatives, scaffold project | ✅ After | `3-architecture.md` |
| **4. Documentation** | `documentation-writer` | Create project docs (AGENTS.md, README, glossary) | - | `4-project-documentation.md` |
| **5. Implementation** | `test-generator`<br/>`minimal-impl-generator`<br/>+ Engineer agents | Implement Milestone 1 stories | ✅ After | `5-milestone-1.md` |
| **6. Validation** | `multi-agent-analyzer`<br/>`integration-test-generator`<br/>`refactor-optimizer` | Parallel analysis, integration tests, refactoring | - | `6-validation.md` |
| **7. Code Review** | `code-reviewer` | Comprehensive quality check | - | `7-code-review.md` |
| **8. Next Steps** | — | Summary, handoff for remaining milestones | - | `8-summary.md` |

#### Key Difference: Task Breakdown Phase

The greenfield workflow adds a **Task Breakdown** phase (Phase 2) between specification and architecture. This ensures:

1. **Milestone-driven delivery** — The project is broken into 2-4 milestones, each delivering usable value
2. **Prioritization before design** — MoSCoW prioritization ensures architecture focuses on what matters most
3. **Clear handoff path** — After Milestone 1, remaining milestones can be handled by the feature-workflow
4. **External tracking** — Optional sync to Notion, GitHub Issues, or Linear via MCP

#### After Greenfield: Continue with Feature Workflow

Once the greenfield workflow completes Milestone 1, the remaining milestones from the task breakdown should be implemented using the **feature-workflow** agent. Each milestone is essentially a feature with its own specification, architecture, and implementation cycle.

---

## Workflow Comparison

| Aspect | Bug | Improvement | Feature | Greenfield |
|--------|-----|-------------|---------|------------|
| **Philosophy** | Never jump to fix | Understand before changing | Design before code | Vision before code |
| **Starting point** | Something is broken | Working but suboptimal | New capability needed | New project from scratch |
| **Phase 1** | Component mapping | Component mapping + impact | Specification extraction | Specification extraction |
| **Phase 2** | Root cause analysis | Tradeoff analysis + design | Architecture design | Task breakdown & prioritization |
| **Phase 3** | Solution evaluation | Documentation | Documentation | Architecture & design |
| **Implementation** | Minimal patch (Phase 6) | Full implementation (Phase 5) | Full implementation (Phase 5) | Milestone 1 only (Phase 5) |
| **Unique skills** | root-cause-analyzer, solution-critic, patch-implementer, post-fix-reviewer | tradeoff-analyzer (primary), system-designer (design) | spec-extractor, refactor-optimizer | product-manager |
| **Checkpoints** | After root cause, after solution eval | After tradeoff & design | After spec, after architecture, after tests | After spec, after milestones, after architecture, after milestone 1 |
| **Total phases** | 9 (0-8) | 9 (0-8) | 10 (0-9) | 8 (0-8) |

---

## Skills

### Shared Skills (5)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [grill-me](../skills/grill-me/SKILL.md) | Adversarial spec refinement (Phase 0.1) | Refined understanding, resolved assumptions |
| [multi-agent-analyzer](../skills/multi-agent-analyzer/SKILL.md) | Parallel code validation (Phase 5.1/6.1) | 3-lane analysis report (quality, edge cases, regression) |
| [documentation-writer](../skills/documentation-writer/SKILL.md) | Documentation updates + ubiquitous language glossary | AGENTS.md, feature docs, architecture docs, glossary |
| [code-reviewer](../skills/code-reviewer/SKILL.md) | Comprehensive quality check | Security, performance, maintainability review |
| [btw](../skills/btw/SKILL.md) | Side questions without context pollution | Quick answer, no artifacts created |

### Feature Skills (7)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [spec-extractor](../skills/spec-extractor/SKILL.md) | Extract complete requirements | Functional/non-functional requirements, edge cases, acceptance criteria |
| [system-designer](../skills/system-designer/SKILL.md) | Design architecture | Domain model, API contracts, data model, simple text diagrams |
| [tradeoff-analyzer](../skills/tradeoff-analyzer/SKILL.md) | Compare alternatives | Comparison matrix, recommendation, failure scenarios |
| [test-generator](../skills/test-generator/SKILL.md) | Generate failing tests | Unit tests (AAA), integration tests, edge tests |
| [minimal-impl-generator](../skills/minimal-impl-generator/SKILL.md) | Simplest implementation | YAGNI code, happy path first, edge handling |
| [integration-test-generator](../skills/integration-test-generator/SKILL.md) | Integration & E2E tests | Integration tests, backward compatibility tests |
| [refactor-optimizer](../skills/refactor-optimizer/SKILL.md) | Code quality improvement | SOLID, DRY, performance, all tests still green |

### Bug Skills (5)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [component-mapper](../skills/component-mapper/SKILL.md) | Map affected code | Component list, dependency graph, data flow |
| [root-cause-analyzer](../skills/root-cause-analyzer/SKILL.md) | Find true root cause | Evidence-based root cause, alternatives, NO FIX |
| [solution-critic](../skills/solution-critic/SKILL.md) | Adversarial review | ≥2 failure modes, edge cases, security/performance concerns |
| [patch-implementer](../skills/patch-implementer/SKILL.md) | Minimal bug fix | Failing tests → minimal fix → addresses critique |
| [post-fix-reviewer](../skills/post-fix-reviewer/SKILL.md) | Verify fix works | Bug verified fixed, tests pass, no regressions |

### Improvement Skills (2)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [tradeoff-analyzer](../skills/tradeoff-analyzer/SKILL.md) | Evaluate approaches | Comparison matrix on Feasibility/Impact/Maintainability/Risk |
| [system-designer](../skills/system-designer/SKILL.md) | Design chosen approach | Migration strategy, backward compatibility plan |

### Greenfield Skills (1)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [product-manager](../skills/product-manager/SKILL.md) | Break down specs into actionable tasks | Epics, stories, MoSCoW prioritization, dependency map, milestones |

### Deployment Skills (1)

| Skill | Purpose | Key Output |
|-------|---------|------------|
| [deploy-to-staging](../skills/deploy-to-staging/SKILL.md) | Multi-repo deployment | Branch sync, conflict resolution, staging merge |

---

## Usage Examples

### Using the Workflow Router (Recommended)

```
@orchestrator Fix null pointer exception when user has no email
```

The router will:
1. Classify as "Bug" (keywords: fix, null pointer, exception)
2. Delegate to `@debug-workflow`
3. Bug workflow takes over from Phase 0

### Starting Bug Workflow Directly

```
@debug-workflow Fix null pointer exception when user has no email
```

The workflow will:
1. Capture bug description in `0-startpoint.md`
2. Grill the user on assumptions in `0.1-grill-me.md`
3. Map affected components
4. Analyze root cause (evidence-based, no fix proposed)
5. Ask for confirmation (never skips this)
6. Evaluate solutions with tradeoff analysis + adversarial critique
7. Ask for approval (must address blocking issues)
8. Update documentation
9. Generate failing tests
10. Implement minimal fix
11. Verify fix works and no regressions
12. Final code review

### Starting Improvement Workflow Directly

```
@improvement-workflow Optimize query performance on dashboard
```

The workflow will:
1. Capture improvement description in `0-startpoint.md`
2. Grill the user on scope and assumptions in `0.1-grill-me.md`
3. Map components and assess impact
4. Evaluate approaches with tradeoff analysis
5. Design chosen approach with migration strategy
6. Ask for approval at checkpoint
7. Update documentation
8. Generate tests for improvement + regression tests
9. Implement following approved design
10. Run integration tests
11. Final code review

### Starting Feature Workflow Directly

```
@feature-workflow Add discount code functionality to checkout flow
```

The workflow will:
1. Capture feature description in `0-startpoint.md`
2. Grill the user on requirements in `0.1-grill-me.md`
3. Extract requirements using `spec-extractor`
4. Ask for confirmation at checkpoint
5. Design architecture with `system-designer` and `tradeoff-analyzer`
6. Ask for approval at checkpoint
7. Update documentation
8. Generate failing tests
9. Ask for test approval at checkpoint
10. Hand off to engineer agents for implementation
11. Run integration & E2E tests
12. Refactor code
13. Final code review

### Starting Greenfield Workflow Directly

```
@greenfield-workflow Build a task management SaaS application
```

The workflow will:
1. Capture project vision in `0-startpoint.md`
2. Grill the user on vision and assumptions in `0.1-grill-me.md`
3. Extract requirements using `spec-extractor`
4. Ask for confirmation at checkpoint
5. Break down into epics, stories, and milestones using `product-manager`
6. Ask for milestone approval at checkpoint
7. Design architecture with `system-designer` and `tradeoff-analyzer`
8. Ask for architecture approval at checkpoint
9. Create project documentation
10. Implement Milestone 1 (smallest usable product)
11. Demo Milestone 1 at checkpoint
12. Validate, refactor, and review
13. Provide summary and handoff for remaining milestones

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

### 1. Workflow Artifact Tracking

**Problem**: Long workflows lose context and have no audit trail

**Solution**: Every phase produces a numbered file in `.ai-workflow/[feature-folder]/`

```
.ai-workflow/fix-null-pointer/
├── 0-startpoint.md
├── 0.1-grill-me.md
├── 1-component-map.md
├── 2-root-cause-analysis.md
├── 3-solution-evaluation.md
├── 4-solution-documentation.md
├── 5-tdd-tests.md
├── 6-fix-implementation.md
├── 7-post-fix-review.md
└── 8-pr-creation.md
```

**Phase-Scoped Naming**:
- `N-file-name.md` for the primary output of phase N
- `N.1-file-name.md`, `N.2-file-name.md` for extra files within the same phase
- Never bump to the next phase number for auxiliary files

**Feature Folder Naming**: Derived from git branch name:
- Strip ticket prefixes (e.g., `MW-123-`)
- Convert to kebab-case
- Truncate to 60 chars max

### 2. Context Rehydration

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

### 3. Grill Me (Phase 0.1)

**Problem**: Users often have unspoken assumptions and incomplete requirements

**Solution**: Adversarial questioning before any analysis begins

```markdown
## Grill Me Questions

### Q1: You say "optimize performance" — what's the current response time?
**Recommended Answer**: Measure current p50/p95/p99 latencies first
**Impact**: Defines the success criteria for the improvement

### Q2: Who are the consumers of this API?
**Recommended Answer**: Audit all callers before changing the interface
**Impact**: Determines backward compatibility requirements
```

**When**: Phase 0.1 in all three workflows (between startpoint and first analysis phase)

### 4. Parallel Code Analysis (Phase 5.1/6.1)

**Problem**: Single-perspective code review misses issues that other perspectives would catch

**Solution**: Run 3 parallel analysis lanes after implementation, before testing

```
Implementation Complete
    ↓
Lane 1: Code Quality & Maintainability
    ├─ Readability, naming, complexity
    ├─ DRY, SOLID violations
    └─ Dead code, error handling, type safety
    ↓
Lane 2: Edge Cases & Robustness
    ├─ Null/undefined, empty collections
    ├─ Boundary values, concurrency
    └─ Partial failures, idempotency
    ↓
Lane 3: Regression & Performance
    ├─ API contract changes, consumer impact
    ├─ Query performance, memory usage
    └─ CPU usage, network calls
    ↓
Synthesize → Fix critical issues → Proceed to testing
```

**When**: Phase 5.1 (improvement/feature) or Phase 6.1 (bug) in all workflows

**Key rule**: This is NOT testing — it's static code analysis. No test execution.

### 5. Uncertainty Handling

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

### 6. Manual Checkpoints

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

**Checkpoint Locations by Workflow**:

| Workflow | Checkpoints |
|----------|-------------|
| Bug | After root cause analysis, after solution evaluation |
| Improvement | After tradeoff analysis & design |
| Feature | After specification, after architecture, after TDD tests |

### 7. Never Jump to Fix (Bug Workflow Only)

**Problem**: Quick fixes address symptoms, not root causes

**Solution**: Enforce 3-phase investigation before any code changes

```
Bug Report
    ↓
Phase 1: Map Components
    ↓
Phase 2: Root Cause Analysis (NO FIX - Analysis Only)
    ↓
Phase 3: Evaluate & Critique Solution
    ↓
Approved?
    ├─→ Yes → Phase 6: Implement Fix
    └─→ No → Back to Phase 2
```

**Phase 2 Rule**: `root-cause-analyzer` skill **never proposes fixes**, only analyzes

### 8. Understand Before Changing (Improvement Workflow Only)

**Problem**: Modifying working code without understanding impact creates regressions

**Solution**: Enforce impact analysis and tradeoff evaluation before changes

```
Improvement Request
    ↓
Phase 1: Map Components + Assess Impact
    ↓
Phase 2: Tradeoff Analysis + Design (with migration strategy)
    ↓
Approved?
    ├─→ Yes → Phase 5: Implement
    └─→ No → Back to Phase 2
```

### 9. Adversarial Solution Critique (Bug Workflow Only)

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

### 10. TDD Cycle

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

### 11. Skill Composition

**Problem**: Complex tasks need multiple specialized capabilities

**Solution**: Orchestrator agents coordinate skills at appropriate phases

**Example - Bug Solution Evaluation (Phase 3)**:
```
1. Invoke `tradeoff-analyzer` skill
   → Evaluates 2-3 solution approaches on Feasibility/Impact/Maintainability/Risk
   
2. Invoke `solution-critic` skill  
   → Adversarial stress-test of recommended approach
   → Must find ≥2 failure modes

3. Present both to user at checkpoint
   → User approves or requests changes
```

**Example - Improvement Tradeoff & Design (Phase 2)**:
```
1. Invoke `tradeoff-analyzer` skill
   → Evaluates improvement approaches with weighted criteria
   
2. Invoke `system-designer` skill
   → Designs chosen approach with migration strategy
   → Plans backward compatibility

3. Present to user at checkpoint
   → User approves or requests changes
```

---

## Best Practices

### DO

- ✅ Use `@orchestrator` as your entry point for automatic classification
- ✅ Follow workflows in order (don't skip phases)
- ✅ Stop at checkpoints for approval
- ✅ Write tests before implementation
- ✅ Generate context summaries between phases
- ✅ Track confidence levels explicitly
- ✅ For bugs: find root cause before fixing
- ✅ For bugs: stress-test solution before implementing
- ✅ For improvements: evaluate tradeoffs before changing
- ✅ For improvements: assess impact on existing consumers
- ✅ For features: complete spec and architecture before coding

### DON'T

- ❌ Skip checkpoints to save time
- ❌ Implement before writing tests
- ❌ Proceed with low confidence (<70%)
- ❌ For bugs: jump straight to fix
- ❌ For bugs: fix symptoms instead of root cause
- ❌ For improvements: modify code without understanding impact
- ❌ For improvements: skip tradeoff analysis
- ❌ For features: start coding before spec is approved
- ❌ Ignore edge cases raised by skills
- ❌ Skip code review phase
