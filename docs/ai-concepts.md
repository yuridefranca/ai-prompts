# AI-Assisted Development: Concepts & Best Practices

A practical guide for software engineers getting started with AI-assisted development. Covers the core concepts behind this repository's tools and the best practices that make them effective.

---

## Table of Contents

1. [Core Concepts](#core-concepts)
   - [Large Language Models (LLMs)](#large-language-models-llms)
   - [Context Window](#context-window)
   - [Agents](#agents)
   - [Skills](#skills)
   - [Prompts](#prompts)
   - [Workflow Orchestration](#workflow-orchestration)
2. [Key Patterns](#key-patterns)
   - [Context Rehydration](#context-rehydration)
   - [Manual Checkpoints](#manual-checkpoints)
   - [Phase-Scoped Artifacts](#phase-scoped-artifacts)
   - [Confidence Scoring](#confidence-scoring)
3. [Best Practices](#best-practices)
   - [Working with AI Agents](#working-with-ai-agents)
   - [Prompt Engineering](#prompt-engineering)
   - [TDD with AI](#tdd-with-ai)
   - [Avoiding Common Pitfalls](#avoiding-common-pitfalls)
4. [Glossary](#glossary)

---

## Core Concepts

### Large Language Models (LLMs)

**What**: AI systems trained on vast amounts of text that can generate, analyze, and transform code and natural language. Examples: GPT-4, Claude, Gemini.

**How they work**: LLMs predict the next token (word/code fragment) based on the preceding context. They don't "understand" code the way humans do — they recognize patterns from their training data.

**What this means for you**:
- ✅ LLMs are excellent at pattern recognition, boilerplate generation, and following structured processes
- ✅ They can process and synthesize large codebases quickly
- ⚠️ They can hallucinate (confidently generate incorrect information)
- ⚠️ They have no persistent memory between conversations
- ⚠️ They can't run code or verify their outputs actually work

**Why workflows matter**: Because LLMs can hallucinate and have no memory, structured workflows with checkpoints and artifacts provide the guardrails that make AI-assisted development reliable.

### Context Window

**What**: The maximum amount of text (input + output) an LLM can process in a single conversation turn. Think of it as the model's "working memory."

**Typical sizes** (as of 2025):
- GPT-4: ~128K tokens (~96K words)
- Claude 3.5: ~200K tokens (~150K words)
- Gemini 1.5: ~1M tokens (~750K words)

**Why it matters**:
- A large codebase can easily exceed the context window
- Long conversations gradually fill the context, causing the model to "forget" earlier details
- This is why **context rehydration** (10-bullet summaries) is critical — it compresses essential context into a small space

**Practical tips**:
- Keep workflow artifacts concise and structured
- Use context rehydration summaries between phases
- Don't dump entire codebases into prompts — use targeted file reads
- When context gets long, start a new conversation with a rehydration summary

### Agents

**What**: AI agents are LLM-powered orchestrators that can use tools, make decisions, and coordinate multi-step processes. Unlike simple chat, agents have a defined role, access to tools, and a structured approach.

**Simple prompt vs. Agent**:

| Aspect | Simple Prompt | Agent |
|--------|--------------|-------|
| Scope | Single task | Multi-step workflow |
| Tools | None | File creation, terminal, search |
| Memory | None | Context rehydration |
| Decision-making | None | Chooses next steps based on state |
| Quality control | None | Checkpoints, confidence scoring |

**Types in this repository**:

- **Orchestrator Agents** (orchestrator, debug-workflow, improvement-workflow, feature-workflow): Coordinate multi-phase workflows, invoke skills, manage checkpoints
- **Specialist Agents** (backend-engineer, frontend-engineer, documentation-writer): Handle domain-specific implementation

**Key insight**: Agents are not magic — they're structured processes that leverage LLM capabilities with appropriate guardrails. The structure is what makes them reliable.

### Skills

**What**: Focused, single-responsibility capabilities that produce structured output. Skills are the building blocks that agents compose into workflows.

**Why skills instead of one big prompt**:
- **Single responsibility**: Each skill does one thing well → easier to test and maintain
- **Precise triggering**: Clear descriptions mean the right skill activates for the right task
- **Composability**: Skills can be combined in different sequences for different workflows
- **Reusability**: The same skill (e.g., `code-reviewer`) works across all workflows

**Skill anatomy**:
```
skills/my-skill/
└── SKILL.md          # Definition: name, description, process, examples
```

Each SKILL.md contains:
- **Frontmatter**: Name and description (used for auto-discovery)
- **Process**: Step-by-step instructions
- **Workflow Artifact**: Which workflow phase uses this skill and what file it produces
- **Examples**: Input/output samples

### Prompts

**What**: The instructions you give to an LLM to guide its behavior. In this repository, "prompts" refers to versioned, reusable prompt templates.

**Prompt engineering basics**:
- **Be specific**: "Add a REST endpoint for user creation with validation" > "Add an endpoint"
- **Provide context**: Reference existing patterns, file paths, and conventions
- **Define output format**: "Return a markdown table" > "Give me the results"
- **Set constraints**: "Use NestJS decorators" > "Write the code"
- **Give examples**: Show the model what good output looks like

**This repo's approach**: Instead of ad-hoc prompts, we use structured workflows where each phase has a defined prompt (the skill's process). This ensures consistency and quality.

### Workflow Orchestration

**What**: The coordination of multiple agents and skills in a defined sequence to accomplish complex tasks.

**Why orchestration matters**:
- Without structure, AI tends to jump to solutions (especially for bugs)
- Complex tasks need multiple specialized capabilities applied in the right order
- Human oversight at critical points prevents costly mistakes

**The three workflows**:

| Workflow | When | Key Rule |
|----------|------|----------|
| Bug | Something is broken | Never jump to fix |
| Improvement | Working code could be better | Understand before changing |
| Feature | New capability needed | Design before code |

Each workflow enforces its rule through phase sequencing — the "forbidden" action (fixing, changing, coding) can't happen until the analysis phases are complete.

---

## Key Patterns

### Context Rehydration

**Problem**: LLMs lose context in long conversations. By phase 5, the model may have forgotten what was decided in phase 1.

**Solution**: Before every phase transition, generate a 10-bullet summary that captures:
1. What was decided
2. What assumptions were made
3. What's still unclear
4. Why certain choices were made
5. What's next

**Why 10 bullets**: It's enough to capture essential context but small enough to fit in the context window alongside new information.

**Practical application**: If a workflow gets interrupted (context limit, new conversation), you can paste the last rehydration summary to resume where you left off.

### Manual Checkpoints

**Problem**: AI can make wrong decisions with high confidence. Automated workflows that never pause for human review can compound errors.

**Solution**: Insert mandatory approval points at critical decisions:
- After root cause analysis (bug workflow)
- After tradeoff analysis & design (improvement workflow)
- After specification and architecture (feature workflow)

**Why not automate everything**: AI is a tool, not a replacement for engineering judgment. Checkpoints ensure humans stay in the loop for decisions that matter.

### Phase-Scoped Artifacts

**Problem**: When a phase produces multiple files, numbering gets confusing. Is the extra analysis file phase 6 or phase 7?

**Solution**: Use phase-scoped naming:
- `2-root-cause-analysis.md` — primary output of phase 2
- `2.1-alternative-causes.md` — extra file from phase 2
- `2.2-evidence-log.md` — another extra file from phase 2

**Why this matters**: It keeps related artifacts grouped together and makes it clear which phase produced which file. When you see `3-solution-evaluation.md`, you know it's the primary output of phase 3.

### Confidence Scoring

**Problem**: AI often proceeds with incomplete information, leading to rework.

**Solution**: At each checkpoint, assess confidence as a percentage:
- **90-100%**: High confidence — proceed
- **70-89%**: Medium confidence — proceed with caution
- **<70%**: Low confidence — STOP and get clarification

**Missing information tracking**: Explicitly list what's unknown (MISSING-1, MISSING-2, etc.) so it's clear what needs clarification.

---

## Best Practices

### Working with AI Agents

1. **Start with the router**: Use `@orchestrator` to automatically classify your task. It picks the right workflow so you don't have to think about it.

2. **Don't skip phases**: Each phase builds on the previous one. Skipping root cause analysis to "save time" usually costs more time later.

3. **Respect checkpoints**: When a workflow pauses for approval, actually review the output. Don't just click "approve."

4. **Provide context proactively**: The more context you give, the better the output. Mention relevant files, existing patterns, and constraints.

5. **Verify AI output**: Always review generated code before committing. AI can produce syntactically correct code that's logically wrong.

6. **Use artifacts for continuity**: If a conversation gets too long, start a new one and reference the `.ai-workflow/` artifacts. They contain everything the model needs to resume.

### Prompt Engineering

1. **Be specific about what you want**: 
   - ❌ "Fix this bug"
   - ✅ "Fix the null pointer exception in UserService.getProfile() when the user has no email address"

2. **Reference existing patterns**:
   - ❌ "Add an API endpoint"
   - ✅ "Add a REST endpoint following the same pattern as UserController.createUser(), using NestJS decorators and the existing validation pipe"

3. **Define success criteria**:
   - ❌ "Make it faster"
   - ✅ "Reduce dashboard query response time from 3s to under 500ms at p95"

4. **Mention constraints**:
   - ❌ "Refactor this module"
   - ✅ "Refactor this module without changing the public API — existing consumers must not break"

5. **Ask for structured output**:
   - ❌ "What do you think?"
   - ✅ "Provide a comparison table with columns: Approach, Feasibility (1-5), Impact (1-5), Risk (1-5)"

### TDD with AI

AI changes the TDD cycle but doesn't eliminate it:

**Traditional TDD**: You write the test → You write the code → You refactor
**AI-Assisted TDD**: You describe what to test → AI generates tests → AI implements code → AI refactors

**Key differences**:
- AI can generate comprehensive test suites faster than you can write them
- AI can identify edge cases you might miss
- But AI can also generate tests that look correct but test the wrong thing
- **Always review AI-generated tests** — verify they actually test what you intend

**The workflow approach**: Our TDD phases enforce the Red-Green-Refactor cycle:
1. **Red**: `test-generator` creates failing tests
2. **Green**: `minimal-impl-generator` writes the simplest code to pass
3. **Refactor**: `refactor-optimizer` improves code quality while keeping tests green

### Avoiding Common Pitfalls

#### 1. The "Just Fix It" Trap

**What happens**: You report a bug and the AI immediately suggests a fix.

**Why it's bad**: The fix addresses the symptom, not the root cause. The bug will recur.

**What to do instead**: Use the bug workflow, which enforces root cause analysis before any fix is proposed.

#### 2. The "While I'm Here" Trap

**What happens**: While fixing one issue, the AI (or you) suggests improving nearby code.

**Why it's bad**: Scope creep introduces risk. Unrelated changes can break things and make the PR harder to review.

**What to do instead**: Each workflow is scoped to one task. If you spot something else to improve, note it and create a separate task.

#### 3. The "Trust Without Verify" Trap

**What happens**: The AI generates code that looks correct, so you commit it without testing.

**Why it's bad**: AI can produce code that compiles but has logical errors, security vulnerabilities, or performance issues.

**What to do instead**: Always run tests. Use the code-reviewer skill. Verify the output does what you expect.

#### 4. The "Lost Context" Trap

**What happens**: A long workflow conversation fills the context window, and the AI forgets earlier decisions.

**Why it's bad**: The AI may contradict earlier decisions or repeat work already done.

**What to do instead**: Context rehydration summaries compress essential context. If the conversation gets too long, start fresh with the last summary.

#### 5. The "Over-Engineering" Trap

**What happens**: The AI designs an elaborate solution for a simple problem.

**Why it's bad**: Complexity is the enemy of maintainability. Over-engineered solutions are harder to understand, test, and modify.

**What to do instead**: The `minimal-impl-generator` skill enforces YAGNI (You Ain't Gonna Need It). Start with the simplest solution that works.

---

## Glossary

| Term | Definition |
|------|-----------|
| **Agent** | An LLM-powered orchestrator with a defined role, tools, and structured process |
| **Checkpoint** | A mandatory pause in a workflow where a human must approve before proceeding |
| **Confidence Score** | A percentage (0-100%) indicating how certain the AI is about its analysis |
| **Context Rehydration** | A 10-bullet summary generated between phases to preserve context |
| **Context Window** | The maximum text (input + output) an LLM can process in one conversation |
| **Hallucination** | When an LLM generates confident but incorrect information |
| **LLM** | Large Language Model — an AI system trained on text that generates new text |
| **MISSING-N** | A labeled item representing unknown information that needs clarification |
| **Orchestrator Agent** | An agent that coordinates multi-phase workflows and invokes skills |
| **Parallel Analysis** | Running multiple analysis perspectives (quality, edge cases, regression) simultaneously against code |
| **Phase-Scoped Naming** | File naming convention: `N-file.md` (primary), `N.1-file.md` (auxiliary) |
| **Prompt** | Instructions given to an LLM to guide its behavior |
| **Skill** | A focused, single-responsibility capability that produces structured output |
| **Specialist Agent** | An agent that handles domain-specific implementation (backend, frontend, docs) |
| **Token** | A unit of text processing (roughly ¾ of a word in English) |
| **TDD** | Test-Driven Development — write tests before implementation |
| **Ubiquitous Language** | A shared vocabulary ensuring all team members use the same terms for the same concepts |
| **Workflow** | A structured sequence of phases that enforces a specific development process |
| **Workflow Artifact** | A numbered file produced by a workflow phase, stored in `.ai-workflow/` |
| **YAGNI** | You Ain't Gonna Need It — don't build something until you actually need it |
