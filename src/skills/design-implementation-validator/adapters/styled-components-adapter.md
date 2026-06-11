# Styled Components Adapter

Adapter for mapping Figma designs to Styled Components with theme integration.

## Detection

```typescript
async detect(): Promise<boolean> {
  // Check package.json for styled-components
  const packageJson = await readJSON('package.json');
  const dependencies = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies,
  };
  
  if (dependencies['styled-components']) {
    return true;
  }
  
  // Check for @emotion/styled as alternative
  if (dependencies['@emotion/styled']) {
    return true;
  }
  
  // Check for styled imports in source files
  const hasStyledImports = await grepSearch(
    'import styled from',
    { includePattern: 'src/**/*.{ts,tsx,js,jsx}' }
  );
  
  return hasStyledImports.length > 0;
}
```

## Config Loading

```typescript
async loadConfig(): Promise<DesignSystemConfig> {
  // Look for theme file
  const themePath = await findFirst([
    'src/theme/index.ts',
    'src/theme/theme.ts',
    'src/styles/theme.ts',
    'theme.ts',
  ]);
  
  if (!themePath) {
    throw new Error('No theme file found. Expected theme definition for styled-components.');
  }
  
  // Import and parse theme
  const theme = await importTheme(themePath);
  
  return {
    colors: extractColors(theme.colors),
    spacing: extractSpacing(theme.spacing || theme.space),
    typography: extractTypography(theme.typography || theme.fontSizes),
    shadows: extractShadows(theme.shadows),
    borderRadius: extractBorderRadius(theme.radii || theme.borderRadius),
    breakpoints: extractBreakpoints(theme.breakpoints || theme.screens),
  };
}

async function importTheme(themePath: string) {
  // Handle both CommonJS and ESM
  const content = await readFile(themePath);
  
  // Extract theme object using AST parsing
  // This is safer than dynamic import for config files
  const theme = parseThemeObject(content);
  
  return theme;
}
```

## Color Mapping

```typescript
mapColor(figmaColor: string, context: ColorContext): MappingResult {
  const config = this.loadedConfig;
  
  // 1. Try exact variable name match
  if (config.colors[figmaColor]) {
    return {
      value: this.formatColorRef(figmaColor),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // 2. Try nested color scale (e.g., blue.500)
  const nestedMatch = this.findNestedColor(config.colors, figmaColor);
  if (nestedMatch) {
    return {
      value: this.formatColorRef(nestedMatch),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // 3. Try hex/rgb value match
  const matchedToken = findColorByValue(config.colors, figmaColor);
  if (matchedToken) {
    return {
      value: this.formatColorRef(matchedToken),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // 4. Fuzzy match
  const closestMatch = findClosestColor(config.colors, figmaColor);
  if (closestMatch.distance < 10) {
    return {
      value: this.formatColorRef(closestMatch.token),
      exactMatch: false,
      confidence: 0.8,
      warning: `Using ${closestMatch.token} as closest match to ${figmaColor}`,
    };
  }
  
  // 5. Fallback to literal value
  return {
    value: `'${figmaColor}'`,
    exactMatch: false,
    confidence: 0.5,
    suggestion: `Consider adding ${figmaColor} to theme.colors`,
  };
}

formatColorRef(colorPath: string): string {
  // Format: props => props.theme.colors.primary
  // or: props => props.theme.colors.blue[500]
  
  if (colorPath.includes('.')) {
    // Nested path (e.g., "blue.500")
    const parts = colorPath.split('.');
    const path = parts.join('.');
    return `props => props.theme.colors.${path}`;
  }
  
  // Simple key
  return `props => props.theme.colors.${colorPath}`;
}

findNestedColor(colors: any, figmaColor: string): string | null {
  // Handle Figma variable names like "primary-500" → theme.colors.primary[500]
  const match = figmaColor.match(/^(.+)-(\d+)$/);
  if (match) {
    const [, name, shade] = match;
    if (colors[name] && colors[name][shade]) {
      return `${name}[${shade}]`;
    }
  }
  
  return null;
}
```

## Spacing Mapping

