# Figma Extraction Utilities

Utilities for extracting design specifications from Figma using the Figma MCP server.

## Overview

These utilities provide a high-level interface for extracting design data from Figma, handling:
- Auto-detection of Figma Variables vs raw styles
- Multi-breakpoint extraction
- Semantic token mapping
- Responsive behavior detection
- Component state extraction (hover, focus, etc.)

## Figma MCP Integration

Before using these utilities, ensure the Figma MCP server is loaded:

```typescript
// Load Figma MCP tools
await tool_search("figma");

// Available tools:
// - figma-read-file: Read Figma file metadata
// - figma-get-node: Get specific node/frame data  
// - figma-get-styles: Get design tokens and variables
// - figma-get-component: Get component definition
```

## Core Extraction Functions

### extractComponentSpecs()

Main entry point for extracting complete component specifications.

```typescript
async function extractComponentSpecs(
  figmaUrl: string,
  options?: ExtractionOptions
): Promise<ComponentSpecs> {
  // 1. Parse Figma URL to get file ID and node ID
  const { fileId, nodeId } = parseFigmaUrl(figmaUrl);
  
  // 2. Detect Figma structure (Variables, Design Tokens, or raw styles)
  const structure = await detectFigmaStructure(fileId);
  
  // 3. Extract node data
  const nodeData = await figma_get_node({ fileId, nodeId });
  
  // 4. Extract breakpoint variants
  const breakpoints = await extractBreakpoints(nodeData, structure);
  
  // 5. Extract states (hover, focus, etc.)
  const states = await extractStates(nodeData, structure);
  
  // 6. Extract semantic tokens
  const semanticTokens = await extractSemanticTokens(nodeData, structure);
  
  return {
    name: nodeData.name,
    figmaUrl,
    extractedAt: new Date().toISOString(),
    figmaStructure: structure.type,
    breakpoints,
    states,
    semanticTokens,
  };
}

interface ExtractionOptions {
  /** Breakpoints to extract (defaults to auto-detect) */
  breakpoints?: string[];
  
  /** Whether to extract interaction states */
  includeStates?: boolean;
  
  /** Whether to extract component variants */
  includeVariants?: boolean;
  
  /** Tolerance for rounding values (px) */
  roundingTolerance?: number;
}
```

### detectFigmaStructure()

Detects how design tokens are organized in Figma.

```typescript
async function detectFigmaStructure(fileId: string): Promise<FigmaStructure> {
  // 1. Check for Figma Variables (modern approach)
  const variables = await figma_get_styles({ fileId, type: 'variables' });
  if (variables && variables.length > 0) {
    return {
      type: 'variables',
      variables: parseVariables(variables),
    };
  }
  
  // 2. Check for Design Tokens plugin
  const pluginData = await figma_get_plugin_data({ fileId, pluginId: 'design-tokens' });
  if (pluginData) {
    return {
      type: 'design-tokens-plugin',
      tokens: parseDesignTokens(pluginData),
    };
  }
  
  // 3. Check for Styles (legacy approach)
  const styles = await figma_get_styles({ fileId, type: 'all' });
  if (styles && styles.length > 0) {
    return {
      type: 'styles',
      styles: parseStyles(styles),
    };
  }
  
  // 4. Fallback to raw values
  return {
    type: 'raw',
    message: 'No design system structure detected, will use raw values',
  };
}

interface FigmaStructure {
  type: 'variables' | 'design-tokens-plugin' | 'styles' | 'raw';
  variables?: FigmaVariable[];
  tokens?: DesignToken[];
  styles?: FigmaStyle[];
  message?: string;
}
```

### extractBreakpoints()

Extracts responsive variations from Figma component using multiple detection strategies.

**Critical:** This function ensures **ALL breakpoints are extracted** from Figma to support complete responsive implementation. The extracted breakpoints follow a mobile-first approach where the smallest breakpoint becomes the base.

**Detection Strategies (priority order):**

1. **Component Variants** - Figma component sets with "Breakpoint" or "Size" property
   - Example: "Button, Breakpoint=Mobile", "Button, Breakpoint=Tablet"
   - ✅ Most explicit and reliable

2. **Auto Layout Constraints** - Figma's responsive design features
   - Analyzes resize behavior and constraints
   - Detects fluid vs fixed sizing
   - ✅ Works with modern Figma designs

