# Example: UserCard Component Validation

Complete example of the design-implementation-validator skill in action.

## Scenario

Implementing a UserCard component from Figma design with responsive behavior across mobile, tablet, and desktop breakpoints.

## Step 1: Input Figma URL

```
User provides:
- Figma URL: https://figma.com/file/abc123/designs?node-id=456:789
- Component name: UserCard
- Component path: src/components/UserCard.tsx
```

## Step 2: Extraction Phase

### Breakpoint Detection Strategy

The skill detected responsive variants using **Strategy 1: Component Variants**.  
Figma component set had variants named: "UserCard, Breakpoint=Mobile", "UserCard, Breakpoint=Tablet", "UserCard, Breakpoint=Desktop".

**Mobile-First Approach:**
- **Base styles:** Extracted from Mobile variant (foundation)
- **Responsive overrides:** Extracted from Tablet and Desktop variants
- **Code generation order:** Mobile (base) → Tablet (md:) → Desktop (lg:)

### Extracted Design Specs

```json
{
  "name": "UserCard",
  "figmaUrl": "https://figma.com/file/abc123/designs?node-id=456:789",
  "extractedAt": "2026-05-23T10:30:00Z",
  "figmaStructure": "variables",
  "breakpoints": {
    "mobile": {
      "layout": {
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "flex-start",
        "justifyContent": "flex-start"
      },
      "spacing": {
        "gap": 16,
        "padding": 20,
        "margin": 0
      },
      "sizing": {
        "width": "100%",
        "minWidth": null,
        "maxWidth": 360,
        "height": "auto"
      },
      "typography": {
        "fontFamily": "Inter",
        "fontSize": 14,
        "fontWeight": 500,
        "lineHeight": 1.5,
        "letterSpacing": -0.01
      },
      "colors": {
        "background": "surface-primary",
        "color": "text-primary",
        "border": "border-subtle"
      },
      "effects": {
        "borderRadius": 12,
        "borderWidth": 1,
        "boxShadow": "shadow-sm"
      }
    },
    "tablet": {
      "layout": {
        "flexDirection": "row",
        "alignItems": "center"
      },
      "spacing": {
        "gap": 24,
        "padding": 24
      },
      "sizing": {
        "maxWidth": null
      }
    },
    "desktop": {
      "spacing": {
        "gap": 32,
        "padding": 32
      },
      "sizing": {
        "maxWidth": 480
      }
    }
  },
  "states": {
    "hover": {
      "effects": {
        "boxShadow": "shadow-md"
      },
      "colors": {
        "background": "surface-primary-hover"
      }
    }
  },
  "semanticTokens": {
    "colors": ["surface-primary", "surface-primary-hover", "text-primary", "border-subtle"],
    "spacing": ["spacing-4", "spacing-5", "spacing-6", "spacing-8"],
    "typography": ["text-sm", "font-medium"],
    "effects": ["shadow-sm", "shadow-md", "rounded-xl"]
  }
}
```

## Step 3: Design System Mapping

### Detected System: Tailwind

```json
{
  "detectedSystem": "tailwind",
  "configPath": "tailwind.config.ts",
  "mappings": {
    "colors": {
      "surface-primary": {
        "value": "bg-white",
        "exactMatch": true,
        "confidence": 1.0
      },
      "surface-primary-hover": {
        "value": "bg-gray-50",
        "exactMatch": true,
        "confidence": 1.0
      },
      "text-primary": {
        "value": "text-gray-900",
        "exactMatch": true,
        "confidence": 1.0
      },
      "border-subtle": {
        "value": "border-gray-200",
        "exactMatch": true,
        "confidence": 1.0
      }
    },
    "spacing": {
      "16px": {
        "value": "4",
        "exactMatch": true,
        "confidence": 1.0
      },
      "20px": {
        "value": "5",
        "exactMatch": true,
        "confidence": 1.0
      },
      "24px": {
        "value": "6",
        "exactMatch": true,
        "confidence": 1.0
      },
      "32px": {
        "value": "8",
        "exactMatch": true,
        "confidence": 1.0
      }
    },
    "typography": {
      "14px": {
        "value": "text-sm",
        "exactMatch": true,
        "confidence": 1.0
      },
      "500": {
        "value": "font-medium",
        "exactMatch": true,
        "confidence": 1.0
      }
    },
    "effects": {
      "12px": {
        "value": "rounded-xl",
        "exactMatch": true,
        "confidence": 1.0
      },
      "shadow-sm": {
        "value": "shadow-sm",
        "exactMatch": true,
        "confidence": 1.0
      }
    }
  },
  "warnings": [],
  "suggestions": []
}
```

