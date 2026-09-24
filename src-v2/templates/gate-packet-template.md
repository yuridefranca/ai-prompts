# Template: Gate Packet

**Slice**: 2
**Used by**: the orchestrator, at every ⛔ gate (2, 4, 6.0, 9, and debug's 2.5-deep)

A gate packet is the **chat-surface** rendering of a gate artifact's Layer 1 — built fresh every time a gate is presented, including on resume (see [resume procedure § step 3](../schemas/index-frontmatter.md#resume-procedure): "re-present the gate packet — never assume a gate was approved off-record").

## Shape

````markdown
## ⛔ GATE: {phase} — {artifact title}

**Since your last approval**: {N} tasks · {M} deviations · {K} findings

{Layer 1 content, verbatim or lightly re-flowed — never re-summarized into something shorter than the artifact's own Layer 1}

> ⚠️ **DECISION NEEDED**
> {the specific choice: approve as-is / name what to change}

┌ CHECKS (type an answer to at least one before I proceed)
│ 1. {question}
│ 2. {question}
│ 3. {question}
└

Full detail: {artifact path}
````

## Rules

1. **Delta block first.** "Since your last approval: N tasks, M deviations, K findings" — the dev should know the shape of what changed before reading anything else. Omit it only for the very first gate in a flow (phase 2), where there is no "last approval" yet.
2. **The decision box is never buried.** It comes after Layer 1, before CHECKS, always visually distinct (`> ⚠️ **DECISION NEEDED**`).
3. **CHECKS bind here.** At a ⛔ gate the dev must type an answer to at least one question before the orchestrator proceeds. This is the one place in the flow where CHECKS are enforced rather than a reading aid — see [artifact-template.md § What Layer 1 is not](artifact-template.md) and phase 4's specific miss-handling in [feature-flow.md](../flows/feature-flow.md#phase-4--decision-validation--gate-full-tier-only).
4. **Never present raw subagent output as the gate packet.** The packet is built from the artifact's Layer 1, not from the subagent's return message — see [Orchestrator Compression Duty](../PLAN.md#orchestrator-compression-duty).
5. **A gate always names the file path** at the bottom, so the dev can open Layer 2 without asking where it is.

## Related

- [artifact-template.md](artifact-template.md) — where Layer 1 (the content this packet wraps) comes from
- [task-packet-template.md](task-packet-template.md) — the non-gate, per-task sibling of this template
- [../schemas/index-frontmatter.md](../schemas/index-frontmatter.md) — the resume rule that re-triggers this packet
