# Template: Task Spec (`6-solution.md` §T{n})

**Used by**: `solution-planner` (phase 6.0) writes one per task; `implementer` (6.1..n) reads **only** its own §T{n}, plus the contract clauses it names.

## Why this shape

Most tasks run at tier B — a cheap model (see [agent-tiers.md](../schemas/agent-tiers.md)). Cheap models rarely fail at typing code; they fail at **ambiguity**: a missing file path, an unstated convention, a decision left implicit. Every decision in a task is made here, at S, so the implementer only executes. A task the planner can't fully specify is not a B task.

## Shape

````markdown
### T{n}: {imperative one-line name}

**Why**: {AC*/C* IDs} — {one sentence linking to the ADR decision it implements}
**Tier**: {B | A} — {one-line reason; required when A}
**Size**: {S | M | L} · ~{N} lines · **Depends on**: {T* ids or "none"}

**Files**
- create `{exact/path.ts}` — {what it holds}
- modify `{exact/path.ts}` — {which function/section}

**Interfaces** (exact — the implementer copies these, never invents them)
```ts
export function createWallet(userId: UserId, currency: Currency): Promise<Wallet>
```

**Context** (everything needed that isn't in the files above — inlined, not linked)
- {convention: e.g. "errors are thrown as DomainError subclasses, see src/errors.ts:12"}
- {existing code to reuse: path + symbol}
- {the ADR decision this follows, in one line}

**Steps**
1. {ordered, concrete}
2. …

**Tests to turn green**: {C* ids} in `{test file path}` · run `{exact command from project.md §Test}`

**Done when**
- [ ] `{command}` passes
- [ ] {observable check, e.g. "no new exports besides createWallet"}

**Do not touch**: {paths/areas — e.g. "src/ledger/**, the public API types"}
````

## Rules

1. **Tier B only if every section is filled with no decision left open.** If you can't write the **Interfaces** or the **Done when** commands, the task needs a decision the implementer would have to make — mark it **A** and say which decision, or split the decision into its own A task.
2. **Mark A** for: a new abstraction or module boundary, an algorithm or data-structure choice, a data migration, concurrency or transactions, security-sensitive code, or a task touching more than ~3 files with interacting changes. Everything else defaults to B.
3. **Context is inlined, not linked.** The implementer reads nothing outside §T{n} and its named clauses — a link to `3.1-architecture.md` is context it will never see.
4. **Exact paths and commands only.** "The wallet service" is not a path; "run the tests" is not a command. Copy commands from `.ai-rules/project.md` §Test.
5. **≤150 changed lines per task** (L must split or justify, as before). Smaller tasks are what make B safe.
6. **The implementer stops on a gap.** If the spec is missing something, the implementer returns an open question instead of guessing — a gap is a planning defect to fix in §T{n}, not an invitation to improvise.

## Related

- [../agents/solution-planner.agent.md](../agents/solution-planner.agent.md) — writes these
- [../agents/implementer.agent.md](../agents/implementer.agent.md) — executes them
- [../schemas/agent-tiers.md](../schemas/agent-tiers.md) — what B and A mean, and escalation