## Step 4: Code Generation

### Generated Component

```tsx
// UserCard.tsx
// Generated from Figma design
// Date: 2026-05-23T10:30:00Z
// Figma: https://figma.com/file/abc123/designs?node-id=456:789
// Responsive Strategy: Mobile-First

import React from 'react';

interface UserCardProps {
  name: string;
  email: string;
  avatar?: string;
}

export const UserCard: React.FC<UserCardProps> = ({ name, email, avatar }) => {
  return (
    <div
      data-testid="user-card"
      className="
        /* Mobile base styles (375px) */
        flex flex-col items-start
        gap-4 p-5
        w-full max-w-[360px]
        bg-white text-gray-900
        border border-gray-200 rounded-xl shadow-sm
        transition-all duration-200
        
        /* Tablet overrides (768px+) */
        md:flex-row md:items-center
        md:gap-6 md:p-6
        md:max-w-none
        
        /* Desktop overrides (1440px+) */
        lg:gap-8 lg:p-8
        lg:max-w-[480px]
        
        /* Hover state (all breakpoints) */
        hover:bg-gray-50 hover:shadow-md
      "
    >
      {avatar && (
        <img
          src={avatar}
          alt={name}
          className="w-12 h-12 rounded-full object-cover"
        />
      )}
      <div className="flex flex-col gap-1">
        <h3 className="text-sm font-medium text-gray-900">{name}</h3>
        <p className="text-xs text-gray-600">{email}</p>
      </div>
    </div>
  );
};
```

## Step 5: Validation Test

### Generated Playwright Test

