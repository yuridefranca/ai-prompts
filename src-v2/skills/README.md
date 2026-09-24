# Skill Overlays (Slice 3, 4)

Every file here is either **(a) an overlay** on a v1 skill in `../../src/skills/` — a thin file stating only the src-v2-specific delta (skill-params support, output-path override, behavior change) and pointing at the untouched v1 base for the full process — or **(b) new to v2** with no v1 equivalent.

**`../../src/skills/` is never edited to support v2.** See [PLAN.md § Architecture § Three-Layer Separation](../PLAN.md#three-layer-separation) and [v1 / v2 Coexistence](../PLAN.md#v1--v2-coexistence). A v1 skill v2 uses with no behavioral difference (e.g. `system-designer`) has **no overlay here at all** — the subagent reads `../../src/skills/system-designer/SKILL.md` directly.

## Overlays

| Overlay | v1 base skill | Invoked as | Used by (phase) |
|---|---|---|---|
| [grill-me](grill-me/SKILL.md) | `grill-me` | `grill-me` | 2, 4 (inline, no standalone artifact) |
| [solution-critic](solution-critic/SKILL.md) | `solution-critic` | `solution-critic` | 6.0, 7 |
| [code-review](code-review/SKILL.md) | `code-reviewer` (name unchanged in v1) | `code-review` | 7 |
| [root-cause-analyzer](root-cause-analyzer/SKILL.md) | `root-cause-analyzer` | `root-cause-analyzer` | 2.5 (debug) |
| [spec-extractor](spec-extractor/SKILL.md) | `spec-extractor` | `spec-extractor` | 1, 2 |
| [component-mapper](component-mapper/SKILL.md) | `component-mapper` | `component-mapper` | 3.0, 3.2 |
| [tradeoff-analyzer](tradeoff-analyzer/SKILL.md) | `tradeoff-analyzer` | `tradeoff-analyzer` | 3.4, 6.0 |
| [test-generator](test-generator/SKILL.md) | `test-generator` | `test-generator` | 5 |
| [integration-test-generator](integration-test-generator/SKILL.md) | `integration-test-generator` | — (status note only, folded into `test-generator`) | not invoked |
| [design-implementation-validator](design-implementation-validator/SKILL.md) | `design-implementation-validator` | `design-implementation-validator` | 8.3 (UI branch) |
| [create-pr](create-pr/SKILL.md) | `pr-creator` (name unchanged in v1) | `create-pr` | 9, 9.1 |
| [documentation-writer](documentation-writer/SKILL.md) | `documentation-writer` | `documentation-writer` | 6.y |

## New to v2 (no v1 base)

| Skill | Used by (phase) |
|---|---|
| [project-mapper](project-mapper/SKILL.md) | bootstrap (before phase 1) |
| [explain-task](explain-task/SKILL.md) | 0.5 (create), then 2/6.0/6.x/7/9 (update) |

`explain-task` has no proper v1 base to overlay, but isn't purely from scratch either — it's adapted from a WIP skill the dev had already built for a different, non-portable workflow: `src-duelbits/skills/explain-task`. See [explain-task/SKILL.md](explain-task/SKILL.md) for exactly what was kept (the design: stages, watch-out cards, quiz, mobile-first HTML) versus retargeted (repo-specific paths and tooling → `.ai-rules/project.md` and the v2 phase model). The `src-duelbits` original is untouched, same "don't edit the source" discipline as every overlay above.

## Why two skills kept their v1 name

`code-reviewer` and `pr-creator` are invoked in src-v2 as `code-review` and `create-pr` (per the naming convention: a skill invokable as one action gets a verb-noun/action name), but their **v1 base files are untouched and keep the original name** — renaming the v1 directory would have been an edit to `src/skills/`, which is exactly what this correction rules out. The overlay is where the new name lives.

## Related

- [../PLAN.md § Cross-Cutting Skill Refactor](../PLAN.md#cross-cutting-skill-refactor) — the full per-skill table
- [../schemas/skill-params.md](../schemas/skill-params.md) — the block every overlay accepts
- [../agents/README.md](../agents/README.md) — the subagent roster that invokes these overlays
