# Phase 2: Design System Detection & Mapping

## Process

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

2. Load appropriate adapter (see [adapters/](adapters/) directory):
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

## Output

**File:** `design-system-mapping.json`

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
