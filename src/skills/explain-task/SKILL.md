---
name: explain-task
description: >-
  Living mobile-first HTML walkthrough of the current feature/bug for a new
  joiner. Starts with the problem, then screenshots of the problem and
  current state, then simple-term solution alternatives to confirm before
  any formal spec or code. Deepens at each later phase after an approach is
  chosen. Adapted from src-duelbits/skills/explain-task for the flows.
---

# explain-task

Write (or deepen) one **self-contained HTML briefing** so someone new to this codebase can read the current feature/bug on a phone, before any formal spec or code exists.

Adapted from [src-duelbits/skills/explain-task](../../../src-duelbits/skills/explain-task/SKILL.md) — same core idea (living HTML walkthrough, stages, watch-outs, quiz), retargeted from a Cursor-rules/Linear-specific workflow to `.ai-rules/project.md` and the flow phase model. Read [FORMAT.md](FORMAT.md) before writing HTML.

## Parameters

Read `{{phase}}`, `{{output}}`, and `{{inputs}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Backs `task-explainer`, spawned across the whole flow — see [task-explainer.agent.md](../../agents/task-explainer.agent.md) for the full spawn table. The stage this skill's living-file design describes maps directly onto v2 phases:

| This skill's stage | Flow phase | Mode |
|---|---|---|
| Context | 0.5 (Orient) | create |
| Clarify | 2 (PRD) | update |
| Plan | 6.0 (Solution plan) | update |
| Build | 6.x (Reconciliation) | update |
| Review | 7 (Review) | update |
| Ship | 9 (PR) | update |

**Tier gate**: skipped on the `small` feature tier / `trivial` debug tier — see [feature-flow.md § Phase 0.5](../../flows/feature-flow.md#phase-05--orient--mini-gate) — a two-file change doesn't need an onboarding walkthrough. Also skipped for any run where the dev declines it at bootstrap (same opt-out shape as `.ai-rules/project.md` itself).

## Output

```text
.ai-workflow/[feature]/0.5-walkthrough.html
.ai-workflow/[feature]/assets/
```

- **Not `personal/tasks/<slug>/`** (the src-duelbits original's path) — this lives inside the flow's own `.ai-workflow/[feature]/` folder like every other artifact, so it's found, resumed, and promoted the same way.
- Carries the artifact-status header as an HTML comment at the top of the file (see [artifact-status.md § Non-markdown artifacts](../../schemas/artifact-status.md#non-markdown-artifacts)) — same `draft`/`complete` discipline as every other artifact.
- Tier: `[knowledge]` — promoted to `Docs.features` at phase 9 alongside the other knowledge-tier markdown (see [artifact-lifecycle.md](../../schemas/artifact-lifecycle.md)); it's exactly the "why is it built this way" artifact that tier exists for, just HTML instead of markdown.
- **`INDEX.md` is still the flow's index — do not treat this file as replacing it.** (The src-duelbits original's FORMAT.md said "do not keep a separate INDEX.md — the folder name is the index"; that doesn't apply here, `INDEX.md` already exists and means something specific — see [index-frontmatter.md](../../schemas/index-frontmatter.md).)
- After saving: tell the dev the file path so they can open it locally; do not paste the HTML into chat.

## Audience

Assume the reader is new to this codebase and is reading on a phone.

- Define domain terms on first use, then use them. Cite `.ai-rules/project.md` §Docs → `glossary` (if present) rather than dumping it.
- Lead with the user/business experience. File paths, routes, and class names wait until the **Build** update, and only after an approach is confirmed.
- Do not invent, reword, or "improve" user-facing copy. Quote the PRD/ticket or use `[COPY PENDING APPROVAL]`.

## Validate before formal work — the Orient gate

The first run exists so the reader can **check the logic** before `2-prd.md` is written or any code exists.

1. State the **problem**.
2. Show **screenshots of the problem** and of **how it works today**.
3. Offer **ways to solve it** in simple terms (no implementation). If more than one approach is plausible, list them and recommend one. If only one is plausible, still write it as an approach to confirm.
4. **Stop.** This is phase 0.5's mini-gate — the dev picks or confirms an approach before phase 1/2 proceed. See [feature-flow.md § Phase 0.5](../../flows/feature-flow.md#phase-05--orient--mini-gate) for the gate mechanics (same shape as the phase 6.0 mini-gate).

Skip this gate only when the walkthrough is already past Clarify (an approach was chosen on a prior run) or the dev says to proceed.

## Stages (living file)

Detect the current phase from `INDEX.md`. Fill **Context** on the first run even if the flow is already further along (e.g. resuming a session that never ran Orient). On later runs, keep earlier sections and deepen the current stage only.

| Stage | Flow phase | Add to the HTML |
|---|---|---|
| **Context** | 0.5, first run | Problem, current-state screenshots, solution alternatives in simple terms, first **Watch outs**. Then wait for the reader to pick an approach |
| **Clarify** | 2 (after PRD gate passes) | Chosen approach (from `2-prd.md`), in/out of scope, terms; refresh Watch outs |
| **Plan** | 6.0 (after solution-plan gate passes) | The task list from `6-solution.md` in plain language, what "done" looks like; which tasks exist to catch which flaws |
| **Build** | 6.x (after reconciliation) | Grouped code walkthrough of the actual diff; confirm or drop each Watch out against the real code |
| **Review** | 7 (after review finalized) | What a reviewer checked (from `7-review.md`); Watch outs become evidence-backed |
| **Ship** | 9 (after PR created) | How to try it, what shipped, what to watch post-merge (from `9-pr-notes.md`) |

Progress UI in the HTML must show all six stages and mark the current one.

## Load first

1. `.ai-rules/project.md` §Structure for path aliases/component locations (replaces the src-duelbits original's `.cursor/rules` router table).
2. The dev's original request. Existing ticket/issue/PR if the request references one — don't assume a specific tracker.
3. `.ai-rules/project.md` §Docs → `glossary` for terms you will use, if present.
4. Surrounding product behavior for **The problem** and **Current state** — explore the codebase, don't just restate the request.
5. `.ai-rules/project.md` §Docs → other paths (ADR, API) when relevant to the change.
6. **Consumers** of anything this change touches: routes, fields, events, flags, shared packages. Search sibling repos/packages this repo is known to interact with (per `.ai-rules/project.md` or `AGENTS.md`) even if the request names only one. Use that search to name alternatives and Watch outs, not to open with code.

Never guess product behavior. If a source is missing, say so in a callout.

## Visuals (required, not decorative)

Pair pictures with the problem, not with the eventual code. Caption every figure as **Problem**, **Current**, or **Proposed**.

**Problem** — evidence of the pain: the broken/missing screen, the wrong value, the user-facing symptom. Design-tool export of "what is wrong," or a browser capture of the failing flow.

**Current** — how the product works today on the screens this change touches. Browser/staging when possible; otherwise an HTML phone-frame mock labeled Current.

**Proposed** — only under **Ways we can solve it**, and only for the alternative it belongs to. Do not present a future design as if it were today's product.

**Design tool exports** — if the request, comments, or an existing PR mention a Figma (or equivalent) URL, use whatever design-extraction tooling this session has available; this is illustration, not implementation — do not run a design-to-code skill here. Save the source image under `.ai-workflow/[feature]/assets/` **and** embed a `data:image/png;base64,...` URI in the HTML so the walkthrough stays one file on a phone. Caption what the user sees; do not transcribe unreadable copy.

**Browser / product UI** — capture the current screens the change actually touches. One render is not enough when a flow has more than one step.

If design capture and browser capture both fail, say that in a callout and build HTML mocks using the phone-frame diagram family (see [FORMAT.md](FORMAT.md)). Never ship a walkthrough that is only text.

## Ways we can solve it

Describe each approach so a new joiner can check the logic. No class names, routes, or file paths.

For every alternative:

- What would change for the user
- What would stay the same
- Main risk (tie to a watch-out when you can)
- Why you would or would not pick it

If more than one approach is plausible, list 2–3, mark **Recommended**, and say why in one sentence. If the request already chose an approach, still show the discarded options when they're real, so the reader can disagree.

Do not invent a second option to look thorough. One honest approach is better than a fake choice.

## Watch outs (required from the first run)

A new joiner should finish the page knowing **what can go wrong**, not only the happy path. Put it in the HTML as the **Watch outs** section in [FORMAT.md](FORMAT.md), **after** the alternatives so it helps pick one.

Investigate, then write **2–5 concrete cards**. Empty "be careful" lists are a miss. Each card needs:

| Field | What to write |
|---|---|
| **Watch for** | The trap in simple terms |
| **Logic flaw** | How the request or an alternative could be wrong: missing branch, two sources of truth, race condition, misread event |
| **Who feels it** | End user, support, another team — name one |
| **Other features** | What else moves or breaks — name real systems this repo touches |
| **If we get this wrong** | The business outcome in one sentence |
| **How we know** | Request/ticket, code path, or "uncertain — confirm at the phase 2 gate" |

Probe at least these when they apply (skip a row that doesn't, and don't invent categories the repo doesn't have — use `.ai-rules/project.md`/`AGENTS.md` known-risk areas if the repo names any):

- Money, permissions, auth, or anything irreversible once it happens
- External integrations / third-party APIs
- Events, jobs, or projections that can drift out of step
- Feature flags and partial rollouts (some users on old behavior)
- Cross-team or cross-service consumers of what this change touches

Reuse the stack-hop diagram (see [FORMAT.md](FORMAT.md)) with the affected hops highlighted — that's the blast radius. At phase 0.5 this is usually your own best guess at the request→service→persistence chain (phase 3's real component map doesn't exist yet); redraw it accurately once `3.0-component-map.md`/`3.2-data-flow.md` exist, at the Clarify update.

Mark guesses as guesses. Prefer "I have not traced X" over a confident invention.

## First run vs update

**First run (Context, phase 0.5) — stop before formal work:**

1. Skippable codebase-orientation in `<details>` (source: `AGENTS.md`, `.ai-rules/project.md`, or direct exploration).
2. **The problem** — who feels it, what is wrong, why this change is needed. Toy data. No implementation.
3. **What it looks like** — Problem screenshots, then Current screenshots.
4. **Ways we can solve it** — simple-term alternatives; recommend one if there are several.
5. **Watch outs** — at least two cards.
6. Quiz on the *problem* and *which approach handles a watch-out*. Not class names.
7. Next step: ask them to pick (or confirm) an approach. Do not suggest starting `2-prd.md` yet — the orchestrator does that once this gate passes.

**Update:** rewrite the current stage in place. After they pick an approach at the 0.5 gate, lock it in at the Clarify update once `2-prd.md`'s own gate passes. Refresh Watch outs at each update (confirm, drop, or add). Add **Code** only at the Build update (phase 6.x). Refresh the quiz. Keep prior stages. Group code changes in an understandable order; do not walk files in diff order.

## Chat wrap-up

Keep the in-chat reply short: file path, which stage you filled, the alternatives in one line each, and **which approach you recommend**. Ask the dev to confirm before phase 1/2 proceed on the first run. Do not paste the HTML into chat.

## Related

- [FORMAT.md](FORMAT.md) — HTML structure, mobile-first CSS rules, diagram families, quiz mechanics
- [src-duelbits/skills/explain-task](../../../src-duelbits/skills/explain-task/SKILL.md) — the original this was adapted from (still WIP, client-specific, untouched)
- [../../agents/task-explainer.agent.md](../../agents/task-explainer.agent.md) — the subagent that invokes this skill across the flow
- [../../flows/feature-flow.md](../../flows/feature-flow.md), [../../flows/debug-flow.md](../../flows/debug-flow.md)
