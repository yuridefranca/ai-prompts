# Tailwind CSS Adapter

Adapter for mapping Figma designs to Tailwind CSS utility classes.

## Detection

```typescript
async detect(): Promise<boolean> {
  const configFiles = [
    'tailwind.config.js',
    'tailwind.config.ts',
    'tailwind.config.mjs',
    'tailwind.config.cjs',
  ];
  
  // Check for config file
  for (const file of configFiles) {
    if (await fileExists(file)) {
      return true;
    }
  }
  
  // Check package.json
  const packageJson = await readJSON('package.json');
  const dependencies = {
    ...packageJson.dependencies,
    ...packageJson.devDependencies,
  };
  
  return Object.keys(dependencies).some(dep => 
    dep === 'tailwindcss' || dep.startsWith('@tailwindcss/')
  );
}
```

## Config Loading

```typescript
async loadConfig(): Promise<DesignSystemConfig> {
  // Find config file
  const configPath = await findFirst([
    'tailwind.config.ts',
    'tailwind.config.js',
    'tailwind.config.mjs',
    'tailwind.config.cjs',
  ]);
  
  // Load config (handle TypeScript and JavaScript)
  const config = await loadTailwindConfig(configPath);
  
  // Extract theme (including defaults + extends)
  const theme = resolveTheme(config);
  
  return {
    colors: extractColors(theme.colors),
    spacing: extractSpacing(theme.spacing),
    typography: extractTypography(theme.fontSize, theme.fontWeight),
    shadows: extractShadows(theme.boxShadow),
    borderRadius: extractBorderRadius(theme.borderRadius),
    breakpoints: extractBreakpoints(theme.screens),
  };
}

function resolveTheme(config) {
  // Merge default theme with user extensions
  const defaultTheme = require('tailwindcss/defaultTheme');
  return {
    ...defaultTheme,
    ...config.theme,
    // Handle extend separately
    ...(config.theme?.extend || {}),
  };
}
```

## Color Mapping

```typescript
mapColor(figmaColor: string, context: ColorContext): MappingResult {
  const config = this.loadedConfig;
  
  // 1. Try exact variable name match
  if (config.colors[figmaColor]) {
    return {
      value: this.formatColorClass(figmaColor, context),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // 2. Try hex/rgb value match
  const matchedToken = findColorByValue(config.colors, figmaColor);
  if (matchedToken) {
    return {
      value: this.formatColorClass(matchedToken, context),
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  // 3. Fuzzy match (find closest color)
  const closestMatch = findClosestColor(config.colors, figmaColor);
  if (closestMatch.distance < 10) { // perceptual distance threshold
    return {
      value: this.formatColorClass(closestMatch.token, context),
      exactMatch: false,
      confidence: 0.8,
      warning: `Using ${closestMatch.token} as closest match to ${figmaColor}`,
    };
  }
  
  // 4. Fallback to arbitrary value
  return {
    value: this.formatColorClass(`[${figmaColor}]`, context),
    exactMatch: false,
    confidence: 0.5,
    suggestion: `Consider adding ${figmaColor} to tailwind.config colors`,
  };
}

formatColorClass(color: string, context: ColorContext): string {
  const prefixes = {
    'background': 'bg',
    'text': 'text',
    'border': 'border',
    'fill': 'fill',
    'stroke': 'stroke',
  };
  
  const prefix = prefixes[context];
  return `${prefix}-${color}`;
}
```

## Spacing Mapping

```typescript
mapSpacing(figmaSpacing: number, context: SpacingContext): MappingResult {
  const config = this.loadedConfig;
  
  // Tailwind default scale: 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 72, 80, 96
  // where: spacing[4] = 1rem = 16px
  
  // 1. Convert px to rem equivalent
  const pxValue = figmaSpacing;
  const remValue = pxValue / 16;
  
  // 2. Find exact match in spacing scale
  for (const [key, value] of Object.entries(config.spacing)) {
    if (parseSpacingValue(value) === pxValue) {
      return {
        value: this.formatSpacingClass(key, context),
        exactMatch: true,
        confidence: 1.0,
      };
    }
  }
  
  // 3. Check if value is on the scale (4px increments)
  if (pxValue % 4 === 0) {
    const scaleKey = pxValue / 4;
    if (config.spacing[scaleKey]) {
      return {
        value: this.formatSpacingClass(scaleKey.toString(), context),
        exactMatch: true,
        confidence: 1.0,
      };
    }
  }
  
  // 4. Find closest spacing value
  const closest = findClosestSpacing(config.spacing, pxValue);
  if (Math.abs(closest.value - pxValue) <= 2) { // ±2px tolerance
    return {
      value: this.formatSpacingClass(closest.key, context),
      exactMatch: false,
      confidence: 0.8,
      warning: `Using ${closest.key} (${closest.value}px) for ${pxValue}px`,
    };
  }
  
  // 5. Use arbitrary value for exact match
  return {
    value: this.formatSpacingClass(`[${pxValue}px]`, context),
    exactMatch: false,
    confidence: 0.6,
    suggestion: `Consider adding ${pxValue}px to spacing scale if used frequently`,
  };
}

formatSpacingClass(value: string, context: SpacingContext): string {
  const prefixes = {
    'padding': 'p',
    'margin': 'm',
    'gap': 'gap',
    'width': 'w',
    'height': 'h',
  };
  
  return `${prefixes[context]}-${value}`;
}
```

