# Figma Design Inventory — Implementation Specs

> Auto-generated from Figma designs referenced in Jira epic: **[EPIC-KEY]**
> These specs are the source of truth for implementation and validation.

## Overview

- **Figma File**: [File Name]
- **Figma URL**: [URL]
- **Pages Inspected**: [N]
- **Breakpoints**: Mobile (≤767px), Tablet (768–1023px), Desktop (1024–1439px), Wide (≥1440px)
- **Date Generated**: [YYYY-MM-DD]

---

## Design Tokens

### Colors

| Token Name | Value | Usage |
|------------|-------|-------|
| `--color-primary` | `#HEX` | Primary actions, links |
| `--color-bg-surface` | `#HEX` | Card backgrounds |

### Typography

| Token Name | Font | Size | Weight | Line-Height | Letter-Spacing |
|------------|------|------|--------|-------------|----------------|
| `--text-heading-lg` | [Family] | [N]px / [N]rem | [N] | [N] | [N]px |
| `--text-body` | [Family] | [N]px / [N]rem | [N] | [N] | [N]px |

### Spacing Scale

| Token Name | Value | Usage Example |
|------------|-------|---------------|
| `--space-xs` | 4px | Inline icon gap |
| `--space-sm` | 8px | Compact padding |
| `--space-md` | 16px | Standard padding |
| `--space-lg` | 24px | Section padding |
| `--space-xl` | 32px | Page margins |

### Effects

| Token Name | Value |
|------------|-------|
| `--shadow-card` | `0 2px 8px rgba(0,0,0,0.1)` |
| `--radius-md` | `8px` |

### Z-Index Scale

| Token Name | Value | Usage |
|------------|-------|-------|
| `--z-dropdown` | 100 | Dropdowns, popovers |
| `--z-sticky` | 200 | Sticky headers, navbars |
| `--z-overlay` | 300 | Modal backdrops |
| `--z-modal` | 400 | Modal dialogs |
| `--z-toast` | 500 | Toast notifications |

### Theme Variants

| Token Name | Light | Dark |
|------------|-------|------|
| `--color-bg` | `#FFFFFF` | `#1A1A1A` |
| `--color-text` | `#000000` | `#F0F0F0` |

---

## Page-Level Layout: [Page Name]

### Page Grid Structure

| Region | Mobile | Tablet | Desktop | Wide |
|--------|--------|--------|---------|------|
| Header | full-width, height: [N]px | full-width, height: [N]px | full-width, height: [N]px | full-width, height: [N]px |
| Sidebar | hidden | width: [N]px, collapsible | width: [N]px, fixed | width: [N]px, fixed |
| Content | full-width, padding: [N]px | width: [N]px, padding: [N]px | width: [N]px, padding: [N]px | max-[N]px, centered |
| Footer | full-width | full-width | full-width | full-width |

### Page Container

| Property | Mobile | Tablet | Desktop | Wide |
|----------|--------|--------|---------|------|
| Max-width | 100% | [N]px | [N]px | [N]px |
| Margin (horizontal) | 0 auto | 0 auto | 0 auto | 0 auto |
| Gutters | [N]px | [N]px | [N]px | [N]px |

### Fixed / Sticky Regions

| Element | Behavior | Offset | Z-Index | Breakpoint |
|---------|----------|--------|---------|------------|
| Header | sticky top | top: 0 | `--z-sticky` | All |
| Sidebar | fixed left | left: 0 | `--z-sticky` | Desktop+ |

---

## Page: [Page Name]

### Component: [Component Name]

**Figma Node**: [Node path or ID]
**Parent**: [Parent component or layout]
**Children**: [List of child components]

#### Layout

| Property | Mobile | Tablet | Desktop | Wide |
|----------|--------|--------|---------|------|
| Width | [N]px / 100% | [N]px / 100% | [N]px / 100% | [N]px / max-[N]px |
| Min/Max Width | — | — | max-[N]px | max-[N]px |
| Height | auto / [N]px | auto / [N]px | auto / [N]px | auto / [N]px |
| Padding (T/R/B/L) | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px |
| Margin (T/R/B/L) | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px | [N]px [N]px [N]px [N]px |
| Gap | [N]px | [N]px | [N]px | [N]px |
| Direction | column / row | column / row | column / row | column / row |
| Align | [value] | [value] | [value] | [value] |
| Justify | [value] | [value] | [value] | [value] |
| Wrap | nowrap / wrap | nowrap / wrap | nowrap / wrap | nowrap / wrap |

#### Grid (if applicable)

