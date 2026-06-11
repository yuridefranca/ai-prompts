# API Mapping

> API call comparison: Legacy (React 17) vs New (React 19)

## Overview

- **Legacy Repo**: [Path]
- **New Repo**: [Path]
- **Date Generated**: [YYYY-MM-DD]

---

## Endpoint Inventory

| Endpoint | Method | Legacy Usage | New Usage | Status | Notes |
|----------|--------|-------------|-----------|--------|-------|
| `/api/user` | GET | `useEffect` + axios | RSC `fetch` | Migrate | Pattern change |
| `/api/v2/bet` | POST | — | New feature | Create | New endpoint |
| `/api/legacy-feed` | GET | Redux action | — | Delete | Deprecated |

---

## Data Fetching Patterns

### Legacy Patterns

| Pattern | Usage Count | Example |
|---------|-------------|---------|
| `useEffect` + axios | [N] | `src/hooks/useUser.ts` |
| Redux thunk | [N] | `src/store/actions.ts` |
| SWR | [N] | `src/pages/Dashboard.tsx` |

### New Patterns

| Pattern | Usage Count | Example |
|---------|-------------|---------|
| RSC `fetch` | [N] | `app/dashboard/page.tsx` |
| Server Actions | [N] | `app/actions.ts` |
| React Query | [N] | `src/hooks/useBets.ts` |

---

## Authentication Flow

| Aspect | Legacy | New | Delta |
|--------|--------|-----|-------|
| Auth method | [JWT / Cookie] | [JWT / Cookie] | [Same / Changed] |
| Token storage | [localStorage / httpOnly] | [httpOnly / RSC] | [Changed] |
| Refresh flow | [Pattern] | [Pattern] | [Delta] |

---

## Summary

| Status | Count |
|--------|-------|
| Migrate | [N] |
| Create | [N] |
| Delete | [N] |
| Unchanged | [N] |
| **Total** | [N] |

## Flags

- [List endpoints with breaking changes, missing documentation, or unclear migration path]
