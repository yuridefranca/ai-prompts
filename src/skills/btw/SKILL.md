---
name: btw
description: Ask a side question or get a quick answer without adding it to the workflow context. Use when you need a quick clarification, definition, or tangential answer that should NOT become part of the workflow artifacts or context. Keywords btw, side question, quick question, off-topic, tangent.
---

# BTW — Side Questions Without Context Pollution

Ask a question, get an answer, and keep it out of the workflow. This skill answers your question without creating artifacts, updating context, or affecting the workflow state.

## When to Use

- You need a quick definition ("What's a circuit breaker pattern?")
- You want a second opinion on something tangential ("Is Redis better than Memcached for this?")
- You need a clarification that doesn't belong in the workflow ("What does this error code mean?")
- You want to explore an idea without committing to it ("Could we use event sourcing here?")

## When NOT to Use

- The question is directly related to the current workflow phase → just ask normally
- The answer should be documented → use the appropriate workflow phase
- The question changes the scope of work → update the startpoint instead

## Rules

1. **No artifacts**: Do NOT create any files in `.ai-workflow/`
2. **No context update**: Do NOT add this Q&A to the context rehydration summary
3. **No workflow impact**: Do NOT change the workflow state, phase, or decisions
4. **Keep it brief**: Answer concisely. If the answer needs deep exploration, suggest starting a separate conversation.
5. **Stay focused**: Answer the question, then remind the user what phase they were in

## Process

1. **Acknowledge the side question**: "Quick answer:"
2. **Answer concisely**: Direct, practical answer. No fluff.
3. **Remind context**: "Back to [Phase N] — we were [doing what]"

## Example

**User**: /btw what's the difference between a saga and a transaction outbox pattern?

**Response**:

> **Quick answer**:
>
> - **Saga**: Orchestrates a sequence of local transactions across services, with compensating actions on failure. Good for complex multi-service workflows.
> - **Transaction Outbox**: Writes to an outbox table in the same DB transaction as the business operation, then a relay publishes to a message broker. Good for "at-least-once" delivery guarantees.
> - Key difference: Saga is about coordination; Outbox is about reliable publishing. They're often used together.
>
> _Back to Phase 2 (Tradeoff Analysis) — we were evaluating the caching approach._