```typescript
// .ai-workflow/user-card-validation/design-validation.spec.ts
import { test, expect } from '@playwright/test';

/**
 * Design Validation Test
 * Component: UserCard
 * Figma: https://figma.com/file/abc123/designs?node-id=456:789
 * Generated: 2026-05-23T10:30:00Z
 */

// Helper functions
function parsePixels(value: string): number {
  return parseFloat(value.replace('px', ''));
}

function rgbToHex(rgb: string): string {
  const match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return rgb;
  
  const [, r, g, b] = match;
  return `#${[r, g, b]
    .map(x => parseInt(x).toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase()}`;
}

test.describe('UserCard - Mobile (375px)', () => {
  test('matches Figma layout specs', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('http://localhost:3000/components/user-card');
    await page.waitForSelector('[data-testid="user-card"]');
    
    const element = page.locator('[data-testid="user-card"]');
    
    const styles = await element.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        display: computed.display,
        flexDirection: computed.flexDirection,
        alignItems: computed.alignItems,
        gap: computed.gap,
        padding: computed.padding,
        maxWidth: computed.maxWidth,
        backgroundColor: computed.backgroundColor,
        borderColor: computed.borderColor,
        borderRadius: computed.borderRadius,
        boxShadow: computed.boxShadow,
      };
    });
    
    // Layout validation
    expect(styles.display).toBe('flex');
    expect(styles.flexDirection).toBe('column');
    expect(styles.alignItems).toBe('flex-start');
    
    // Spacing validation (±1px tolerance)
    const gapValue = parsePixels(styles.gap);
    expect(gapValue).toBeGreaterThanOrEqual(15);
    expect(gapValue).toBeLessThanOrEqual(17);
    
    const paddingValue = parsePixels(styles.padding);
    expect(paddingValue).toBeGreaterThanOrEqual(19);
    expect(paddingValue).toBeLessThanOrEqual(21);
    
    // Sizing validation
    expect(styles.maxWidth).toBe('360px');
    
    // Color validation
    const bgColor = rgbToHex(styles.backgroundColor);
    expect(bgColor).toBe('#FFFFFF');
    
    // Effects validation
    expect(styles.borderRadius).toBe('12px');
  });
});

test.describe('UserCard - Tablet (768px)', () => {
  test('matches Figma layout specs', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await page.goto('http://localhost:3000/components/user-card');
    await page.waitForSelector('[data-testid="user-card"]');
    
    const element = page.locator('[data-testid="user-card"]');
    
    const styles = await element.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        flexDirection: computed.flexDirection,
        alignItems: computed.alignItems,
        gap: computed.gap,
        padding: computed.padding,
        maxWidth: computed.maxWidth,
      };
    });
    
    // Responsive layout changes
    expect(styles.flexDirection).toBe('row');
    expect(styles.alignItems).toBe('center');
    
    // Responsive spacing
    const gapValue = parsePixels(styles.gap);
    expect(gapValue).toBeGreaterThanOrEqual(23);
    expect(gapValue).toBeLessThanOrEqual(25);
    
    const paddingValue = parsePixels(styles.padding);
    expect(paddingValue).toBeGreaterThanOrEqual(23);
    expect(paddingValue).toBeLessThanOrEqual(25);
    
    // Max width removed at tablet
    expect(styles.maxWidth).toBe('none');
  });
});

test.describe('UserCard - Hover state', () => {
  test('matches Figma hover specs', async ({ page }) => {
    await page.goto('http://localhost:3000/components/user-card');
    const element = page.locator('[data-testid="user-card"]');
    
    // Trigger hover
    await element.hover();
    await page.waitForTimeout(300); // Wait for transition
    
    const styles = await element.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        backgroundColor: computed.backgroundColor,
        boxShadow: computed.boxShadow,
      };
    });
    
    // Hover state validation
    const bgColor = rgbToHex(styles.backgroundColor);
    expect(bgColor).toBe('#F9FAFB'); // gray-50
    
    // Shadow should be more prominent
    expect(styles.boxShadow).toContain('4px'); // shadow-md
  });
});
```

## Step 6: Validation Results

### Test Execution

```
Running design validation tests...

✅ UserCard - Mobile (375px) > matches Figma layout specs
✅ UserCard - Tablet (768px) > matches Figma layout specs  
✅ UserCard - Desktop (1440px) > matches Figma layout specs
✅ UserCard - Hover state > matches Figma hover specs

4 passed (2.3s)
```

### Validation Analysis

```json
{
  "status": "pass",
  "passedTests": 4,
  "failedTests": 0,
  "criticalFailures": [],
  "acceptableDeviations": [],
  "breakdownByBreakpoint": {
    "mobile": {
      "status": "pass",
      "passed": 1,
      "failed": 0,
      "properties": {
        "flexDirection": { "expected": "column", "actual": "column", "match": true },
        "gap": { "expected": "16px", "actual": "16px", "match": true },
        "padding": { "expected": "20px", "actual": "20px", "match": true },
        "maxWidth": { "expected": "360px", "actual": "360px", "match": true }
      }
    },
    "tablet": {
      "status": "pass",
      "passed": 1,
      "failed": 0,
      "properties": {
        "flexDirection": { "expected": "row", "actual": "row", "match": true },
        "gap": { "expected": "24px", "actual": "24px", "match": true }
      }
    }
  }
}
```

## Step 7: Validation Report

