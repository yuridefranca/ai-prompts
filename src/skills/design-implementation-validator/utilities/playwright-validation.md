# Playwright Validation System

Automated validation of component implementations against Figma designs using Playwright.

## Overview

This system validates that rendered components match Figma specifications **at ALL breakpoints** (mobile, tablet, desktop, wide) by:
1. Starting/connecting to dev server
2. Navigating to component in browser
3. Setting viewport size for each breakpoint (mobile-first order)
4. Measuring computed CSS values at each breakpoint
5. Comparing with Figma specs using smart tolerance
6. Taking screenshots for visual regression (optional)
7. Generating detailed validation reports with per-breakpoint results

**Critical:** Tests run for EVERY breakpoint extracted from Figma, ensuring complete responsive coverage following mobile-first principles.

## Prerequisites

```typescript
// Load Playwright MCP tools
await tool_search("playwright");

// Available tools:
// - playwright-run-test: Run Playwright test file
// - playwright-screenshot: Take screenshots
// - playwright-evaluate: Execute JavaScript in browser context
```

## Core Validation Functions

### validateImplementation()

Main entry point for validation.

```typescript
async function validateImplementation(
  componentPath: string,
  figmaSpecs: ComponentSpecs,
  options?: ValidationOptions
): Promise<ValidationReport> {
  // 1. Ensure dev server is running
  const serverInfo = await ensureDevServer(options?.devServer);
  
  // 2. Generate Playwright test file
  const testFile = await generateValidationTest(componentPath, figmaSpecs, options);
  
  // 3. Run Playwright tests
  const testResults = await runPlaywrightTests(testFile);
  
  // 4. Analyze results with smart tolerance
  const analysis = await analyzeResults(testResults, figmaSpecs, options);
  
  // 5. Optional: Take screenshots for visual regression
  const screenshots = options?.visualRegression 
    ? await captureScreenshots(componentPath, figmaSpecs.breakpoints)
    : undefined;
  
  // 6. Generate validation report
  return generateValidationReport({
    componentPath,
    figmaSpecs,
    testResults,
    analysis,
    screenshots,
    serverInfo,
  });
}

interface ValidationOptions {
  /** Dev server configuration */
  devServer?: DevServerConfig;
  
  /** Tolerance settings */
  tolerance?: ToleranceConfig;
  
  /** Visual regression testing */
  visualRegression?: boolean;
  
  /** Compare screenshots with baselines */
  compareBaselines?: boolean;
  
  /** Breakpoints to validate (default: all) */
  breakpoints?: string[];
  
  /** Test location */
  testOutputDir?: string;
  
  /** Keep test files after validation */
  keepTestFiles?: boolean;
}

interface ToleranceConfig {
  /** Spacing tolerance in pixels (default: 1) */
  spacing: number;
  
  /** Color tolerance (0-255, default: 0 for exact match) */
  color: number;
  
  /** Typography tolerance in pixels (default: 1) */
  typography: number;
  
  /** Allow acceptable deviations based on context */
  contextAware: boolean;
}
```

### ensureDevServer()

Ensures development server is running.

```typescript
async function ensureDevServer(
  config?: DevServerConfig
): Promise<ServerInfo> {
  // 1. Try to connect to existing server
  const existingServer = await checkServerRunning(config?.url);
  if (existingServer) {
    return existingServer;
  }
  
  // 2. Detect dev server command
  const command = config?.command || await detectDevCommand();
  
  // 3. Start dev server
  console.log(`Starting dev server: ${command}`);
  const terminal = await run_in_terminal({
    command,
    goal: 'Start development server',
    explanation: 'Starting dev server for component validation',
    mode: 'async',
  });
  
  // 4. Wait for server to be ready
  const serverInfo = await waitForServer({
    url: config?.url || 'http://localhost:3000',
    readyPattern: config?.readyPattern || /ready|compiled|started/i,
    timeout: 60000,
    terminalId: terminal.id,
  });
  
  return serverInfo;
}

async function detectDevCommand(): Promise<string> {
  // Check package.json scripts
  const packageJson = await readJSON('package.json');
  const scripts = packageJson.scripts || {};
  
  if (scripts.dev) return 'npm run dev';
  if (scripts.start) return 'npm start';
  if (scripts['dev:vite']) return 'npm run dev:vite';
  
  // Check for common frameworks
  if (packageJson.dependencies?.next || packageJson.devDependencies?.next) {
    return 'npm run dev'; // Next.js
  }
  
  if (packageJson.dependencies?.vite || packageJson.devDependencies?.vite) {
    return 'vite'; // Vite
  }
  
  throw new Error('Cannot detect dev server command. Please specify in config.');
}

async function waitForServer(options: WaitOptions): Promise<ServerInfo> {
  const startTime = Date.now();
  
  while (Date.now() - startTime < options.timeout) {
    // Check if server is responding
    try {
      const response = await fetch(options.url);
      if (response.ok) {
        return {
          url: options.url,
          ready: true,
          startTime,
        };
      }
    } catch (error) {
      // Server not ready yet, continue waiting
    }
    
    // Check terminal output for ready pattern
    if (options.terminalId) {
      const output = await get_terminal_output({ id: options.terminalId });
      if (options.readyPattern.test(output)) {
        return {
          url: options.url,
          ready: true,
          startTime,
        };
      }
    }
    
    await sleep(500);
  }
  
  throw new Error(`Server did not start within ${options.timeout}ms`);
}
```

