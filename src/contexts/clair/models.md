---
company: clair
source: openrouter-public   # Clair's models aren't listed by any API; OpenRouter's public catalog tracks their releases and prices
vendors: anthropic, openai
---

# Models: Clair

Clair provides Claude, GPT, and Cursor's own models, used through **Claude Code** and **Cursor**. What the tiers mean, and which agent runs at which tier: [agent-tiers.md](../../schemas/agent-tiers.md).

## Models

The **first row of each tier is the default** the install step uses; later rows are alternates. A `?` tool ID means it hasn't been confirmed — copy the exact ID from the tool (Cursor: Settings → Models), never the display name. An agent that needs images (`needs: vision`) skips rows without ✅ in **Vision**.

| Tier | Model | Claude Code | Cursor | Vision | $ in / out per M | Context | Why |
|---|---|---|---|---|---|---|---|
| S | anthropic/claude-opus-5.5 | opus | ? | ✅ | 4 / 20 | 1000000 | Best reasoning in regular use; planning, ADR, review, rules |
| A | anthropic/claude-sonnet-5.5 | sonnet | ? | ✅ | 2 / 10 | 1000000 | Analysis and contracts at half Opus' price |
| B | anthropic/claude-sonnet-5.5 | sonnet | ? | ✅ | 2 / 10 | 1000000 | Clair has no cheap strong coder in regular use yet, so B = A here — see candidates |
| C | anthropic/claude-haiku-5.5 | haiku | ? | ✅ | 0.1 / 0.5 | 1000000 | Side questions, summaries |

**Independent agents** (`plan-critic`, `feature-analyst`) need an A model from a vendor other than Anthropic — Clair has none classified yet, so they fall back to Sonnet and say `not independent`. Classifying a GPT model at A (see candidates) fixes that.

Claude Code IDs are aliases that follow the latest model of each family, so they don't go stale on a version bump — the `Model` column still records which version was classified. Fable is left out on purpose: the harness makes Opus good enough at S.

## Candidates to evaluate

Not classified yet: prices are known, capability isn't. Run a couple of real tasks on one before giving it a tier.

| Model | $ in / out per M | Note |
|---|---|---|
| anthropic/claude-haiku-5.5 as **B** | 0.1 / 0.5 | 20× cheaper than Sonnet; try it on `implementer` tasks that 6.0 specified tightly |
| Cursor's own models (e.g. Composer) | — | Not on OpenRouter; could be the cheap B inside Cursor |
| openai/gpt-6.2-sol | 2 / 10 | A/B candidate |
| anthropic/claude-fable-5.2 | 8 / 40 | Excluded by choice; here if Opus at S ever falls short |

## Refresh

```bash
src/scripts/models_refresh.py clair            # report: new, removed, repriced, suggested tiers
src/scripts/models_refresh.py clair --apply    # confirm each change, then rewrite the table above
```
