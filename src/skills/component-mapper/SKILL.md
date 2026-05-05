---
name: component-mapper
description: Map affected components, dependencies, and data flow when debugging issues or improving existing code. Always use when starting bugfix workflow, investigating issues, or understanding code impact. Traces dependencies bidirectionally and identifies relevant documentation. Keywords component mapping, dependency tracing, impact analysis, code navigation, data flow, affected components, debugging preparation.
---

# Component Mapper

Identify what components are affected by a bug or improvement request, trace dependencies, and understand data flow before diving into analysis.

## When to Use

- Starting bugfix workflow
- Investigating reported issue
- Understanding code impact
- Before making changes to existing code
- Documentation is unclear

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Bug Workflow Phase 1**: Produces `.ai-workflow/[feature-folder]/1-component-map.md`
- **Improvement Workflow Phase 1**: Produces `.ai-workflow/[feature-folder]/1-component-map.md`

**Context**: Read `0-startpoint.md` and `0.1-grill-me.md` for the user's problem/improvement description before mapping components.

## Process

### Step 1: Identify Affected Components

**From bug report/improvement request**:

- What feature/functionality is affected?
- What files/modules are likely involved?
- What user journey is impacted?

**Search codebase**:

- Grep for error messages
- Search for related function names
- Check recent commits (git log)
- Look for similar issues (git blame)

**List components**:

```markdown
## Affected Components

1. **ComponentA** (`path/to/file.ts`)
    - Role: [What it does]
    - Status: [Primary/Secondary affected]

2. **ComponentB** (`path/to/service.ts`)
    - Role: [What it does]
    - Status: [Dependency/Related]
```

### Step 2: Trace Dependencies

**Upstream (what calls this)**:

- Controllers/routes that trigger component
- Services that depend on it
- Other features using it

**Downstream (what this calls)**:

- Database queries
- External APIs
- Other services/utilities
- Third-party libraries

**Create dependency diagram** (text-based):

```
Controller
  ↓ calls
Service
  ↓ queries          ↓ calls
Database        ExternalAPI
↑ uses
OtherFeature
```

### Step 3: Map Data Flow

**Trace data through system**:

1. Where does data originate? (user input, API, DB)
2. How is data transformed?
3. Where is data validated?
4. Where is data stored?
5. Where is data output?

**Document flow**:

```markdown
## Data Flow

1. User Input (HTTP POST /api/resource)
2. Controller validation
3. Service processing
4. Database query/update
5. Response formatting
6. Return to user
```

### Step 4: Check Documentation

**Look for**:

- Feature docs in AGENTS.md/CLAUDE.md
- README sections
- Inline comments
- Architecture docs

**If found**:

- Link to documentation
- Note discrepancies (code vs docs)

**If missing**:

- Flag for documentation creation
- Proceed with code analysis

### Step 5: Invoke Feature Doc Writer (If Needed)

**If documentation is**:

- Missing entirely
- Severely outdated
- Confusing/incorrect

**Then**:

- Invoke `feature-doc-writer` skill
- Create concise feature documentation
- Helps future debugging

## Output Format

````markdown
# Component Map: [Issue/Feature]

## Summary

[1-sentence description of what's affected]

## Affected Components

### Primary

- **Component1** (`path/file.ts`)
    - **Role**: [What it does]
    - **Lines**: [Approximate line range]
    - **Complexity**: [Low/Medium/High]

### Secondary

- **Component2** (`path/file.ts`)
    - **Role**: [Dependency/caller]
    - **Why affected**: [Reason]

## Dependency Graph

```
Component relationships (text format):

PrimaryComponent
  ↓ depends on / calls
SecondaryComponent
  ↓ uses
Database / ExternalService
```

## Data Flow

1. [Step] - [Component] - [Data state]
2. [Step] - [Component] - [Data transformation]
3. ...

## Documentation Status

**Existing Docs**:

- [Link to AGENTS.md section] (if exists)
- [Link to feature docs] (if exists)

**Documentation Gaps**:

- [What's missing]
- [What's outdated]

**Action**: [Created new docs / Updated docs / No action needed]

## Complexity Assessment

**Overall Complexity**: [Low/Medium/High]

**Factors**:

- [Factor 1: e.g., "Multiple async operations"]
- [Factor 2: e.g., "Complex state management"]

**Confidence in Mapping**: [X]%

**Unknown Areas**:

- [What's still unclear]

```

## Uncertainty Handling

**List unknowns**:
- Components that might be affected
- Dependencies that aren't obvious
- Data flow gaps

**Confidence scoring**:
- 90-100%: Complete understanding
- 70-89%: Good understanding, minor gaps
- <70%: Significant unknowns remain

## Evals

- [ ] All affected components identified
- [ ] Dependencies traced (up and downstream)
- [ ] Data flow documented
- [ ] Documentation status assessed
- [ ] Complexity level determined
- [ ] Unknown areas flagged
```
````
