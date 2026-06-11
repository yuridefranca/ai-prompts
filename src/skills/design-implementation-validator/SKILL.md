# Design Implementation Validator

**Automated Figma-to-Code-to-Validation pipeline for UI components**

## Purpose

Ensures frontend implementations pixel-perfectly match Figma designs by:

1. Extracting design specifications from Figma (all breakpoints)
2. Mapping Figma values to the project's design system
3. Generating/validating responsive code with proper tokens
4. Running Playwright validation to verify computed styles
5. Providing actionable fix suggestions with auto-healing

## When to Use

✅ **Use this skill when:**

- Implementing new UI components from Figma designs
- Updating existing components to match new designs
- Frontend Engineer agent is invoked for UI work
- User provides a Figma URL/link
- Phase 7 (Implementation) of Feature Workflow for UI tasks
- Phase 3/4 of Improvement Workflow for UI updates

❌ **Do NOT use when:**

- No Figma design exists (prototyping/exploration)
- Backend-only tasks
- Logic-only changes without visual impact
- User explicitly requests manual implementation

## Automatic Triggering

This skill is **automatically invoked** during workflows when:

1. Task involves UI/frontend components (detected by keywords or frontend-engineer agent)
2. Figma URL is provided in requirements OR detected in task description
3. User has not explicitly opted out with `--skip-design-validation`

## Prerequisites

Before running this skill, ensure:

- Figma MCP server is available and configured
- Playwright MCP server is available
- Dev server can be started or is already running
- Component path/location is identified

## Workflow Phases

### Phase 1: Design Extraction & Analysis

**Input:**

- Figma URL (component/frame/page)
- Component name/path (where to implement)
- Target breakpoints (or auto-detect from Figma)

**Critical:** This phase extracts **ALL breakpoints** (mobile, tablet, desktop, wide) from Figma to ensure complete responsive coverage. The skill uses a mobile-first approach by default.

**Process:**

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

**Output File:** `design-specs.json`

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

---

### Phase 2: Design System Detection & Mapping

**Process:**

1. Auto-detect project's design system:

    ```typescript
    // Priority order:
    1. Check for tailwind.config.{js,ts,mjs}
    2. Check for styled-components in package.json
    3. Check for @emotion in package.json
    4. Check for design-tokens.json or tokens.ts
    5. Check for CSS variables in :root
    6. Fall back to vanilla CSS
    ```

2. Load appropriate adapter:
    - `TailwindAdapter`: Maps to Tailwind classes and config
    - `StyledComponentsAdapter`: Maps to theme tokens
    - `CustomTokenAdapter`: Maps to custom design tokens
    - `VanillaCSSAdapter`: Generates CSS custom properties

3. Map Figma specs to design system tokens:
    - **Exact matches**: Figma variable "primary-500" → Tailwind "bg-primary-500"
    - **Fuzzy matches**: Figma "#3B82F6" → Tailwind "bg-blue-500" (closest match)
    - **No match**: Flag as custom value, suggest adding to design system
4. Detect inconsistencies:
    - Colors not in design system
    - Spacing values not on the scale (e.g., 17px when scale is 4px based)
    - Font sizes not in typography scale
    - Suggest design system additions or Figma adjustments

**Output File:** `design-system-mapping.json`

```json
{
	"detectedSystem": "tailwind",
	"configPath": "tailwind.config.ts",
	"mappings": {
		"colors": {
			"figma.primary-500": "blue-500",
			"figma.#3B82F6": "blue-500"
		},
		"spacing": {
			"figma.spacing-4": "4",
			"figma.16px": "4"
		}
	},
	"warnings": [
		{
			"type": "color-not-in-system",
			"figmaValue": "#FF5733",
			"suggestion": "Add to tailwind.config.ts as 'brand-orange'"
		}
	]
}
```

---

### Phase 3: Responsive Code Generation

**Critical:** Code generation follows **mobile-first approach** by default:

- Base styles = mobile breakpoint
- Responsive overrides for larger screens using breakpoint prefixes
- Order: mobile (base) → tablet → desktop → wide

**Process:**

1. **Start with mobile/base breakpoint** as foundation (mobile-first)
2. Determine responsive strategy based on design specs:

    ```typescript
    if (smoothScalingBetweenBreakpoints) {
    	strategy = 'fluid'; // clamp(), calc()
    } else if (componentLevelResponsive) {
    	strategy = 'container-query'; // @container
    } else {
    	strategy = 'media-query'; // @media (mobile-first)
    }
    ```

