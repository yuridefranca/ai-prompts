---
name: explain-task
description: >-
  Living mobile-first HTML walkthrough of the current ticket for a new joiner.
  Starts with the problem, then screenshots of the problem and current state,
  then simple-term solution alternatives to validate before any code. Deepens
  with watch-outs, impact, and implementation after an approach is chosen.
  Use when the user says explain this task, explain this ticket, walk me
  through this ticket, task walkthrough, or as the Orient step after focus /
  at the start of a human-driven build ticket.
disable-model-invocation: true
argument-hint: "Ticket ID, PR URL, or current task"
---

# Explain Task

Write (or deepen) one **self-contained HTML briefing** so a new joiner can read the current ticket on a phone.

This is not `explain <topic>` (one-shot in-chat) and not `learn <topic>` (a multi-session domain course). This file is **this ticket**, and it gets richer at each workspace step.

Read [FORMAT.md](FORMAT.md) before writing HTML. Load `.cursor/rules/personal-task-artifacts.mdc` and write **all** files for this ticket into that one kebab-case folder.

## Output

```text
personal/tasks/<kebab-slug>/walkthrough.html
personal/tasks/<kebab-slug>/assets/
```

Example: `FD-1234` “Ineligible dashboard” → `personal/tasks/fd-1234-ineligible-dashboard/`.

- Resolve the folder from the rule (reuse `personal/tasks/<ticket>-*` if it already exists).
- **Later steps:** update `walkthrough.html` in place. Save new captures under `assets/`.
- After saving: `open "personal/tasks/<kebab-slug>/walkthrough.html"` (macOS), `xdg-open` (Linux). Tell the user the folder path so they can AirDrop the HTML.

Skip this skill for the autonomous Linear bot.

## Audience

Assume the reader joined recently and is reading on a phone.

- Define Clair terms on first use, then use them. Link `docs/reference/glossary.md` in citations, do not dump the glossary.
- Lead with the employee or partner experience. File paths, HTTP routes, and class names wait until the **Build** stage, and only after an approach is confirmed.
- Do not invent, reword, or “improve” cardholder-facing copy. Quote the ticket or use `[COPY PENDING PATHWARD APPROVAL — FD-XXXX]`.

## Validate before code

The first run exists so the reader can **check the logic** before anyone writes tests or production code.

1. State the **problem**.
2. Show **screenshots of the problem** and of **how it works today**.
3. Offer **ways to solve it** in simple terms (no implementation). If more than one approach is plausible, list them and recommend one. If only one is plausible, still write it as an approach to confirm.
4. **Stop.** Ask in chat which approach to take (or to confirm the only one). Do not start `tdd`, a dev plan’s implementation, or a **Code** section until they answer.

Skip this gate only when the HTML is already past Clarify (an approach was chosen) or the user says to proceed.

## Stages (living file)

Detect the current workspace step from the chat, ticket, branch, or diff. Fill **Context** on the first run even if the work is already further along. On later runs, keep earlier sections and deepen the current stage.

| Stage | When | Add to the HTML |
|-------|------|-----------------|
| **Context** | After `focus`, first run | Problem, current-state screenshots, solution alternatives in simple terms, first **Watch outs**. Then wait for the reader to pick an approach |
| **Clarify** | After they pick / after `grill` | Chosen approach, in/out of scope, terms; refresh Watch outs |
| **Plan** | After `dev plan` | The TDD slices in user language, what “done” looks like; which slices exist to catch the flaws |
| **Build** | During `tdd` / implementation | Grouped code walkthrough of the actual change; confirm or drop each Watch out against the code |
| **Review** | During `code review` / `consensus review` | What a reviewer should check; Watch outs become evidence-backed |
| **Ship** | After `ship this` / draft PR | How to try it, what shipped, what Care/partners should watch |

Progress UI in the HTML must show all six stages and mark the current one.

## Load first

1. Focus file for the inferred area (router table in `.cursor/rules/clair-workspace-context.mdc`).
2. Linear issue (acceptance criteria, comments, Figma/attachments). GitHub PR if one exists.
3. `docs/reference/glossary.md` for terms you will use.
4. Surrounding product behavior for **The problem** and **Current state**, not a dump of the ticket description.
5. `docs/reference/data-models.md` when identity, employment, or partner/core records are involved.
6. **Consumers** of anything this ticket changes: routes, fields, enums, tokens, jobs, events, flags, copy. Search sibling repos (SDKs, clair-flex, Kraken, partner-portal) even if the ticket names one repo. Use that search to name alternatives and Watch outs, not to open with code.

Never guess product behavior. If a source is missing, say so in a callout.

## Visuals (required, not decorative)

