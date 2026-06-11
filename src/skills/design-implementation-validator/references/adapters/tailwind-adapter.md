# Tailwind Adapter

## Detection

**Detects:**
- `tailwind.config.{js,ts,mjs,cjs}`
- `@tailwindcss/` in package.json

## Mapping Rules

**Maps:**
- Colors → `bg-{color}`, `text-{color}`, `border-{color}`
- Spacing → `p-{size}`, `m-{size}`, `gap-{size}`
- Typography → `text-{size}`, `font-{weight}`
- Arbitrary values → `gap-[8.512px]`
- Responsive → `md:`, `lg:`, `xl:` prefixes

## Config Parsing

```typescript
const config = require('./tailwind.config.js');
const theme = config.theme.extend || config.theme;

// Map Figma spacing to Tailwind scale
const spacing = theme.spacing;
// e.g., 16px → spacing[4] → class "gap-4"
```

## Example Output

```tsx
// Mobile-first responsive classes
<div className="
  flex flex-col gap-[28px] w-full max-w-[351px]
  md:flex-row md:gap-[8.512px] md:max-w-none
  lg:gap-8 lg:p-8
">
```
