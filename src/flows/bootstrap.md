# Shared Flow-Start Bootstrap

**Slice**: 1
**Runs once per flow**, before phase 1 of every flow ([feature](feature-flow.md), [debug](debug-flow.md), [improvement](improvement-flow.md); [greenfield](greenfield-flow.md) uses a variant — see its Bootstrap section), and at the top of every resumed session (alongside the [resume procedure](../schemas/index-frontmatter.md#resume-procedure)).

## Steps

1. **Resume check** — if `.ai-workflow/[feature]/INDEX.md` already exists, this is a resume, not a fresh start: run the [resume procedure](../schemas/index-frontmatter.md#resume-procedure) instead of the steps below.
2. **`.ai-rules/project.md` check**:
   - **Missing** → offer to run `project-mapper map` (a few minutes) before phase 1. Record the decision (ran it / declined) in `INDEX.md`'s decision log.
   - **Present** → run `project-mapper check`; surface any drift in the phase-1 Layer 1, never silently tolerated.
   - **Declined** → the flow still runs. Every phase that would have read a fact instead states which fact it had to guess; every guess made during the run is listed at the phase 9 gate.
3. **`.gitignore` check** — if the target repo's `.gitignore` doesn't exclude `.ai-workflow/`, add the entry now, before any artifact is written.
4. **Folder + branch** — create `.ai-workflow/[feature]/`, write the initial `INDEX.md` (from [templates/index-template.md](../templates/index-template.md)), create/confirm the feature branch per `.ai-rules/project.md` §Git & PR (or ask, if project.md was declined).
5. **Overlap check (stage 1)** — path-glob from the request's nouns, compared against other active flows' `INDEX.md` (see [Parallel Flows](../PLAN.md#parallel-flows--git-worktrees)). Flag and ask before proceeding if another active flow's `INDEX.md` claims overlapping paths.

See [project-md-schema.md](../schemas/project-md-schema.md) for the full schema this step reads, and [Repository Conventions](../PLAN.md#repository-conventions) for the narrative rationale.

## What this step is not

This is not the severity gate. Bootstrap establishes *how the repo works*; the severity gate (phase 0 in both flow manifests) decides *how much process this specific change needs*. Bootstrap always runs; the severity gate's tier decides which later phases run.
