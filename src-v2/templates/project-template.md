# Template: .ai-rules/project.md

**Slice**: 2 · **Schema**: [../schemas/project-md-schema.md](../schemas/project-md-schema.md)
**Written by**: `project-mapper` skill in `map` mode (slice 4). This file is the fillable copy of that schema — copy it into a target repo's `.ai-rules/project.md` and fill every field, or run `project-mapper map` to fill it automatically.

````markdown
# Project Conventions — {Project Name}

## Run
package_manager: {pnpm|npm|yarn|...}      verify: {cheap command that proves it}
install: {command}
dev: {command}                            verify: {cheap command that proves it}
dev_url: {http://localhost:PORT}
ready_pattern: {regex matched against dev server stdout}
build: {command}
typecheck: {command}

## Test
unit:        cmd: {command}   location: {glob}
integration: cmd: {command}   location: {glob}
e2e:         cmd: {command}   location: {glob}
single_file: {command with a <path> placeholder}
mocking: {policy sentence — what each level mocks and what it doesn't}
fixtures: {path}          seed: {command}    reset: {command}

## Browser
base_url: {url}
auth: {storageState path + how it's produced, or "none"}
selectors: {convention — e.g. "data-testid required — never text content or CSS classes"}
isolation: {how test data isolation works, e.g. "one transaction per spec, rolled back in afterEach"}
viewports: {breakpoints the repo cares about}

## Git & PR
branch: {pattern}   ticket_regex: {regex, or "none"}
base: {branch}                      merge: {squash|merge|rebase}
commit: {convention, e.g. "conventional commits"}
pr_template: {path, or "none"}
required_checks: [{list}]

## Docs
features: {path}           adr: {path, or "none"}
glossary: {path, or "none"}     api: {path, or "none"}

## Structure
aliases: {alias → path, comma-separated, or "none"}
new_component: {path pattern}
new_service: {path pattern}
new_route: {path pattern}
````

## Filling this in

- **Every field needs its `verify:` command where one is listed in the schema.** A field without a mechanical way to check it is either inherently unverifiable (`dev_url`) or a bare fact with no drift risk — don't invent a verify command just to fill the column.
- **No `last_reviewed` date field, ever.** See [Keeping It Accurate](../PLAN.md#keeping-it-accurate) — accuracy is proven by re-running `verify:` commands (`project-mapper check`), not by an edit timestamp.
- If a section genuinely doesn't apply to this repo (e.g. no `Browser` section for a CLI-only tool), write `not applicable — {one-line reason}` rather than deleting the section — a missing section reads as "not yet mapped," an explicit "not applicable" reads as "checked, doesn't exist here."

## Related

- [../schemas/project-md-schema.md](../schemas/project-md-schema.md) — full field reference, the two modes (`map`/`check`), and what each phase stops guessing once this file exists
- Slice 4 builds the `project-mapper` skill that generates and verifies this file automatically