```typescript
mapSpacing(figmaSpacing: number, context: SpacingContext): MappingResult {
  const config = this.loadedConfig;
  
  // Styled-components themes often use arrays: spacing = [0, 4, 8, 16, 32, 64]
  // Or objects: spacing = { xs: 4, sm: 8, md: 16, lg: 32, xl: 64 }
  
  const spacingScale = config.spacing;
  
  // 1. Array-based spacing
  if (Array.isArray(spacingScale)) {
    const index = spacingScale.indexOf(figmaSpacing);
    if (index !== -1) {
      return {
        value: `props => props.theme.spacing[${index}]`,
        exactMatch: true,
        confidence: 1.0,
      };
    }
  }
  
  // 2. Object-based spacing
  if (typeof spacingScale === 'object') {
    for (const [key, value] of Object.entries(spacingScale)) {
      if (parseSpacingValue(value) === figmaSpacing) {
        return {
          value: `props => props.theme.spacing.${key}`,
          exactMatch: true,
          confidence: 1.0,
        };
      }
    }
  }
  
  // 3. Find closest match
  const closest = findClosestSpacing(spacingScale, figmaSpacing);
  if (Math.abs(closest.value - figmaSpacing) <= 2) {
    return {
      value: closest.ref,
      exactMatch: false,
      confidence: 0.8,
      warning: `Using ${closest.key} (${closest.value}px) for ${figmaSpacing}px`,
    };
  }
  
  // 4. Use literal value
  return {
    value: `'${figmaSpacing}px'`,
    exactMatch: false,
    confidence: 0.6,
    suggestion: `Consider adding ${figmaSpacing}px to theme.spacing`,
  };
}
```

## Typography Mapping

```typescript
mapTypography(figmaTypography: TypographySpec): MappingResult {
  const config = this.loadedConfig;
  
  // Check if theme has typography presets (e.g., heading1, body, etc.)
  const preset = this.findTypographyPreset(figmaTypography);
  if (preset) {
    return {
      value: this.formatTypographyPreset(preset),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // Map individual properties
  const styles: string[] = [];
  
  // Font family
  if (figmaTypography.fontFamily) {
    const fontFamily = this.mapFontFamily(figmaTypography.fontFamily);
    styles.push(`font-family: ${fontFamily.value};`);
  }
  
  // Font size
  const fontSize = this.mapFontSize(figmaTypography.fontSize);
  styles.push(`font-size: ${fontSize.value};`);
  
  // Font weight
  const fontWeight = this.mapFontWeight(figmaTypography.fontWeight);
  styles.push(`font-weight: ${fontWeight.value};`);
  
  // Line height
  if (figmaTypography.lineHeight) {
    const lineHeight = this.mapLineHeight(figmaTypography.lineHeight);
    styles.push(`line-height: ${lineHeight.value};`);
  }
  
  // Letter spacing
  if (figmaTypography.letterSpacing) {
    const letterSpacing = this.mapLetterSpacing(figmaTypography.letterSpacing);
    styles.push(`letter-spacing: ${letterSpacing.value};`);
  }
  
  return {
    value: styles.join('\n  '),
    exactMatch: false,
    confidence: 0.8,
  };
}

findTypographyPreset(spec: TypographySpec): string | null {
  const config = this.loadedConfig;
  
  // Check if theme.typography exists with presets
  if (!config.typography) return null;
  
  for (const [key, preset] of Object.entries(config.typography)) {
    if (
      preset.fontSize === spec.fontSize &&
      preset.fontWeight === spec.fontWeight &&
      (!spec.lineHeight || preset.lineHeight === spec.lineHeight)
    ) {
      return key;
    }
  }
  
  return null;
}

formatTypographyPreset(preset: string): string {
  return `
  font-family: \${props => props.theme.typography.${preset}.fontFamily};
  font-size: \${props => props.theme.typography.${preset}.fontSize};
  font-weight: \${props => props.theme.typography.${preset}.fontWeight};
  line-height: \${props => props.theme.typography.${preset}.lineHeight};
  `;
}
```

## Code Generation

