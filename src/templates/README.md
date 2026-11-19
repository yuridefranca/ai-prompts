# Templates (Slice 2)

Fillable shapes for every artifact the flows produce. Each template implements the conventions defined in [../schemas/](../schemas/); read those first if a rule here seems unmotivated.

| Template | Fills | Used at |
|---|---|---|
| [artifact-template.md](artifact-template.md) | The generic Layer 1/Layer 2 + CHECKS skeleton every phase artifact follows | every phase |
| [gate-packet-template.md](gate-packet-template.md) | The chat-surface packet built from a gate artifact's Layer 1 | phases 2, 4, 6.0, 9 |
| [task-spec-template.md](task-spec-template.md) | One task's spec in `6-solution.md` §T{n} — exact enough for a cheap model, with its own tier | phase 6.0 (written), 6.1..n (read) |
| [task-packet-template.md](task-packet-template.md) | The per-task review packet | phase 6.1..n |
| [visual-standards.md](visual-standards.md) | Symbol vocabulary, Mermaid/table conventions, the four-backtick fence rule, the NOT-used list | every artifact |
| [index-template.md](index-template.md) | `INDEX.md` | flow bootstrap, updated every phase |
| [findings-template.md](findings-template.md) | `FINDINGS.md` | flow bootstrap, appended by every adversarial pass |
| [project-template.md](project-template.md) | `.ai-rules/project.md` | `project-mapper map` (slice 4) |
| [review-rules-template.md](review-rules-template.md) | `.ai-rules/review.md` | seeded by the dev, grown by phase 9.5 |
| [runs-template.md](runs-template.md) | `RUNS.md` — one row per spawn: agent, tier, model, outcome | appended every spawn, recorded at 9.5 |
| [qa-plan-template.md](qa-plan-template.md) | `8-qa-plan.md` | phase 8.1 |

All templates containing a fenced code example are themselves four-backtick fenced — see the fence rule in [visual-standards.md](visual-standards.md).
