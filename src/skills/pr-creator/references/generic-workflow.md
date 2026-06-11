# Generic GitHub PR Workflow

Standard GitHub Pull Request creation workflow for non-organization-specific repositories.

## Process

### Step 1: Check Remote Branch Status

**Verify current branch is pushed**:

```bash
git branch --show-current
git ls-remote --heads origin $(git branch --show-current)
```

**If not pushed**:
```
⚠️ Current branch has not been pushed to remote yet.

Push the branch first:
git push -u origin {branchName}
```

**If pushed**: Proceed to Step 2

### Step 2: Determine Base Branch

**Auto-detect default branch**:

```bash
git remote show origin | grep 'HEAD branch' | cut -d' ' -f5
```

**Common defaults**:
- `main`
- `master`
- `develop`

**Confirmation**:
```
I detected the default branch as: {defaultBranch}

Use this as the base branch for your PR?
- Yes, use {defaultBranch}
- No, specify custom base: _____
```

### Step 3: Create PR Title

**Suggestions** (in order of preference):

1. **From recent commits**: Use the most recent meaningful commit message
2. **From branch name**: Convert branch name to readable title
3. **Ask user**: Request custom title

**Branch name to title conversion**:
```typescript
function branchToTitle(branchName: string): string {
  // feature/add-dark-mode → Add dark mode
  // fix/payment-bug → Fix payment bug
  // 123-user-authentication → User authentication
  
  return branchName
    .replace(/^(feature|fix|bugfix|hotfix|chore)\//, '')
    .replace(/^\d+-/, '')
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}
```

**Confirmation**:
```
Suggested PR title: "{suggestedTitle}"

Use this or provide a custom title:
- Use suggested title
- Custom: _____
```

### Step 4: Find and Fill PR Template

**Search for PR template**:

```bash
# Check common locations
.github/pull_request_template.md
.github/PULL_REQUEST_TEMPLATE.md
docs/pull_request_template.md
PULL_REQUEST_TEMPLATE.md
```

**If template found**: Use it and fill relevant sections
**If no template found**: Use generic template

### Generic PR Template

```markdown
## Description

{Summary of changes}

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Changes Made

{Bullet points of key changes}

## Testing

{How the changes were tested}

## Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [ ] No new warnings generated
- [ ] Tests added/updated (if applicable)
- [ ] All tests passing
```

### Step 5: Gather Change Information

**Get changed files**:

```bash
git diff --name-only {baseBranch}...HEAD
```

**Categorize changes**:
- New files created
- Modified files
- Deleted files

**Get commit messages**:

```bash
git log {baseBranch}..HEAD --oneline
```

### Step 6: Fill PR Description

**Auto-fill strategy**:

1. **Description**: Summarize based on commits and changed files
2. **Type of Change**: Best guess from branch name and changes
   - `fix/*` or `bugfix/*` → Bug fix
   - `feature/*` → New feature
   - `docs/*` → Documentation update
   - `refactor/*` → Refactoring
3. **Changes Made**: List changed files with brief description
4. **Testing**: Mention if test files were added/modified

**Example filled template**:

```markdown
## Description

Adds dark mode support to the application with theme switching functionality. Users can toggle between light and dark themes via a new settings panel.

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)

## Changes Made

- Added ThemeProvider component
- Created theme toggle button in settings
- Updated CSS variables for dark mode colors
- Added theme persistence to localStorage
- Updated 12 components to support theme switching

## Testing

- Added unit tests for ThemeProvider (8 tests)
- Manually tested theme switching across all pages
- Verified theme persistence after page reload

## Checklist

- [x] Code follows the project's style guidelines
- [x] Self-review completed
- [x] Comments added for complex logic
- [ ] Documentation updated (if applicable)
- [x] No new warnings generated
- [x] Tests added/updated (if applicable)
- [x] All tests passing
```

**Keep it concise**: Focus on what changed and why, not implementation details.

### Step 7: Create Pull Request

**Use GitHub CLI or MCP**:

```bash
gh pr create \
  --base {baseBranch} \
  --title "{prTitle}" \
  --body "{prDescription}"
```

**Or via GitHub MCP tool** (if available)

### Step 8: Return Success

```markdown
✅ Pull Request created successfully!

🔗 PR URL: {prUrl}

**Summary**:
- Title: {prTitle}
- Base: {baseBranch} ← {currentBranch}
- Files changed: {fileCount}
- Commits: {commitCount}

**Next Steps**:
1. Review the PR on GitHub
2. Request reviews from team members
3. Monitor CI/CD checks
4. Address review comments if any
5. Merge when approved
```

## Evals

- [ ] Remote branch status verified (branch pushed)
- [ ] Default branch detected correctly
- [ ] PR title is clear and descriptive
- [ ] PR template located (or generic used)
- [ ] Changed files listed accurately
- [ ] Type of change selected appropriately
- [ ] Description is concise but informative
- [ ] Testing section filled if tests exist
- [ ] PR created successfully
- [ ] PR URL returned to user
