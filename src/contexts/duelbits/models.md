---
company: duelbits
source: openrouter-key      # GET /models/user — only what the Duelbits key can use. Needs OPENROUTER_API_KEY in the environment
vendors: all
---

# Models: Duelbits

Duelbits provides an **OpenRouter** key, used through **GitHub Copilot** (VS Code, "bring your own key"). What the tiers mean, and which agent runs at which tier: [agent-tiers.md](../../schemas/agent-tiers.md).

> ⚠️ **Unconfirmed**: that Duelbits' Copilot policy allows bring-your-own-key, that an OpenRouter model can be named in a Copilot agent's `model:` field, and the exact ID format Copilot uses for it (the `Copilot` column). Test once in VS Code: add the key under *Manage Models*, start typing `model:` in an `.agent.md` file, and copy the ID Copilot completes.

## Models

The **first row of each tier is the default** the install step uses; later rows are alternates. An agent that needs images (`needs: vision`) skips rows without ✅ in **Vision**.

| Tier | Model | Copilot | Vision | $ in / out per M | Context | Why |
|---|---|---|---|---|---|---|
| S | anthropic/claude-opus-5.5 | ? | ✅ | 4 / 20 | 1000000 | Best reasoning in the set; planning, ADR, review, rules |
| A | anthropic/claude-sonnet-5.5 | ? | ✅ | 2 / 10 | 1000000 | Strong analysis and contracts at half Opus' price |
| A | moonshotai/kimi-k3.1-pro | ? | ✅ | 0.253 / 8.8 | 1048576 | Alternate A: much cheaper input than Sonnet — evaluate against Sonnet on analysis phases |
| B | z-ai/glm-5.3 | ? | ❌ | 0.0699 / 1.4 | 1048576 | Default coder for specified tasks; ~7× cheaper output than Sonnet. No images |
| B | minimax/minimax-m3 | ? | ✅ | 0.3 / 1.2 | 1048576 | Cheap coder with vision — the B pick for `qa-automator`'s UI branch |
| B | qwen/qwen3.8-max-0902 | ? | ✅ | 2 / 6 | 1000000 | Stronger, pricier B — try it when GLM tasks escalate often |
| C | z-ai/glm-5.3-flash | ? | ✅ | 0.15 / 0.5 | 1048576 | Side questions, summaries |
| C | qwen/qwen3.8-flash | ? | ✅ | 0.15 / 0.47 | 1000000 | Alternate C |
| C | minimax/minimax-m3.1-flash | ? | ✅ | 0.15 / 0.6 | 1048576 | Alternate C |

Tiers set 2026-11-19 from the models in regular use: Opus/Sonnet for judgment, GLM/MiniMax/Qwen/Kimi for the cheaper work. Fable is left out on purpose — the harness makes Opus good enough at S.

## Candidates to evaluate

Not classified yet. Run a few real tasks on one before moving it into the table.

| Model | $ in / out per M | Note |
|---|---|---|
| anthropic/claude-fable-5.2 | 8 / 40 | Excluded by choice (see above); here if Opus at S ever falls short |
| qwen/qwen4-max | 1.42 / 4.27 | Newest Qwen (2026-11-15) — B/A candidate, may replace qwen3.8-max |
| openai/gpt-6.2-astra | 8 / 40 | Priced like an S candidate |
| google/gemini-4-neon | 3 / 15 | Priced like an A candidate |
| openai/gpt-6.2-sol | 2 / 10 | A/B candidate |
| deepseek/deepseek-v4.1-flash | 0.3 / 1.2 | Cheap B candidate |

## Refresh

```bash
export OPENROUTER_API_KEY=...                     # never committed or written by the script
src/scripts/models_refresh.py duelbits            # report: new, removed, repriced, suggested tiers
src/scripts/models_refresh.py duelbits --apply    # confirm each change, then rewrite the table above
```
