# Base Design System Adapter Interface

All design system adapters must implement this interface to ensure consistent behavior across different frameworks.

## Interface Definition

```typescript
interface DesignSystemAdapter {
  /**
   * Unique identifier for this adapter
   */
  name: string;
  
  /**
   * Framework/library this adapter supports
   */
  framework: string;
  
  /**
   * Detect if this design system is used in the current project
   * @returns Promise<boolean> - true if detected
   */
  detect(): Promise<boolean>;
  
  /**
   * Load and parse the design system configuration
   * @returns Promise<DesignSystemConfig> - parsed config object
   */
  loadConfig(): Promise<DesignSystemConfig>;
  
  /**
   * Map Figma color to design system token/class
   * @param figmaColor - Color from Figma (hex, rgb, or variable name)
   * @param context - Where the color is used (background, text, border, etc.)
   * @returns string - Design system token/class
   */
  mapColor(figmaColor: string, context: ColorContext): MappingResult;
  
  /**
   * Map Figma spacing to design system token/class
   * @param figmaSpacing - Spacing value in pixels
   * @param context - Where spacing is used (padding, margin, gap, etc.)
   * @returns string - Design system token/class
   */
  mapSpacing(figmaSpacing: number, context: SpacingContext): MappingResult;
  
  /**
   * Map Figma typography to design system token/class
   * @param figmaTypography - Typography specs from Figma
   * @returns string - Design system token/class
   */
  mapTypography(figmaTypography: TypographySpec): MappingResult;
  
  /**
   * Map Figma shadow to design system token/class
   * @param figmaShadow - Shadow/elevation from Figma
   * @returns string - Design system token/class
   */
  mapShadow(figmaShadow: ShadowSpec): MappingResult;
  
  /**
   * Map Figma border radius to design system token/class
   * @param figmaRadius - Border radius value
   * @returns string - Design system token/class
   */
  mapBorderRadius(figmaRadius: number): MappingResult;
  
  /**
   * Generate responsive code from component specs
   * @param specs - Complete component specifications
   * @param options - Generation options (code style, formatting, etc.)
   * @returns string - Generated code
   */
  generateCode(specs: ComponentSpecs, options?: GenerationOptions): string;
  
  /**
   * Generate responsive breakpoint code
   * @param breakpoint - Breakpoint identifier (mobile, tablet, desktop)
   * @param styles - Styles to apply at this breakpoint
   * @returns string - Breakpoint-specific code
   */
  generateBreakpoint(breakpoint: string, styles: StyleMap): string;
  
  /**
   * Validate that generated code will produce expected styles
   * @param code - Generated code
   * @param expectedStyles - Expected computed styles
   * @returns ValidationResult - Validation outcome
   */
  validateCode(code: string, expectedStyles: ComputedStyles): ValidationResult;
}
```

## Type Definitions

```typescript
type ColorContext = 'background' | 'text' | 'border' | 'fill' | 'stroke';

type SpacingContext = 'padding' | 'margin' | 'gap' | 'width' | 'height';

interface MappingResult {
  /** The mapped token/class */
  value: string;
  
  /** Whether it's an exact match from design system */
  exactMatch: boolean;
  
  /** Confidence level (0-1) */
  confidence: number;
  
  /** Warning if any */
  warning?: string;
  
  /** Suggestion for design system update */
  suggestion?: string;
}

interface TypographySpec {
  fontFamily: string;
  fontSize: number;
  fontWeight: number | string;
  lineHeight: number | string;
  letterSpacing?: number;
}

interface ShadowSpec {
  x: number;
  y: number;
  blur: number;
  spread: number;
  color: string;
}

interface DesignSystemConfig {
  colors: Record<string, string>;
  spacing: Record<string, string>;
  typography: Record<string, TypographySpec>;
  shadows: Record<string, string>;
  borderRadius: Record<string, string>;
  breakpoints: Record<string, number>;
}

interface ComponentSpecs {
  name: string;
  breakpoints: Record<string, BreakpointSpecs>;
  states?: Record<string, StateSpecs>;
}

interface BreakpointSpecs {
  layout: LayoutSpecs;
  spacing: SpacingSpecs;
  typography: TypographySpec;
  colors: ColorSpecs;
  effects: EffectSpecs;
}

interface StyleMap {
  [property: string]: string | number;
}

interface ComputedStyles {
  [property: string]: string;
}

interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}

interface GenerationOptions {
  codeStyle?: 'compact' | 'readable';
  includeComments?: boolean;
  responsiveStrategy?: 'mobile-first' | 'desktop-first';
}
```

## Implementation Guidelines

### 1. Detection Method

