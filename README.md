# AI Prompts

Agents, skills, and flows for AI-assisted development — written as markdown, kept in one place, and linked into the projects that use them.

## What's here

```
ai-prompts/
├── src/                 # the flows — single source of truth (edit here)
│   ├── PLAN.md          # the design: read this first
│   ├── agents/          # orchestrator, 4 flow adapters, 18 subagents
│   ├── skills/          # the skills those subagents apply
│   ├── flows/           # tool-agnostic phase manifests
│   ├── schemas/         # conventions (skill-params, findings, contract IDs, ...)
│   ├── templates/       # artifact templates
│   ├── contexts/        # per-org overrides (duelbits/)
│   └── scripts/         # manifest-lint.sh
├── src-duelbits/        # client-specific skills (site-rewrite-planner, explain-task original)
├── docs/ai-concepts.md  # background: agents, skills, context engineering
└── AGENTS.md            # how to write and maintain a skill
```

## The flows

Every task starts at the [orchestrator](src/agents/orchestrator.agent.md). It resumes an in-progress flow if there is one, otherwise classifies the request and hands off:

| Request | Flow | Core rule |
|---|---|---|
| Something is broken | [debug](src/flows/debug-flow.md) | Never jump to the fix — root cause first |
| New functionality | [feature](src/flows/feature-flow.md) | Design before code |
| Working code, make it better | [improvement](src/flows/improvement-flow.md) | Understand before changing; measure before and after |
| New project from scratch | [greenfield](src/flows/greenfield-flow.md) | Vision before code; build Milestone 1 only |

A thin orchestrator spawns stateless subagents, one bounded task each. Markdown artifacts in `.ai-workflow/[feature]/` are the contract between them, and `INDEX.md` lets a flow resume in a new session. A severity gate at the start sizes the process to the change, so a two-file fix doesn't get the full treatment. Repo facts (commands, test runner, PR conventions) come from `.ai-rules/project.md` in the target repo instead of being guessed.

**Model tiers.** Agents carry a tier, not a model: **S** for planning, the ADR, review, and rules; **A** for analysis; **B** for executing a decided plan (coding, docs, specs); **C** for trivial work. Each company's `models.md` says which model is each tier in each tool — [Duelbits](src/contexts/duelbits/models.md) (OpenRouter via Copilot), [Clair](src/contexts/clair/models.md) (Claude Code, Cursor). Keep them current with `src/scripts/models_refresh.py <company>`. Details: [agent-tiers.md](src/schemas/agent-tiers.md).

Start with [src/README.md](src/README.md) for the index, then [src/PLAN.md](src/PLAN.md) for the design.

**Status**: everything is written, but no flow has been run end to end on a real task yet — see [src/VERIFICATION.md](src/VERIFICATION.md).

## Using it in a project

Link the agents and skills into the folders your AI tool discovers:

```bash
# GitHub Copilot
mkdir -p .github/agents .github/skills
ln -s ~/Projects/personal/ai-prompts/src/agents/* .github/agents/
ln -s ~/Projects/personal/ai-prompts/src/skills/* .github/skills/

# Claude Code
mkdir -p .claude/agents .claude/skills
ln -s ~/Projects/personal/ai-prompts/src/agents/* .claude/agents/
ln -s ~/Projects/personal/ai-prompts/src/skills/* .claude/skills/
```

Agents and skills link to `flows/`, `schemas/`, and `templates/` by relative path inside `src/`, so the tool has to read them through the symlink to their real location.

Mechanical checks run as scripts from this repo, so point `AI_PROMPTS` at your checkout (e.g. in `~/.zshrc`):

```bash
export AI_PROMPTS=~/Projects/personal/ai-prompts
```

Then start a task through the orchestrator, e.g. `@orchestrator add user profile picture upload`.

Check for broken links after moving things:

```bash
find .github .claude -type l ! -exec test -e {} \; -print
```

## Contributing

- Edit in `src/` only — never in a project's `.github/` or `.claude/` links.
- Skills follow [AGENTS.md](AGENTS.md). A skill a flow phase invokes opens with `## Parameters` and `## Where this runs`.
- After changing a flow manifest, run `src/scripts/manifest-lint.sh`.

## History

`src/` was built as `src-v2/` next to an earlier set of workflows (v1). v1 has been retired and merged in — see [src/PLAN.md § History](src/PLAN.md#history-v1-retirement). It's all in git history.
