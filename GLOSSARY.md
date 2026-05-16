# AI Development Workflow Glossary

## Core Concepts

### Orchestration Model
A **hierarchical agent system** where work flows through three layers:
1. **Orchestrator** (router) - Entry point that classifies tasks
2. **Workflow Agents** (coordinators) - Sequence phases for specific task types
3. **Skills** (workers) - Execute focused, single-responsibility operations

### Workflow Artifact
Numbered files stored in `.ai-workflow/[task-name]/` that document decisions and outputs from each workflow phase (e.g., `01-requirements.md`, `02-architecture.md`).

### Context Rehydration
10-bullet summary at the start of each phase to prevent context loss across multi-turn conversations.

### Manual Checkpoint
Critical decision point requiring explicit human approval before proceeding (e.g., after root cause analysis, before implementation).

---

## Agents

### Orchestrator Agents

**Current Name** | **Proposed Name** | **Role** | **When to Use**
---|---|---|---
`orchestrator` | `orchestrator` | Entry point that classifies task type and delegates to specialized workflows | Any task when workflow type is unclear
`debug-workflow` | `debug-workflow` | Coordinates 9-phase bug fix process | Something is broken, errors occur, unexpected behavior
`improvement-workflow` | `enhancement-workflow` | Coordinates 9-phase code improvement process | Existing code works but needs optimization/refactoring
`feature-workflow` | `feature-workflow` | Coordinates 10-phase new feature development | Building new functionality from scratch
`greenfield-workflow` | `greenfield-workflow` | Coordinates 8-phase new project creation | Starting entirely new project/application

### Specialist Agents

**Current Name** | **Proposed Name** | **Role** | **Specialization**
---|---|---|---
`backend-engineer` | `backend-engineer` | Implements backend code following NestJS best practices | Node.js, NestJS, APIs, databases
`frontend-engineer` | `frontend-engineer` | Implements frontend code following React best practices | React, TypeScript, UI components
`documentation-writer` ⚠️ | `documentation-writer` | Creates and maintains project documentation | Technical writing, README files

---

## Skills

### Shared Skills (All Workflows)

**Current Name** | **Proposed Name** | **Purpose** | **Phase**
---|---|---|---
`grill-me` | `requirements-clarifier` | Adversarial questioning to refine vague requirements | Phase 0.1 (all workflows)
`multi-agent-analyzer` | `parallel-validator` | Three-perspective code validation (quality, edge cases, regression) | Phase 5.1/6.1 (all workflows)
`documentation-writer` | `documentation-writer` | Updates AGENTS.md, feature docs, ubiquitous language glossary | Phase 3 (all workflows)
`code-reviewer` | `code-reviewer` | Security, performance, quality review before merge | Phase 6/7 (all workflows)
`btw` | `quick-answer` | Answers side questions without polluting workflow context | Ad-hoc (any workflow)

### Feature Workflow Skills

**Current Name** | **Proposed Name** | **Purpose** | **When Used**
---|---|---|---
`spec-extractor` | `spec-extractor` | Extracts requirements, edge cases, acceptance criteria | Phase 1 (Feature)
`system-designer` | `architect` | Designs domain model, APIs, data model, diagrams | Phase 2 (Feature, Improvement)
`tradeoff-analyzer` | `tradeoff-analyzer` | Evaluates alternatives and provides recommendations | Phase 2 (Feature, Bug, Improvement)
`test-generator` | `test-generator` | Generates failing unit/integration tests (TDD red phase) | Phase 4 (all workflows)
`minimal-impl-generator` | `implementation-generator` | Creates simplest working implementation (TDD green phase) | Phase 5 (Feature, Improvement)
`integration-test-generator` | `integration-tester` | Generates integration & E2E tests | Phase 5.2 (Feature, Improvement)
`refactor-optimizer` | `code-optimizer` | Refactors for SOLID, DRY, performance (TDD refactor phase) | Phase 5.3 (Feature)

### Bug Workflow Skills

**Current Name** | **Proposed Name** | **Purpose** | **When Used**
---|---|---|---
`component-mapper` | `component-analyzer` | Identifies affected components and dependencies | Phase 1 (Bug, Improvement)
`root-cause-analyzer` | `root-cause-analyzer` | Evidence-based investigation to find bug's true cause | Phase 2 (Bug)
`solution-critic` | `solution-validator` | Stress-tests proposed fix for failure modes and edge cases | Phase 3 (Bug)
`patch-implementer` | `patch-generator` | Implements minimal, targeted bug fix | Phase 5 (Bug)
`post-fix-reviewer` | `fix-validator` | Verifies fix works and causes no regressions | Phase 6 (Bug)