3. **Sibling Frames** - Multiple frames with breakpoint naming
   - Example: "Component / Mobile", "Component / Tablet"
   - ✅ Fallback for older Figma files

4. **Single Breakpoint** - No responsive variants found
   - Returns `{ base: specs }`
   - ⚠️ Will generate non-responsive code

```typescript
async function extractBreakpoints(
  nodeData: FigmaNode,
  structure: FigmaStructure
): Promise<Record<string, BreakpointSpecs>> {
  // Strategy 1: Component variants with breakpoint names
  if (nodeData.type === 'COMPONENT_SET') {
    return extractBreakpointsFromVariants(nodeData);
  }
  
  // Strategy 2: Auto Layout constraints (Figma's responsive design)
  if (nodeData.children) {
    return extractBreakpointsFromAutoLayout(nodeData);
  }
  
  // Strategy 3: Frame names (e.g., "Component / Mobile", "Component / Desktop")
  const siblingFrames = await findSiblingFrames(nodeData);
  if (siblingFrames.length > 1) {
    return extractBreakpointsFromSiblings(siblingFrames);
  }
  
  // Fallback: Single breakpoint (no responsive variants found)
  return {
    base: await extractSingleBreakpoint(nodeData, structure),
  };
}

async function extractBreakpointsFromVariants(
  componentSet: FigmaComponentSet
): Promise<Record<string, BreakpointSpecs>> {
  const breakpoints: Record<string, BreakpointSpecs> = {};
  
  // Figma component variants with "Breakpoint" or "Size" property
  // Example: "Button, Breakpoint=Mobile", "Button, Breakpoint=Tablet"
  for (const variant of componentSet.children) {
    const breakpointName = detectBreakpointName(variant.name);
    
    if (breakpointName) {
      breakpoints[breakpointName] = await extractSingleBreakpoint(variant);
    }
  }
  
  // Ensure mobile-first order
  return sortBreakpoints(breakpoints);
}

function detectBreakpointName(variantName: string): string | null {
  // Common patterns:
  // - "Button / Mobile"
  // - "Button, Size=Mobile"
  // - "Button, Breakpoint=sm"
  
  const patterns = [
    /breakpoint[=:]?\s*(mobile|tablet|desktop|wide)/i,
    /size[=:]?\s*(mobile|tablet|desktop|wide)/i,
    /\/(mobile|tablet|desktop|wide)/i,
    /\b(mobile|tablet|desktop|wide)\b/i,
  ];
  
  for (const pattern of patterns) {
    const match = variantName.match(pattern);
    if (match) {
      return normalizeBreakpointName(match[1]);
    }
  }
  
  return null;
}

function normalizeBreakpointName(name: string): string {
  // Normalize Figma breakpoint names to standard names
  // Ensures consistent naming across different Figma conventions
  const map = {
    'xs': 'mobile',
    'sm': 'mobile',
    'small': 'mobile',
    'phone': 'mobile',
    'md': 'tablet',
    'medium': 'tablet',
    'ipad': 'tablet',
    'lg': 'desktop',
    'large': 'desktop',
    'xl': 'wide',
    '2xl': 'wide',
    'ultrawide': 'wide',
  };
  
  return map[name.toLowerCase()] || name.toLowerCase();
}

function sortBreakpoints(breakpoints: Record<string, BreakpointSpecs>): Record<string, BreakpointSpecs> {
  // Sort breakpoints in mobile-first order for code generation
  const order = ['mobile', 'tablet', 'desktop', 'wide'];
  const sorted: Record<string, BreakpointSpecs> = {};
  
  for (const key of order) {
    if (breakpoints[key]) {
      sorted[key] = breakpoints[key];
    }
  }
  
  // Add any custom breakpoints not in standard order
  for (const [key, value] of Object.entries(breakpoints)) {
    if (!sorted[key]) {
      sorted[key] = value;
    }
  }
  
  return sorted;
}
```

### extractSingleBreakpoint()

Extracts styles for a single breakpoint/variant.

