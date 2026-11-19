# Schema: `.ai-rules/project.md`

**Slice**: 0 (Foundations)
**Used by**: severity gate (phase 0), phase 5, phase 6.1..n, phase 6.y, phase 8.3, phase 9 — see the full consumer table below
**Nature**: descriptive — "how does this repo work?" (contrast with `.ai-rules/review.md`, normative — "is this code acceptable?" — schema for that lands with [Repository-Specific Review Rules](../PLAN.md#repository-specific-review-rules) in slice 2)

## Purpose

Flows must run against any repo without subagents guessing. Today they guess constantly: `test-generator` asks the user which framework every single run, `design-implementation-validator` hardcodes `http://localhost:3000` and throws when it can't infer a dev command, `create-pr` carries org-detection heuristics. Every one of those is a repo fact that should be stated once, verified mechanically, and read — not re-derived per run.

## File structure

Every fact carries the command that proves it. There is deliberately **no `last_reviewed` date** — a date measures editing, not accuracy (same reasoning as the review-rules staleness mechanism — see [Keeping It Accurate](../PLAN.md#keeping-it-accurate)).

````markdown
# Project Conventions — [Project Name]

## Run
package_manager: pnpm              verify: ls pnpm-lock.yaml
install: pnpm install --frozen-lockfile
dev: pnpm dev                      verify: jq -e '.scripts.dev' package.json
dev_url: http://localhost:5173
ready_pattern: /ready in \d+ms/
build: pnpm build
typecheck: pnpm typecheck

## Test
unit:        cmd: pnpm test:unit   location: src/**/*.spec.ts
integration: cmd: pnpm test:int    location: test/integration/**/*.spec.ts
e2e:         cmd: pnpm test:e2e    location: e2e/**/*.spec.ts
single_file: pnpm test:unit -- <path>
mocking: unit mocks all I/O; integration mocks nothing below the HTTP boundary
fixtures: test/factories/          seed: pnpm db:seed:test    reset: pnpm db:reset:test

## Browser
base_url: http://localhost:5173
auth: storageState e2e/.auth/user.json, produced by e2e/auth.setup.ts
selectors: data-testid required — never text content or CSS classes
isolation: one transaction per spec, rolled back in afterEach
viewports: mobile 375, tablet 768, desktop 1280

## Git & PR
branch: <TICKET>-<kebab-summary>   ticket_regex: ^[A-Z]{2,4}-\d+
base: develop                      merge: squash
commit: conventional commits
pr_template: .github/pull_request_template.md
required_checks: [lint, test:unit, test:int]

## Docs
features: docs/features/           adr: docs/adr/
glossary: docs/glossary.md         api: docs/api/

## Structure
aliases: @/ → src/, @components/ → src/components/
new_component: src/components/<Domain>/<Name>/
new_service: src/services/<domain>/
new_route: src/routes/

## Agents
company: duelbits      tool: copilot
````

### Section reference

| Section | Fields | Consumers |
|---|---|---|
| `Run` | package manager + verify command, install, dev command + verify + url + ready pattern, build, typecheck | severity gate, phase 8.3 |
| `Test` | per-level `cmd`/`location`, `single_file`, `mocking` policy, `fixtures`/`seed`/`reset` | phase 5, phase 6.x contract diff, phase 8.3 |
| `Browser` | `base_url`, `auth`, `selectors`, `isolation`, `viewports` | phase 8.3 (both scripted and `design-implementation-validator`) |
| `Git & PR` | branch pattern + ticket regex, base branch, merge strategy, commit convention, PR template path, required checks | phase 9 |
| `Docs` | `features`, `adr`, `glossary`, `api` paths | phase 6.y, phase 9 promotion (see [artifact-lifecycle.md](artifact-lifecycle.md)) |
| `Structure` | path aliases, `new_component`/`new_service`/`new_route` conventions | severity gate, phase 6.1..n |
| `Agents` (optional) | `company` — the context pack under `src/contexts/` (model list, PR conventions); `tool` — `copilot` \| `claude` \| `cursor`. Dev-supplied, not inspected | `create-pr` (`context_pack`), 9.5 run log, the install step |

Every `verify:` command is a **cheap, mechanical check** (`ls`, `jq`, a grep) — never a heuristic guess. A field with no verify command is either unverifiable in principle (e.g. `dev_url`) or the field itself *is* a command.

## Two modes

| Mode | What it does | When |
|---|---|---|
| `map` | Inspects the repo — lockfiles, `package.json` scripts, existing test files, CI config, PR template, branch history — and writes `.ai-rules/project.md`. Asks the user **only** where inspection is genuinely ambiguous, and records the answer rather than re-asking next run | First run in a repo; after a tooling change |
| `check` | Executes every `verify:` command and reports drift as a concrete diff | Flow start; optionally wired into CI |

## Bootstrapping (flow-start behavior)

At flow start the orchestrator checks for `.ai-rules/project.md`:

- **Missing** → offers to run `project-mapper map` (a few minutes) before phase 1; the decision (ran it / declined) is recorded in `INDEX.md`'s decision log.
- **Present** → runs `check`; any drift is surfaced in the phase-1 Layer 1, never silently tolerated.
- **Declined** → the flow still runs, but every phase that would have read a fact instead states which fact it had to guess, and every guess made during the run is listed at the phase 9 gate for the dev to see before merge.

## What each phase stops guessing

| Phase | Without project.md | With it |
|---|---|---|
| 0 severity gate | Blind glob from the request's nouns | Globs scoped by the real module layout (`Structure`) |
| 5 TDD | Asks the user the test framework **every run** | Framework, per-level command, file location, mocking policy (`Test`) |
| 6.1..n | Implementer invents file paths | `Structure.new_*` and path aliases |
| 6.y docs | Guesses where docs live | `Docs.features`, `Docs.adr`, `Docs.glossary` |
| 8.3 browser QA | Hardcoded `localhost:3000`, throws if undetectable | `Run.dev_url`/`ready_pattern`, `Browser.*` |
| 9 PR | Org-detection heuristics | `Git & PR.*` |

## Drift is mechanical, not calendar-based

`check` runs the cheap verifications — does `package.json` still declare `test:e2e`? does the PR template path exist? does `e2e/.auth/user.json` get produced by the named setup spec? A failed verify produces a diff the dev approves, the same mechanism as [trigger-count pruning](../PLAN.md#keeping-it-accurate) for review rules. Nothing warns on a schedule; nothing goes stale silently.

## Related

- `.ai-rules/review.md` — the normative sibling of this file; separate lifecycle, separate failure mode (a stale review rule is an arguable false positive, a stale dev-server command is a hard crash mid-flow)
- [Repository Conventions](../PLAN.md#repository-conventions) — narrative source
- Slice 4 builds the `project-mapper` skill (`map` + `check`) and `repo-mapper` agent that implement this schema
- Slice 2 builds the fillable `project-template.md` derived from this schema