| Property | Mobile | Tablet | Desktop | Wide |
|----------|--------|--------|---------|------|
| Columns | [N] | [N] | [N] | [N] |
| Column template | `1fr` | `repeat(2, 1fr)` | `repeat(3, 1fr)` | `repeat(4, 1fr)` |
| Rows | auto | auto | auto | auto |
| Row template | — | — | — | — |
| Gap (row/col) | [N]px / [N]px | [N]px / [N]px | [N]px / [N]px | [N]px / [N]px |
| Auto-fill / Auto-fit | — | — | auto-fill, minmax([N]px, 1fr) | auto-fill, minmax([N]px, 1fr) |
| Grid areas | — | — | `"sidebar content"` | `"sidebar content aside"` |
| Cell placement | — | — | [e.g., "sidebar: col 1, content: col 2"] | — |

#### Typography (within this component)

| Element | Property | Mobile | Tablet | Desktop | Wide |
|---------|----------|--------|--------|---------|------|
| Title | Font size | [N]px | [N]px | [N]px | [N]px |
| Title | Font weight | [N] | [N] | [N] | [N] |
| Title | Line height | [N] | [N] | [N] | [N] |
| Body | Font size | [N]px | [N]px | [N]px | [N]px |
| Body | Font weight | [N] | [N] | [N] | [N] |

#### Colors & Effects

| Property | Value | Token (if any) |
|----------|-------|----------------|
| Background | `#HEX` | `--color-*` |
| Text color | `#HEX` | `--color-*` |
| Border | [N]px solid `#HEX` | `--color-*` |
| Border radius | [N]px | `--radius-*` |
| Box shadow | [value] | `--shadow-*` |
| Opacity | [N] | — |

#### Icons & Images

| Element | Size | Color / Object-Fit | Notes |
|---------|------|---------------------|-------|
| [Icon name] | [N]×[N]px | `currentColor` / — | Inline SVG |
| [Image slot] | [N]×[N]px | `cover` / `contain` | Aspect ratio [N:N] |

#### Interactive States

| State | Background | Text | Border | Shadow | Other |
|-------|------------|------|--------|--------|-------|
| Default | `#HEX` | `#HEX` | [value] | [value] | — |
| Hover | `#HEX` | `#HEX` | [value] | [value] | cursor: pointer |
| Focus | `#HEX` | `#HEX` | [value] | [value] | outline: [value] |
| Active / Pressed | `#HEX` | `#HEX` | [value] | [value] | scale(0.98) |
| Disabled | `#HEX` | `#HEX` | [value] | — | opacity: 0.5 |
| Loading | — | — | — | — | [Spinner overlay spec] |
| Error | — | `#HEX` | [value] | — | [Error message spec] |
| Empty | — | — | — | — | [Empty state illustration spec] |

#### Transitions & Animations

| Property | Duration | Easing | Trigger |
|----------|----------|--------|---------|
| background-color | 200ms | ease-in-out | hover |
| transform | 150ms | ease-out | active |
| opacity | 300ms | ease | mount/unmount |

#### Z-Index & Stacking

| Element | Z-Index | Stacking Context | Notes |
|---------|---------|-------------------|-------|
| [Dropdown] | `--z-dropdown` | Creates new context | Above siblings |
| [Modal overlay] | `--z-overlay` | Root level | Full-screen backdrop |
| [Modal content] | `--z-modal` | Inside overlay | Above overlay |

#### Overflow & Clipping

| Element | Overflow-X | Overflow-Y | Text Truncation | Clip / Mask | Notes |
|---------|-----------|-----------|-----------------|-------------|-------|
| [Container] | hidden | auto | — | — | Scrollable list |
| [Title] | hidden | hidden | ellipsis | — | Single line truncate |
| [Description] | hidden | hidden | line-clamp: 3 | — | Max 3 lines |
| [Avatar] | hidden | hidden | — | border-radius: 50% | Circular clip |

#### Scroll Behavior

| Element | Scroll Type | Snap | Sticky/Fixed | Trigger | Notes |
|---------|------------|------|-------------|---------|-------|
| [Header] | — | — | sticky, top: 0 | scroll > [N]px | Shrinks on scroll |
| [Tab bar] | horizontal | snap-x mandatory | — | — | Scroll snap to tabs |
| [Feed list] | vertical | — | — | scroll event | Virtual scroll candidate |

#### Content Constraints

