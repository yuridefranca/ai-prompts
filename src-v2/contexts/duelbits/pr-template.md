# Context Pack: Duelbits PR Template

**Slice**: 7
**Resolved by**: `create-pr` skill (phase 9, `pr-manager`) when spawned with `context_pack: src-v2/contexts/duelbits` in its [skill-params block](../../schemas/skill-params.md).

This is a **template override**, not a skill fork — `create-pr`'s logic is identical for every repo; only the PR body shape and the project-abbreviation lookup below differ here. Per [Context Packs § Rules](../../PLAN.md#rules-3): context packs contain templates and configuration, never skill logic. See the v1 reference this was derived from: [src/skills/pr-creator/references/duelbits-workflow.md](../../../src/skills/pr-creator/references/duelbits-workflow.md).

## Project abbreviation lookup

| Branch signal | Abbreviation | Used in PR title |
|---|---|---|
| Contains `mw` or `MW-` | `[MW1]` | `[MW1] {title}` |
| Contains `wcj` or `WCJ-` | `[WCJ]` | `[WCJ] {title}` |
| No match | — | `{title}` (no prefix) |

This lookup is duelbits-specific configuration, not inferred by `project-mapper` — `.ai-rules/project.md` §Git & PR still supplies the generic `ticket_regex`/`branch` pattern; this table adds the project-abbreviation layer on top for repos that need it.

## PR body template

Read the repo's actual `.github/pull_request_template.md` (or the path in `.ai-rules/project.md` §Git & PR → `pr_template`) and fill **only its existing sections** — never add sections beyond the template, never remove its HTML comments, never restructure it. The sections below are what Duelbits templates commonly contain, for reference when the repo's real template needs to be matched:

````markdown
## Related Tickets
{ticket link(s)}

## Description
{2-3 sentence description of the approach}

## Apps Affected
{backend only: microservices list}

## Dependencies
{FE/BE/Contentful/Translation dependencies, or "None"}

## Database Migrations
{backend only: checkbox}

## Screenshots
{frontend only, if applicable}
````

## QA notes — chat-only, never in the PR body

Duelbits' QA handover notes are generated and shown **in chat only**. They are never added to the PR description, regardless of how thorough they are. This is a hard rule inherited from v1 — see [qa-notes-generator.md](../../../src/skills/pr-creator/references/qa-notes-generator.md).

## What this context pack does NOT change

- `create-pr`'s core logic (branch push check, template discovery, findings-block check) — identical across repos.
- The environment/Git-PR facts already in `.ai-rules/project.md` (base branch, merge strategy, required checks) — those come from `project-mapper`, not from this pack.

## Related

- [../../schemas/skill-params.md](../../schemas/skill-params.md) — the `context_pack` key that resolves this file
- [../../PLAN.md § Context Packs](../../PLAN.md#context-packs) — narrative source and the "fork only when behavior differs" rule
- [../../agents/pr-manager.agent.md](../../agents/pr-manager.agent.md) — the subagent that reads this pack
