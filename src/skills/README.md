# Skills

Specialized capabilities for development workflows. Each skill focuses on a single responsibility and produces structured, validated output.

## Quick Reference

| Skill | Type | Use When | Output |
|-------|------|----------|--------|
| [spec-extractor](spec-extractor/SKILL.md) | Feature | Starting new feature | Requirements, edge cases, acceptance criteria |
| [system-designer](system-designer/SKILL.md) | Feature | After requirements | Domain model, APIs, data model, diagrams |
| [tradeoff-analyzer](tradeoff-analyzer/SKILL.md) | Feature | Evaluating alternatives | Comparison matrix, recommendation |
| [feature-doc-writer](feature-doc-writer/SKILL.md) | Shared | Updating docs | AGENTS.md, feature docs |
| [tdd-test-generator](tdd-test-generator/SKILL.md) | Shared | Before implementation | Failing unit/integration tests |
| [minimal-impl-generator](minimal-impl-generator/SKILL.md) | Feature | After tests written | Simplest working code |
| [refactor-optimizer](refactor-optimizer/SKILL.md) | Feature | After tests pass | SOLID, DRY, performant code |
| [component-mapper](component-mapper/SKILL.md) | Bugfix | Starting bugfix | Component list, dependency graph |
| [root-cause-analyzer](root-cause-analyzer/SKILL.md) | Bugfix | After component mapping | Evidence-based root cause |
| [solution-critic](solution-critic/SKILL.md) | Bugfix | Before implementing fix | Failure modes, edge cases, concerns |
| [patch-implementer](patch-implementer/SKILL.md) | Bugfix | After critique approved | Minimal bug fix |
| [post-fix-reviewer](post-fix-reviewer/SKILL.md) | Bugfix | After patch | Fix verification, regression check |
| [code-reviewer](code-reviewer/SKILL.md) | Shared | Before merge | Security, performance, quality review |

---

## Skill Categories

### Feature Skills

**Purpose**: Build new functionality using TDD approach

**Flow**:
```
spec-extractor → system-designer → tradeoff-analyzer → 
feature-doc-writer → tdd-test-generator → minimal-impl-generator → 
refactor-optimizer → code-reviewer
```

**Characteristics**:
- Start with unclear requirements
- Design before implementation
- Evaluate alternatives
- Tests before code
- Optimize after working

### Bugfix Skills

**Purpose**: Fix existing issues through root cause analysis

**Flow**:
```
component-mapper → root-cause-analyzer → solution-critic → 
feature-doc-writer → tdd-test-generator → patch-implementer → 
post-fix-reviewer → code-reviewer
```

**Characteristics**:
- Start with symptoms
- Evidence-based investigation
- Never jump to fix
- Stress-test solution
- Verify no regressions

### Shared Skills

**Purpose**: Used by both feature and bugfix workflows

- `feature-doc-writer` - Documentation updates
- `tdd-test-generator` - Test generation
- `code-reviewer` - Quality assurance

---

## Skill Interactions

### Dependencies

```
Feature Workflow Skills:

spec-extractor
    ↓
system-designer
    ↓
tradeoff-analyzer
    ↓
feature-doc-writer (*shared*)
    ↓
tdd-test-generator (*shared*)
    ↓
minimal-impl-generator
    ↓
refactor-optimizer
    ↓
code-reviewer (*shared*)

Bugfix Workflow Skills:

component-mapper
    ↓
root-cause-analyzer
    ↓
solution-critic
    ↓
feature-doc-writer (*shared*)
    ↓
tdd-test-generator (*shared*)
    ↓
patch-implementer
    ↓
post-fix-reviewer
    ↓
code-reviewer (*shared*)
```

*Shared skills (*) are used by both workflows
    style TTG fill:#ffd93d
    style CR fill:#ffd93d
