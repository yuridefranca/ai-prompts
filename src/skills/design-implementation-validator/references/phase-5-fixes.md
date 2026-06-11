# Phase 5: Fix Generation & Self-Healing

## Process

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

## Output Template

See [assets/templates/validation-report-template.md](../assets/templates/validation-report-template.md) for the complete report format.

**File:** `validation-report.md`

Brief structure:
- Summary (total tests, pass/fail counts)
- Breakpoint results
- Acceptable deviations
- Applied fixes
- Design system updates suggested
- Next steps