## Typography Mapping

```typescript
mapTypography(figmaTypography: TypographySpec): MappingResult {
  const config = this.loadedConfig;
  const classes: string[] = [];
  let exactMatch = true;
  let confidence = 1.0;
  
  // Map font size
  const fontSize = this.mapFontSize(figmaTypography.fontSize);
  classes.push(fontSize.value);
  exactMatch = exactMatch && fontSize.exactMatch;
  confidence = Math.min(confidence, fontSize.confidence);
  
  // Map font weight
  const fontWeight = this.mapFontWeight(figmaTypography.fontWeight);
  classes.push(fontWeight.value);
  exactMatch = exactMatch && fontWeight.exactMatch;
  confidence = Math.min(confidence, fontWeight.confidence);
  
  // Map line height (if specified)
  if (figmaTypography.lineHeight) {
    const lineHeight = this.mapLineHeight(figmaTypography.lineHeight);
    classes.push(lineHeight.value);
    exactMatch = exactMatch && lineHeight.exactMatch;
    confidence = Math.min(confidence, lineHeight.confidence);
  }
  
  // Map letter spacing (if specified)
  if (figmaTypography.letterSpacing) {
    const letterSpacing = this.mapLetterSpacing(figmaTypography.letterSpacing);
    classes.push(letterSpacing.value);
    exactMatch = exactMatch && letterSpacing.exactMatch;
    confidence = Math.min(confidence, letterSpacing.confidence);
  }
  
  return {
    value: classes.join(' '),
    exactMatch,
    confidence,
  };
}

mapFontSize(size: number): MappingResult {
  // Tailwind default scale: xs, sm, base, lg, xl, 2xl, 3xl, 4xl, 5xl, 6xl, 7xl, 8xl, 9xl
  const sizeMap = {
    12: 'xs',
    14: 'sm',
    16: 'base',
    18: 'lg',
    20: 'xl',
    24: '2xl',
    // ... etc
  };
  
  if (sizeMap[size]) {
    return {
      value: `text-${sizeMap[size]}`,
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  return {
    value: `text-[${size}px]`,
    exactMatch: false,
    confidence: 0.7,
  };
}

mapFontWeight(weight: number | string): MappingResult {
  const weightMap = {
    100: 'thin',
    200: 'extralight',
    300: 'light',
    400: 'normal',
    500: 'medium',
    600: 'semibold',
    700: 'bold',
    800: 'extrabold',
    900: 'black',
  };
  
  const numericWeight = typeof weight === 'string' ? parseInt(weight) : weight;
  
  if (weightMap[numericWeight]) {
    return {
      value: `font-${weightMap[numericWeight]}`,
      exactMatch: true,
      confidence: 1.0,
    };
  }
  
  return {
    value: `font-[${numericWeight}]`,
    exactMatch: false,
    confidence: 0.7,
  };
}
```

## Code Generation

```typescript
generateCode(specs: ComponentSpecs, options?: GenerationOptions): string {
  const { responsiveStrategy = 'mobile-first' } = options || {};
  
  // Start with base (mobile) styles
  const baseBreakpoint = specs.breakpoints['mobile'] || specs.breakpoints['base'];
  const baseClasses = this.generateBreakpointClasses(baseBreakpoint);
  
  // Generate responsive classes
  const responsiveClasses: string[] = [];
  const breakpointOrder = responsiveStrategy === 'mobile-first' 
    ? ['tablet', 'desktop', 'wide']
    : ['desktop', 'tablet', 'mobile'];
  
  for (const breakpoint of breakpointOrder) {
    if (specs.breakpoints[breakpoint]) {
      const bpClasses = this.generateBreakpoint(
        breakpoint, 
        this.getBreakpointDiff(baseBreakpoint, specs.breakpoints[breakpoint])
      );
      responsiveClasses.push(bpClasses);
    }
  }
  
  // Combine all classes
  const allClasses = [
    ...baseClasses,
    ...responsiveClasses,
  ].filter(Boolean).join(' ');
  
  // Generate component code
  return this.formatComponent(specs.name, allClasses, options);
}

generateBreakpointClasses(breakpointSpecs: BreakpointSpecs): string[] {
  const classes: string[] = [];
  
  // Layout classes
  if (breakpointSpecs.layout.display) {
    classes.push(this.mapDisplay(breakpointSpecs.layout.display));
  }
  if (breakpointSpecs.layout.flexDirection) {
    classes.push(this.mapFlexDirection(breakpointSpecs.layout.flexDirection));
  }
  
  // Spacing classes
  if (breakpointSpecs.spacing.gap) {
    const gap = this.mapSpacing(breakpointSpecs.spacing.gap, 'gap');
    classes.push(gap.value);
  }
  
  // Add all other mapped classes...
  
  return classes;
}

generateBreakpoint(breakpoint: string, styles: StyleMap): string {
  const prefix = this.getBreakpointPrefix(breakpoint);
  const classes = this.generateBreakpointClasses(styles);
  
  // Add prefix to each class
  return classes.map(cls => `${prefix}:${cls}`).join(' ');
}

getBreakpointPrefix(breakpoint: string): string {
  const prefixes = {
    'tablet': 'md',
    'desktop': 'lg',
    'wide': 'xl',
  };
  
  return prefixes[breakpoint] || breakpoint;
}

formatComponent(name: string, classes: string, options?: GenerationOptions): string {
  const { codeStyle = 'readable', includeComments = true } = options || {};
  
  if (codeStyle === 'compact') {
    return `<div className="${classes}">`;
  }
  
  // Readable format with line breaks
  const classGroups = this.groupClasses(classes);
  const formattedClasses = classGroups
    .map(group => `  ${group}`)
    .join('\n');
  
  return `<div 
  className="
