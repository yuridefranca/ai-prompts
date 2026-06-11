# Flow Comparison

> User flow and data flow comparison: Legacy (React 17) vs New (React 19)

## Overview

- **Date Generated**: [YYYY-MM-DD]

---

## Flow: [Flow Name — e.g., User Login]

### Legacy Implementation (React 17)

| Aspect | Detail |
|--------|--------|
| Entry Point | [Route / Component] |
| State Management | [Redux / Context / Local] |
| API Calls | [Method + Endpoint] |
| Data Flow | [Step-by-step] |
| Error Handling | [Pattern] |
| Redirect | [Target] |

### New Implementation (React 19)

| Aspect | Detail |
|--------|--------|
| Entry Point | [Route / Component] |
| State Management | [RSC / Hooks / Server Actions] |
| API Calls | [Method + Endpoint] |
| Data Flow | [Step-by-step] |
| Error Handling | [Pattern] |
| Redirect | [Target] |

### Delta

| Aspect | Legacy | New | Change Type |
|--------|--------|-----|-------------|
| [Route] | `/login` | `/auth/login` | Changed |
| [State] | Redux | RSC | Architecture |
| [API] | `POST /api/auth` | `POST /api/v2/auth` | Version bump |

---

## Flow: [Next Flow Name]

*(same structure)*

---

## Summary

| Metric | Count |
|--------|-------|
| Total flows analyzed | [N] |
| Flows with changes | [N] |
| New flows (not in legacy) | [N] |
| Removed flows (not in new) | [N] |
| Architecture changes | [N] |

## Flags

- [List flows with unclear migration path or missing new implementation details]