```

**Yellow** = Shared skills used by both workflows

### Data Flow

**Feature Workflow**:
1. **spec-extractor** → Requirements spec
2. **system-designer** → Consumes spec, produces architecture
3. **tradeoff-analyzer** → Consumes architecture, produces recommendation
4. **feature-doc-writer** → Consumes spec + architecture, updates docs
5. **tdd-test-generator** → Consumes spec, produces failing tests
6. **minimal-impl-generator** → Consumes tests, produces implementation
7. **refactor-optimizer** → Consumes implementation, produces optimized code
8. **code-reviewer** → Consumes all, produces approval/feedback

**Bugfix Workflow**:
1. **component-mapper** → Component map
2. **root-cause-analyzer** → Consumes component map, produces root cause analysis
3. **solution-critic** → Consumes root cause, produces critique
4. **feature-doc-writer** → Updates docs
5. **tdd-test-generator** → Produces failing tests
6. **patch-implementer** → Consumes root cause + critique + tests, produces fix
7. **post-fix-reviewer** → Consumes fix, verifies it works
8. **code-reviewer** → Consumes all, produces approval/feedback

---

## Integration with Agents

Skills integrate with orchestrator and specialist agents:

### Orchestrator Agents

- [feature-workflow](../agents/feature-workflow.agent.md) - Coordinates feature skills
- [improvement-workflow](../agents/improvement-workflow.agent.md) - Coordinates bugfix skills

### Specialist Agents

Skills delegate implementation to specialist agents:

| Skill | Delegates To | For What |
|-------|--------------|----------|
| minimal-impl-generator | backend-engineer, frontend-engineer | Actual code implementation |
| patch-implementer | backend-engineer, frontend-engineer | Bug fix implementation |
| feature-doc-writer | doc-writter | Comprehensive documentation |
| root-cause-analyzer | breakdown-task | Complex analysis |

**Example**:
```markdown
minimal-impl-generator skill:
  → Generates implementation requirements
  → Delegates to @backend-engineer:
    "Implement user service with these methods..."
  → backend-engineer produces code
  → Skill validates tests pass
```

---

## Skill Patterns

### 1. Structured Output

All skills produce **structured, parseable output**:

```markdown
## [Skill Output Title]

**Summary**: [1-sentence summary]

## [Section 1]
[Content with clear format]

## [Section 2]  
[Content with clear format]

## Confidence: X%

