---
name: documentation-writer
aliases:
    - feature-doc-writer
description: Write what a feature changed into the repo's real docs — AGENTS.md/CLAUDE.md, the feature README, architecture docs, glossary — from decisions already made in the flow's artifacts. Use at phase 6.y, after implementation and before review. Keywords documentation, AGENTS.md, CLAUDE.md, feature documentation, architecture documentation, glossary.
---

# Documentation

Transcribe what shipped into the repo's own docs, so the next developer or AI assistant finds and understands it. You record decisions; you don't make them.

## Parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md). **`{{output}}` defaults to the repo's own docs**, not a `.ai-workflow/` artifact.

## Where this runs

Backs [`doc-writer`](../../agents/doc-writer.agent.md) at phase 6.y. Reads `2-prd.md`, `3.4-tradeoffs.md`, `5-contract.md`, `6-solution.md`, and the diff. Writes to the paths in `.ai-rules/project.md` §Docs. Runs before phase 7, so the reviewer checks the docs against what shipped.

## Checklist

1. **Find the targets** in `.ai-rules/project.md` §Docs: agent context file (`AGENTS.md`/`CLAUDE.md`), `features` folder, architecture docs, glossary. A target that doesn't exist yet is created only if §Docs names it.
2. **Feature README** at `{Docs.features}/[feature]/README.md`: Overview (from the PRD) · Architecture (from the ADR) · API · Data model · Usage · Edge cases (from the contract). One short paragraph or table each; skip a section that doesn't apply.
3. **Agent context file**: add the feature in the existing format — purpose, location (paths), key components, dependencies, how it's used. Use `agents-md-generator` if the file needs restructuring.
4. **Architecture docs**: add the new components and data flow to the existing diagrams. **Mermaid only — never ASCII box art.**
5. **Glossary**: every domain term this feature introduces or redefines — one-sentence definition, also-known-as, context. Flag terms that mean different things in different layers.
6. **Inline comments**: only where the code does something non-obvious; explain why, not what.
7. **Check every statement against the diff**, not just the plan — the plan may have changed during implementation (see each §T{n}'s "plan said → actually did").

## Don't

- Invent behavior, limits, or rationale the artifacts don't state — write `TODO: confirm` instead.
- Paste whole artifacts into the docs; summarize and link.
- Leave docs only in chat: write the real files.

## Done when

- [ ] Every target in step 1 updated, or skipped with a one-line reason
- [ ] Nothing documented that the diff doesn't contain
- [ ] New domain terms are in the glossary

Templates (feature README, glossary) and examples: [references/guide.md](references/guide.md).
