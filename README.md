# AI Prompts

Central repository of AI-powered development tools: orchestrator agents, specialized skills, and versioned prompt templates that can be linked to any project.

## Overview

This repository provides a **complete development workflow orchestration system** with:

- **4 Orchestrator Agents**: Workflow router + 3 specialized workflows (bug, improvement, feature)
- **17 Specialized Skills**: Requirements extraction, architecture design, TDD testing, adversarial grilling, parallel code analysis, code review, and more
- **Symlink-Based Distribution**: Single source of truth in `src/`, discoverable by AI tools via symlinks
- **Versioned Templates**: Langchain-compatible prompt templates in `prompts/`

## Quick Start

### Using in Your Project

Link this repository's tools to your project. Choose between automated setup or manual symlink creation:

**Option 1: Automated Setup (Recommended)**

```bash
# Clone this repo (if not already)
git clone <repo-url> ~/projects/personal/ai-prompts

# From your project directory
~/projects/personal/ai-prompts/create-symlink.sh
```

**Option 2: Manual Symlinks (Custom Paths)**

Create symlinks to any directory structure you prefer:

```bash
# For GitHub Copilot (agents in .github/agents/)
ln -s ~/projects/personal/ai-prompts/src/agents/* ~/path/to/your-project/.github/agents/

# For Claude Desktop (agents in .claude/agents/)
ln -s ~/projects/personal/ai-prompts/src/agents/* ~/path/to/your-project/.claude/agents/

# Link skills
ln -s ~/projects/personal/ai-prompts/src/skills/* ~/path/to/your-project/.github/skills/

# Link rules (for Claude Desktop)
ln -s ~/projects/personal/ai-prompts/src/rules/* ~/path/to/your-project/.claude/rules/
```

Replace `~/path/to/your-project` with your actual project path. This makes agents and skills discoverable by GitHub Copilot and Claude Desktop.

### Starting a Workflow

**Any task** (auto-routed):
```
@workflow-router Fix null pointer when user has no email
```

**New Feature**:
```
@feature-workflow Add discount code functionality to checkout
```

**Bug Fix**:
```
@bug-workflow Fix null pointer when user has no email
```

**Improvement**:
```
@improvement-workflow Optimize query performance on dashboard
```

See [Workflows Documentation](src/workflows/README.md) for detailed usage.

---

## Project Structure

```
ai-prompts/
├── src/                          # Single source of truth (edit here)
│   ├── agents/                   # Orchestrator and specialist agents
│   │   ├── workflow-router.agent.md          (Entry point: classifies & delegates)
│   │   ├── bug-workflow.agent.md             (9-phase bug fix workflow)
│   │   ├── improvement-workflow.agent.md     (9-phase improvement workflow)
│   │   ├── feature-workflow.agent.md         (9-phase feature development)
│   │   ├── backend-engineer.agent.md
│   │   ├── frontend-engineer.agent.md
│   │   └── doc-writter.agent.md
│   │
│   ├── skills/                   # Specialized capabilities
│   │   ├── grill-me/             (Adversarial spec refinement)
│   │   ├── spec-extractor/       (Requirements extraction)
│   │   ├── system-designer/      (Architecture design)
│   │   ├── tradeoff-analyzer/    (Alternative evaluation)
│   │   ├── feature-doc-writer/   (Documentation updates)
│   │   ├── tdd-test-generator/   (Test generation)
│   │   ├── minimal-impl-generator/ (Simple implementation)
│   │   ├── refactor-optimizer/   (Code improvement)
│   │   ├── component-mapper/     (Component analysis)
│   │   ├── root-cause-analyzer/  (Bug investigation)
│   │   ├── solution-critic/      (Adversarial review)
│   │   ├── patch-implementer/    (Minimal bug fix)
│   │   ├── post-fix-reviewer/    (Fix verification)
│   │   ├── code-reviewer/        (Quality assurance)
│   │   ├── deploy-to-staging/    (Multi-repo deployment)
│   │   └── README.md             (Skills documentation)
│   │
│   ├── workflows/                # Workflow documentation
│   │   └── README.md             (Complete workflow guide)
│   │
│   ├── prompts/                  # Versioned templates (future)
│   └── rules/                    # Development guidelines
│
├── .github/                      # Symlinks for GitHub Copilot discovery
│   ├── agents/                   # → src/agents/*
│   ├── skills/                   # → src/skills/*
│   └── prompts/                  # → src/prompts/*
│
├── .claude/                      # Symlinks for Claude Desktop discovery
│   └── rules/                    # → src/rules/*
│
├── prompts/                      # Langchain template registry
│   ├── registry.yaml
│   └── [template-name]/
│       └── v1.0.0/
│           ├── prompt.yaml
│           └── prompt.md
│
├── create-symlink.sh             # Link tools to your projects
└── README.md                     # This file
```