### generateValidationTest()

Generates Playwright test file for validation.

```typescript
async function generateValidationTest(
  componentPath: string,
  figmaSpecs: ComponentSpecs,
  options?: ValidationOptions
): Promise<string> {
  const testCode = `
import { test, expect } from '@playwright/test';

/**
 * Design Validation Test
 * Component: ${figmaSpecs.name}
 * Figma: ${figmaSpecs.figmaUrl}
 * Generated: ${new Date().toISOString()}
 */

${generateBreakpointTests(componentPath, figmaSpecs, options)}

${generateInteractionTests(componentPath, figmaSpecs, options)}
`;

  const testFile = options?.testOutputDir 
    ? `${options.testOutputDir}/design-validation.spec.ts`
    : '.ai-workflow/design-validation.spec.ts';
  
  await create_file({
    filePath: testFile,
    content: testCode,
  });
  
  return testFile;
}

function generateBreakpointTests(
  componentPath: string,
  figmaSpecs: ComponentSpecs,
  options?: ValidationOptions
): string {
  const breakpointsToTest = options?.breakpoints 
    ? Object.entries(figmaSpecs.breakpoints).filter(([name]) => options.breakpoints!.includes(name))
    : Object.entries(figmaSpecs.breakpoints);
  
  return breakpointsToTest.map(([breakpoint, specs]) => `
