# Migration Plan

> Phased migration plan for site rewrite: React 17 → React 19

## Overview

- **Epic**: [EPIC-KEY]
- **Date Generated**: [YYYY-MM-DD]
- **Total Phases**: [N]
- **Total Jira Tickets Covered**: [N]

---

## Phase 0: Foundation

**Goal**: Set up shared infrastructure needed by all subsequent phases.

**Components**:
| Component | Classification | Complexity | Dependencies |
|-----------|---------------|------------|--------------|
| [Design system setup] | Create | L | None |
| [Auth provider] | Migrate | M | None |
| [API client] | Migrate | S | None |

**API Changes**:
- [List API changes needed]

**Jira Tickets**: [TICKET-001, TICKET-002]

**Figma Designs**: [Links to relevant frames]

**Dependencies**: None (first phase)

---

## Phase 1: Core Pages

**Goal**: Implement main navigation and authentication flows.

**Components**:
| Component | Classification | Complexity | Dependencies |
|-----------|---------------|------------|--------------|
| [Header/Nav] | Migrate | M | Phase 0 |
| [Login page] | Migrate | M | Phase 0 |
| [Dashboard] | Create | L | Phase 0 |

**API Changes**:
- [List API changes needed]

**Jira Tickets**: [TICKET-003, TICKET-004]

**Figma Designs**: [Links]

**Dependencies**: Phase 0

---

## Phase 2: Feature Pages

*(same structure, grouped by feature area)*

---

## Phase 3: Polish

**Goal**: Animations, edge cases, performance optimization.

*(same structure)*

---

## Gaps Requiring Resolution

| Gap ID | Priority | Phase Affected | Resolution Needed Before |
|--------|----------|----------------|--------------------------|
| GAP-001 | HIGH | Phase 1 | Phase 1 start |
| GAP-003 | MEDIUM | Phase 2 | Phase 2 start |

---

## Assumptions

| ID | Assumption | Affects Phase | Risk |
|----|-----------|----------------|------|
| A-001 | [Text] | Phase 1 | [Risk] |

---

## Summary

| Phase | Components | Migrate | Create | Exists | Jira Tickets | Complexity |
|-------|-----------|---------|--------|--------|---------------|------------|
| 0 | [N] | [N] | [N] | [N] | [N] | [S/M/L] |
| 1 | [N] | [N] | [N] | [N] | [N] | [S/M/L] |
| 2 | [N] | [N] | [N] | [N] | [N] | [S/M/L] |
| 3 | [N] | [N] | [N] | [N] | [N] | [S/M/L] |
| **Total** | [N] | [N] | [N] | [N] | [N] | — |

## Validation Checklist

- [ ] Every Jira ticket maps to a phase
- [ ] Every component classification appears in a phase
- [ ] All HIGH priority gaps have resolution plan
- [ ] All assumptions are documented
- [ ] Phase dependencies are acyclic
- [ ] No orphaned components (classified but not in any phase)