3. Generate component code using design system tokens:
    - **Tailwind**: Generate class strings with breakpoint prefixes (mobile-first)
    - **Styled Components**: Generate styled component with theme tokens and media queries
    - **Vanilla CSS**: Generate CSS with custom properties and media queries

4. **Apply mobile-first responsive approach:**

    ```tsx
    // Tailwind Example (mobile-first):
    // Base = mobile, then tablet/desktop overrides
    <div className="
      flex flex-col gap-[28px] w-full max-w-[351px]
      md:flex-row md:gap-[8.512px] md:max-w-none
      lg:gap-8 lg:p-8
    ">

    // Styled Components Example (mobile-first):
    const Container = styled.div`
      /* Mobile base styles */
      display: flex;
      flex-direction: column;
      gap: ${props => props.theme.spacing[7]};

      /* Tablet overrides (min-width approach = mobile-first) */
      @media (min-width: ${props => props.theme.breakpoints.tablet}) {
        flex-direction: row;
        gap: ${props => props.theme.spacing[2]};
      }

      /* Desktop overrides */
      @media (min-width: ${props => props.theme.breakpoints.desktop}) {
        gap: ${props => props.theme.spacing[8]};
      }
    `

    // Fluid Example (smooth scaling between breakpoints):
    font-size: clamp(1rem, 0.875rem + 0.5vw, 1.25rem);
    gap: clamp(16px, 4vw, 32px);
    ```

5. Handle edge cases:
    - Arbitrary values when exact token doesn't exist: `gap-[8.512px]`
    - Complex calculations: `calc(100% - ${spacing.4})`
    - Browser compatibility fallbacks

**Output File:** Component code file (e.g., `UserCard.tsx`)

---

### Phase 4: Playwright Validation

**Process:**

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

**Output File:** `validation-results.json`

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

---

### Phase 5: Fix Generation & Self-Healing Loop

**Process:**

1. Analyze validation failures:
    - Categorize: critical vs acceptable
    - Identify root cause: code error vs browser limitation vs design mismatch

2. Generate fix suggestions:

    ```typescript
    const fixes = [
    	{
    		type: 'code-adjustment',
    		property: 'gap',
    		current: 'gap-[8px]',
    		suggested: 'gap-[8.512px]',
    		reason: 'Exact Figma value',
    		confidence: 'high',
    	},
    	{
    		type: 'tolerance-adjustment',
    		property: 'width',
    		expected: '351px',
    		actual: '350.8px',
    		action: 'accept',
    		reason: 'Sub-pixel rendering, within ±1px tolerance',
    	},
    	{
    		type: 'design-system-update',
    		property: 'color',
    		figmaValue: '#FF5733',
    		action: 'Add to tailwind.config.ts as custom color',
    		confidence: 'medium',
    	},
    ];
    ```

3. Auto-apply fixes (with approval):
    - Present fix suggestions to user
    - Apply approved fixes
    - Re-run validation
    - Repeat until all critical issues resolved or max iterations (3)

4. Handle impossible-to-match scenarios:

    ```markdown
    ## Validation Limitation Detected

    **Property:** width
    **Expected:** 351px (Figma)
    **Actual:** 340px
    **Reason:** Parent container has `max-width: 340px` constraint

    **Options:**

    1. Adjust parent container width (may affect other components)
    2. Mark as acceptable deviation (document in design-validation.md)
    3. Consult designer to adjust Figma to match implementation constraints
    ```

**Output File:** `validation-report.md`

```markdown
# Design Validation Report: UserCard

**Component:** UserCard
**Figma URL:** [View in Figma](https://figma.com/...)
**Validation Date:** 2026-05-23 10:45:00
**Status:** ✅ PASSED (with acceptable deviations)

## Summary

- **Total Tests:** 12
- **Passed:** 10
- **Failed (Critical):** 0
- **Failed (Acceptable):** 2

## Breakpoint Results

### ✅ Desktop (1440px)

All properties match Figma specs perfectly.

### ✅ Tablet (768px)

Minor deviation in gap property (8px vs 8.512px) - within sub-pixel tolerance.

### ✅ Mobile (375px)

All properties match.

## Acceptable Deviations

1. **Gap at tablet breakpoint**
    - Expected: 8.512px
    - Actual: 8px
    - Reason: Browser sub-pixel rounding
    - Impact: Negligible visual difference

## Applied Fixes

1. Changed `gap-2` to `gap-[8.512px]` for exact match
2. Added `max-w-[351px]` to match Figma container width

## Design System Updates Suggested

None

## Next Steps

- [ ] Review acceptable deviations with designer (optional)
- [ ] Merge component implementation
- [ ] Delete validation test file (temporary validation only)
```