test.describe('${figmaSpecs.name} - ${breakpoint}', () => {
  test('matches Figma layout specs', async ({ page }) => {
    // Set viewport
    await page.setViewportSize(${JSON.stringify(getViewportSize(breakpoint))});
    
    // Navigate to component
    await page.goto('${getComponentUrl(componentPath)}');
    
    // Wait for component to render
    await page.waitForSelector('[data-testid="${figmaSpecs.name.toLowerCase()}"]');
    
    // Get component element
    const element = page.locator('[data-testid="${figmaSpecs.name.toLowerCase()}"]');
    
    // Extract computed styles
    const styles = await element.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        display: computed.display,
        flexDirection: computed.flexDirection,
        alignItems: computed.alignItems,
        justifyContent: computed.justifyContent,
        gap: computed.gap,
        padding: computed.padding,
        paddingTop: computed.paddingTop,
        paddingRight: computed.paddingRight,
        paddingBottom: computed.paddingBottom,
        paddingLeft: computed.paddingLeft,
        width: computed.width,
        maxWidth: computed.maxWidth,
        backgroundColor: computed.backgroundColor,
        color: computed.color,
        borderColor: computed.borderColor,
        borderRadius: computed.borderRadius,
        boxShadow: computed.boxShadow,
        fontSize: computed.fontSize,
        fontWeight: computed.fontWeight,
        fontFamily: computed.fontFamily,
        lineHeight: computed.lineHeight,
        letterSpacing: computed.letterSpacing,
      };
    });
    
    // Validate layout
    ${generateLayoutAssertions(specs.layout)}
    
    // Validate spacing
    ${generateSpacingAssertions(specs.spacing, options)}
    
    // Validate sizing
    ${generateSizingAssertions(specs.sizing, options)}
    
    // Validate colors
    ${generateColorAssertions(specs.colors, options)}
    
    // Validate typography
    ${specs.typography ? generateTypographyAssertions(specs.typography, options) : ''}
    
    // Validate effects
    ${generateEffectAssertions(specs.effects, options)}
  });
});
`).join('\n');
}

function generateLayoutAssertions(layout: LayoutSpecs): string {
  const assertions: string[] = [];
  
  if (layout.display) {
    assertions.push(`expect(styles.display).toBe('${layout.display}');`);
  }
  
  if (layout.flexDirection) {
    assertions.push(`expect(styles.flexDirection).toBe('${layout.flexDirection}');`);
  }
  
  if (layout.alignItems) {
    assertions.push(`expect(styles.alignItems).toBe('${layout.alignItems}');`);
  }
  
  if (layout.justifyContent) {
    assertions.push(`expect(styles.justifyContent).toBe('${layout.justifyContent}');`);
  }
  
  return assertions.join('\n    ');
}

function generateSpacingAssertions(
  spacing: SpacingSpecs,
  options?: ValidationOptions
): string {
  const tolerance = options?.tolerance?.spacing || 1;
  const assertions: string[] = [];
  
  if (spacing.gap !== undefined) {
    assertions.push(`
    // Gap with ±${tolerance}px tolerance
    const gapValue = parseFloat(styles.gap);
    expect(gapValue).toBeGreaterThanOrEqual(${spacing.gap - tolerance});
    expect(gapValue).toBeLessThanOrEqual(${spacing.gap + tolerance});
    `);
  }
  
  if (spacing.padding !== undefined) {
    assertions.push(`
    // Padding with ±${tolerance}px tolerance
    const paddingValue = parseFloat(styles.padding);
    expect(paddingValue).toBeGreaterThanOrEqual(${spacing.padding - tolerance});
    expect(paddingValue).toBeLessThanOrEqual(${spacing.padding + tolerance});
    `);
  }
  
  return assertions.join('\n    ');
}

function generateColorAssertions(
  colors: ColorSpecs,
  options?: ValidationOptions
): string {
  const assertions: string[] = [];
  
  if (colors.background) {
    assertions.push(`
    // Background color
    const bgColor = rgbToHex(styles.backgroundColor);
    expect(bgColor).toBe('${normalizeColor(colors.background)}');
    `);
  }
  
  if (colors.color) {
    assertions.push(`
    // Text color
    const textColor = rgbToHex(styles.color);
    expect(textColor).toBe('${normalizeColor(colors.color)}');
    `);
  }
  
  return assertions.join('\n    ');
}

function generateInteractionTests(
  componentPath: string,
  figmaSpecs: ComponentSpecs,
  options?: ValidationOptions
): string {
  if (!figmaSpecs.states) return '';
  
  return Object.entries(figmaSpecs.states).map(([state, specs]) => `
test.describe('${figmaSpecs.name} - ${state} state', () => {
  test('matches Figma ${state} specs', async ({ page }) => {
    await page.goto('${getComponentUrl(componentPath)}');
    const element = page.locator('[data-testid="${figmaSpecs.name.toLowerCase()}"]');
    
    // Trigger ${state} state
    ${generateStateTrigger(state)}
    
    // Wait for transition
    await page.waitForTimeout(300);
    
    // Extract computed styles
    const styles = await element.evaluate((el) => {
      const computed = window.getComputedStyle(el);
      return {
        boxShadow: computed.boxShadow,
        backgroundColor: computed.backgroundColor,
        transform: computed.transform,
        opacity: computed.opacity,
      };
    });
    
    // Validate state styles
    ${specs.effects?.boxShadow ? `expect(styles.boxShadow).toBe('${specs.effects.boxShadow}');` : ''}
  });
});
`).join('\n');
}

function generateStateTrigger(state: string): string {
  switch (state) {
    case 'hover':
      return 'await element.hover();';
    case 'focus':
      return 'await element.focus();';
    case 'active':
      return 'await element.click({ delay: 100 });';
    default:
      return '';
  }
}
```

### analyzeResults()

Analyzes test results with smart tolerance.