```typescript
async function extractSingleBreakpoint(
  node: FigmaNode,
  structure?: FigmaStructure
): Promise<BreakpointSpecs> {
  return {
    layout: extractLayoutSpecs(node),
    spacing: extractSpacingSpecs(node),
    sizing: extractSizingSpecs(node),
    typography: extractTypographySpecs(node),
    colors: extractColorSpecs(node, structure),
    effects: extractEffectSpecs(node, structure),
  };
}

function extractLayoutSpecs(node: FigmaNode): LayoutSpecs {
  // Figma Auto Layout → Flexbox mapping
  if (node.layoutMode === 'HORIZONTAL') {
    return {
      display: 'flex',
      flexDirection: 'row',
      alignItems: mapFigmaAlign(node.primaryAxisAlignItems),
      justifyContent: mapFigmaJustify(node.counterAxisAlignItems),
    };
  }
  
  if (node.layoutMode === 'VERTICAL') {
    return {
      display: 'flex',
      flexDirection: 'column',
      alignItems: mapFigmaAlign(node.counterAxisAlignItems),
      justifyContent: mapFigmaJustify(node.primaryAxisAlignItems),
    };
  }
  
  // No Auto Layout - absolute positioning
  return {
    display: 'block',
    position: 'relative',
  };
}

function extractSpacingSpecs(node: FigmaNode): SpacingSpecs {
  return {
    padding: node.paddingTop || node.padding,
    paddingTop: node.paddingTop,
    paddingRight: node.paddingRight,
    paddingBottom: node.paddingBottom,
    paddingLeft: node.paddingLeft,
    gap: node.itemSpacing, // Figma's gap property
  };
}

function extractTypographySpecs(node: FigmaNode): TypographySpec | null {
  // Find text nodes within component
  const textNode = findFirstTextNode(node);
  if (!textNode) return null;
  
  return {
    fontFamily: textNode.style.fontFamily,
    fontSize: textNode.style.fontSize,
    fontWeight: textNode.style.fontWeight,
    lineHeight: calculateLineHeight(textNode.style.lineHeightPx, textNode.style.fontSize),
    letterSpacing: textNode.style.letterSpacing,
  };
}

function extractColorSpecs(
  node: FigmaNode,
  structure?: FigmaStructure
): ColorSpecs {
  const colors: ColorSpecs = {};
  
  // Background color
  if (node.fills && node.fills.length > 0) {
    const fill = node.fills[0];
    if (fill.type === 'SOLID') {
      colors.background = resolveColor(fill, structure);
    }
  }
  
  // Border color
  if (node.strokes && node.strokes.length > 0) {
    const stroke = node.strokes[0];
    if (stroke.type === 'SOLID') {
      colors.border = resolveColor(stroke, structure);
    }
  }
  
  // Text color
  const textNode = findFirstTextNode(node);
  if (textNode && textNode.fills && textNode.fills.length > 0) {
    const fill = textNode.fills[0];
    if (fill.type === 'SOLID') {
      colors.color = resolveColor(fill, structure);
    }
  }
  
  return colors;
}

function resolveColor(
  fill: FigmaPaint,
  structure?: FigmaStructure
): string {
  // Priority 1: Figma Variable reference
  if (fill.boundVariables?.color) {
    const variable = structure?.variables?.find(v => v.id === fill.boundVariables.color);
    if (variable) {
      return variable.name; // Return semantic name
    }
  }
  
  // Priority 2: Style reference
  if (fill.styleId && structure?.styles) {
    const style = structure.styles.find(s => s.id === fill.styleId);
    if (style) {
      return style.name;
    }
  }
  
  // Priority 3: Raw color value
  if (fill.color) {
    return rgbaToHex(fill.color);
  }
  
  return '#000000'; // fallback
}

function extractEffectSpecs(
  node: FigmaNode,
  structure?: FigmaStructure
): EffectSpecs {
  const effects: EffectSpecs = {};
  
  // Border radius
  if (node.cornerRadius !== undefined) {
    effects.borderRadius = node.cornerRadius;
  } else if (node.rectangleCornerRadii) {
    // Individual corner radii
    effects.borderRadius = {
      topLeft: node.rectangleCornerRadii[0],
      topRight: node.rectangleCornerRadii[1],
      bottomRight: node.rectangleCornerRadii[2],
      bottomLeft: node.rectangleCornerRadii[3],
    };
  }
  
  // Box shadow
  const dropShadow = node.effects?.find(e => e.type === 'DROP_SHADOW');
  if (dropShadow) {
    effects.boxShadow = formatBoxShadow(dropShadow, structure);
  }
  
  // Opacity
  if (node.opacity !== undefined && node.opacity !== 1) {
    effects.opacity = node.opacity;
  }
  
  return effects;
}
```

### extractStates()

