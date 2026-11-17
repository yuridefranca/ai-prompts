# Parallel Flows — Git Worktrees

**Slice**: 7
**Used by**: [feature-workflow.agent.md](../agents/feature-workflow.agent.md) and the debug adapter, whenever more than one flow is active in the same repo.

Multiple flows can run simultaneously using **git worktrees** — isolated working directories on different branches within the same repo.

```
main repo:  /projects/my-app/             (branch: main)
worktree A: /projects/my-app-feat-auth/   (branch: feat/auth)   → flow A
worktree B: /projects/my-app-feat-wallet/ (branch: feat/wallet) → flow B
```

Each worktree gets its own working directory, `.ai-workflow/[feature]/` folder, branch, and editor window — true parallelism, no file conflicts.

## Commands

| Action | Command |
|---|---|
| Start | `git worktree add ../my-app-feat-auth feat/auth` |
| Remove (after merge) | `git worktree remove ../my-app-feat-auth` |
| Rebase a sibling worktree on updated main | offered to every remaining worktree after one merges |

## The real constraint

**Parallel flows don't double throughput — the bottleneck is the dev's gate attention, not the machine's.** Two full-tier flows means two PRD gates, two plan gates, two task loops, two PR gates, interleaved.

**Before starting a second flow**, the orchestrator warns if the first is below phase 6, and suggests staggering: one flow in its task loop (frequent small approvals) while the other is in analysis (long unattended stretches) keeps the dev from context-switching between two gate-heavy phases at once.

## Overlap detection (two stages, because accurate data doesn't exist at flow start)

### Stage 1 — at flow start (cheap, approximate)

Path-glob from the request's nouns, compared against other active flows' `INDEX.md`. This is [flows/bootstrap.md](bootstrap.md)'s step 5, run for every new flow before phase 1:

```
feat/wallet may touch src/wallet/**, which flow A is also editing.
Proceed or serialize?
```

### Stage 2 — at phase 3.0 (accurate)

Component maps (`3.0-component-map.md`) are compared directly across active flows once both exist. If overlap is confirmed and **wasn't** flagged at stage 1, the orchestrator raises it at the next gate rather than silently continuing — a stage-1 miss is not swept under the rug once better data exists.

## What the orchestrator does on a confirmed overlap

1. State exactly which paths overlap and which flows/branches are involved.
2. Offer: proceed anyway (dev accepts merge-conflict risk), serialize (pause one flow until the other reaches a stable point), or split scope (one flow's task list is adjusted to avoid the overlapping paths).
3. Log the decision in the affected flows' `INDEX.md` decision logs — this is a cross-flow decision, so log it in both.

## Related

- [bootstrap.md](bootstrap.md) — where stage-1 detection is invoked
- [../schemas/index-frontmatter.md](../schemas/index-frontmatter.md) — the `INDEX.md` fields overlap detection reads across flows
- [../PLAN.md § Parallel Flows — Git Worktrees](../PLAN.md#parallel-flows--git-worktrees) — narrative source