```typescript
async function analyzeResults(
  testResults: PlaywrightResults,
  figmaSpecs: ComponentSpecs,
  options?: ValidationOptions
): Promise<ValidationAnalysis> {
  const analysis: ValidationAnalysis = {
    status: 'pass',
    passedTests: 0,
    failedTests: 0,
    criticalFailures: [],
    acceptableDeviations: [],
    breakdownByBreakpoint: {},
  };
  
  for (const [breakpoint, result] of Object.entries(testResults.breakpoints)) {
    const breakpointAnalysis = analyzeBreakpoint(
      result,
      figmaSpecs.breakpoints[breakpoint],
      options
    );
    
    analysis.breakdownByBreakpoint[breakpoint] = breakpointAnalysis;
    analysis.passedTests += breakpointAnalysis.passed;
    analysis.failedTests += breakpointAnalysis.failed;
    
    // Categorize failures
    for (const failure of breakpointAnalysis.failures) {
      if (isAcceptableDeviation(failure, options)) {
        analysis.acceptableDeviations.push({
          breakpoint,
          ...failure,
        });
      } else {
        analysis.criticalFailures.push({
          breakpoint,
          ...failure,
        });
      }
    }
  }
  
  // Overall status
  if (analysis.criticalFailures.length > 0) {
    analysis.status = 'fail';
  } else if (analysis.acceptableDeviations.length > 0) {
    analysis.status = 'partial-pass';
  }
  
  return analysis;
}

function isAcceptableDeviation(
  failure: TestFailure,
  options?: ValidationOptions
): boolean {
  const tolerance = options?.tolerance || { spacing: 1, color: 0, typography: 1 };
  
  // Sub-pixel rendering tolerance
  if (failure.category === 'spacing') {
    const diff = Math.abs(failure.actual - failure.expected);
    if (diff <= tolerance.spacing) {
      failure.reason = 'Browser sub-pixel rounding';
      return true;
    }
  }
  
  // Typography rendering differences
  if (failure.category === 'typography') {
    const diff = Math.abs(failure.actual - failure.expected);
    if (diff <= tolerance.typography) {
      failure.reason = 'Font rendering variance';
      return true;
    }
  }
  
  // Context-aware tolerance
  if (options?.tolerance?.contextAware) {
    return isContextuallyAcceptable(failure);
  }
  
  return false;
}

function isContextuallyAcceptable(failure: TestFailure): boolean {
  // Parent constraint makes exact match impossible
  if (failure.property === 'width' && failure.actual < failure.expected) {
    failure.reason = 'Constrained by parent container width';
    failure.recommendation = 'Verify parent container constraints match design intent';
    return true;
  }
  
  // Height affected by content
  if (failure.property === 'height' && failure.actual > failure.expected) {
    failure.reason = 'Height expanded by content';
    failure.recommendation = 'Check if min-height constraint is appropriate';
    return true;
  }
  
  // Inherited font affecting line height
  if (failure.property === 'lineHeight' && failure.inheritedValue !== failure.expected) {
    failure.reason = 'Inherited from parent styles';
    failure.recommendation = 'Explicitly set line-height on component';
    return true;
  }
  
  return false;
}
```

### generateValidationReport()

Generates comprehensive validation report.

```typescript
function generateValidationReport(data: ReportData): ValidationReport {
  const { componentPath, figmaSpecs, testResults, analysis, screenshots } = data;
  
  const report: ValidationReport = {
    component: figmaSpecs.name,
    componentPath,
    figmaUrl: figmaSpecs.figmaUrl,
    validationDate: new Date().toISOString(),
    status: analysis.status,
    summary: {
      totalTests: analysis.passedTests + analysis.failedTests,
      passed: analysis.passedTests,
      failed: analysis.failedTests,
      criticalFailures: analysis.criticalFailures.length,
      acceptableDeviations: analysis.acceptableDeviations.length,
    },
    breakpoints: analysis.breakdownByBreakpoint,
    criticalFailures: analysis.criticalFailures,
    acceptableDeviations: analysis.acceptableDeviations,
    screenshots: screenshots || [],
    recommendations: generateRecommendations(analysis),
  };
  
  return report;
}

function generateRecommendations(analysis: ValidationAnalysis): string[] {
  const recommendations: string[] = [];
  
  // Critical failures
  if (analysis.criticalFailures.length > 0) {
    recommendations.push('❌ Fix critical failures before merging');
    
    // Group by category
    const byCategory = groupBy(analysis.criticalFailures, 'category');
    
    if (byCategory.spacing) {
      recommendations.push(`  - Review spacing values (${byCategory.spacing.length} issues)`);
    }
    if (byCategory.colors) {
      recommendations.push(`  - Verify color mappings (${byCategory.colors.length} issues)`);
    }
  }
  
  // Acceptable deviations
  if (analysis.acceptableDeviations.length > 0) {
    recommendations.push(`ℹ️  ${analysis.acceptableDeviations.length} acceptable deviation(s) detected:`);
    
    for (const deviation of analysis.acceptableDeviations.slice(0, 3)) {
      recommendations.push(`  - ${deviation.property}: ${deviation.reason}`);
    }
    
    if (analysis.acceptableDeviations.length > 3) {
      recommendations.push(`  - ...and ${analysis.acceptableDeviations.length - 3} more`);
    }
  }
  
  // Design system updates
  if (analysis.suggestDesignSystemUpdates) {
    recommendations.push('💡 Consider updating design system:');
    for (const suggestion of analysis.designSystemSuggestions) {
      recommendations.push(`  - ${suggestion}`);
    }
  }
  
  return recommendations;
}
```