Pair pictures with the problem, not with the eventual code. Caption every figure as **Problem**, **Current**, or **Proposed**.

**Problem** — evidence of the pain: the broken/missing screen, the wrong amount, the Care-facing symptom. Figma of “what is wrong” or a browser capture of the failing flow.

**Current** — how the product works today on the screens this ticket touches. Browser/staging when possible; otherwise an HTML phone-frame mock labeled Current.

**Proposed** — only under **Ways we can solve it**, and only for the alternative it belongs to (usually Figma of the intended UI). Do not present a future design as if it were today’s product.

**Figma** — if the ticket, comments, or PR mention a Figma URL:

1. Parse `fileKey` and `nodeId` (`node-id=1-2` → `1:2`).
2. Discover `plugin-figma-figma` / `get_screenshot`, then call it. Do **not** run the design-to-code skill; this is illustration, not implementation.
3. Download the PNG (screenshot URLs are short-lived). Save it under `personal/tasks/<kebab-slug>/assets/` **and** embed a `data:image/png;base64,...` URI in the HTML so the walkthrough stays one file on a phone.
4. Caption what the employee or partner sees. Do not transcribe unreadable copy.

**Browser / product UI** — capture the current screens the ticket actually touches. One render is not enough when a flow has more than one step.

If Figma and browser capture both fail, say that in a callout and build HTML mocks using the phone-frame diagram family. Never ship a walkthrough that is only text.

## Ways we can solve it

Describe each approach so a new joiner can check the logic. No class names, routes, or file paths.

For every alternative:

- What would change for the employee or partner
- What would stay the same
- Main risk (tie to a Watch out when you can)
- Why you would or would not pick it

If more than one approach is plausible, list 2–3, mark **Recommended**, and say why in one sentence. If the ticket already chose, still show the discarded options when they are real (so the reader can disagree).

Do not invent a second option to look thorough. One honest approach is better than a fake choice.

## Watch outs (required from the first run)

A new joiner should finish the page knowing **what can go wrong**, not only the happy path. Put it in the HTML as the **Watch outs** section in [FORMAT.md](FORMAT.md), **after** the alternatives so it helps them pick.

Investigate, then write **2–5 concrete cards**. Empty “be careful” lists are a miss. Each card needs:

| Field | What to write |
|-------|----------------|
| **Watch for** | The trap in simple terms (wrong employment, stale limit, copy that is not Pathward-approved) |
| **Logic flaw** | How the ticket or an alternative could be wrong: missing branch, two sources of truth, race, treating a log as a tap, celebrating a denial |
| **Who feels it** | Employee, partner, Care, finance, another team — name one |
| **Other features** | What else moves or breaks: lending/eligibility, SDK init, widget, Kraken, ECL, score limits, notifications, another ticket |
| **If we get this wrong** | The business outcome in one sentence (`employee sees $80 they cannot take`, `Care thinks the advance failed`, `partner roster drifts from core`) |
| **How we know** | Ticket, code path, or “uncertain — confirm in grill” |

Probe at least these when they apply (skip a row that does not):

- Money, limits, eligibility, underwriting, repayments
- SDK init, session, widget, entry-point logging (a `click` is not always a tap)
- Employment lens vs user vs roster employee; partner-flex vs core-flex as source of truth
- Cardholder copy / Pathward
- Feature flags and partial rollouts (some employees on old behavior)
- Events, jobs, projections getting out of step
- Kraken / Care seeing a different story than the widget
- Hot paths: do not add synchronous non-critical work on init/session/widget load

Reuse the **stack hop** diagram with the affected hops highlighted. That is the blast radius.

Mark guesses as guesses. Prefer “I have not traced X” over a confident invention.

## First run vs update

**First run (Context) — stop before code:**

1. Skippable Clair background in `<details>`.
2. **The problem** — who feels it, what is wrong, why this ticket exists. Toy data. No implementation.
3. **What it looks like** — Problem screenshots, then Current screenshots.
4. **Ways we can solve it** — simple-term alternatives; recommend one if there are several.
5. **Watch outs** — at least two cards (from ticket + surrounding system).
6. Quiz on the *problem* and *which approach handles a watch-out*. Not class names.
7. Next step: ask them to pick (or confirm) an approach. Do not suggest `tdd` yet.

**Update:** rewrite the current stage in place. After they pick an approach, lock it in Clarify. Refresh Watch outs (confirm, drop, or add). Add **Code** only at Build. Refresh the quiz. Keep prior stages. Group code changes in an understandable order; do not walk files in diff order.

## Chat wrap-up

Keep the in-chat reply short: folder path, which stage you filled, the alternatives in one line each, and **which approach you recommend**. Ask them to confirm before any implementation. Do not paste the HTML into chat.