### Greenfield Workflow Skills

**Current Name** | **Proposed Name** | **Purpose** | **When Used**
---|---|---|---
`product-manager` | `product-planner` | Breaks down tasks, prioritizes, creates milestones | Phase 3 (Greenfield, optional Feature)

### Utility Skills

**Current Name** | **Proposed Name** | **Purpose** | **When Used**
---|---|---|---
`agents-md-generator` | `agent-documenter` | Generates AGENTS.md file documenting all agents | After creating/updating agents
`pr-creator` | `pr-creator` | Creates GitHub pull requests with proper metadata | Phase 7/8 (all workflows, optional)
`deploy-to-staging` | `staging-deployer` | Deploys code to staging environment | Phase 8 (optional)
`debug-issue` | ❓ | (Review if redundant with debug-workflow) | TBD

---

## Naming Conventions

### Agent Naming Pattern
```
[domain]-[role]
```
- **Domain**: `workflow`, `backend`, `frontend`, `documentation`
- **Role**: `orchestrator`, `engineer`, `writer`
- **Examples**: `workflow-orchestrator`, `backend-engineer`, `documentation-writer`

### Skill Naming Pattern
```
[action]-[object]
```
- **Action**: `clarify`, `extract`, `generate`, `analyze`, `validate`, `optimize`
- **Object**: `requirements`, `tests`, `components`, `code`, `fix`
- **Examples**: `requirements-clarifier`, `test-generator`, `code-optimizer`

### File Naming Pattern
- **Agents**: `[name].agent.md` (e.g., `orchestrator.agent.md`)
- **Skills**: `[name]/SKILL.md` (e.g., `test-generator/SKILL.md`)
- **Workflows**: `[name]-workflow.agent.md` (e.g., `dedebug-workflow.agent.md`)

---

## Architectural Patterns

### Hierarchical Orchestration
```
User Request
    ↓
Orchestrator (classifies)
    ↓
Workflow Agent (coordinates phases)
    ↓
Skills (execute tasks)
```

**Benefits:**
- ✅ Clear separation of concerns
- ✅ Reusable skills across workflows
- ✅ Easy to add new workflows
- ✅ Centralized routing logic

### Workflow Phases
Each workflow follows a structured phase sequence:

**Debug Workflow (9 phases)**
```
0.1 Requirements Clarification → 1 Component Mapping → 2 Root Cause Analysis → 
3 Tradeoff + Solution Validation → 4 Documentation → 5 Test Generation → 
6 Patch Implementation → 7 Fix Validation + Code Review → 8 PR Creation (optional)
```

**Feature Workflow (10 phases)**
```
0.1 Requirements Clarification → 1 Spec Extraction → 2 System Design + Tradeoff → 
3 Documentation → 4 Test Generation → 5 Implementation → 5.2 Integration Tests → 
5.3 Code Optimization → 6 Code Review → 7 PR Creation (optional)
```

**Enhancement Workflow (9 phases)**
```
0.1 Requirements Clarification → 1 Component Mapping → 2 Tradeoff + System Design → 
3 Documentation → 4 Test Generation → 5 Implementation → 5.2 Integration Tests → 
6 Code Review → 7 PR Creation (optional)
```

**Greenfield Workflow (8 phases)**
```
0.1 Requirements Clarification → 1 Spec Extraction → 2 Product Planning → 
3 System Design + Tradeoff → 4 Documentation → 5 Test Generation → 
6 Setup + Implementation → 7 Review
```

### TDD Workflow
All workflows follow **Test-Driven Development**:
1. **Red** - Write failing tests (`test-generator`)
2. **Green** - Minimal implementation to pass (`implementation-generator` or `patch-generator`)
3. **Refactor** - Optimize while keeping tests green (`code-optimizer`)

---

## Industry Alignment

### Roo Code Modes Mapping

**Roo Code Mode** | **Our Agent** | **Alignment Notes**
---|---|---
🪃 Orchestrator | `orchestrator` | Entry point, delegates via classification
💻 Code | `feature-workflow`, `enhancement-workflow` | Full implementation workflows
🪲 Debug | `debug-workflow` | Systematic bug investigation and fixing
🏗️ Architect | `system-designer` (skill) | System design and architecture
❓ Ask | `quick-answer` (skill) | Read-only Q&A without modifications

