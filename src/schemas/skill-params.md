# Schema: Skill-Params Block

**Slice**: 0 (Foundations)
**Used by**: every skill under [skills/](../skills/) that a flow phase invokes; every orchestrator/adapter that spawns a subagent using a skill

## Purpose

Skills are markdown — they have no function signature. This block is how an orchestrator "passes parameters" to a skill without forking it per flow, instead of hardcoding phase numbers and output paths inside the skill body.

## Format

The orchestrator prepends this HTML-comment block to the task prompt when spawning a subagent that invokes a skill:

````markdown
<!-- skill-params
phase: "3.1"
output: .ai-workflow/multi-wallet/3.1-architecture.md
inputs:
  - .ai-workflow/multi-wallet/2-prd.md
  - .ai-workflow/multi-wallet/3.0-component-map.md
findings: .ai-workflow/multi-wallet/FINDINGS.md
context_pack: src/contexts/duelbits
-->
````

It is HTML comment syntax so it renders as nothing in any markdown viewer, including inside the artifact it may get pasted into.

## Placeholders

| Key | Meaning | Required? |
|---|---|---|
| `phase` | The phase/sub-phase ID this invocation belongs to (e.g. `"3.1"`, `"6.0"`) | Yes — every skill uses it in headers/logging |
| `output` | Exact file path the skill must write | Yes |
| `inputs` | List of exact file paths (and, where the skill's own docs say so, sections) the skill must read — never "the whole folder" | Yes |
| `findings` | Path to the flow's `FINDINGS.md`, for skills that read or write findings | Only for skills that touch the ledger — see [findings.md](findings.md) |
| `context_pack` | Path to a `src/contexts/<ctx>/` directory the skill should resolve template overrides from | No — omit for the default templates |

A skill may ignore placeholders it has no use for. A skill must not invent new placeholder names without documenting them in its own `## Parameters` section.

## Rules

1. **Every placeholder has a documented default** — the phase and output the skill normally runs at. The default lives in the skill's own `## Parameters` section, not in this schema.
2. **Unknown keys are ignored.** A skill-params block may carry keys a given skill doesn't consume (e.g. `context_pack` passed to a skill with no context-pack support yet) — the skill silently skips them.
3. **A missing required key falls back to the skill's default**, and the skill's return summary says so in one line (e.g. `output defaulted to .ai-workflow/[feature]/3.1-architecture.md — no output key in skill-params`). Never fail the phase over a missing key; a stale caller is a caller bug, not a blocking error.
4. **`inputs` names files and, where relevant, sections** — see the Input Budget rule in [Quality Rules](../PLAN.md#quality-rules). A skill given a bare folder path in `inputs` should treat it as underspecified and read only the files it can justify from the task description.
5. The block sits at the very top of the spawned subagent's task prompt, before any task-specific prose.

## Skill-side contract

Every skill a flow phase invokes has two sections near the top of its `SKILL.md` (e.g. [skills/grill-me/SKILL.md](../skills/grill-me/SKILL.md)):

- `## Parameters` — which placeholders it reads, and its defaults
- `## Where this runs` — which phases and subagents invoke it, what it reads, and what it writes

## Related

- [artifact-status.md](artifact-status.md) — the header every `output` file must carry
- [index-frontmatter.md](index-frontmatter.md) — where `current_phase` (source of `phase`) lives
- [Skill Parameterization](../PLAN.md#skill-parameterization) — what each skill used to hardcode, and what it reads now