### Why This Structure?

**Single Source of Truth (`src/`)**:
- All files are authored and maintained in `src/`
- No duplication between `.github/` and `.claude/`
- Clear ownership and versioning

**Symlink Discovery**:
- `.github/` → GitHub Copilot discovers tools automatically
- `.claude/` → Claude Desktop discovers tools automatically
- Both point to the same source files in `src/`

**Versioned Templates**:
- `prompts/` contains Langchain-compatible templates
- Multiple versions can coexist
- `registry.yaml` tracks all available templates

---

## Development Workflows

This repository provides three specialized workflows, each with a dedicated orchestrator agent, plus a router for automatic classification:

### Workflow Router

**Single entry point** that classifies tasks and delegates to the correct workflow:

```
User Request → @workflow-router → Bug? → @bug-workflow
                                → Improvement? → @improvement-workflow
                                → Feature? → @feature-workflow
```

| Signal Keywords | Workflow |
|----------------|----------|
| broken, error, crash, null pointer, unexpected | Bug |
| optimize, refactor, improve, enhance, migrate | Improvement |
| new, add, create, build, implement | Feature |

### Bug Workflow

**9-phase evidence-based approach for fixing bugs**

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

**Critical Rule**: Never jump to fix — complete root cause analysis and solution evaluation first.

### Improvement Workflow

**9-phase tradeoff-aware approach for improving existing code**

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

**Critical Rule**: Understand before changing — evaluate tradeoffs and impact before modifying working code.

### Feature Workflow

**9-phase TDD approach for building new functionality**

```
Phase 0: Starting Point
    ↓
Phase 0.1: Grill Me (spec refinement)
    ↓
Phase 1: Specification
    ↓
[✓ Checkpoint: Review Spec]
    ↓
Phase 2: Architecture
    ↓
[✓ Checkpoint: Review Design]
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

**Critical Rule**: Design before code — complete specification and architecture before implementation.

### Shared Patterns

All three workflows share these patterns:

- **Workflow Artifact Tracking**: Every phase produces a numbered file under `.ai-workflow/[feature-folder]/`
- **Phase-Scoped Naming**: `N-file.md` for primary, `N.1-extra.md` for auxiliary files
- **Context Rehydration**: 10-bullet summaries between phases prevent context loss
- **Manual Checkpoints**: Critical decision points require human approval
- **Grill Me Phase**: Adversarial questioning refines understanding before work begins
```

**Phases**:
1. **Component Mapping**: Identify affected code
2. **Root Cause**: Evidence-based investigation (**NO FIX**)
3. **Solution Critique**: Adversarial stress-testing (find ≥2 failure modes)
4. **Documentation**: Update docs
5. **TDD Tests**: Generate failing tests
6. **Patch**: Minimal fix addressing critique
7. **Post-Fix Review**: Verify fix, check regressions

**Checkpoints**: After phases 2, 3 (manual approval required)

**Critical Rule**: Never jump to fix - complete phases 1-3 first

### Key Patterns

- **Manual Checkpoints**: Pause at critical decisions for human approval
- **Context Rehydration**: 10-bullet summaries between phases prevent context loss
- **Uncertainty Handling**: Explicit confidence scoring and missing information tracking
- **TDD Cycle**: Red (failing test) → Green (minimal code) → Refactor (optimize)
- **Adversarial Grilling**: Spec refinement through relentless questioning (Phase 0.1)
- **Adversarial Critique**: Actively search for failure modes before implementing (bug workflow)
- **Tradeoff Analysis**: Evaluate approaches on Feasibility/Impact/Maintainability/Risk (improvement workflow)
- **Workflow Artifacts**: Persistent numbered files in `.ai-workflow/` for audit trail and context rehydration

See [Workflows Documentation](src/workflows/README.md) for complete details.

---

## Skills

15 specialized skills provide focused capabilities:

### Shared Skills (3)

