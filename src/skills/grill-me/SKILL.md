---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me".
---

## Workflow Artifact

This skill is invoked as **Phase 0.1** in all three workflows:

- **Bug Workflow Phase 0.1**: Produces `.ai-workflow/[feature-folder]/0.1-grill-me.md`
- **Improvement Workflow Phase 0.1**: Produces `.ai-workflow/[feature-folder]/0.1-grill-me.md`
- **Feature Workflow Phase 0.1**: Produces `.ai-workflow/[feature-folder]/0.1-grill-me.md`

**Context**: Read `0-startpoint.md` for the user's initial description before grilling.

---

Interview me relentlessly about every aspect of this plan until
we reach a shared understanding. Walk down each branch of the design
tree resolving dependencies between decisions one by one.

If a question can be answered by exploring the codebase, explore
the codebase instead.

For each question, provide your recommended answer.