```markdown
# Design Validation Report: UserCard

**Component:** UserCard  
**Figma URL:** [View in Figma](https://figma.com/file/abc123/designs?node-id=456:789)  
**Validation Date:** 2026-05-23 10:45:00  
**Status:** ✅ PASSED

---

## Summary

- **Total Tests:** 4
- **Passed:** 4
- **Failed:** 0
- **Critical Failures:** 0
- **Acceptable Deviations:** 0

---

## Breakpoint Results

### ✅ Mobile (375px)
All properties match Figma specs perfectly.

**Validated Properties:**
- Layout: `flex`, `flex-direction: column`, `align-items: flex-start` ✅
- Spacing: `gap: 16px`, `padding: 20px` ✅
- Sizing: `max-width: 360px` ✅
- Colors: `background: #FFFFFF`, `border: #E5E7EB` ✅
- Effects: `border-radius: 12px`, `box-shadow: shadow-sm` ✅

### ✅ Tablet (768px)
All responsive changes implemented correctly.

**Responsive Changes:**
- Layout: `flex-direction: row`, `align-items: center` ✅
- Spacing: `gap: 24px`, `padding: 24px` ✅
- Sizing: `max-width: none` ✅

### ✅ Desktop (1440px)
All desktop-specific styles applied correctly.

**Desktop Changes:**
- Spacing: `gap: 32px`, `padding: 32px` ✅
- Sizing: `max-width: 480px` ✅

### ✅ Hover State
Interaction state matches Figma design.

**Hover Changes:**
- Background: `#F9FAFB` (gray-50) ✅
- Shadow: `shadow-md` ✅
- Transition: `200ms` ✅

---

## Design System Alignment

✅ All colors mapped to design system tokens  
✅ All spacing values on 4px scale  
✅ Typography matches design system  
✅ Effects use standard shadow tokens  

No design system updates needed.

---

## Recommendations

✅ **Implementation Complete** - All Figma specs matched perfectly  
✅ **Code Review** - Ready for code review  
✅ **Merge** - Safe to merge after review  

---

## Next Steps

1. ✅ Delete temporary validation test file
2. ✅ Proceed to code review
3. ✅ Merge component implementation

---

## Artifacts

- **Component:** `src/components/UserCard.tsx`
- **Test File:** `.ai-workflow/user-card-validation/design-validation.spec.ts` (temporary)
- **Design Specs:** `.ai-workflow/user-card-validation/design-specs.json`
- **Mapping:** `.ai-workflow/user-card-validation/design-system-mapping.json`
- **Report:** `.ai-workflow/user-card-validation/validation-report.md`
```

---

## Example with Deviations

### Scenario: Parent Container Constraint

```json
{
  "property": "maxWidth",
  "breakpoint": "mobile",
  "expected": "360px",
  "actual": "340px",
  "match": false,
  "category": "sizing",
  "severity": "acceptable",
  "reason": "Constrained by parent container max-width: 340px",
  "recommendation": "Verify if parent constraint is intentional or adjust parent container"
}
```

### Report Section

```markdown
## Acceptable Deviations

1. **Max Width at Mobile Breakpoint**
   - Expected: 360px (Figma)
   - Actual: 340px
   - Reason: Parent container has `max-width: 340px` constraint
   - Impact: Minimal visual difference, component fits parent as expected
   - Action: Document that component adapts to parent constraints

**Options:**
1. ✅ Accept deviation (recommended) - Component correctly adapts to parent
2. Adjust parent container to allow full 360px width
3. Consult designer to adjust Figma spec to match parent constraint
```

---

## Files Created During Validation

```
.ai-workflow/user-card-validation/
├── design-specs.json                    # Extracted from Figma
├── design-system-mapping.json           # Figma → Tailwind mappings
├── design-validation.spec.ts            # Generated Playwright test (temp)
├── validation-results.json              # Test execution results
├── validation-report.md                 # This report
└── screenshots/                         # Visual regression (optional)
    ├── mobile.png
    ├── tablet.png
    └── desktop.png
```

---

## Workflow Integration

This validation runs automatically during:
- **Feature Workflow, Phase 7** (Implementation)
- **Improvement Workflow, Phase 3/4** (UI Updates)

Triggered when:
- Figma URL is provided in requirements
- Component involves UI/visual changes
- User hasn't opted out with `--skip-design-validation`