| Element | Min Width | Max Width | Min Items | Max Items | Text Limit | Empty Fallback |
|---------|-----------|-----------|-----------|-----------|------------|----------------|
| [Card] | [N]px | [N]px | — | — | title: 80 chars | Show placeholder |
| [List] | — | — | 0 | 50 | — | "No items yet" message |
| [Image] | [N]px | [N]px | — | — | — | Skeleton loader |
| [Avatar] | 32×32px | 64×64px | — | — | — | Initials fallback |

#### Cursor & Touch Targets

| Element | Cursor | Visual Size | Touch Target | Hit Area Expansion | Notes |
|---------|--------|-------------|-------------|-------------------|-------|
| [Button] | pointer | [N]×[N]px | min 44×44px | padding expansion | — |
| [Link] | pointer | auto | min 44×44px | — | — |
| [Drag handle] | grab / grabbing | [N]×[N]px | min 44×44px | — | Cursor changes on drag |
| [Disabled] | not-allowed | — | — | — | No interaction |

#### Accessibility

| Element | Tab Index | ARIA Role | ARIA Label | Keyboard Nav | Focus Indicator | Contrast Ratio |
|---------|-----------|-----------|------------|-------------|-----------------|----------------|
| [Button] | 0 | button | [label] | Enter/Space | 2px solid `--color-focus` | 4.5:1 (AA) |
| [Modal] | — | dialog | [title] | Escape closes, trap focus | — | — |
| [Nav] | — | navigation | "Main navigation" | Arrow keys | — | — |
| [Input] | 0 | — | [label] | — | 2px solid `--color-focus` | 3:1 (AA) |
| [Icon btn] | 0 | button | [action name] | Enter/Space | 2px ring | — |

#### Dark Mode / Theme Variants (if applicable)

| Property | Light | Dark | Token Override |
|----------|-------|------|----------------|
| Background | `#FFFFFF` | `#1A1A1A` | `--color-bg` |
| Text | `#000000` | `#F0F0F0` | `--color-text` |
| Border | `#E0E0E0` | `#333333` | `--color-border` |
| Shadow | `0 2px 8px rgba(0,0,0,0.1)` | `0 2px 8px rgba(0,0,0,0.3)` | `--shadow-card` |

> If dark mode designs are not provided, flag as `[MISSING: dark mode specs]` in Missing Specs.

#### Responsive Behavior Notes

- **Mobile → Tablet**: [e.g., "Stacked layout becomes horizontal; sidebar collapses to hamburger"]
- **Tablet → Desktop**: [e.g., "Navigation moves from bottom bar to top header"]
- **Desktop → Wide**: [e.g., "Content max-width caps at 1200px and centers; gutters widen"]
- **Hidden at breakpoint**: [e.g., "Promo banner hidden on mobile; secondary nav hidden on tablet"]

---

## Responsive Summary

| Component | Mobile | Tablet | Desktop | Wide | Missing Breakpoint |
|-----------|--------|--------|---------|------|--------------------|
| [Name] | ✅ | ✅ | ✅ | ⚠️ | Wide missing |
| [Name] | ✅ | ❌ | ✅ | ✅ | Tablet missing |

---

## Missing Specs

| Component | Missing Item | Breakpoint | State | Priority | Action Needed |
|-----------|-------------|------------|-------|----------|---------------|
| [Name] | Error state | All | error | HIGH | Request from design |
| [Name] | Tablet layout | Tablet | default | MEDIUM | Infer from mobile+desktop |
| [Name] | Hover color | Desktop | hover | LOW | Use token default |
| [Name] | Z-index for dropdown | All | default | HIGH | Define stacking order |
| [Name] | Focus indicator | All | focus | HIGH | Define focus ring spec |
| [Name] | Dark mode tokens | All | default | MEDIUM | Request dark mode designs |
| [Name] | Touch target size | Mobile | default | MEDIUM | Verify meets 44×44px minimum |

---

## Summary

| Metric | Count |
|--------|-------|
| Total components | [N] |
| Components with full specs (all breakpoints + states) | [N] |
| Components with missing breakpoints | [N] |
| Components with missing states | [N] |
| Components with missing z-index | [N] |
| Components with missing accessibility specs | [N] |
| Components with missing dark mode | [N] |
| Total missing specs | [N] |
| Breakpoints covered | [List] |

## Flags

- [List all missing specs, inconsistencies, and items needing design team input]
- [Flag any values that appear inconsistent across similar components — may be design error or intentional variation]
- [Flag any z-index conflicts or unclear stacking order]
- [Flag any touch targets below 44×44px minimum]
- [Flag any color contrast ratios below WCAG AA (4.5:1 for text, 3:1 for large text/UI)]
- [Flag any components missing dark mode specs if the project supports them]
