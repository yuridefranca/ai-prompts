---
name: project-mapper
description: Inspect a repository and write or verify .ai-rules/project.md, the machine-readable file that lets every flow phase stop guessing dev commands, test frameworks, browser config, and PR conventions. Two modes — map (first run, or after a tooling change) and check (every flow start, drift detection). Always use before any flow phase reads project facts. Keywords project conventions, repo mapping, project.md, bootstrap, drift check, environment contract.
---

# Project Mapper

Writes and verifies `.ai-rules/project.md` — the descriptive (not normative) repo-facts file defined in [schemas/project-md-schema.md](../../schemas/project-md-schema.md). This is the mechanism that retires per-run guessing in `test-generator` (framework), `design-implementation-validator` (dev server/URL), and `create-pr` (org/branch conventions).

## When to Use

- **`map` mode**: `.ai-rules/project.md` doesn't exist yet, or the repo's tooling changed enough that a full re-inspection is warranted
- **`check` mode**: at every flow bootstrap when `.ai-rules/project.md` already exists (see [flows/bootstrap.md](../../flows/bootstrap.md))

**Do NOT use for**: `.ai-rules/review.md` (normative rules — that's dev-authored and grown by the phase 9.5 harvest, not inspected from the repo).

## Core Principle

**Every fact carries the command that proves it.** No field is filled from a plausible-looking guess, and no field carries a `last_reviewed` date — dates measure editing, not accuracy. See [Keeping It Accurate](../../PLAN.md#keeping-it-accurate).

## Process — `map` mode

### Step 1: Inspect, don't ask, wherever inspection is conclusive

| Section | Inspect |
|---|---|
| `Run` | lockfile presence (`pnpm-lock.yaml`/`package-lock.json`/`yarn.lock`) for package manager; `package.json` `scripts.dev`/`scripts.build`/`scripts.typecheck`; dev server startup log for a ready-pattern regex |
| `Test` | `package.json` test scripts; existing test file extensions/locations (`*.spec.ts`, `__tests__/`, `e2e/`); CI config for which levels actually run; existing mock usage to infer the mocking policy |
| `Browser` | Playwright/Cypress config for `baseURL`; existing `*.auth.setup.ts` or storageState files; existing test selectors (grep for `data-testid` vs `getByText` vs CSS classes) to infer the convention already in use, not the one you'd prefer |
| `Git & PR` | branch names in `git log`/`git branch -a` for the pattern and ticket regex; `.github/pull_request_template.md` or equivalent; CI config for required checks; recent commit messages for the commit convention |
| `Docs` | existing `docs/` structure, `AGENTS.md`, ADR folders |
| `Structure` | `tsconfig.json`/`vite.config`/`webpack.config` for path aliases; existing component/service folder naming pattern |

### Step 2: Ask only where inspection is genuinely ambiguous

Two conflicting signals (e.g. both `pnpm-lock.yaml` and `package-lock.json` present), or a fact inspection cannot determine at all (e.g. no existing e2e tests to infer a selector convention from). Record the dev's answer in the written file — the next `map` run does not re-ask a question this run already resolved.

### Step 3: Attach a `verify:` command to every field the schema marks verifiable

A `verify:` command is cheap and mechanical — `ls`, `jq -e`, a grep — never itself a heuristic. See the field reference in [project-md-schema.md](../../schemas/project-md-schema.md#section-reference).

### Step 4: Write the file

Follow [templates/project-template.md](../../templates/project-template.md) exactly — section order, field names, the `not applicable — {reason}` convention for sections that don't apply to this repo.

## Process — `check` mode

1. Read the existing `.ai-rules/project.md`.
2. Execute every `verify:` command against the live repo.
3. For each field whose verify command fails or whose value looks stale (e.g. `dev: pnpm dev` but `package.json` no longer has a `dev` script): produce a concrete diff — old value → new value, with the command output that proves the change.
4. Present the diff to the dev for approval. Do not silently rewrite the file.
5. Report drift in the flow's phase-1 Layer 1 (per [flows/bootstrap.md](../../flows/bootstrap.md)) — never a silent pass-through.

## Output Format

`.ai-rules/project.md`, per [templates/project-template.md](../../templates/project-template.md). Not a `.ai-workflow/` artifact and not tagged `[knowledge]`/`[process]` — it's a standing repo file with its own lifecycle (updated on tooling change, not per-feature).

`check` mode's output is a diff, shown to the dev, applied only on approval.

## Uncertainty Handling

A field that inspection genuinely cannot resolve and the dev doesn't answer is written as `unknown — {what was tried}`, never a plausible-looking default. Every phase that reads an `unknown` field must say so explicitly in its own output rather than silently treating the guess as fact.

## Evals

- [ ] Every field with a schema `verify:` requirement has a real, cheap, mechanical command attached
- [ ] No field was filled with a guess presented as fact — ambiguous fields are either dev-confirmed or marked `unknown`
- [ ] `check` mode never rewrites the file without dev approval
- [ ] No `last_reviewed` or similar staleness-date field was added
- [ ] Sections that don't apply are marked `not applicable — {reason}`, not deleted

## Related

- [schemas/project-md-schema.md](../../schemas/project-md-schema.md) — full field schema this skill implements
- [templates/project-template.md](../../templates/project-template.md) — the exact file shape to produce
- [agents/repo-mapper.agent.md](../../agents/repo-mapper.agent.md) — the thin subagent wrapper that invokes this skill
- [flows/bootstrap.md](../../flows/bootstrap.md) — when this skill runs relative to the rest of a flow