```typescript
generateCode(specs: ComponentSpecs, options?: GenerationOptions): string {
  const { includeComments = true } = options || {};
  
  // Generate base component
  const baseStyles = this.generateBreakpointStyles(specs.breakpoints.mobile || specs.breakpoints.base);
  
  // Generate responsive styles
  const responsiveStyles = this.generateResponsiveStyles(specs.breakpoints);
  
  // Generate state styles (hover, focus, etc.)
  const stateStyles = specs.states ? this.generateStateStyles(specs.states) : '';
  
  // Combine into styled component
  return this.formatStyledComponent(
    specs.name,
    baseStyles,
    responsiveStyles,
    stateStyles,
    includeComments
  );
}

generateBreakpointStyles(breakpointSpecs: BreakpointSpecs): string {
  const styles: string[] = [];
  
  // Layout
  if (breakpointSpecs.layout.display) {
    styles.push(`display: ${breakpointSpecs.layout.display};`);
  }
  if (breakpointSpecs.layout.flexDirection) {
    styles.push(`flex-direction: ${breakpointSpecs.layout.flexDirection};`);
  }
  if (breakpointSpecs.layout.alignItems) {
    styles.push(`align-items: ${breakpointSpecs.layout.alignItems};`);
  }
  if (breakpointSpecs.layout.justifyContent) {
    styles.push(`justify-content: ${breakpointSpecs.layout.justifyContent};`);
  }
  
  // Spacing
  if (breakpointSpecs.spacing.gap) {
    const gap = this.mapSpacing(breakpointSpecs.spacing.gap, 'gap');
    styles.push(`gap: ${gap.value};`);
  }
  if (breakpointSpecs.spacing.padding) {
    const padding = this.mapSpacing(breakpointSpecs.spacing.padding, 'padding');
    styles.push(`padding: ${padding.value};`);
  }
  
  // Colors
  if (breakpointSpecs.colors.background) {
    const bg = this.mapColor(breakpointSpecs.colors.background, 'background');
    styles.push(`background: ${bg.value};`);
  }
  if (breakpointSpecs.colors.color) {
    const color = this.mapColor(breakpointSpecs.colors.color, 'text');
    styles.push(`color: ${color.value};`);
  }
  
  // Effects
  if (breakpointSpecs.effects.borderRadius) {
    const radius = this.mapBorderRadius(breakpointSpecs.effects.borderRadius);
    styles.push(`border-radius: ${radius.value};`);
  }
  if (breakpointSpecs.effects.boxShadow) {
    const shadow = this.mapShadow(breakpointSpecs.effects.boxShadow);
    styles.push(`box-shadow: ${shadow.value};`);
  }
  
  return styles.join('\n  ');
}

generateResponsiveStyles(breakpoints: Record<string, BreakpointSpecs>): string {
  const responsiveBlocks: string[] = [];
  
  // Skip mobile/base (already in base styles)
  const responsiveBreakpoints = Object.entries(breakpoints)
    .filter(([key]) => key !== 'mobile' && key !== 'base');
  
  for (const [breakpoint, specs] of responsiveBreakpoints) {
    const mediaQuery = this.getMediaQuery(breakpoint);
    const styles = this.generateBreakpointStyles(specs);
    
    responsiveBlocks.push(`
  ${mediaQuery} {
    ${styles}
  }`);
  }
  
  return responsiveBlocks.join('\n');
}

getMediaQuery(breakpoint: string): string {
  const config = this.loadedConfig;
  const breakpointValue = config.breakpoints[breakpoint];
  
  if (typeof breakpointValue === 'number') {
    return `@media (min-width: ${breakpointValue}px)`;
  }
  
  // Use theme reference
  return `@media (min-width: \${props => props.theme.breakpoints.${breakpoint}})`;
}

generateStateStyles(states: Record<string, StateSpecs>): string {
  const stateBlocks: string[] = [];
  
  for (const [state, specs] of Object.entries(states)) {
    const styles = this.generateBreakpointStyles(specs);
    
    stateBlocks.push(`
  &:${state} {
    ${styles}
  }`);
  }
  
  return stateBlocks.join('\n');
}

formatStyledComponent(
  name: string,
  baseStyles: string,
  responsiveStyles: string,
  stateStyles: string,
  includeComments: boolean
): string {
  const comment = includeComments 
    ? `// Generated from Figma design\n// Date: ${new Date().toISOString()}\n` 
    : '';
  
  return `${comment}const ${name} = styled.div\`
  ${baseStyles}${responsiveStyles}${stateStyles}
\`;`;
}
```

## Example Mappings

### Input Figma Specs

```json
{
  "name": "UserCard",
  "breakpoints": {
    "mobile": {
      "layout": {
        "display": "flex",
        "flexDirection": "column",
        "gap": 28
      },
      "spacing": {
        "padding": 24
      },
      "sizing": {
        "width": "100%",
        "maxWidth": 351
      },
      "colors": {
        "background": "#FFFFFF",
        "border": "#E5E7EB"
      },
      "effects": {
        "borderRadius": 12,
        "boxShadow": "0 1px 3px rgba(0,0,0,0.1)"
      }
    },
    "tablet": {
      "layout": {
        "flexDirection": "row",
        "gap": 8.512
      },
      "sizing": {
        "maxWidth": null
      }
    }
  },
  "states": {
    "hover": {
      "effects": {
        "boxShadow": "0 4px 6px rgba(0,0,0,0.1)"
      }
    }
  }
}
```

### Output Styled Component

```typescript
// Generated from Figma design
// Date: 2026-05-23T10:30:00Z
const UserCard = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing[7]};
  padding: ${props => props.theme.spacing[6]};
  width: 100%;
  max-width: 351px;
  background: ${props => props.theme.colors.white};
  border: 1px solid ${props => props.theme.colors.gray[200]};
  border-radius: ${props => props.theme.radii.xl};
  box-shadow: ${props => props.theme.shadows.sm};

  @media (min-width: ${props => props.theme.breakpoints.tablet}) {
    flex-direction: row;
    gap: 8.512px;
    max-width: none;
  }

  &:hover {
    box-shadow: ${props => props.theme.shadows.md};
  }
