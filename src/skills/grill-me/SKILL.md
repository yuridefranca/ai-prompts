---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

## Parameters

Read `{{phase}}` and `{{output}}` from a [skill-params block](../../schemas/skill-params.md) — this skill never runs standalone, so there are no defaults.

## Where this runs

The interview is folded **inline** into whichever artifact is being produced — there is no standalone grill-me artifact:

| Caller | Phase | `{{output}}` |
|---|---|---|
| [`prd-writer`](../../agents/prd-writer.agent.md) (PRD mode) | 2 | `2-prd.md` |
| [`quiz-master`](../../agents/quiz-master.agent.md) | 4 | `4-quiz.md` |

The grilling and its resolution live inside the phase artifact they informed.

---

Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore
the codebase instead.

For each question, provide your recommended answer.