| Skill | Purpose |
|-------|---------|
| [grill-me](src/skills/grill-me/SKILL.md) | Adversarial spec refinement — question assumptions before work begins |
| [multi-agent-analyzer](src/skills/multi-agent-analyzer/SKILL.md) | Parallel code validation from 3 perspectives (quality, edge cases, regression) |
| [feature-doc-writer](src/skills/feature-doc-writer/SKILL.md) | Update AGENTS.md, feature docs, architecture docs, ubiquitous language glossary |
| [code-reviewer](src/skills/code-reviewer/SKILL.md) | Comprehensive security, performance, quality review |
| [btw](src/skills/btw/SKILL.md) | Ask side questions without polluting workflow context |

### Feature Skills (5)

| Skill | Purpose |
|-------|---------|
| [spec-extractor](src/skills/spec-extractor/SKILL.md) | Extract requirements, edge cases, acceptance criteria |
| [system-designer](src/skills/system-designer/SKILL.md) | Design architecture with domain model, APIs, data model |
| [tradeoff-analyzer](src/skills/tradeoff-analyzer/SKILL.md) | Compare technical alternatives with scoring |
| [tdd-test-generator](src/skills/tdd-test-generator/SKILL.md) | Generate failing tests (Red phase of TDD) |
| [minimal-impl-generator](src/skills/minimal-impl-generator/SKILL.md) | Simplest implementation (Green phase of TDD) |
| [refactor-optimizer](src/skills/refactor-optimizer/SKILL.md) | Code quality improvement (Refactor phase of TDD) |
| [integration-test-generator](src/skills/integration-test-generator/SKILL.md) | Integration & E2E test generation |

### Bug Skills (4)

| Skill | Purpose |
|-------|---------|
| [component-mapper](src/skills/component-mapper/SKILL.md) | Map affected components, dependencies, data flow |
| [root-cause-analyzer](src/skills/root-cause-analyzer/SKILL.md) | Evidence-based root cause analysis (never proposes fix) |
| [solution-critic](src/skills/solution-critic/SKILL.md) | Adversarial stress-testing (must find ≥2 failure modes) |
| [patch-implementer](src/skills/patch-implementer/SKILL.md) | Minimal bug fix addressing critique feedback |
| [post-fix-reviewer](src/skills/post-fix-reviewer/SKILL.md) | Verify fix works, no regressions |

### Improvement Skills (2)

| Skill | Purpose |
|-------|---------|
| [tradeoff-analyzer](src/skills/tradeoff-analyzer/SKILL.md) | Evaluate approaches on Feasibility/Impact/Maintainability/Risk |
| [system-designer](src/skills/system-designer/SKILL.md) | Design chosen approach with migration strategy |

### Deployment Skills (1)

| Skill | Purpose |
|-------|---------|
| [deploy-to-staging](src/skills/deploy-to-staging/SKILL.md) | Multi-repo branch sync and staging deployment |

See [Skills Documentation](src/skills/README.md) for detailed information.

---

## Agents

### Orchestrator Agents (4)

- **[workflow-router](src/agents/workflow-router.agent.md)**: Entry point — classifies tasks as bug/improvement/feature and delegates
- **[bug-workflow](src/agents/bug-workflow.agent.md)**: 9-phase bug fix workflow with root cause analysis and solution evaluation
- **[improvement-workflow](src/agents/improvement-workflow.agent.md)**: 9-phase improvement workflow with tradeoff analysis and design
- **[feature-workflow](src/agents/feature-workflow.agent.md)**: 9-phase feature development workflow with TDD

### Specialist Agents (5)

- **[backend-engineer](src/agents/backend-engineer.agent.md)**: Backend implementation (NestJS, TypeScript)
- **[frontend-engineer](src/agents/frontend-engineer.agent.md)**: Frontend implementation (React, TypeScript)
- **[doc-writter](src/agents/doc-writter.agent.md)**: Documentation generation
- **[breakdown-task](src/agents/breakdown-task.agent.md)**: Complex problem analysis
- **[requirements-extractor](src/agents/requirements-extractor.agent.md)**: Requirements extraction

---

## Installation & Usage

### 1. Clone Repository

```bash
git clone <repo-url> ~/projects/personal/ai-prompts
cd ~/projects/personal/ai-prompts
```

### 2. Link to Your Project

Choose between automated setup or manual symlink creation:

**Option A: Automated Setup**

From your project directory:

```bash
~/projects/personal/ai-prompts/create-symlink.sh
```

This automatically creates:
- `.github/agents/` → symlinks to `src/agents/`
- `.github/skills/` → symlinks to `src/skills/`
- `.github/prompts/` → symlinks to `src/prompts/`
- `.claude/rules/` → symlinks to `src/rules/`