`;
```

### With Arbitrary Values

```typescript
const UserCard = styled.div`
  display: flex;
  flex-direction: column;
  gap: 28px; /* ⚠️ Not in spacing scale */
  padding: ${props => props.theme.spacing[6]};
  width: 100%;
  max-width: 351px; /* ⚠️ Exact Figma value */
  background: ${props => props.theme.colors.white};
  border-radius: ${props => props.theme.radii.xl};

  @media (min-width: ${props => props.theme.breakpoints.tablet}) {
    flex-direction: row;
    gap: 8.512px; /* ⚠️ Precise Figma measurement */
    max-width: none;
  }
`;

// Warnings:
// - gap: 28px not in theme.spacing - suggest adding or using closest value
// - gap: 8.512px precise value - consider rounding to 8px or adding to theme
```

## Advanced Features

### CSS Helper Functions

```typescript
// Use polished or custom helpers for color manipulation
import { darken, lighten } from 'polished';

const Button = styled.button`
  background: ${props => props.theme.colors.primary};
  
  &:hover {
    background: ${props => darken(0.1, props.theme.colors.primary)};
  }
`;
```

### Theming Support

```typescript
// Handle light/dark themes
const Card = styled.div`
  background: ${props => 
    props.theme.mode === 'dark' 
      ? props.theme.colors.gray[800]
      : props.theme.colors.white
  };
`;
```

### TypeScript Integration

```typescript
import { DefaultTheme } from 'styled-components';

// Generate TypeScript types from Figma
interface FigmaTheme extends DefaultTheme {
  colors: {
    primary: string;
    secondary: string;
    // ...
  };
  spacing: number[];
  breakpoints: {
    mobile: string;
    tablet: string;
    desktop: string;
  };
}

const theme: FigmaTheme = {
  // ... theme values
};
```

### CSS-in-JS Optimizations

```typescript
// Use css helper for reusable styles
import styled, { css } from 'styled-components';

const flexColumn = css`
  display: flex;
  flex-direction: column;
`;

const Card = styled.div`
  ${flexColumn}
  gap: ${props => props.theme.spacing[4]};
`;
```

## Best Practices

1. **Always use theme references** instead of hardcoded values
2. **Group related properties** (layout, spacing, colors) for readability
3. **Comment non-standard values** that don't match theme
4. **Use semantic theme keys** (e.g., `colors.primary` not `colors.blue500`)
5. **Leverage TypeScript** for theme type safety
6. **Extract common patterns** into css helpers
7. **Consider performance** - avoid excessive nesting and dynamic calculations
8. **Document theme structure** so designers understand available tokens

## Emotion Support

This adapter also supports `@emotion/styled` with minimal changes:

```typescript
// Detection
import styled from '@emotion/styled';

// Theme access (same as styled-components)
const Card = styled.div`
  color: ${props => props.theme.colors.primary};
`;

// With emotion, you can also use the css prop:
/** @jsxImportSource @emotion/react */
<div css={{
  display: 'flex',
  gap: theme.spacing[4],
}} />
```

## Limitations

- Cannot detect custom theme provider implementations
- Dynamic theme switching may require runtime validation
- Server-side rendering requires separate handling
- Theme file structure must be parseable (no complex logic)
- CSS variables fallback not generated automatically
