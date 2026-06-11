# Phase 1: Design Extraction & Analysis

## Input

- Figma URL (component/frame/page)
- Component name/path (where to implement)
- Target breakpoints (or auto-detect from Figma)

## Critical Notes

This phase extracts **ALL breakpoints** (mobile, tablet, desktop, wide) from Figma to ensure complete responsive coverage. The skill uses a mobile-first approach by default.

## Process

1. Load Figma MCP tools (if not already loaded)
2. Fetch component/frame from Figma URL
3. Detect Figma structure:
    - Check for Figma Variables (colors, spacing, typography)
    - Check for Design Tokens plugin data
    - Fall back to raw styles if neither exists
4. **Extract design specs for ALL breakpoints** (auto-detect from Figma):
    - Layout: flexbox/grid properties, dimensions, constraints
    - Spacing: padding, margin, gap
    - Typography: font-family, size, weight, line-height, letter-spacing
    - Colors: fills, strokes, background
    - Effects: shadows, blur, opacity
    - Borders: radius, width, style
    - States: hover, focus, active, disabled (if available)
5. Identify responsive behavior:
    - Auto Layout resize constraints
    - Breakpoint-specific overrides
    - Fluid vs fixed sizing
6. **Breakpoint detection strategies** (in priority order):
    - **Strategy 1:** Component variants with breakpoint names ("Mobile", "Tablet", "Desktop")
    - **Strategy 2:** Auto Layout constraints (Figma's responsive design features)
    - **Strategy 3:** Sibling frames with breakpoint naming (e.g., "Component / Mobile")
    - **Fallback:** Extract single breakpoint if no responsive variants found

## Output

**File:** `design-specs.json`

```json
{
  "component": "UserCard",
  "figmaUrl": "https://figma.com/...",
  "extractedAt": "2026-05-23T10:30:00Z",
  "figmaStructure": "variables",
  "breakpoints": {
    "mobile": { "width": 375, "specs": {...} },
    "tablet": { "width": 768, "specs": {...} },
    "desktop": { "width": 1440, "specs": {...} }
  },
  "semanticTokens": {
    "colors": ["primary-500", "neutral-100"],
    "spacing": ["spacing-4", "spacing-6"],
    "typography": ["text-base", "font-medium"]
  }
}
```