Extracts interaction states (hover, focus, active, disabled).

```typescript
async function extractStates(
  nodeData: FigmaNode,
  structure: FigmaStructure
): Promise<Record<string, StateSpecs> | undefined> {
  // Check for component variants with state names
  if (nodeData.type === 'COMPONENT_SET') {
    return extractStatesFromVariants(nodeData);
  }
  
  // Check for interactive component states (Figma's built-in feature)
  if (nodeData.reactions && nodeData.reactions.length > 0) {
    return extractStatesFromReactions(nodeData);
  }
  
  return undefined;
}

function extractStatesFromVariants(
  componentSet: FigmaComponentSet
): Record<string, StateSpecs> {
  const states: Record<string, StateSpecs> = {};
  
  for (const variant of componentSet.children) {
    const stateName = detectStateName(variant.name);
    
    if (stateName) {
      states[stateName] = extractSingleBreakpoint(variant);
    }
  }
  
  return states;
}

function detectStateName(variantName: string): string | null {
  // Common patterns:
  // - "Button, State=Hover"
  // - "Button / Hover"
  // - "Button:hover"
  
  const statePatterns = {
    hover: /state[=:]?\s*hover|:hover|\/hover/i,
    focus: /state[=:]?\s*focus|:focus|\/focus/i,
    active: /state[=:]?\s*active|:active|\/active/i,
    disabled: /state[=:]?\s*disabled|:disabled|\/disabled/i,
  };
  
  for (const [state, pattern] of Object.entries(statePatterns)) {
    if (pattern.test(variantName)) {
      return state;
    }
  }
  
  return null;
}
```

### extractSemanticTokens()

Extracts semantic design token names used in the component.

```typescript
function extractSemanticTokens(
  nodeData: FigmaNode,
  structure: FigmaStructure
): SemanticTokens {
  const tokens: SemanticTokens = {
    colors: [],
    spacing: [],
    typography: [],
    effects: [],
  };
  
  // Extract from Variables
  if (structure.type === 'variables' && structure.variables) {
    tokens.colors = extractColorVariables(nodeData, structure.variables);
    tokens.spacing = extractSpacingVariables(nodeData, structure.variables);
    tokens.typography = extractTypographyVariables(nodeData, structure.variables);
    tokens.effects = extractEffectVariables(nodeData, structure.variables);
  }
  
  // Extract from Styles
  if (structure.type === 'styles' && structure.styles) {
    tokens.colors = extractColorStyles(nodeData, structure.styles);
    tokens.typography = extractTextStyles(nodeData, structure.styles);
    tokens.effects = extractEffectStyles(nodeData, structure.styles);
  }
  
  return tokens;
}

function extractColorVariables(
  node: FigmaNode,
  variables: FigmaVariable[]
): string[] {
  const usedVariables = new Set<string>();
  
  // Traverse node tree
  traverseNode(node, (n) => {
    // Check fills
    n.fills?.forEach(fill => {
      if (fill.boundVariables?.color) {
        const variable = variables.find(v => v.id === fill.boundVariables.color);
        if (variable) {
          usedVariables.add(variable.name);
        }
      }
    });
    
    // Check strokes
    n.strokes?.forEach(stroke => {
      if (stroke.boundVariables?.color) {
        const variable = variables.find(v => v.id === stroke.boundVariables.color);
        if (variable) {
          usedVariables.add(variable.name);
        }
      }
    });
  });
  
  return Array.from(usedVariables);
}
```

## Utility Functions

### parseFigmaUrl()

```typescript
function parseFigmaUrl(url: string): { fileId: string; nodeId?: string } {
  // Figma URL patterns:
  // https://www.figma.com/file/{fileId}/{title}?node-id={nodeId}
  // https://www.figma.com/design/{fileId}/{title}?node-id={nodeId}
  
  const fileMatch = url.match(/figma\.com\/(file|design)\/([a-zA-Z0-9]+)/);
  if (!fileMatch) {
    throw new Error(`Invalid Figma URL: ${url}`);
  }
  
  const fileId = fileMatch[2];
  
  const nodeMatch = url.match(/node-id=([0-9]+-[0-9]+)/);
  const nodeId = nodeMatch ? nodeMatch[1].replace('-', ':') : undefined;
  
  return { fileId, nodeId };
}
```

### Color Conversion Utilities

