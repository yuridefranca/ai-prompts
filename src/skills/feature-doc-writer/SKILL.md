---
name: feature-doc-writer
description: Update project documentation (AGENTS.md, CLAUDE.md, feature docs) when adding new features, ensuring discoverability and comprehension. Always use when feature is being implemented, documentation needs updating, or new capabilities need to be documented. Integrates with agents-md-generator skill for format consistency. Keywords documentation, AGENTS.md, CLAUDE.md, feature documentation, API documentation, architecture documentation, code documentation.
---

# Feature Documentation Writer

Update project documentation to capture new feature context, ensuring future developers and AI assistants can discover and understand the feature.

## When to Use

- After architecture design is approved
- When implementing new feature
- Before implementation (document design)
- When feature behavior changes
- Missing documentation discovered

## Workflow Artifact

This skill is invoked in multiple phases across both workflows:

- **Feature Workflow Phase 3**: Produces `.ai-workflow/[feature-folder]/3-feature-documentation.md`
- **Improvement Workflow Phase 1**: Contributes to `.ai-workflow/[feature-folder]/1-component-map.md` (if docs missing)
- **Improvement Workflow Phase 4**: Produces `.ai-workflow/[feature-folder]/4-solution-documentation.md`

**Context**: Read `0-startpoint.md` for initial requirements. Read the relevant phase output files for context about what's being documented.

## Process

### Step 0: CRITICAL - Use File Creation Tools

**⚠️ ALWAYS CREATE ACTUAL FILES** - Do NOT just output documentation text in chat.

**Required actions**:

- Use `create_file` tool to create new documentation files
- Use `replace_string_in_file` tool to update existing files
- Verify files are created in the workspace
- Never just display documentation content without creating files

**Why this matters**: Documentation is worthless if it only exists in chat history. It must be committed to the repository.

### Step 0.1: CRITICAL - Avoid ASCII Art Diagrams

**⚠️ NEVER CREATE ASCII BOX DIAGRAMS** - They ALWAYS break formatting and are unmaintainable.

**Forbidden formats**:

```
❌ Box diagrams with ┌─┐│└┘ characters
❌ Complex ASCII art structures
❌ Multi-line text boxes
❌ Nested box hierarchies
```

**Use instead**:

```
✅ Simple indented lists
✅ Markdown code blocks with comments
✅ Plain text with arrows (→, ↓, ├─)
✅ Mermaid syntax (if supported)
✅ Markdown tables
✅ Bullet point hierarchies
```

**Example - Instead of boxes, use indented structure**:

```markdown
Browser Client
→ HTTP/REST
→ Next.js Application
├─ API Routes Layer
│ ├─ /api/auth/_
│ └─ /api/playlists/_
├─ Service Layer
│ ├─ ConversionService
│ └─ MatchingService
└─ Abstraction Layer
└─ IMusicService
```

### Step 1: Identify Documentation Targets

**Determine what needs updating**:

- `AGENTS.md` or `CLAUDE.md` (project context)
- Feature-specific docs
- API documentation
- Architecture diagrams
- README sections

### Step 2: Update Project Context Files

**For AGENTS.md/CLAUDE.md**:

- Invoke `agents-md-generator` skill for format consistency
- Add feature to relevant sections
- Update architecture overview if needed
- Add to features list
- Link to detailed docs

**Content to add**:

```markdown
### [Feature Name]

**Purpose**: [What it does]
**Location**: [Code modules/files]
**Key Components**: [List]
**Dependencies**: [What it relies on]
**Usage**: [How to use/trigger]
```

### Step 3: Create Feature-Specific Documentation

**⚠️ Use `create_file` tool** to create new doc file (e.g., `docs/features/feature-name.md`):

**File path**: `docs/features/[feature-name].md` (create directory if needed)

**Content template**:

```markdown
# [Feature Name]

## Overview

[What, why, when to use]

## Architecture

[Component diagram]
[How it fits in system]

## API

### Endpoints

[List with examples]

### Request/Response

[Schemas]

## Data Model

[Tables, relationships]

## Usage Examples

[Code examples]

## Edge Cases

[From spec]

## Troubleshooting

[Common issues]
```

### Step 4: Update Architecture Maps

**If architecture diagrams exist**:

- Add new components to diagrams
- Update data flow diagrams
- Update deployment diagrams if needed

**Tools**: Simple text diagrams, ASCII art, or existing documentation tooling

### Step 5: Add Inline Code Documentation

**For complex implementations**:

- Add JSDoc/TSDoc comments
- Document "why" not just "what"
- Link to feature docs
- Explain non-obvious decisions

## Output

1. Updated `AGENTS.md` or `CLAUDE.md`
2. New feature documentation file
3. Updated architecture diagrams
4. Inline code comments (if applicable)

## Delegation

**For AGENTS.md updates**: Invoke `agents-md-generator` skill
**For comprehensive docs**: Delegate to `doc-writter` agent

## Evals

- [ ] Project context files updated
- [ ] Feature discoverable by AI/developers
- [ ] API documented with examples
- [ ] Architecture impact documented
- [ ] Inline comments for complex code