**Option B: Manual Symlinks (Custom Locations)**

Create symlinks to any directory you prefer:

```bash
# Example: Link to .claude/agents/ instead of .github/agents/
ln -s ~/projects/personal/ai-prompts/src/agents/* ~/path/to/your-project/.claude/agents/

# Example: Link to custom directory structure
ln -s ~/projects/personal/ai-prompts/src/skills/* ~/path/to/your-project/.ai/skills/

# Example: Link to multiple projects from one location
ln -s ~/projects/personal/ai-prompts/src/agents/* ~/work/project-a/.github/agents/
ln -s ~/projects/personal/ai-prompts/src/agents/* ~/work/project-b/.github/agents/
```

**Common Directory Patterns:**

| AI Tool | Agents Discovery Path | Skills Discovery Path |
|---------|----------------------|----------------------|
| GitHub Copilot | `.github/agents/` | `.github/skills/` |
| Claude Desktop | `.claude/agents/` | `.claude/skills/` |
| Custom | Any path you choose | Any path you choose |

Replace `~/path/to/your-project` with your actual project path.

### 3. Verify Symlinks

```bash
ls -la .github/agents/
# Should show symlinks pointing to ~/projects/personal/ai-prompts/src/agents/*

ls -la .github/skills/
# Should show symlinks pointing to ~/projects/personal/ai-prompts/src/skills/*
```

### 4. Use Workflows

**GitHub Copilot**:
```
@feature-workflow Add user profile picture upload
```

**Claude Desktop**:
```
@feature-workflow Add user profile picture upload
```

---

## Development

### Adding New Skills

1. **Create skill directory**: `mkdir -p src/skills/new-skill`
2. **Write SKILL.md**: Follow [skills.instructions.md](.claude/rules/skills.instructions.md)
3. **Test skill**: Create test prompts and validate output
4. **Create symlink**: `ln -s ../../src/skills/new-skill .github/skills/`
5. **Update registry**: Add entry to `prompts/registry.yaml`

See [Skills Documentation](src/skills/README.md) for detailed guidelines.

### Modifying Workflows

1. **Edit source**: Modify `src/agents/[workflow].agent.md`
2. **Test workflow**: Run through example scenarios
3. **Update docs**: Reflect changes in `src/workflows/README.md`
4. **Commit changes**: Symlinks automatically reflect updates

### Creating Versioned Templates

1. **Create version directory**: `mkdir -p prompts/skill-name/v1.0.0`
2. **Write prompt.yaml**: Langchain-compatible format
3. **Write prompt.md**: Human-readable template
4. **Update registry**: Add entry to `prompts/registry.yaml`

---

## Architecture Decisions

### Why Symlinks?

**Problem**: AI tools (GitHub Copilot, Claude Desktop) discover files in specific locations (`.github/`, `.claude/`)

**Challenge**: Need single source of truth without duplication

**Solution**: 
- Store all files in `src/` (version controlled, single source of truth)
- Create symlinks in `.github/` and `.claude/` for tool discovery
- Both tools see the same files, zero duplication

**Benefits**:
- ✅ Edit once, available everywhere
- ✅ No synchronization issues
- ✅ Clear ownership (everything lives in `src/`)
- ✅ Works across projects (symlink to any project)

### Why Separate Orchestrator and Specialist Agents?

**Orchestrators**: Handle workflow logic, checkpoints, context rehydration
**Specialists**: Handle implementation details (backend, frontend, docs)

**Benefits**:
- ✅ Orchestrators focus on "when" and "what"
- ✅ Specialists focus on "how"
- ✅ Specialists reusable across workflows
- ✅ Clear separation of concerns

### Why 3 Separate Workflows Instead of 1?

**Alternative Considered**: 1 generic workflow with conditional phases

**We Chose**: 3 specialized workflows (bug, improvement, feature) because:
- ✅ Single responsibility → each workflow is focused and clear
- ✅ Different core philosophies (evidence vs tradeoff vs design)
- ✅ Different phase sequences (root cause vs tradeoff analysis vs spec extraction)
- ✅ Easier to maintain and evolve independently
- ✅ Router agent handles classification automatically

### Why 15 Granular Skills Instead of 4 Broad Skills?

**Alternative Considered**: 4 broad skills (analyze, design, implement, review)

