---
name: refactor-optimizer
description: Clean up the code a task just made pass — readability, duplication, alignment with the project's patterns — while keeping every test green. The "Refactor" step of TDD, scoped to the current task. Use at the end of each implementation task (phases 6.1..n) once its tests pass. Keywords refactoring, code quality, readability, DRY, clean code, keep tests green.
---

# Refactoring

Improve the code this task touched, without changing behavior. Tests stay green after every single change.

## Parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Backs [`implementer`](../../agents/implementer.agent.md) as the last step of each task at phases 6.1..n — **after** the task's tests are green, **within the same task's files**. No separate artifact: record what you refactored, and what you deliberately left alone, in the task's `6-solution.md` §T{n} append.

## Checklist

Do these in order, running the task's tests after **each** change. If a test fails, revert that change — never edit the test to make a refactor pass.

1. **Names**: rename unclear variables and functions to say what they hold or do. Keep names from the spec's Interfaces unchanged.
2. **Magic values**: replace unexplained literals with named constants.
3. **Conditions**: extract complex conditions into well-named functions or variables.
4. **Duplication**: extract code repeated within this task's files. Extract to a shared utility only if it already appears 3+ times.
5. **Project patterns**: match the conventions in §T{n}'s Context — error handling, file layout, existing helpers. Reuse a helper instead of re-writing it.
6. **Obvious inefficiency only**: an N+1 query, or a nested loop over the same data that a Set/Map fixes. Anything else needs a measurement first, so leave it.

## Don't

- Change behavior, public interfaces, or anything a test asserts.
- Refactor outside this task's files — report it as an open question instead ("while I'm here" is how regressions ship).
- Add caching, indexes, or new abstractions — those are plan decisions, not refactors.
- Refactor code you don't understand, or code without tests.

## Done when

- [ ] All tests pass after the last change
- [ ] §T{n} records what changed and what was left alone

Patterns and before/after examples: [references/guide.md](references/guide.md).
