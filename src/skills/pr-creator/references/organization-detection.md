# Organization Detection

Detects whether the repository belongs to a specific organization (Duelbits) or uses generic GitHub workflows.

## Detection Strategy

**Priority order** (first match wins):

1. **Git remote URL analysis**
2. **Manual user confirmation** (if uncertain)

## Implementation

### Step 1: Check Git Remote

```bash
git remote get-url origin
```

**Expected outputs**:
- `git@github.com:duelbits/*` or `https://github.com/duelbits/*` → **Duelbits**
- `git@github.com:yuridefranca/*` or other organizations → **Generic**

### Step 2: Extract Organization

```typescript
function detectOrganization(remoteUrl: string): string {
  // SSH format: git@github.com:organization/repo.git
  // HTTPS format: https://github.com/organization/repo.git
  
  const sshMatch = remoteUrl.match(/git@github\.com:([^/]+)\//);
  const httpsMatch = remoteUrl.match(/github\.com\/([^/]+)\//);
  
  const org = sshMatch?.[1] || httpsMatch?.[1];
  
  if (org === 'duelbits') {
    return 'duelbits';
  }
  
  return 'generic';
}
```

## Output

Returns one of:
- `duelbits` → Use Duelbits-specific workflow
- `generic` → Use generic GitHub workflow

## Uncertainty Handling

If organization cannot be detected from remote:

```
I couldn't determine the repository organization from the git remote.

Remote URL: {remoteUrl}

Is this repository part of Duelbits organization?
- Yes (use Duelbits workflow)
- No (use generic GitHub workflow)
```
