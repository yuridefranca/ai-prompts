# Phase 3: Responsive Code Generation

## Critical Notes

Code generation follows **mobile-first approach** by default:

- Base styles = mobile breakpoint
- Responsive overrides for larger screens using breakpoint prefixes
- Order: mobile (base) → tablet → desktop → wide

## Process

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

## Output

**File:** Component code file (e.g., `UserCard.tsx`)
