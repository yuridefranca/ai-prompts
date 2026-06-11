# Component Inventory

> Legacy (React 17) vs New (React 19) component mapping

## Overview

- **Legacy Repo**: [Path]
- **New Repo**: [Path]
- **Date Generated**: [YYYY-MM-DD]

---

## Pages and Routes

| Page | Legacy Route | New Route | Classification | Notes |
|------|-------------|-----------|-----------------|-------|
| [Home] | `/` | `/home` | Migrate | Route changed |

---

## UI Components

| Component | Legacy Path | New Repo Path | Classification | Notes |
|-----------|-------------|---------------|----------------|-------|
| [Header] | `src/Header.tsx` | `src/components/Header.tsx` | Migrate | API changed |
| [Button] | `src/Button.tsx` | `src/ui/Button.tsx` | Exists | Different styling |
| [Dashboard] | — | — | Create | New page in Figma |

---

## Custom Hooks

| Hook | Legacy Path | New Repo Path | Classification | Notes |
|------|-------------|---------------|----------------|-------|
| [useAuth] | `src/hooks/useAuth.ts` | — | Migrate | Needs RSC adaptation |

---

## Context Providers

| Provider | Legacy Path | New Repo Path | Classification | Notes |
|----------|-------------|---------------|----------------|-------|
| [AuthProvider] | `src/context/Auth.tsx` | — | Migrate | Convert to RSC pattern |

---

## Utilities

| Utility | Legacy Path | New Repo Path | Classification | Notes |
|---------|-------------|---------------|----------------|-------|
| [formatDate] | `src/utils/date.ts` | `src/lib/utils.ts` | Exists | Verify API match |

---

## Third-Party Dependencies

| Package | Legacy Version | New Version | Status | Notes |
|---------|---------------|-------------|--------|-------|
| [react-router] | v5 | v6 | Migrate | API breaking changes |

---

## Summary

| Classification | Count |
|----------------|-------|
| Migrate | [N] |
| Exists | [N] |
| Create | [N] |
| Delete | [N] |
| **Total** | [N] |

## Flags

- [List components with unclear classification or compatibility concerns]
