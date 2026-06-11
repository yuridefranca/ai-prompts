# Styled Components Adapter

## Detection

**Detects:**
- `styled-components` in package.json
- `import styled from 'styled-components'` in files

## Mapping Rules

**Maps:**
- Theme tokens → `${props => props.theme.colors.primary}`
- Spacing → `${props => props.theme.spacing[4]}`
- Breakpoints → `@media (min-width: ${props => props.theme.breakpoints.md})`

## Example Output

```typescript
const UserCard = styled.div`
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing[7]};
  width: 100%;
  max-width: 351px;

  @media (min-width: ${props => props.theme.breakpoints.tablet}) {
    flex-direction: row;
    gap: 8.512px; // No exact token, use literal
    max-width: none;
  }
`;
```