## Visual Regression Testing

```typescript
async function captureScreenshots(
  componentPath: string,
  breakpoints: Record<string, BreakpointSpecs>
): Promise<Screenshot[]> {
  const screenshots: Screenshot[] = [];
  
  for (const [breakpoint, specs] of Object.entries(breakpoints)) {
    const viewport = getViewportSize(breakpoint);
    
    const screenshot = await playwright_screenshot({
      url: getComponentUrl(componentPath),
      selector: `[data-testid="${componentPath}"]`,
      viewport,
      path: `.ai-workflow/screenshots/${breakpoint}.png`,
    });
    
    screenshots.push({
      breakpoint,
      path: screenshot.path,
      viewport,
    });
  }
  
  return screenshots;
}

async function compareWithBaselines(
  screenshots: Screenshot[],
  baselinePath: string
): Promise<VisualDiff[]> {
  const diffs: VisualDiff[] = [];
  
  for (const screenshot of screenshots) {
    const baseline = `${baselinePath}/${screenshot.breakpoint}.png`;
    
    if (await fileExists(baseline)) {
      const diff = await compareImages(screenshot.path, baseline);
      
      if (diff.percentageDifferent > 0.1) { // 0.1% threshold
        diffs.push({
          breakpoint: screenshot.breakpoint,
          current: screenshot.path,
          baseline,
          diff: diff.diffPath,
          percentage: diff.percentageDifferent,
        });
      }
    }
  }
  
  return diffs;
}
```

## Utility Functions

```typescript
function getViewportSize(breakpoint: string): { width: number; height: number } {
  const viewports = {
    mobile: { width: 375, height: 667 },
    tablet: { width: 768, height: 1024 },
    desktop: { width: 1440, height: 900 },
    wide: { width: 1920, height: 1080 },
  };
  
  return viewports[breakpoint] || viewports.desktop;
}

function getComponentUrl(componentPath: string): string {
  // Detect component URL strategy
  // - Storybook: http://localhost:6006/?path=/story/components-usercard
  // - Direct: http://localhost:3000/components/user-card
  // - Test page: http://localhost:3000/test-components/user-card
  
  // This should be configurable or auto-detected
  return `http://localhost:3000/components/${kebabCase(componentPath)}`;
}

function parsePixels(value: string): number {
  return parseFloat(value.replace('px', ''));
}

function rgbToHex(rgb: string): string {
  // Convert "rgb(59, 130, 246)" to "#3B82F6"
  const match = rgb.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  if (!match) return rgb;
  
  const [, r, g, b] = match;
  return `#${[r, g, b]
    .map(x => parseInt(x).toString(16).padStart(2, '0'))
    .join('')
    .toUpperCase()}`;
}

function normalizeColor(color: string): string {
  // Handle semantic names, hex, rgb
  if (color.startsWith('#')) {
    return color.toUpperCase();
  }
  
  // For semantic names, this would need to resolve from theme
  // For now, return as-is
  return color;
}
```

## Best Practices

1. **Add data-testid attributes** to components for reliable selectors
2. **Use smart tolerance** - don't fail on sub-pixel differences
3. **Test in multiple browsers** if cross-browser consistency is critical
4. **Keep test files temporary** - delete after validation passes
5. **Document acceptable deviations** for future reference
6. **Screenshot at key breakpoints** for visual verification
7. **Handle async rendering** - wait for components to fully render
8. **Test interaction states** (hover, focus) separately
9. **Consider dynamic content** - use fixtures for consistent validation
10. **Fail fast on critical issues** - don't waste time on minor issues if major ones exist