---

## Integration with Workflows

### Feature Workflow Integration

```yaml
# Phase 7: Implementation
frontend-implementation:
    - Check if task involves UI components
    - If yes:
          - Ask for Figma URL (if not already provided)
          - Invoke design-implementation-validator skill
          - Wait for validation report
          - Review acceptable deviations
          - Proceed only after validation passes
```

### Improvement Workflow Integration

```yaml
# Phase 3/4: Implementation
ui-update-check:
    - If component exists and has Figma link in comments/docs:
          - Ask: 'Should I validate against Figma design?'
          - Default: Yes (unless user opts out)
          - Invoke design-implementation-validator skill
```

---

## Usage Examples

### Example 1: New Component

```bash
# User in workflow:
"Implement the UserCard component from Figma: https://figma.com/file/abc123/..."

# Skill automatically:
1. Extracts Figma specs (mobile/tablet/desktop)
2. Detects Tailwind in repo
3. Generates UserCard.tsx with responsive Tailwind classes
4. Starts dev server
5. Runs Playwright validation
6. Reports: ✅ All breakpoints match perfectly
```

### Example 2: Update with Deviation

```bash
# User:
"Update the Header component to match the new design"

# Skill:
1. Detects Figma URL in Header.tsx comments
2. Extracts updated specs
3. Identifies changes: spacing, color
4. Updates code
5. Validation finds: width doesn't match due to parent constraint
6. Flags as impossible-to-match
7. User reviews and approves acceptable deviation
```

---

## Configuration

### Skill Config File (Optional)

Create `.design-validation.config.js` in project root:

```javascript
module.exports = {
	// Design system
	designSystem: 'tailwind', // auto-detect if omitted

	// Breakpoints
	breakpoints: {
		mobile: { width: 375, height: 667 },
		tablet: { width: 768, height: 1024 },
		desktop: { width: 1440, height: 900 },
	},

	// Validation strictness
	tolerance: {
		spacing: 1, // ±1px
		colors: 0, // exact match
		typography: 1,
	},

	// Auto-fix settings
	autoFix: {
		enabled: true,
		requireApproval: true,
		maxIterations: 3,
	},

	// Dev server
	devServer: {
		command: 'npm run dev',
		url: 'http://localhost:3000',
		readyPattern: 'ready in',
	},

	// Responsive approach
	responsiveStrategy: 'mobile-first', // or 'desktop-first' (not recommended)

	// Breakpoints (auto-detected from Figma by default)
	breakpoints: {
		mobile: { width: 375, height: 667 },
		tablet: { width: 768, height: 1024 },
		desktop: { width: 1440, height: 900 },
	},

	// Test output
	validationTests: {
		location: '.ai-workflow/[feature]/',
		keepAfterValidation: false, // delete test files after validation
	},
};
```

---

## MCP Dependencies

This skill requires:

1. **Figma MCP** - For design extraction
    - Tools: `figma-read-file`, `figma-get-component`, `figma-get-variables`

2. **Playwright MCP** - For validation
    - Tools: `playwright-run-test`, `playwright-screenshot`

3. **Browser MCP (optional)** - For visual comparison
    - Tools: `browser-screenshot`, `browser-navigate`

---

## Design System Adapters

### Tailwind Adapter

**Detects:**

- `tailwind.config.{js,ts,mjs,cjs}`
- `@tailwindcss/` in package.json

**Maps:**

- Colors → `bg-{color}`, `text-{color}`, `border-{color}`
- Spacing → `p-{size}`, `m-{size}`, `gap-{size}`
- Typography → `text-{size}`, `font-{weight}`
- Arbitrary values → `gap-[8.512px]`
- Responsive → `md:`, `lg:`, `xl:` prefixes

**Config parsing:**

```typescript
const config = require('./tailwind.config.js');
const theme = config.theme.extend || config.theme;

// Map Figma spacing to Tailwind scale
const spacing = theme.spacing;
// e.g., 16px → spacing[4] → class "gap-4"
```

---

### Styled Components Adapter

**Detects:**

- `styled-components` in package.json
- `import styled from 'styled-components'` in files

**Maps:**

