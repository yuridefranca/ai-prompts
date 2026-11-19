# Schema: Artifact Lifecycle & Tiers

**Slice**: 0 (Foundations)
**Used by**: every phase that writes an artifact; phase 9 (`pr-manager`) promotion; phase 9.5 cleanup

## The question this answers

*Do we need all the files the AI generates?* Every artifact is tagged `[knowledge]` or `[process]` at the moment it's written, and the tag decides where the file ends up.

## Tier definitions

| Tier | Definition | Lives in | On merge | Tracked in git |
|---|---|---|---|---|
| **`[knowledge]`** | Answers a question someone will ask again after this feature ships (why is it built this way, what does it promise, how does data flow) | `.ai-workflow/[feature]/` during the run | Moved to `docs.features` (path from `.ai-rules/project.md`) by phase 9 | ✅ committed with the PR |
| **`[process]`** | Records how *this run* went (quiz answers, review findings, QA results). Useful during the run, noise afterwards | `.ai-workflow/[feature]/` | Deleted | ❌ `.ai-workflow/` is gitignored |

## Tier assignment (canonical, per artifact)

| Artifact | Tier | Rationale |
|---|---|---|
| `0.5-walkthrough.html` | knowledge | The onboarding artifact — a future reader's fastest way to understand why this shipped, deepened across the whole run. Non-markdown; see [artifact-status.md § Non-markdown artifacts](artifact-status.md#non-markdown-artifacts) |
| `1-overview.md` | knowledge | Business context outlives the run |
| `2-prd.md` | knowledge | Acceptance criteria are referenced in future bug reports |
| `2.1-roadmap.md` (greenfield) | knowledge | The plan for every later milestone — each starts as a feature flow from it |
| `2.5-root-cause.md` (debug) | knowledge | Root cause explains "why did this break" long after the fix |
| `3.0-component-map.md` | knowledge | Reused by the next flow touching this area |
| `3.1-architecture.md` | knowledge | Diagrams answer "why is it shaped like this" |
| `3.2-data-flow.md` | knowledge | Same |
| `3.4-tradeoffs.md` | knowledge | The ADR — the highest-value survivor |
| `4-quiz.md` | process | Comprehension record, no future value |
| `5-contract.md` | knowledge | Source of truth for behavior; referenced by future changes |
| `6-solution.md` | knowledge | Plan + as-built record explains surprising code |
| `6.y-docs.md` | knowledge | Written straight into the repo's real docs, not the workflow folder |
| `7.0-rules.md` | process | Rules compliance for this diff; its catches feed `review.md`'s `triggered:` counts |
| `7-review.md` | process | Findings are either fixed or promoted to the ledger |
| `8-qa-plan.md` | knowledge | Scenarios become the regression suite's starting point |
| `8-qa-results.md` / `8-qa-automated-results.md` | process | Point-in-time run record |
| `9-pr-notes.md` | knowledge | The PR body itself; survives in GitHub |
| `RUNS.md` | process | Which model ran each spawn and how it went; anonymized into the company run log at 9.5, then deleted |
| `FINDINGS.md` | process | Open findings block the PR; resolved ones die with the run |
| `INDEX.md` | process | Flow state — see [index-frontmatter.md](index-frontmatter.md) |

A new artifact type not in this table defaults to `process` until a slice author adds a row here with a rationale — knowledge tier is opt-in, not assumed.

## Rules

1. **Phase 9 performs the promotion.** `pr-manager` copies every `[knowledge]` artifact to the path named by `.ai-rules/project.md` §Docs → `features:` (default `docs/features/[feature]/`), strips Layer 1 status blocks (they're run-scoped, not documentation), and includes the copies in the PR diff.
2. **`.ai-workflow/` is gitignored.** If the target repo's `.gitignore` doesn't exclude it, the flow adds the entry at flow start (see the bootstrap step in [Repository Conventions](../PLAN.md#repository-conventions)).
3. **Nothing is deleted before merge.** Process artifacts are removed by the dev after merge (phase 9.5 may prompt for it), or left to rot harmlessly in the untracked folder.
4. **A dev wanting a process artifact to survive promotes the *finding*, not the file.** The correct move is adding a one-line Gotcha to the relevant skill (phase 9.5 harvest) — see [findings.md](findings.md) — never committing `.ai-workflow/` content directly.
5. Every artifact's own frontmatter carries its `tier:` value (see [artifact-status.md](artifact-status.md)) — this table is the source of truth an author copies from, the frontmatter is the machine-readable copy on the file itself.

## Related

- [artifact-status.md](artifact-status.md) — per-file frontmatter schema, including `tier`
- [index-frontmatter.md](index-frontmatter.md) — flow-level state that references these artifacts
- [Artifact Lifecycle](../PLAN.md#artifact-lifecycle) — narrative source this schema was extracted from