```typescript
function rgbaToHex(rgba: RGBA): string {
  const r = Math.round(rgba.r * 255);
  const g = Math.round(rgba.g * 255);
  const b = Math.round(rgba.b * 255);
  
  return `#${[r, g, b].map(x => x.toString(16).padStart(2, '0')).join('')}`.toUpperCase();
}

function rgbaToHexWithAlpha(rgba: RGBA): string {
  const hex = rgbaToHex(rgba);
  
  if (rgba.a !== undefined && rgba.a < 1) {
    const alpha = Math.round(rgba.a * 255);
    return `${hex}${alpha.toString(16).padStart(2, '0')}`;
  }
  
  return hex;
}
```

### Figma → CSS Mapping

```typescript
function mapFigmaAlign(alignment: string): string {
  const map = {
    'MIN': 'flex-start',
    'CENTER': 'center',
    'MAX': 'flex-end',
    'SPACE_BETWEEN': 'space-between',
  };
  
  return map[alignment] || 'flex-start';
}

function mapFigmaJustify(alignment: string): string {
  // Same mapping as align
  return mapFigmaAlign(alignment);
}

function calculateLineHeight(
  lineHeightPx: number,
  fontSize: number
): number | string {
  if (lineHeightPx === fontSize) {
    return 1;
  }
  
  // Return as multiplier
  return lineHeightPx / fontSize;
}

function formatBoxShadow(
  effect: FigmaEffect,
  structure?: FigmaStructure
): string {
  const x = effect.offset.x;
  const y = effect.offset.y;
  const blur = effect.radius;
  const spread = effect.spread || 0;
  const color = effect.color ? rgbaToHexWithAlpha(effect.color) : '#000000';
  
  return `${x}px ${y}px ${blur}px ${spread}px ${color}`;
}
```

## Error Handling

```typescript
class FigmaExtractionError extends Error {
  constructor(
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
    this.name = 'FigmaExtractionError';
  }
}

// Usage
try {
  const specs = await extractComponentSpecs(figmaUrl);
} catch (error) {
  if (error instanceof FigmaExtractionError) {
    switch (error.code) {
      case 'INVALID_URL':
        console.error('Invalid Figma URL provided');
        break;
      case 'ACCESS_DENIED':
        console.error('Cannot access Figma file. Check permissions.');
        break;
      case 'NODE_NOT_FOUND':
        console.error('Component/frame not found in Figma file');
        break;
      default:
        console.error('Extraction failed:', error.message);
    }
  }
}
```

## Output Format

### Complete Component Specs

```json
{
  "name": "UserCard",
  "figmaUrl": "https://figma.com/file/abc123?node-id=123:456",
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
        "gap": 28,
        "padding": 24,
        "paddingTop": 24,
        "paddingRight": 24,
        "paddingBottom": 24,
        "paddingLeft": 24
      },
      "sizing": {
        "width": "100%",
        "maxWidth": 351
      },
      "typography": {
        "fontFamily": "Inter",
        "fontSize": 16,
        "fontWeight": 500,
        "lineHeight": 1.5,
        "letterSpacing": 0
      },
      "colors": {
        "background": "surface-primary",
        "color": "text-primary",
        "border": "border-default"
      },
      "effects": {
        "borderRadius": 12,
        "boxShadow": "0px 1px 3px 0px rgba(0,0,0,0.1)"
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
  },
  "states": {
    "hover": {
      "effects": {
        "boxShadow": "0px 4px 6px 0px rgba(0,0,0,0.1)"
      }
    }
  },
  "semanticTokens": {
    "colors": [
      "surface-primary",
      "text-primary",
      "border-default"
    ],
    "spacing": [
      "spacing-6",
      "spacing-7"
    ],
    "typography": [
      "text-base",
      "font-medium"
    ],
    "effects": [
      "shadow-sm",
      "shadow-md",
      "radius-xl"
    ]
  }
}
```

## Best Practices

1. **Always validate Figma URLs** before extraction
2. **Handle missing node IDs gracefully** (extract whole page if needed)
3. **Cache extracted data** to avoid repeated API calls
4. **Normalize breakpoint names** for consistency
5. **Preserve semantic token names** when available
6. **Document extraction strategy used** in output
7. **Handle partial data** - some properties may be undefined
8. **Log warnings** for unexpected Figma structures
9. **Provide fallbacks** for missing data
10. **Validate extracted data** before passing to adapters