${formattedClasses}
  "
>`;
}

groupClasses(classes: string): string[] {
  // Group by category for readability
  const groups = {
    layout: [],
    spacing: [],
    sizing: [],
    typography: [],
    colors: [],
    effects: [],
    responsive: [],
  };
  
  for (const cls of classes.split(' ')) {
    if (cls.includes(':')) {
      groups.responsive.push(cls);
    } else if (cls.startsWith('flex') || cls.startsWith('grid')) {
      groups.layout.push(cls);
    } else if (cls.startsWith('p-') || cls.startsWith('m-') || cls.startsWith('gap-')) {
      groups.spacing.push(cls);
    } else if (cls.startsWith('w-') || cls.startsWith('h-')) {
      groups.sizing.push(cls);
    } else if (cls.startsWith('text-') || cls.startsWith('font-')) {
      groups.typography.push(cls);
    } else if (cls.startsWith('bg-') || cls.startsWith('border-')) {
      groups.colors.push(cls);
    } else {
      groups.effects.push(cls);
    }
  }
  
  return Object.values(groups)
    .filter(group => group.length > 0)
    .map(group => group.join(' '));
}
```

## Example Mappings

### Input Figma Specs

```json
{
  "mobile": {
    "layout": {
      "display": "flex",
      "flexDirection": "column",
      "alignItems": "flex-start"
    },
    "spacing": {
      "gap": 28,
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
      "flexDirection": "row"
    },
    "spacing": {
      "gap": 8.512
    },
    "sizing": {
      "maxWidth": null
    }
  }
}
```

### Output Tailwind Classes

```tsx
<div 
  className="
    flex flex-col items-start
    gap-[28px] p-6
    w-full max-w-[351px]
    bg-white border border-gray-200
    rounded-xl shadow-sm
    md:flex-row
    md:gap-[8.512px]
    md:max-w-none
  "
  data-testid="user-card"
>
```

### Mapping Warnings

```markdown
⚠️ Spacing: gap-[28px] - Using arbitrary value (not on 4px scale)
  Suggestion: Consider using gap-7 (28px) if it exists in config

⚠️ Spacing: gap-[8.512px] - Using arbitrary value (precise Figma measurement)
  Suggestion: Round to gap-2 (8px) for consistency, or document why precision needed

✅ Colors: All colors matched design system tokens
✅ Border radius: rounded-xl (12px) - exact match
```

## Advanced Features

### Arbitrary Values

Tailwind 3.0+ supports arbitrary values for exact matches:

```tsx
// Exact Figma values
gap-[8.512px]
w-[351px]
text-[17.5px]
bg-[#FF5733]

// With modifiers
hover:bg-[#FF5733]/90  // with opacity
md:gap-[8.512px]       // responsive
```

### Container Queries (Tailwind 3.2+)

```tsx
// Use @container instead of media queries when appropriate
@container (min-width: 768px) {
  .card { flex-direction: row; }
}

// Tailwind classes:
@container/card (md:flex-row)
```

### Dynamic Class Generation

```typescript
// For very dynamic scenarios, generate utility classes
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      spacing: {
        // Generated from Figma
        'figma-1': '8.512px',
        'figma-2': '28px',
      }
    }
  }
}

// Then use: gap-figma-1, gap-figma-2
```

## Best Practices

1. **Prefer standard scale values** over arbitrary when possible
2. **Document arbitrary values** with comments explaining why needed
3. **Group classes logically** for readability (layout, spacing, colors)
4. **Use semantic breakpoint names** from config (not pixel values)
5. **Avoid overly specific classes** - balance precision with maintainability
6. **Test responsive behavior** at all breakpoints, not just exact widths
7. **Consider fluid sizing** (clamp) for smooth transitions when appropriate

## Limitations

- Cannot detect JIT mode - always assume modern Tailwind 3+
- Plugin-generated utilities may not be detected
- Custom plugins may require manual mapping
- Dynamic class names (template literals) not validated at build time