- Theme tokens → `${props => props.theme.colors.primary}`
- Spacing → `${props => props.theme.spacing[4]}`
- Breakpoints → `@media (min-width: ${props => props.theme.breakpoints.md})`

**Example output:**

```typescript
const UserCard = styled.div`
	display: flex;
	flex-direction: column;
	gap: ${(props) => props.theme.spacing[7]};
	width: 100%;
	max-width: 351px;

	@media (min-width: ${(props) => props.theme.breakpoints.tablet}) {
		flex-direction: row;
		gap: 8.512px; // No exact token, use literal
		max-width: none;
	}
`;
```

---

### Extensibility

To add a new design system adapter:

1. Create `adapters/[system]-adapter.ts`
2. Implement `DesignSystemAdapter` interface:
    ```typescript
    interface DesignSystemAdapter {
    	name: string;
    	detect(): Promise<boolean>;
    	loadConfig(): Promise<DesignSystemConfig>;
    	mapColor(figmaColor: string): string;
    	mapSpacing(figmaSpacing: number): string;
    	mapTypography(figmaTypography: TypographySpec): string;
    	generateCode(specs: ComponentSpecs): string;
    }
    ```
3. Register in `adapters/index.ts`

---

## Limitations & Future Enhancements

### Current Limitations

1. **Complex Animations**: Doesn't validate transitions/animations yet
2. **Pseudo-elements**: ::before, ::after validation limited
3. **Dynamic Content**: Can't validate components with dynamic data without mocks
4. **Cross-browser**: Validates in Chromium only (Playwright default)

### Planned Enhancements

1. **Animation Validation**: Record and compare animation timings
2. **Interaction States**: Validate hover, focus, active states
3. **Accessibility**: Auto-check color contrast, focus indicators
4. **Design Token Sync**: Bi-directional sync between Figma Variables and code
5. **Multi-browser**: Validate in Chrome, Firefox, Safari
6. **Component Library**: Validate entire component library in one run

---

## Error Handling

### Common Issues

**Issue:** Figma URL not accessible

```
Solution: Check Figma MCP authentication, verify URL permissions
```

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

---

## Best Practices

1. **Figma Organization**:
    - Use Figma Variables for consistency
    - Name components clearly (matches code component names)
    - Define all breakpoint variants explicitly
    - Document responsive behavior in Figma

2. **Code Organization**:
    - Add Figma URL as comment in component file
    - Use `data-testid` attributes for Playwright selectors
    - Keep design system config in sync with Figma

3. **Validation Workflow**:
    - Run validation before code review
    - Document acceptable deviations
    - Update Figma when implementation constraints discovered
    - Delete temporary validation tests after approval

4. **Team Collaboration**:
    - Share validation reports with designers
    - Use reports to identify design system gaps
    - Establish tolerance guidelines as a team

---

## Output Artifacts

All artifacts stored in `.ai-workflow/[feature]/design-validation/`:

```
.ai-workflow/user-card-component/design-validation/
├── design-specs.json                    # Extracted Figma specs
├── design-system-mapping.json           # Figma → Design system mappings
├── validation-results.json              # Test results data
├── validation-report.md                 # Human-readable report
├── design-validation.spec.ts            # Playwright test (temp)
└── screenshots/                         # Visual regression (optional)
    ├── desktop-baseline.png
    ├── tablet-baseline.png
    └── mobile-baseline.png
```

---

## Success Criteria

This skill is successful when:

✅ Figma specs are accurately extracted across all breakpoints  
✅ Design system mappings are correct (no hallucinated tokens)  
✅ Generated code is idiomatic for the detected design system  
✅ Validation catches mismatches before code review  
✅ Fix suggestions are actionable and accurate  
✅ Acceptable deviations are properly documented  
✅ Designer-developer handoff friction is minimized

---

## Invocation Template

```markdown
@design-implementation-validator

**Component:** UserCard
**Figma URL:** https://figma.com/file/abc123/design?node-id=123-456
**Component Path:** src/components/UserCard.tsx
**Breakpoints:** mobile, tablet, desktop (or auto-detect)
**Design System:** tailwind (or auto-detect)
**Strict Mode:** false (allow acceptable deviations)

Please validate that the implementation matches the Figma design.
```

---

## Related Skills

- `frontend-engineer.agent.md` - Often invokes this skill
- `minimal-impl-generator` - Generates implementation, this validates it
- `refactor-optimizer` - May run after validation passes
- `code-reviewer` - Final review after design validation