## Missing Information
- MISSING-1: [What's unclear]
```

### 2. Uncertainty Tracking

Skills explicitly track what they don't know:

```markdown
## Assumptions Made
- ASSUMPTION-1: Discount codes never expire
- ASSUMPTION-2: Only one code per order

## Missing Information
- MISSING-1: What happens if code deleted after use?
- MISSING-2: Should codes be case-sensitive?

## Confidence: 75%
```

### 3. Evaluation Checklists

Skills include self-evaluation criteria:

```markdown
## Evals
- [ ] All requirements extracted
- [ ] Edge cases identified  
- [ ] Acceptance criteria defined
- [ ] Confidence ≥70%
```

### 4. Evidence-Based

Skills require evidence for conclusions:

```markdown
## Root Cause

**Primary Cause**: Null pointer in email validation

**Evidence**:
1. Stack trace shows `email.toLowerCase()` on line 45
2. Reproduction confirms crash when email is null
3. Log analysis shows 15 occurrences in past week
```

### 5. Examples and Templates

Skills provide examples for clarity:

````markdown
## Output Format

```typescript
// Example test
it('should validate email format', () => {
  const result = validateEmail('user@example.com');
  expect(result).toBe(true);
});
```
````

---

## Skill Development Guidelines

When creating new skills, follow these patterns:

### Skill Structure

```markdown
---
name: skill-name
description: When to trigger and what it does. Include contexts for triggering.
---

# Skill Name

[Brief purpose statement]

## When to Use
- [Specific trigger 1]
- [Specific trigger 2]

## Core Principle
[Guiding philosophy in 1-2 sentences]

## Process
### Step 1: [Action]
[Detailed instructions]

### Step 2: [Action]
[Detailed instructions]

## Output Format
[Structured template]

## Uncertainty Handling
[How to deal with missing info]

## Evals
- [ ] [Success criterion 1]
- [ ] [Success criterion 2]
```

### Skill Descriptions

Skill descriptions determine **triggering accuracy**. Include:

1. **What it does** (capability)
2. **When to use it** (contexts)
3. **Related keywords** (for matching)

**Good**:
```yaml
description: Extract complete feature requirements including edge cases and acceptance criteria. Always use when starting new feature development, analyzing user stories, or clarifying feature scope. Keywords requirements, specifications, user stories, feature planning.
```

**Bad** (undertriggers):
```yaml
description: Extract requirements from user input.
```

### Skill Length

- **Target**: <500 lines
- **Metadata**: ~100 words (always loaded)
- **Body**: <500 lines (loaded when triggered)
- **References**: Unlimited (loaded as needed)

### Progressive Disclosure

For large skills:

```
skill-name/
├── SKILL.md (<500 lines, general process)
└── references/
    ├── examples.md (detailed examples)
    ├── edge-cases.md (comprehensive list)
    └── patterns.md (common patterns)
```

SKILL.md references other files:
```markdown
## Advanced Edge Cases

See [edge-cases.md](references/edge-cases.md) for comprehensive list.
```

---

## Skill Invocation

### Direct Invocation

```markdown
Invoke the `spec-extractor` skill to analyze this feature request:
[Feature description]
```

### Workflow Invocation

Orchestrator agents invoke skills automatically:

```markdown
@feature-workflow Add discount codes to checkout

[feature-workflow agent automatically invokes:]
1. spec-extractor
2. system-designer
3. tradeoff-analyzer
...
```

### Conditional Invocation

Some skills invoke others conditionally:

```markdown
## In component-mapper skill:

If documentation is missing:
- Invoke `feature-doc-writer` skill
- Create concise feature documentation
```

---

## Common Invocation Patterns

### Sequential (Feature)

```
spec-extractor
  ↓ (spec)
system-designer  
  ↓ (architecture)
tradeoff-analyzer
  ↓ (recommendation)
tdd-test-generator
  ↓ (tests)
minimal-impl-generator
```

### Evidence Chain (Bugfix)

```
component-mapper
  ↓ (component list)
root-cause-analyzer
  ↓ (root cause + evidence)
solution-critic
  ↓ (critique feedback)
patch-implementer
```

### Parallel (When Independent)

```
system-designer ----+
                    |
tradeoff-analyzer --+--→ Both feed checkpoint
```

---

## Testing Skills

### Manual Testing

1. **Create test prompt**: Realistic user request
2. **Invoke skill**: Follow skill instructions yourself
3. **Check output**: Matches expected format?
4. **Evaluate**: Pass all evals?

### Evaluation Criteria

Each skill has eval checklist:

```markdown
## Evals
- [ ] All requirements extracted
- [ ] Edge cases identified (minimum 3)
- [ ] Acceptance criteria in Given-When-Then format
- [ ] Confidence level calculated
- [ ] Missing information flagged if confidence <70%
```

### Example Test Cases

**Good test prompts**:
```
spec-extractor: "Add ability for users to upload profile pictures"
root-cause-analyzer: "App crashes when user has no email address"
solution-critic: "Proposed fix: add null check before accessing email"
```

**Bad test prompts** (too vague):
```
spec-extractor: "Make the site better"
root-cause-analyzer: "Something is broken"
```

---

## Troubleshooting

### Skill Not Triggering

**Cause**: Description doesn't match user request

**Solution**:
1. Review skill description
2. Add missing keywords/contexts
3. Make description more "pushy"
4. Test with realistic prompts

### Output Format Inconsistent

**Cause**: Skill instructions not specific enough

**Solution**:
1. Provide explicit template
2. Use "ALWAYS use this format"
3. Include examples
4. Add format to evals

### Skill Produces Wrong Results

**Cause**: Instructions unclear or process flawed

**Solution**:
1. Walk through process yourself
2. Identify where it breaks down
3. Add clarifications
4. Add examples for tricky parts
5. Update evals to catch issue

---

## Skill Maintenance

### When to Update

- Skill consistently produces wrong output
- New patterns emerge from usage
- Better approach discovered
- Edge cases found

### Versioning

Track major changes in skill files:

```markdown
## Version History

- **v1.1.0** (2024-03-15): Added support for async edge cases
- **v1.0.0** (2024-03-09): Initial implementation
```

### Deprecation

If replacing a skill:

1. Create new skill with improved approach
2. Add deprecation notice to old skill
3. Update workflows to use new skill
4. Archive old skill after transition

---

## Related Documentation

- [Workflows](../workflows/README .md) - How skills are orchestrated
- [Agents](../agents/) - Orchestrator and specialist agents
- [Prompts Registry](../../prompts/registry.yaml) - Versioned skill templates
- [Skills Instructions](.claude/rules/skills.instructions.md) - Skill creation guide

---

## Contributing New Skills

See [skills.instructions.md](../../.claude/rules/skills.instructions.md) for detailed guidance on:

- Skill creation process
- Writing effective descriptions
- Test case development
- Iteration and improvement
- Description optimization

---

## Questions?

For workflow usage questions, see [Workflows README](../workflows/README.md).

For skill development questions, see [skills.instructions.md](../../.claude/rules/skills.instructions.md).
