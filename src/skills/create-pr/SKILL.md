---
name: create-pr
aliases:
    - pr-creator
    - github-pr-creator
description: Create the GitHub Pull Request at the end of a flow (phase 9) and address its review comments (phase 9.1). Reads branch, base, template, and required checks from .ai-rules/project.md instead of guessing; org-specific behavior (e.g. Duelbits ticket titles and QA notes) comes from a context pack. Promotes knowledge-tier artifacts into the repo docs as part of the PR diff, and refuses to open a PR while a 🔴 finding is open. Keywords pull request, GitHub PR, base branch, PR template, context pack, knowledge promotion, phase 9, QA notes.
---

# Create PR

Create a well-structured GitHub Pull Request using the repo's own conventions. **The skill's logic is the same for every repo**: repo facts come from `.ai-rules/project.md`, and org-specific behavior comes from a context pack — never from detecting the organization.

## When to Use

- Phase 9 of every flow, after review (7) and QA (8)
- Phase 9.1, addressing PR review comments

**Do NOT use**:

- While any 🔴 finding is `open` in `FINDINGS.md`
- When tests are failing
- For work-in-progress (unless creating a draft PR)

## Parameters

Read `{{phase}}`, `{{output}}`, and `{{context_pack}}` from a [skill-params block](../../schemas/skill-params.md) (default output: `9-pr-notes.md`).

## Where this runs

Backs [`pr-manager`](../../agents/pr-manager.agent.md) at phases 9 and 9.1.

## Process

### Step 1: Check the Findings Block

Read `FINDINGS.md`. If any 🔴 finding is `open`, **stop** and list them — the PR waits. See [findings.md](../../schemas/findings.md).

### Step 2: Read Repo Facts

From `.ai-rules/project.md` §Git & PR: branch pattern, ticket regex, base branch, PR template path, required checks, merge strategy, commit convention. No heuristics, no git-remote sniffing. A field marked `unknown` is asked about, not guessed. See [project-md-schema.md](../../schemas/project-md-schema.md).

### Step 3: Resolve the Context Pack

- **`{{context_pack}}` given** (e.g. `src/contexts/duelbits`): read its `pr-template.md` and follow what it points to. The pack supplies templates and configuration — title prefixes, body shape, chat-only QA notes — and never changes Steps 1, 2, 4, 5, or 6.
- **No context pack**: follow [references/generic-workflow.md](references/generic-workflow.md), using the values from Step 2 wherever it would otherwise detect or ask.

### Step 4: Promote Knowledge Artifacts

Copy every `[knowledge]`-tagged artifact from `.ai-workflow/[feature]/` into `.ai-rules/project.md` §Docs `features:` (default `docs/features/[feature]/`), with the artifact-status header stripped. Make sure the phase-8.3 Playwright specs are in `Test.e2e.location`. Both go in the PR diff. Process-tier artifacts never do. See [artifact-lifecycle.md](../../schemas/artifact-lifecycle.md).

### Step 5: Confirm, Then Create

Phase 9 is a ⛔ gate: show the dev the title, base ← head branch, and body, and wait for a yes. Then verify the branch is pushed, check for an existing PR, and create it (`gh pr create` or a GitHub MCP tool).

### Step 6: Write `9-pr-notes.md`

The PR body plus a **"verify in 2 min"** block: the shortest path for a reviewer to see the change working. It must describe steps **actually executed** during phase 8.2, not a hypothetical quick-check. Tier: `[knowledge]`.

## Phase 9.1 — Review Comments

For each PR comment: answer it, or push back with a reason, and record the resolution in `9-pr-notes.md`. A comment that needs a code change is **not** patched here — it re-enters the flow as a new task at 6.1. A comment that reveals a real defect also becomes a `FINDINGS.md` entry, so the phase 9.5 gotcha harvest counts it.

## Critical Rules

- ✅ Never open a PR over an open 🔴 finding
- ✅ Get the dev's confirmation before creating the PR
- ✅ Verify the branch is pushed; check for an existing PR first
- ✅ Use the repo's PR template: fill only its sections, keep its HTML comments, never restructure it
- ✅ Keep the description short: what changed and why, not implementation details

## Output Example

```markdown
✅ Pull Request created successfully!

🔗 PR URL: https://github.com/some-org/project/pull/45

**Summary**:

- Title: Add dark mode support
- Base: main ← feature/add-dark-mode
- Files changed: 15 (incl. docs/features/dark-mode/)
- Commits: 8

**Verify in 2 min**: toggle Settings → Appearance → Dark, reload, confirm it sticks.
```

## Evals

- [ ] Open 🔴 findings checked before anything else
- [ ] Base branch, template, and checks read from `.ai-rules/project.md`, not detected
- [ ] Context pack, if given, used for templates only
- [ ] Knowledge-tier artifacts and Playwright specs present in the PR diff; process-tier absent
- [ ] Dev confirmation obtained at the gate
- [ ] Existing PR checked; branch pushed
- [ ] PR template structure preserved exactly
- [ ] `9-pr-notes.md` written with a "verify in 2 min" block
- [ ] PR URL returned

## Related

- [references/generic-workflow.md](references/generic-workflow.md) — the default process when no context pack is given
- [../../contexts/duelbits/pr-template.md](../../contexts/duelbits/pr-template.md) — the Duelbits context pack
- [../../agents/pr-manager.agent.md](../../agents/pr-manager.agent.md)
