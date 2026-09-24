# Schema: Artifact Status Header

**Slice**: 0 (Foundations)
**Used by**: every subagent that writes a phase artifact; the resume procedure in [index-frontmatter.md](index-frontmatter.md)

## Purpose

A half-written file is otherwise indistinguishable from a finished one until someone reads it end to end. Every artifact opens with a small frontmatter block that makes "did this phase actually finish" a one-line check.

## Schema

````yaml
---
artifact: 3.1-architecture     # filename stem, no extension
phase: "3.1"                   # matches INDEX.md current_phase when this was produced
tier: knowledge                # knowledge | process — see artifact-lifecycle.md
status: draft                  # draft | complete
produced_by: architect         # subagent name that wrote this file
updated: 2026-01-14
---
````

| Field | Type | Notes |
|---|---|---|
| `artifact` | string | the file's own stem, redundant with the filename on purpose — makes a copy-pasted or renamed file self-identifying |
| `phase` | string | quoted, same reasoning as `INDEX.md`'s `current_phase` |
| `tier` | enum | `knowledge` or `process`, per [artifact-lifecycle.md](artifact-lifecycle.md)'s tier-assignment table |
| `status` | enum | `draft` while the subagent is writing; flipped to `complete` as its literal last write action |
| `produced_by` | string | the subagent name (matches the roster in [Build Slices §Subagent Roster](../PLAN.md#subagent-roster-slice-3)) |
| `updated` | date | `YYYY-MM-DD`, the date of the write that set the current `status` |

## The draft rule

A subagent writes `status: draft` on its **first** write to the file (or immediately, before writing any body content), then rewrites the header with `status: complete` as its **final** action once the whole artifact is in place.

**A `draft` artifact means the phase died mid-write.** It must be **re-run from scratch**, never resumed or patched — a partially-written file cannot be trusted to represent a coherent state, and patching risks stitching together two different reasoning passes into one inconsistent document. See step 2 of the [resume procedure](index-frontmatter.md#resume-procedure).

## Rules

1. Every phase artifact — knowledge or process tier — carries this header. There is no exemption for "small" outputs; `4-quiz.md` and `9-pr-notes.md` both carry it.
2. `FINDINGS.md` and `INDEX.md` are the two exceptions with their own frontmatter shapes (append-only ledger; flow-state record respectively) — see [findings.md](findings.md) and [index-frontmatter.md](index-frontmatter.md).
3. Idempotent overwrite (from [index-frontmatter.md](index-frontmatter.md#idempotency-rule)) applies here: re-running a phase replaces the entire file, header included — the `updated` date always reflects the most recent run, not the first.
4. Phase 9 promotion (see [artifact-lifecycle.md](artifact-lifecycle.md)) **strips this header** from knowledge-tier copies landing in `docs.features` — it is run-scoped metadata, not documentation.

## Non-markdown artifacts

Every artifact so far is markdown, so YAML frontmatter is the natural header. `0.5-walkthrough.html` (see [artifact-lifecycle.md](artifact-lifecycle.md)) is the first exception: it's HTML, so the same six fields go in an **HTML comment** at the top of the file instead of YAML frontmatter:

```html
<!--
artifact: 0.5-walkthrough
phase: "0.5"
tier: knowledge
status: draft
produced_by: task-explainer
updated: 2026-01-14
-->
```

Same fields, same semantics, same draft/complete discipline — only the delimiter syntax changes to match the file's own format. Any future non-markdown artifact follows the same rule: use that format's native comment syntax, keep the six field names identical.

## Related

- [artifact-lifecycle.md](artifact-lifecycle.md) — what `tier` means and where the file ends up
- [index-frontmatter.md](index-frontmatter.md) — flow-level state that reads this header during resume
- [State & Resumption](../PLAN.md#state--resumption) — narrative source
