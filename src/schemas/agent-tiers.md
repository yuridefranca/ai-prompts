# Schema: Agent Model Tiers

**Used by**: every agent file (`tier:` frontmatter), every standalone skill that carries a `tier:`, the per-company model lists in [contexts/](../contexts/), and the install step that writes `model:` into agent files.

## Purpose

Run the expensive, best-reasoning models where judgment decides the outcome — planning, the ADR, stress tests, review, rules — and cheap models where the work is already decided and only needs doing — implementing a task `6-solution.md` specified, writing docs from a diff, translating a QA plan into Playwright specs.

**Tiers name a job, not a model.** Which concrete model is "S" depends on which company you're working for (which provider key you have) and which tool runs the agents. Agent files therefore carry a tier, never a model name; the model is resolved from the company's `models.md` when the agents are installed into a project. This keeps the agent files and flow manifests tool-agnostic.

## The tiers

| Tier | Job | Pick a model that is… |
|---|---|---|
| **S** | Planning, adjudicating, setting rules — work whose mistakes every later phase inherits | the best reasoning model available, regardless of price |
| **A** | Independent analysis and structured writing that a gate or reviewer will check | strong at reasoning and code, noticeably cheaper than S |
| **B** | Executing a decided plan: code for a specified task, docs from a diff, specs from a written plan | good at code and tool use, fast and cheap |
| **C** | Trivial: side questions, summaries, formatting | the cheapest model that follows instructions |

A model is classified by **capability first, price second**: S is "best available," not "most expensive."

## Default tier per agent

The tier lives on the **agent**, because the agent is the job: the same skill can run at different tiers in different phases (`grill-me` is S inside `prd-writer` at phase 2 and A inside `quiz-master` at phase 4). Skills inside the flows carry no tier.

| Agent | Phase(s) | Tier | Why |
|---|---|---|---|
| `orchestrator` + the four `*-workflow` adapters | all | **S** | Gates, tier proposals, failure-edge decisions, the 9.5 rule harvest (`.ai-rules/review.md` additions). Cheap to run at S: the orchestrator only ever reads Layer 1 summaries |
| `prd-writer` | 1, 2 | **S** | The PRD and its grilling define what everything after it builds |
| `roadmap-planner` | 2.1 (greenfield) | **S** | Scopes Milestone 1 — a planning decision |
| `rca-analyst` | 2.5 (debug) | **S** | A wrong root cause wastes every phase after it |
| `synthesizer` | 3.4 | **S** | The most judgment-heavy step: adjudicates three conflicting analyses into the ADR |
| `solution-planner` | 6.0 | **S** | Task plan + stress test + pre-mortem |
| `reviewer` | 7 | **S** | Business-logic judgment and the re-attack of open findings |
| `task-explainer` | 0.5 + updates | **A** | Plain-language alternatives and watch-outs; the dev checks it at the 0.5 gate |
| `architect`, `data-flow-analyst`, `feature-analyst` | 3.1–3.3 | **A** | Independent analyses; `synthesizer` (S) reconciles them |
| `quiz-master` | 4 | **A** | Decision questions, answered by the dev |
| `tdd-engineer` | 5 | **A** | Clause kind/level is judgment; the test code is mechanical |
| `qa-planner` | 8.1 | **A** | Adversarial scenario design |
| `implementer` | 6.1..n, 6.x, 3.5 | **B** | Implements a task 6.0 already specified; reconciliation is a mechanical diff |
| `doc-writer` | 6.y | **B** | Transcribes decisions already made |
| `qa-automator` | 8.3 | **B** | Plan + real DOM → specs |
| `pr-manager` | 9, 9.1 | **B** | Assembles already-decided content |
| `repo-mapper` | bootstrap | **B** | Inspection; every fact carries a `verify:` command |

Phase 3.0 (`component-mapper`, run standalone by the adapter) runs at **B**.

## Standalone skills

Skills used **outside** the flows may carry a `tier:` in their frontmatter (`btw` → C, `agents-md-generator` → A). Only Claude Code can honor it: the install step turns it into `model:` + `context: fork` (a skill whose model differs from the session's should run in its own context). Copilot and Cursor have no per-skill model and ignore the field.

## Rules

1. **Gate artifacts are produced at S or A, never B/C.** Every agent that writes a ⛔ artifact is S except `task-explainer` (A, 0.5 mini-gate) and `pr-manager` (B) — the phase 9 gate is the dev approving a PR assembled from S/A artifacts, which is acceptable.
2. **Escalation, not retry at the same tier.** When the dev rejects a B/C agent's output at per-task review (or a QA failure loops back to 6.1), the re-spawn runs **one tier up**, via the escalation twin `<agent>-up` that the install step generates for every B/C agent (e.g. `implementer-up` at A). The adapter logs the escalation in `INDEX.md`'s decision log. A second rejection follows the normal [failure edges](../flows/feature-flow.md#failure-edges).
3. **The tier shows in the packet.** Task and gate packets note the tier that produced the artifact (`spawned at B · implementer`), so a reviewer knows what to expect and a pattern of escalations is visible.
4. **Capabilities filter the pick.** An agent that declares `needs: vision` (`task-explainer` for screenshots, `qa-automator` for the UI branch) gets the first model in its tier with ✅ in the **Vision** column, not just the first row.
5. **A tier with no model falls up.** If a company's `models.md` has no B model for a tool, B agents use that tool's A model, and so on up to S. Never down.
6. **A repeated escalation is a gotcha.** If the same kind of task escalates in two runs, the 9.5 harvest proposes a tier change for that agent or a sharper task template in 6.0 — so the defaults above self-correct.

## Resolving a tier to a model

```
agent file  tier: B
    ↓  install step, given --company and --tool
contexts/<company>/models.md  →  row for tier B, column for that tool
    ↓
installed agent file  model: <exact model ID for that tool>
```

- Each company's model list lives in its context pack: [contexts/duelbits/models.md](../contexts/duelbits/models.md), [contexts/clair/models.md](../contexts/clair/models.md).
- Use the **exact model ID** each tool expects, not the display name — Cursor silently falls back to the parent's model on an unknown ID, and Copilot BYOK models have provider-qualified IDs.
- Lists are refreshed with [scripts/models_refresh.py](../scripts/models_refresh.py): it pulls the provider's current models and prices, flags what's new, removed, or repriced, and suggests a tier. **A person confirms every tier change**; the script never writes one on its own.

**Not yet built**: the install step (`scripts/install-agents`) that writes `model:` into agent files and generates the `-up` twins. Until it exists, set `model:` by hand when linking agents into a project. It waits on confirming that Copilot honors a BYOK (OpenRouter) model in an agent file's `model:` field, and whether a subagent keeps its own model when spawned.

## Related

- [../agents/README.md](../agents/README.md) — the roster, with tiers
- [../flows/feature-flow.md § Failure Edges](../flows/feature-flow.md#failure-edges) — where escalation plugs in
- [../contexts/](../contexts/) — per-company model lists
