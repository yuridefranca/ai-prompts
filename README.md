# AI Prompts

Central repository of AI-powered development tools: orchestrator agents, specialized skills, and versioned prompt templates that can be linked to any project.

## Overview

This repository provides a **complete development workflow orchestration system** with:

- **2 Orchestrator Agents**: Feature development and bug fixing workflows
- **13 Specialized Skills**: Requirements extraction, architecture design, TDD testing, code review, and more
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

**New Feature**:
```
@feature-workflow Add discount code functionality to checkout
```

**Bug Fix**:
```
@improvement-workflow Fix null pointer when user has no email
```

See [Workflows Documentation](src/workflows/README.md) for detailed usage.

---

## Project Structure

```
ai-prompts/
├── src/                          # Single source of truth (edit here)
│   ├── agents/                   # Orchestrator and specialist agents
│   │   ├── feature-workflow.agent.md         (7-phase feature development)
│   │   ├── improvement-workflow.agent.md     (7-phase bug fixing)
│   │   ├── backend-engineer.agent.md
│   │   ├── frontend-engineer.agent.md
│   │   └── doc-writter.agent.md
│   │
│   ├── skills/                   # Specialized capabilities
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

This repository provides two main orchestration workflows:

### Feature Workflow

**7-phase TDD approach for building new functionality**

```
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
Phase 6: Refactoring
    ↓
Phase 7: Code Review
```

**Phases**:
1. **Specification**: Extract requirements, edge cases, acceptance criteria
2. **Architecture**: Design system, evaluate alternatives
3. **Documentation**: Update project docs
4. **TDD Tests**: Generate failing tests
5. **Implementation**: Minimal solution to pass tests
6. **Refactoring**: Improve code quality (SOLID, DRY)
7. **Code Review**: Final quality check

**Checkpoints**: After phases 1, 2, 4 (manual approval required)

### Improvement Workflow

**7-phase evidence-based approach for fixing bugs**

```
Phase 1: Component Mapping
    ↓
Phase 2: Root Cause
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
Phase 6: Patch
    ↓
Phase 7: Post-Fix Review
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
- **Adversarial Critique**: Actively search for failure modes before implementing

See [Workflows Documentation](src/workflows/README.md) for complete details.

---

## Skills

13 specialized skills provide focused capabilities:

### Feature Skills (7)

| Skill | Purpose |
|-------|---------|
| [spec-extractor](src/skills/spec-extractor/SKILL.md) | Extract requirements, edge cases, acceptance criteria |
| [system-designer](src/skills/system-designer/SKILL.md) | Design architecture with domain model, APIs, data model |
| [tradeoff-analyzer](src/skills/tradeoff-analyzer/SKILL.md) | Compare technical alternatives with scoring |
| [feature-doc-writer](src/skills/feature-doc-writer/SKILL.md) | Update AGENTS.md, feature docs, architecture docs |
| [tdd-test-generator](src/skills/tdd-test-generator/SKILL.md) | Generate failing tests (Red phase of TDD) |
| [minimal-impl-generator](src/skills/minimal-impl-generator/SKILL.md) | Simplest implementation (Green phase of TDD) |
| [refactor-optimizer](src/skills/refactor-optimizer/SKILL.md) | Code quality improvement (Refactor phase of TDD) |

### Bugfix Skills (5)

| Skill | Purpose |
|-------|---------|
| [component-mapper](src/skills/component-mapper/SKILL.md) | Map affected components, dependencies, data flow |
| [root-cause-analyzer](src/skills/root-cause-analyzer/SKILL.md) | Evidence-based root cause analysis (never proposes fix) |
| [solution-critic](src/skills/solution-critic/SKILL.md) | Adversarial stress-testing (must find ≥2 failure modes) |
| [patch-implementer](src/skills/patch-implementer/SKILL.md) | Minimal bug fix addressing critique feedback |
| [post-fix-reviewer](src/skills/post-fix-reviewer/SKILL.md) | Verify fix works, no regressions |

### Shared Skills (1)

| Skill | Purpose |
|-------|---------|
| [code-reviewer](src/skills/code-reviewer/SKILL.md) | Comprehensive security, performance, quality review |

See [Skills Documentation](src/skills/README.md) for detailed information.

---

## Agents

### Orchestrator Agents (2)

- **[feature-workflow](src/agents/feature-workflow.agent.md)**: 7-phase feature development orchestrator
- **[improvement-workflow](src/agents/improvement-workflow.agent.md)**: 7-phase bug fixing orchestrator

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

### Why 13 Granular Skills Instead of 4 Broad Skills?

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

---

## Documentation

- **[Workflows README](src/workflows/README.md)**: Complete workflow guide with diagrams, examples, best practices
- **[Skills README](src/skills/README.md)**: Skill interactions, patterns, development guide
- **[Skills Instructions](.claude/rules/skills.instructions.md)**: Detailed skill creation guide
- **Individual Skills**: Each skill has detailed SKILL.md with process, examples, evals

---

## Version History

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