# Design Implementation Validator

Automated Figma-to-Code-to-Validation pipeline for pixel-perfect UI implementations.

## Overview

This skill ensures frontend implementations match Figma designs through a comprehensive 5-phase validation process that extracts design specs, maps to design systems, generates responsive code, and validates with Playwright.

## Quick Start

```markdown
@design-implementation-validator

**Component:** UserCard
**Figma URL:** https://figma.com/file/abc123?node-id=456:789
**Component Path:** src/components/UserCard.tsx

Validate implementation against Figma design.
```

## Features

✅ **Multi-breakpoint extraction** - Automatically extracts **ALL breakpoints** from Figma (mobile, tablet, desktop, wide)  
✅ **Mobile-first approach** - Default responsive strategy (configurable to desktop-first if needed)  
✅ **Design system integration** - Maps Figma values to Tailwind, Styled Components, or custom tokens  
✅ **Auto-detection** - Detects Figma Variables, Design Tokens, or raw styles  
✅ **Responsive code generation** - Generates idiomatic mobile-first code with proper breakpoint prefixes  
✅ **Playwright validation** - Validates computed CSS against Figma specs at **all breakpoints**  
✅ **Smart tolerance** - Pixel-perfect with context-aware acceptable deviations  
✅ **Visual regression** - Optional screenshot comparison at each breakpoint  
✅ **Self-healing** - AI-powered fix suggestions with auto-apply  

## Supported Design Systems

- **Tailwind CSS** - Full support with arbitrary values
- **Styled Components** - Theme-based token mapping
- **Emotion** - Compatible with Styled Components adapter
- **Extensible** - Add custom adapters via plugin system

## Workflow Integration

### Feature Workflow (Phase 5)
Automatically triggered when:
- Figma URL provided in requirements
- Component involves UI/visual work
- User hasn't opted out with `--skip-design-validation`

### Improvement Workflow (Phase 5)
Prompts user when:
- Component involves visual changes
- Figma URL found in component comments

## Documentation

### Core Documentation
- **[SKILL.md](SKILL.md)** - Complete skill specification, usage, and integration
- **[Examples](examples/user-card-example.md)** - Full walkthrough with validation report

### Design System Adapters
- **[Base Adapter](adapters/base-adapter.md)** - Interface and implementation guidelines
- **[Tailwind Adapter](adapters/tailwind-adapter.md)** - Tailwind CSS mapping and code generation
- **[Styled Components Adapter](adapters/styled-components-adapter.md)** - CSS-in-JS mapping

### Utilities
- **[Figma Extraction](utilities/figma-extraction.md)** - Extract design specs from Figma MCP
- **[Playwright Validation](utilities/playwright-validation.md)** - Automated validation system

## Validation Process

```
┌─────────────────┐
│  Figma Design   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Extract Specs   │ ← Detect Variables/Tokens/Raw
│(ALL breakpoints)│ ← Mobile, Tablet, Desktop, Wide
└────────┬────────┘
         ↓
┌─────────────────┐
│ Detect Design   │ ← Auto-detect Tailwind/Styled/Custom
│    System       │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Map Figma →     │ ← Exact/Fuzzy/Arbitrary mapping
│ Design Tokens   │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Generate Code   │ ← Mobile-first responsive code
│ (Mobile-First)  │ ← Base = mobile, then breakpoint overrides
└────────┬────────┘
         ↓
┌─────────────────┐
│ Run Playwright  │ ← Test ALL breakpoints
│   Validation    │ ← Mobile, Tablet, Desktop, Wide
└────────┬────────┘
         ↓
┌─────────────────┐
│ Smart Tolerance │ ← Pixel-perfect with context awareness
│    Analysis     │ ← Per-breakpoint validation
└────────┬────────┘
         ↓
┌─────────────────┐
│ Generate Report │ ← Pass/Fail/Acceptable deviations
│ (All Breakpoints)│
└─────────────────┘
```

## Output Artifacts

