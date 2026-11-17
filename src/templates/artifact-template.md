# Template: Generic Phase Artifact

**Slice**: 2
**Used by**: every subagent producing a phase artifact (all of `1-overview.md` through `9-pr-notes.md`)

This is the skeleton every phase artifact follows, implementing [Attention Engineering](../PLAN.md#attention-engineering)'s two-layer rule. Phase-specific templates ([index-template.md](index-template.md), [findings-template.md](findings-template.md), [qa-plan-template.md](qa-plan-template.md), [project-template.md](project-template.md), [review-rules-template.md](review-rules-template.md)) override sections here where the phase's content shape differs; they don't opt out of the header, Layer 1/2 split, or CHECKS box.

## Fence rule

**Any template containing a fenced code block must itself be fenced with four backticks.** A three-backtick fence nested inside a three-backtick fence terminates early and breaks rendering for everything after it. This template and its siblings all follow that rule.

## Skeleton

````markdown
---
artifact: {stem}
phase: "{phase}"
tier: knowledge | process
status: draft
produced_by: {subagent-name}
updated: {YYYY-MM-DD}
---

# {Artifact Title}

[status badge] · {one-line context, e.g. feature name, phase}

## Layer 1 — {verdict-first summary, max ~15–20 lines}

- Status block, never prose
- Tables, not paragraphs
- Deviation format where relevant: "plan said → actually did"
- A decision box if the dev needs to act:

> ⚠️ **DECISION NEEDED**
> {the specific choice, with options}

<details>
<summary>📊 Full detail</summary>

## Layer 2 — {everything else}

Full rationale, full analysis, full diagrams. This is what subagents read on
their next invocation — Layer 1's length budget is for the dev's attention,
not the model's. Never compress this section; compress only what the chat
surface shows.

</details>

┌ CHECKS (answer in your head — if you can't, read Layer 2)
│ 1. {why/what-happens-if question 1}
│ 2. {why/what-happens-if question 2}
└
````

## Section rules

| Section | Rule |
|---|---|
| Frontmatter | Exactly the [artifact-status header](../schemas/artifact-status.md) — `status: draft` written first, flipped to `complete` as the subagent's last action |
| Status badge | One of `[🟡 IN PROGRESS]` `[✅ COMPLETE]` `[⛔ GATED]` — see [Visual Document Standards](../PLAN.md#visual-document-standards) |
| Layer 1 | ≤15–20 lines. Prose is **banned** here — allowed only in Layer 2 rationale. If Layer 1 is boring, that's a quality signal, not a failure |
| `<details>` | Layer 2 is always present, even when short — a subagent's next read is always the full file, never the collapsed summary |
| CHECKS | 2 questions on regular artifacts, 3 at gate artifacts (`2-prd.md`, `4-quiz.md`, `6-solution.md`, `9-pr-notes.md`). "Why" and "what happens if" only, never "what". Written by the subagent that did the work — it knows which decisions were non-obvious. Answers live at the bottom of Layer 2 |

## What Layer 1 is not

> **Layer 1 is the chat surface only. Subagents always read the full file.** `<details>` means nothing to a subagent — the orchestrator compresses at the **chat boundary**, never in the file, and never passes its own Layer 1 summary downstream in place of a file path. See [Orchestrator Compression Duty](../PLAN.md#orchestrator-compression-duty).

## Comprehension check quality gate

The subagent writes the CHECKS; the **orchestrator** grades them, not the subagent grading itself. Reject and re-request a check that is:

- answerable by copying a phrase from Layer 1 verbatim
- a "what" question in disguise (`"What does the retry use?"`)
- about a decision the subagent didn't actually make

Three rejections on one artifact → flag the *work* as too mechanical to need a gate, and propose dropping a tier (this is an orchestrator judgment call, logged in the decision log, not an automatic tier change).

## Visual grammar (every artifact uses this vocabulary)

| Symbol | Meaning |
|---|---|
| ⛔ | Gate (requires approval) |
| ⚠️ | Deviation / flag |
| ✅ | As-planned / passed |
| ❓ | Open question |
| 🔴 | High severity |
| 🔵 | Low severity |

See [visual-standards.md](visual-standards.md) for the full Mermaid/table conventions and the explicit NOT-used list.

## Related

- [gate-packet-template.md](gate-packet-template.md) — the chat-surface packet the orchestrator builds *from* a gate artifact's Layer 1
- [task-packet-template.md](task-packet-template.md) — the 6.1..n per-task variant
- [Attention Engineering](../PLAN.md#attention-engineering) — narrative source