**We Chose**: 13 granular skills because:
- ✅ Single responsibility → easier to maintain
- ✅ Precise triggering → less ambiguity
- ✅ Reusable across workflows → composition
- ✅ Explicit process → better quality
- ✅ Easier to test → smaller surface area

---

## Troubleshooting

### Tools Not Discovering Skills

**Cause**: Symlinks not created or broken

**Solution**:
```bash
# Re-run symlink script
~/projects/personal/ai-prompts/create-symlink.sh

# Verify symlinks
find .github .claude -type l -exec test ! -e {} \; -print
# Should output nothing (no broken links)
```

### Workflow Stuck at Checkpoint

**Cause**: Missing information or low confidence (<70%)

**Solution**:
1. Review uncertainty assessment in checkpoint output
2. Provide missing information
3. Answer clarifying questions
4. If justified, request checkpoint skip

### Skill Not Triggering

**Cause**: Skill description doesn't match user request

**Solution**:
1. Review skill description in SKILL.md frontmatter
2. Add missing keywords or contexts
3. Test with realistic prompts

See [Workflows Documentation](src/workflows/README.md#troubleshooting) for more.

---

## Contributing

### Guidelines

1. **Edit in `src/` only**: Never edit files in `.github/` or `.claude/` directly
2. **Follow patterns**: Study existing agents/skills before creating new ones
3. **Test thoroughly**: Create test prompts and validate outputs
4. **Document changes**: Update relevant README files
5. **Version templates**: Use semantic versioning for prompt templates

### Pull Request Checklist

- [ ] Changes made in `src/` (not in `.github/` or `.claude/`)
- [ ] Tests created (for new skills)
- [ ] Documentation updated (README files)
- [ ] Symlinks verified (no broken links)
- [ ] Version bumped (if applicable)
V
---

## Documentation

- **[AI Concepts & Best Practices](docs/ai-concepts.md)**: Onboarding guide for engineers new to AI-assisted development (LLMs, agents, skills, context windows, prompt engineering, common pitfalls)
- **[Workflows README](src/workflows/README.md)**: Complete workflow guide with diagrams, examples, best practices
- **[Skills README](src/skills/README.md)**: Skill interactions, patterns, development guide
- **[Skills Instructions](.claude/rules/skills.instructions.md)**: Detailed skill creation guide
- **Individual Skills**: Each skill has detailed SKILL.md with process, examples, evals

---

## Version History

- **v2.1.0** (2025-05-07): P2 enhancements
  - Added `multi-agent-analyzer` skill for parallel code validation (quality, edge cases, regression)
  - Added Phase 5.1/6.1 parallel analysis to all workflows (after implementation, before testing)
  - Added `btw` skill for side questions without context pollution
  - Added ubiquitous language glossary to `feature-doc-writer` skill
  - 17 specialized skills (7 feature, 5 bug, 2 improvement, 5 shared, 1 deployment)

- **v2.0.0** (2025-05-04): Three-workflow architecture
  - 4 orchestrator agents (workflow-router, bug-workflow, improvement-workflow, feature-workflow)
  - Split improvement-workflow into bug-workflow (root cause → minimal fix) and improvement-workflow (tradeoff analysis → full implementation)
  - Added workflow-router for automatic task classification
  - Added grill-me skill as Phase 0.1 in all workflows
  - Added deploy-to-staging skill for multi-repo deployment
  - Added integration-test-generator skill
  - Workflow artifact tracking with `.ai-workflow/[feature-folder]/`
  - Phase-scoped artifact naming (N-file.md, N.1-extra.md)
  - Enhanced startpoint template with structured sections
  - 15 specialized skills (7 feature, 5 bug, 2 improvement, 3 shared, 1 deployment)

- **v1.0.0** (2024-03-09): Initial implementation
  - 2 orchestrator agents (feature-workflow, improvement-workflow)
  - 13 specialized skills (7 feature, 5 bugfix, 1 shared)
  - 5 specialist agents (backend, frontend, doc, breakdown, requirements)
  - Symlink-based distribution system
  - Comprehensive workflow documentation
  - Manual checkpoints and context rehydration
  - Uncertainty handling protocols

---

## License

[Add your license here]

---

## Questions?

- **Workflow Usage**: See [Workflows README](src/workflows/README.md)
- **Skill Development**: See [Skills Instructions](.claude/rules/skills.instructions.md)
- **Skill Details**: See [Skills README](src/skills/README.md)
- **Project Structure**: See [Project Structure](#project-structure) above