The `detect()` method should check for:
- Config files in the project root
- Package dependencies
- Imports in source files
- Specific file patterns

**Example:**
```typescript
async detect(): Promise<boolean> {
  const checks = [
    fileExists('tailwind.config.js'),
    fileExists('tailwind.config.ts'),
    packageJsonContains('@tailwindcss/'),
  ];
  
  return checks.some(check => check === true);
}
```

### 2. Config Loading

Parse the design system configuration to extract all tokens.

**Example for Tailwind:**
```typescript
async loadConfig(): Promise<DesignSystemConfig> {
  const configPath = findConfig(['tailwind.config.ts', 'tailwind.config.js']);
  const config = await import(configPath);
  
  return {
    colors: extractColors(config.theme),
    spacing: extractSpacing(config.theme),
    typography: extractTypography(config.theme),
    // ...
  };
}
```

### 3. Mapping Strategy

**Priority order for mappings:**
1. **Exact variable name match**: Figma variable "primary-500" → exists in design system
2. **Exact value match**: Figma "#3B82F6" → matches design system color value
3. **Fuzzy match**: Find closest color using color distance algorithm
4. **Arbitrary value**: Use exact Figma value as fallback

**Return confidence scores:**
- Exact match: confidence = 1.0
- Fuzzy match: confidence = 0.7-0.9 (based on similarity)
- Arbitrary value: confidence = 0.5

### 4. Code Generation

Generate idiomatic code for each framework:

**Tailwind:**
```tsx
<div className="flex flex-col gap-4 p-6 bg-white rounded-lg">
```

**Styled Components:**
```tsx
const Card = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing[4]};
  padding: ${props => props.theme.spacing[6]};
  background: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.borderRadius.lg};
`;
```

### 5. Responsive Code

Each adapter handles breakpoints differently:

**Tailwind:** Use breakpoint prefixes
```tsx
<div className="flex-col md:flex-row gap-4 md:gap-6">
```

**Styled Components:** Use media queries
```tsx
const Card = styled.div`
  flex-direction: column;
  gap: ${props => props.theme.spacing[4]};
  
  @media (min-width: ${props => props.theme.breakpoints.md}) {
    flex-direction: row;
    gap: ${props => props.theme.spacing[6]};
  }
`;
```

## Best Practices

1. **Always return MappingResult**, not just strings
2. **Flag mismatches** with warnings/suggestions
3. **Prefer design system tokens** over arbitrary values
4. **Document assumptions** in code comments
5. **Handle edge cases** gracefully (undefined tokens, invalid values)
6. **Cache parsed configs** for performance
7. **Validate generated code** before returning

## Testing

Each adapter should include tests for:
- Detection accuracy
- Config parsing
- Color mapping (exact, fuzzy, arbitrary)
- Spacing mapping (scale alignment)
- Typography mapping
- Code generation (all breakpoints)
- Edge cases (missing tokens, invalid values)

## Example Test

```typescript
describe('TailwindAdapter', () => {
  it('should map exact color match', async () => {
    const adapter = new TailwindAdapter();
    await adapter.loadConfig();
    
    const result = adapter.mapColor('#3B82F6', 'background');
    
    expect(result.value).toBe('bg-blue-500');
    expect(result.exactMatch).toBe(true);
    expect(result.confidence).toBe(1.0);
  });
  
  it('should suggest design system addition for unmapped color', async () => {
    const adapter = new TailwindAdapter();
    await adapter.loadConfig();
    
    const result = adapter.mapColor('#FF5733', 'background');
    
    expect(result.value).toBe('bg-[#FF5733]'); // arbitrary value
    expect(result.exactMatch).toBe(false);
    expect(result.suggestion).toContain('Add to tailwind.config');
  });
});
```

## Extensibility

To add a new adapter:

1. Create `[framework]-adapter.md` with implementation details
2. Implement the `DesignSystemAdapter` interface
3. Add detection logic specific to the framework
4. Define mapping strategies for framework conventions
5. Implement code generation templates
6. Add comprehensive tests
7. Register in `adapters/index.ts`:

```typescript
import { TailwindAdapter } from './tailwind-adapter';
import { StyledComponentsAdapter } from './styled-components-adapter';
import { YourNewAdapter } from './your-new-adapter';

export const adapters = [
  new TailwindAdapter(),
  new StyledComponentsAdapter(),
  new YourNewAdapter(),
];

export async function detectAdapter(): Promise<DesignSystemAdapter> {
  for (const adapter of adapters) {
    if (await adapter.detect()) {
      return adapter;
    }
  }
  
  // Fallback to vanilla CSS
  return new VanillaCSSAdapter();
}
```
