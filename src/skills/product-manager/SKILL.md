---
name: product-manager
description: Break down specifications into actionable tasks with priorities, dependencies, and timelines. Use when specs are approved and work needs to be organized, when creating a project plan from requirements, when breaking epics into stories, or when setting up task tracking. Produces concise task breakdowns with MoSCoW prioritization, dependency maps, and effort estimates. Keywords project management, task breakdown, sprint planning, prioritization, stories, epics, roadmap, MoSCoW, effort estimation, dependencies, project plan.
---

# Product Manager

Break down approved specifications into an actionable, prioritized task plan. This skill converts requirements into a concise work breakdown that teams can execute immediately.

## When to Use This Skill

- After specification extraction (spec is approved)
- After architecture design is approved
- Breaking epics into implementable stories
- Prioritizing work for a sprint or milestone
- Setting up project tracking (Notion, GitHub Issues, etc.)
- When the user asks "what should we build first?" or "how do we break this down?"

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Greenfield Workflow Phase 2**: Produces `.ai-workflow/[project-folder]/2-task-breakdown.md`
- **Feature Workflow** (optional): Produces `.ai-workflow/[feature-folder]/2.1-task-breakdown.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, and `1-specification.md` before breaking down tasks. If architecture exists (`2-architecture.md`), read it for technical context on dependencies.

## Process

### Step 1: Load Context

Read all prior workflow artifacts:

- `0-startpoint.md` — original goal and constraints
- `0.1-grill-me.md` — refined understanding
- `1-specification.md` — approved requirements
- `2-architecture.md` — if available, for technical dependency info

### Step 2: Identify Epics

Group related requirements into 2-5 epics. Each epic should:

- Represent a cohesive chunk of user value
- Be deliverable independently (as much as possible)
- Have a clear name and one-line goal

**Format**:

```
EPIC-[N]: [Name]
Goal: [One-line outcome]
Requirements: REQ-X, REQ-Y, REQ-Z
```

### Step 3: Break Epics into Stories

For each epic, create implementable stories. Each story should:

- Deliver a single piece of user value
- Be completable in 1-3 days
- Have clear acceptance criteria (tied to requirements)

**Format**:

```
STORY-[EPIC].[N]: [Title]
Epic: EPIC-[X]
Requirements: REQ-Y
Acceptance Criteria:
  - [Measurable, testable condition]
  - [Measurable, testable condition]
Effort: [S/M/L] ([1/2/3] days)
Dependencies: [None | STORY-X.Y]
```

### Step 4: Prioritize with MoSCoW

Apply MoSCoW prioritization to stories:

- **Must Have** — Core value proposition, blocks release
- **Should Have** — Important but workarounds exist
- **Could Have** — Nice to have if time permits
- **Won't Have** — Explicitly out of scope for this iteration

**Rules**:

- Must Have ≤ 40% of total stories (enforce ruthless prioritization)
- Every Must Have story must have a clear "why it blocks release" reason
- Won't Have stories need a brief rationale

### Step 5: Map Dependencies

Create a dependency graph showing execution order:

```
STORY-1.1 → STORY-1.2 → STORY-1.3
                      ↘ STORY-2.1 → STORY-2.2
STORY-1.1 → STORY-3.1
```

Identify:

- **Critical path**: Longest dependency chain (determines minimum timeline)
- **Parallel tracks**: Stories that can run simultaneously
- **Blocking stories**: Stories that unblock the most other work

### Step 6: Estimate Effort

Provide lightweight effort estimates:

| Size | Days | Description                                |
| ---- | ---- | ------------------------------------------ |
| S    | 1    | Single component, clear implementation     |
| M    | 2    | Multiple components, some design decisions |
| L    | 3    | Cross-cutting, integration work, unknowns  |

**Total estimate**: Sum of story efforts, with a 1.3x buffer for unknowns.

### Step 7: Define Milestones

Group stories into 2-4 milestones based on dependencies and value:

```
Milestone 1: [Name] ([X] days)
  Must Have stories that form the smallest usable product
  → Delivers: [What the user can do after this milestone]

Milestone 2: [Name] ([X] days)
  Remaining Must Have + high-priority Should Have
  → Delivers: [What the user can do after this milestone]

Milestone 3: [Name] ([X] days)
  Should Have + Could Have
  → Delivers: [Complete experience]
```

### Step 8: External Tracking (Optional)

If the user wants to sync tasks to an external tool (Notion, GitHub Issues, Linear, etc.):

1. Ask which tool they use
2. If an MCP server is available for that tool, offer to create tasks directly
3. Link each created task back to the spec file for traceability
4. Confirm the structure matches the breakdown before creating

## Output

Save to `.ai-workflow/[folder]/2-task-breakdown.md` (or `2.1-task-breakdown.md` for feature workflow):

```markdown
# Task Breakdown: [Project/Feature Name]

**Source Spec**: 1-specification.md
**Total Stories**: [N]
**Estimated Effort**: [X] days (with buffer: [Y] days)

## Epics

### EPIC-1: [Name]

Goal: [One-line outcome]
Requirements: REQ-X, REQ-Y

### EPIC-2: [Name]

Goal: [One-line outcome]
Requirements: REQ-Z

## Stories

### EPIC-1: [Name]

| Story | Title   | Priority | Effort | Dependencies |
| ----- | ------- | -------- | ------ | ------------ |
| 1.1   | [Title] | Must     | S      | None         |
| 1.2   | [Title] | Must     | M      | 1.1          |
| 1.3   | [Title] | Should   | S      | 1.1          |

### EPIC-2: [Name]

| Story | Title   | Priority | Effort | Dependencies |
| ----- | ------- | -------- | ------ | ------------ |
| 2.1   | [Title] | Must     | L      | 1.1          |
| 2.2   | [Title] | Should   | M      | 2.1          |

## Dependency Graph

[Visual dependency map]

**Critical Path**: STORY-1.1 → STORY-1.2 → STORY-2.1 → STORY-2.2 ([X] days)
**Parallel Tracks**: STORY-1.3 can run alongside STORY-2.1

## Milestones

### Milestone 1: [Name] ([X] days)

- STORY-1.1, STORY-1.2
- → Delivers: [User capability]

### Milestone 2: [Name] ([X] days)

- STORY-2.1, STORY-2.2, STORY-1.3
- → Delivers: [User capability]

## Priority Summary

| Priority | Count | Stories |
| -------- | ----- | ------- |
| Must     | [N]   | [List]  |
| Should   | [N]   | [List]  |
| Could    | [N]   | [List]  |
| Won't    | [N]   | [List]  |

## Open Questions

- [Questions that affect task breakdown]
```

## Principles

- **Concise over comprehensive**: The breakdown should be scannable in 2 minutes, not a 10-page document
- **Actionable over abstract**: Every story should be implementable without further decomposition
- **Ruthless prioritization**: If everything is Must, nothing is Must
- **Dependencies are facts**: Don't invent dependencies that don't exist, but don't miss real ones
- **Estimates are guides**: Acknowledge uncertainty, use ranges not point values
