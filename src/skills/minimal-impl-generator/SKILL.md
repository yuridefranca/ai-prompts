---
name: minimal-impl-generator
description: Implement the simplest code that makes a task's failing tests pass — the "Green" step of TDD — exactly as the task spec says, nothing more. Use in each implementation task (phases 6.1..n) after the tests exist. Keywords minimal implementation, simple solution, YAGNI, green phase, TDD implementation, make tests pass, task spec.
---

# Minimal Implementation

Make this task's failing tests pass with the simplest code that follows the task spec. No extras: refactoring comes after, in the same task.

## Parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md).

## Where this runs

Backs [`implementer`](../../agents/implementer.agent.md) task mode at phases 6.1..n — one task per spawn. Reads the task spec `6-solution.md` §T{n} ([shape](../../templates/task-spec-template.md)), the `5-contract.md` clauses it names, and open findings in `FINDINGS.md`. Writes code plus an append to §T{n}.

## Checklist

1. **Read §T{n} fully.** Files, Interfaces, Context, Steps, Tests to turn green, Done when, Do not touch.
2. **Check for gaps before writing anything.** A missing path, interface, convention, or command — or a step that needs a decision the spec didn't make — means **stop and return an open question** naming the gap. Never guess.
3. **Run the named tests once** and confirm they fail for the expected reason.
4. **Write the code in the listed files only**, using the Interfaces exactly as given (names, parameters, types, return shapes).
5. **Make one test pass at a time**: simplest case first, then edge cases, then error cases — only the ones the tests cover.
6. **Run the tests after every change.** A failure gets fixed before anything else.
7. **Tick every Done-when item**, running each command it lists.
8. **Append to §T{n}**: files changed, decisions taken (should be none — say so), anything surprising, plan said → actually did.

## Don't

- Add behavior, options, caching, or abstractions no test asks for.
- Touch a file outside the task's list, or anything under **Do not touch**.
- Rename or reshape an interface from the spec, even to "improve" it.
- Refactor yet — that's the next step (`refactor-optimizer`), once tests are green.
- Leave code only in chat: edit the real files.

## Done when

- [ ] Every test named in §T{n} passes, and no previously passing test fails
- [ ] Every Done-when item ticked, with its command run
- [ ] Nothing changed outside the task's files

Examples of minimal vs over-engineered code: [references/guide.md](references/guide.md).