### Tool Access Levels

**Level** | **Permissions** | **Our Usage**
---|---|---
**Read-only** | `read`, `mcp` | `quick-answer`, early analysis phases
**Planning** | `read`, `mcp`, `edit` (markdown only) | Documentation skills, spec extraction
**Full access** | `read`, `edit`, `command`, `mcp` | Implementation skills, code generation
**Orchestrator** | `new_task` only | Workflow agents (delegate to skills)

---

## Migration Guide

### Recommended Renamings (Priority Order)

#### High Priority (Breaking Changes)
1. ✅ `orchestrator` → `orchestrator`
2. ✅ `documentation-writer` → `documentation-writer` (fixes typo)
3. ✅ `debug-workflow` → `debug-workflow` (industry alignment)
4. ✅ `grill-me` → `requirements-clarifier` (professional naming)

#### Medium Priority (Clarity Improvements)
5. ✅ `btw` → `quick-answer`
6. ✅ `documentation-writer` → `documentation-writer` (merge with doc-writer)
7. ✅ `improvement-workflow` → `enhancement-workflow`
8. ✅ `minimal-impl-generator` → `implementation-generator`

#### Low Priority (Optional Enhancements)
9. ✅ `test-generator` → `test-generator`
10. ✅ `pr-creator` → `pr-creator`
11. ✅ `agents-md-generator` → `agent-documenter`
12. ✅ `component-mapper` → `component-analyzer`

### Deprecation Plan
1. Mark old names as deprecated in documentation
2. Add aliases in agent descriptions for backward compatibility
3. Update all references in workflow documentation
4. Create migration script for existing projects
5. Remove deprecated names in next major version

---

## Cross-Repository Sharing

### Distribution Strategies

**Strategy** | **Pros** | **Cons** | **Best For**
---|---|---|---
Git Submodules | Version controlled, integrated with Git | Manual updates, complexity | Teams familiar with submodules
NPM Package | Semantic versioning, easy updates | Publishing overhead | Enterprise adoption
MCP Server | Dynamic updates, single source of truth | Infrastructure required | Organizations with MCP setup
Template Sync | Simple, allows customization | Can drift over time | Small teams, prototyping

### Recommended Structure
```
@yourcompany/ai-workflows/
├── package.json
├── agents/
│   ├── orchestrator.agent.md
│   ├── dedebug-workflow.agent.md
│   ├── feature-workflow.agent.md
│   └── enhancement-workflow.agent.md
├── skills/
│   ├── requirements-clarifier/
│   ├── test-generator/
│   ├── code-reviewer/
│   └── ...
└── docs/
    ├── GLOSSARY.md
    └── README.md
```

---

## Quick Reference

### Agent Invocation
```bash
@orchestrator [any task description]        # Auto-routes to correct workflow
@debug-workflow [bug description]           # Systematic bug fixing
@feature-workflow [feature description]     # New feature development
@enhancement-workflow [improvement goal]    # Code optimization/refactoring
@greenfield-workflow [project idea]         # New project from scratch
```

### Skill Invocation (within workflows)
Skills are invoked automatically by workflow agents but can be called directly:
```bash
@requirements-clarifier [vague requirements]
@test-generator [specification]
@code-reviewer [pull request]
```

### Common Terminology

**Term** | **Definition**
---|---
**Orchestrator** | Top-level agent that routes tasks to specialized workflows
**Workflow** | Multi-phase process for a specific task type (debug, feature, etc.)
**Skill** | Single-responsibility capability invoked by workflows
**Phase** | Numbered step in a workflow with specific inputs/outputs
**Artifact** | Document produced by a phase, stored in `.ai-workflow/`
**Checkpoint** | Manual approval point before proceeding to next phase
**TDD** | Test-Driven Development: Red (test) → Green (implement) → Refactor
**Context Rehydration** | 10-bullet summary to restore context at phase start

---

## Glossary Maintenance

This glossary is the **single source of truth** for naming conventions and architectural patterns.

**Update this glossary when:**
- Adding new agents or skills
- Renaming existing components
- Changing workflow phase sequences
- Aligning with industry standards
- Adopting new architectural patterns

**Location:** `/GLOSSARY.md` in the root of this repository.

**Last Updated:** {{ date }}
**Maintained By:** Engineering team
