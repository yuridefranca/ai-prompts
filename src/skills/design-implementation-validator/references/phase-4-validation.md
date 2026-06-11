# Phase 4: Playwright Validation

## Process

1. Check if dev server is running:
    - If yes: Use existing server
    - If no: Start dev server (detect: vite, next dev, npm run dev, etc.)

2. Generate Playwright test file:

    ```typescript
    // .ai-workflow/[feature]/design-validation.spec.ts
    test.describe('UserCard Design Validation', () => {
      for (const breakpoint of breakpoints) {
        test(`matches Figma specs at ${breakpoint.name}`, async ({ page }) => {
          await page.setViewportSize(breakpoint.viewport);
          await page.goto('/components/user-card');

          const element = page.locator('[data-testid="user-card"]');

          // Get computed styles
          const styles = await element.evaluate((el) => {
            const computed = window.getComputedStyle(el);
            return {
              flexDirection: computed.flexDirection,
              gap: computed.gap,
              width: computed.width,
              // ... all relevant properties
            };
          });

          // Compare with Figma specs
          expect(styles.flexDirection).toBe(expectedSpecs.flexDirection);
          expect(parsePixels(styles.gap)).toBeCloseTo(expectedSpecs.gap, 1);
        });
      }
    });
    ```

3. Run validation tests:
    - Measure all computed CSS values
    - Compare with Figma specs
    - Use smart tolerance:
        - **Pixel-perfect goal** but allow ±1px for sub-pixel rendering
        - Detect surrounding component influence (e.g., parent width constraints)
        - Flag impossible-to-match scenarios with explanation

4. Optional: Visual regression
    - Take screenshots at each breakpoint
    - Store as baseline or compare with existing
    - Highlight visual differences

## Output

**File:** `validation-results.json`

```json
{
  "status": "partial-pass",
  "passedTests": 8,
  "failedTests": 2,
  "breakpoints": {
    "desktop": {
      "status": "pass",
      "properties": {
        "flexDirection": { "expected": "column", "actual": "column", "match": true },
        "gap": { "expected": "28px", "actual": "28px", "match": true }
      }
    },
    "tablet": {
      "status": "fail",
      "properties": {
        "gap": {
          "expected": "8.512px",
          "actual": "8px",
          "match": false,
          "reason": "Browser sub-pixel rounding",
          "tolerance": "acceptable"
        }
      }
    }
  }
}
```

## Common Issues

**Issue:** Dev server won't start
```
Solution: Check port availability, verify start command in config
```

**Issue:** Component not found in browser
```
Solution: Verify component route, check if component is exported/rendered
```

**Issue:** Excessive validation failures
```
Solution: Check if correct Figma frame selected, verify breakpoints match
```