All artifacts stored in `.ai-workflow/[feature]/design-validation/`:

```
design-validation/
├── design-specs.json              # Extracted Figma specs
├── design-system-mapping.json     # Figma → Design system mappings
├── validation-results.json        # Test execution data
├── validation-report.md           # Human-readable report
├── design-validation.spec.ts      # Playwright test (temporary)
└── screenshots/                   # Visual regression (optional)
    ├── desktop.png
    ├── tablet.png
    └── mobile.png
```

## Configuration

Create `.design-validation.config.js` in project root (optional):

```javascript
module.exports = {
  designSystem: 'tailwind', // auto-detect if omitted
  
  // Responsive approach (default: mobile-first)
  responsiveStrategy: 'mobile-first', // or 'desktop-first' (not recommended)
  
  // Breakpoints (auto-detected from Figma by default)
  breakpoints: {
    mobile: { width: 375, height: 667 },
    tablet: { width: 768, height: 1024 },
    desktop: { width: 1440, height: 900 },
    wide: { width: 1920, height: 1080 }, // optional
  },
  tolerance: {
    spacing: 1,    // ±1px
    colors: 0,     // exact
    typography: 1,
  },
  autoFix: {
    enabled: true,
    requireApproval: true,
    maxIterations: 3,
  },
  devServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    readyPattern: 'ready in',
  },
  validationTests: {
    location: '.ai-workflow/[feature]/',
    keepAfterValidation: false,
  },
};
```

## Example Validation Report

```markdown
# Design Validation Report: UserCard

**Status:** ✅ PASSED
**Total Tests:** 4 | **Passed:** 4 | **Failed:** 0

## Mobile (375px) ✅
- Layout: `flex`, `column`, `flex-start` ✅
- Spacing: `gap: 16px`, `padding: 20px` ✅
- Sizing: `max-width: 360px` ✅
- Colors: All matched design tokens ✅

## Tablet (768px) ✅
- Layout: `flex-direction: row` ✅
- Spacing: `gap: 24px` ✅
- Sizing: `max-width: none` ✅

## Recommendations
✅ Implementation complete - all specs matched
✅ Ready for code review
```

## MCP Dependencies

This skill requires:

1. **Figma MCP** - Design extraction
2. **Playwright MCP** - Validation tests
3. **Browser MCP** (optional) - Visual comparison

## Best Practices

1. Add `data-testid` attributes to components
2. Provide Figma URLs in component file comments
3. Document acceptable deviations for team reference
4. Run validation before code review
5. Update Figma when implementation constraints discovered
6. Clean up temporary validation tests after approval

## Extending

### Add New Design System

1. Create `adapters/[system]-adapter.md`
2. Implement `DesignSystemAdapter` interface
3. Add detection logic
4. Define mapping strategies
5. Implement code generation
6. Register in `adapters/index.ts`

See [Base Adapter](adapters/base-adapter.md) for full interface specification.

## Troubleshooting

### Common Issues

**Figma URL not accessible**
```
→ Check Figma MCP authentication
→ Verify URL permissions
```

**Dev server won't start**
```
→ Check port availability
→ Verify start command in config
```

**Component not found**
```
→ Verify component route
→ Check if component is exported/rendered
→ Ensure data-testid attribute exists
```

**Excessive failures**
```
→ Verify correct Figma frame selected
→ Check breakpoints match actual viewports
→ Ensure design system config is loaded
```

## Future Enhancements

- Animation/transition validation
- Multi-browser testing (Firefox, Safari)
- Pseudo-element validation (::before, ::after)
- Bi-directional Figma sync
- Component library batch validation
- Accessibility validation integration

## Related Skills

- **frontend-engineer.agent.md** - Invokes this skill for UI work
- **minimal-impl-generator** - Implementation before validation
- **refactor-optimizer** - Optimization after validation passes
- **code-reviewer** - Final review after design validation

---

**Created:** 2026-05-23  
**Version:** 1.0.0  
**Status:** Production Ready
