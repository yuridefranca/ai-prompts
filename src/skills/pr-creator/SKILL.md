---
name: pr-creator
aliases:
    - github-pr-creator
description: Create GitHub Pull Request with project-specific rules and conventions. Supports custom base branch detection, PR templates, and organization-specific workflows. Use after code review phase when feature/fix is ready to merge. Handles duelbits and generic GitHub projects. Keywords pull request, GitHub PR, code submission, merge request, duelbits, base branch, PR template.
---

# PR Creator

Create well-structured GitHub Pull Requests following project-specific conventions and templates. Automatically detects project configuration and applies appropriate rules for base branch selection, PR formatting, and ticket linking.

## When to Use

- After code review phase (final step in workflows)
- All tests passing and code approved
- Ready to submit work for merge
- Feature complete or bug fixed

**Do NOT use**:

- Before code review
- When tests are failing
- For work-in-progress (unless creating draft PR)

## Project-Specific Configuration

This skill supports different workflows for different projects/organizations.

### Configuration Detection Strategy

**Priority order** (first match wins):

1. **Project config file**: `.github/ai-pr-config.json` in repository root
2. **Git remote detection**: Check origin URL for known organizations
3. **Generic fallback**: Standard GitHub workflow

### Supported Project Configurations

#### Duelbits Projects

**Detection**: Git remote contains `duelbits` or config file has `"organization": "duelbits"`

**Special rules**:

- Branch naming patterns determine base branch
- Jira ticket integration
- Multi-repo project detection (frontend/backend/chadmin)
- Specific base branch conventions

#### Generic Projects

**Detection**: No special markers found

**Rules**:

- Standard base branch (main/master)
- Generic PR template
- No ticket linking

## Process

### Step 0: Ask User Confirmation

**⚠️ ALWAYS ASK BEFORE CREATING PR**

```markdown
Your code is ready for review. Would you like me to create a GitHub Pull Request?

- Yes, create a PR
- No, I'll create it manually later
```

**If user says no**: Stop here and provide instructions for manual PR creation.

**If user says yes**: Proceed to Step 1.

### Step 1: Detect Version Control Platform

**Currently supported**: GitHub only

```bash
# Check git remote
git remote -v
```

**If GitHub detected**: Proceed to Step 2
**If not GitHub**: Inform user that only GitHub is currently supported

### Step 2: Load Project Configuration

**Check for configuration file** (`.github/ai-pr-config.json`):

```json
{
	"organization": "duelbits",
	"baseBranchRules": [
		{
			"pattern": "MW-\\d+",
			"baseByProject": {
				"frontend": "MW-143-FE-prerequisite",
				"backend": "MW-1-Multi-Wallet-Phase-1",
				"chadmin": "MW-1-Multi-Wallet-Phase-1"
			}
		},
		{
			"pattern": "(SUP|CORE)-\\d+",
			"base": "release/${YYYYMMDD}"
		}
	],
	"jiraUrl": "https://duelbits.atlassian.net/browse",
	"requiresTicketLink": true,
	"prTemplate": ".github/pull_request_template.md"
}
```

**If config file exists**: Use its rules
**If no config file**: Detect from git remote

**Built-in organization presets**:

```typescript
const ORGANIZATION_PRESETS = {
	duelbits: {
		baseBranchRules: [
			{
				pattern: /MW-\d+/,
				baseByProject: {
					frontend: 'MW-143-FE-prerequisite',
					backend: 'MW-1-Multi-Wallet-Phase-1',
					chadmin: 'MW-1-Multi-Wallet-Phase-1',
				},
			},
			{
				pattern: /(SUP|CORE)-\d+/,
				base: 'release/${YYYYMMDD}',
			},
		],
		jiraUrl: 'https://duelbits.atlassian.net/browse',
		requiresTicketLink: true,
	},

	generic: {
		baseBranchRules: [
			{ pattern: /.*/, base: 'main' }, // Auto-detect main/master
		],
		requiresTicketLink: false,
	},
};
```

### Step 3: Detect Current Branch and Project Type

**Get current branch**:

```bash
git branch --show-current
```

**Detect project type** (for multi-repo organizations):

**Method 1: Check config file**:

```json
{
	"projectType": "frontend"
}
```

**Method 2: Check package.json**:

```json
{
	"name": "duelbits-frontend",
	"ai-config": { "projectType": "frontend" }
}
```

**Method 3: Analyze directory structure**:

- **Frontend**: Has `src/components/`, React/Vue imports
- **Backend**: Has `src/controllers/`, `src/services/`, NestJS modules
- **Chadmin**: Specific admin panel structure

**Method 4: Ask user**:

```
I couldn't auto-detect the project type. Is this:
1. Frontend
2. Backend
3. Admin (chadmin)
4. Other
```

**Store**: `currentBranch`, `projectType`

### Step 4: Determine Base Branch

**Apply configuration rules**:

```typescript
function determineBaseBranch(currentBranch: string, projectType: string, config: ProjectConfig): string | null {
	for (const rule of config.baseBranchRules) {
		const pattern = new RegExp(rule.pattern);

		if (pattern.test(currentBranch)) {
			// Rule matches current branch

			if (rule.baseByProject) {
				// Multi-project rule
				return rule.baseByProject[projectType];
			}

			if (rule.base) {
				// Static base or template
				let base = rule.base;

				// Handle date template
				if (base.includes('${YYYYMMDD}')) {
					const today = new Date();
					const yyyymmdd = today.toISOString().slice(0, 10).replace(/-/g, '');
					base = base.replace('${YYYYMMDD}', yyyymmdd);
				}

				return base;
			}
		}
	}

	// No rule matched
	return null;
}
```

**Examples**:

```bash
# Branch: MW-142-wallet-switcher, Project: frontend
# Matches pattern: MW-\d+
# Returns: MW-143-FE-prerequisite

# Branch: CORE-456-fix-bug, Project: backend
# Matches pattern: (SUP|CORE)-\d+
# Returns: release/20260402 (today's date)

# Branch: feature/new-component, Project: frontend
# No pattern match
# Returns: null → Ask user
```

**If base branch determined**: Proceed to Step 5
**If null**: Ask user to provide base branch

### Step 5: Extract PR Information

**Get PR title**:

**Option 1: From specification** (feature workflow):

```
Feature: [Feature name from Phase 1]
```

**Option 2: From fix description** (improvement workflow):

```
Fix: [Issue description from Phase 1]
```

**Option 3: From branch name**:

```
MW-142-wallet-switcher → "MW-142: Wallet switcher"
```

**Option 4: Ask user**:

```
Suggested PR title: "Add wallet switcher component"
Use this title or provide a custom one:
```

**Extract ticket numbers** (if organization requires):

```typescript
// For Duelbits
const ticketPattern = /(MW|SUP|CORE)-\d+/g;
const tickets = currentBranch.match(ticketPattern);

// Result: ["MW-142"] or ["CORE-456"]
```

**Read PR template**:

```bash
# Check for template
if [ -f .github/pull_request_template.md ]; then
  # Use project template
else
  # Use generic template
fi
```

### Step 6: Check for Existing PR

**Search for existing PR** for current branch using GitHub MCP:

```typescript
const existingPR = await githubMcp.listPullRequests({
	owner: repoOwner,
	repo: repoName,
	head: `${repoOwner}:${currentBranch}`,
	state: 'open',
});
```

**If PR exists**:

```markdown
⚠️ A pull request already exists for this branch:

🔗 PR #123: https://github.com/{owner}/{repo}/pull/123

Would you like to:

1. Update the existing PR description
2. Cancel PR creation
```

**If no PR exists**: Proceed to Step 7

### Step 7: Fill PR Template

**Parse template and extract sections**:

```markdown
## Description

<!-- Fill this section -->

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change

## Related Tickets

<!-- Link tickets here -->

## Changes Made

<!-- List changes -->

## Testing

<!-- Describe testing -->

## Checklist

- [ ] Tests added
- [ ] Documentation updated
```

**Auto-fill based on workflow type**:

#### For Feature Workflow

```markdown
## Description

{Specification from Phase 1}

## Type of Change

- [x] New feature
- [ ] Bug fix
- [ ] Breaking change

## Related Tickets

{Extract from branch: [MW-142](https://duelbits.atlassian.net/browse/MW-142)}

## Changes Made

- {Summary from implementation phases}
- {List of files changed}

## Testing

- Unit tests: {Test count} tests passing
- Integration tests: {Test count} tests passing
- Manual testing: {From Phase 6}

## Checklist

- [x] Code follows project style guidelines
- [x] Tests added and passing
- [x] Documentation updated
- [x] Self-review completed
```

#### For Improvement Workflow

```markdown
## Description

Fixes: {Issue description from Phase 1}

Root cause: {From Phase 3 root cause analysis}

## Type of Change

- [ ] New feature
- [x] Bug fix
- [ ] Breaking change

## Related Tickets

{Extract from branch}

## Changes Made

- {Fix description from Phase 4}
- {Files modified}

## Testing

- Unit tests: Added regression test
- Integration tests: {Test count} tests passing
- Verification: {From Phase 7}

## Checklist

- [x] Bug fix does not introduce regressions
- [x] Tests added for bug scenario
- [x] Root cause addressed
- [x] Code reviewed
```

**Project-specific template filling**:

#### Duelbits

```markdown
## Related Tickets

[CORE-123](https://duelbits.atlassian.net/browse/CORE-123)

## QA Notes

{Additional notes if template requires}
```

#### Generic

```markdown
## Related Issues

Closes #123
Fixes #456
```

### Step 8: Create Pull Request

**Use GitHub MCP tool**:

```typescript
const pr = await githubMcp.createPullRequest({
	owner: repoOwner,
	repo: repoName,
	title: prTitle,
	body: filledTemplate,
	head: currentBranch,
	base: baseBranch,
	draft: isDraft, // Ask user if they want draft PR
});
```

**Ask about draft status**:

```
Should this PR be created as a draft?
- No, create as ready for review (default)
- Yes, create as draft
```

**Capture response**:

- PR URL: `pr.html_url`
- PR number: `pr.number`

### Step 9: Return PR URL and Summary

**Success message**:

```markdown
✅ Pull Request created successfully!

🔗 **PR URL**: https://github.com/{owner}/{repo}/pull/{number}

**Summary**:

- **Title**: {prTitle}
- **Base**: {baseBranch} ← {currentBranch}
- **Status**: Open {draft ? "(Draft)" : ""}
- **Organization**: {orgName}
- **Configuration**: {configSource}

**Linked Tickets**:
{tickets.map(t => `- ${t}: ${jiraUrl}/${t}`).join('\n')}

**Next Steps**:

1. Review the PR description on GitHub
2. Request reviews from team members
3. Monitor CI/CD checks
4. Address any review comments
5. Merge when approved

{isDraft ? "💡 Remember to mark as 'Ready for Review' when ready!" : ""}
```

**If user declined PR creation**:

````markdown
No problem! You can create the PR manually when ready.

**Suggested PR details**:

- **Base branch**: {baseBranch}
- **Title**: {suggestedTitle}
- **Description**: See {prTemplate}

**Manual creation command**:

```bash
gh pr create --base {baseBranch} --title "{title}" --body-file pr-description.md
```
````

````

## Configuration File Schemas

### Project Config (.github/ai-pr-config.json)

```json
{
  "organization": "duelbits",
  "projectType": "frontend",
  "baseBranchRules": [
    {
      "pattern": "MW-\\d+",
      "baseByProject": {
        "frontend": "MW-143-FE-prerequisite",
        "backend": "MW-1-Multi-Wallet-Phase-1",
        "chadmin": "MW-1-Multi-Wallet-Phase-1"
      }
    },
    {
      "pattern": "(SUP|CORE)-\\d+",
      "base": "release/${YYYYMMDD}",
      "requiresDate": true
    },
    {
      "pattern": "hotfix-.*",
      "base": "production"
    }
  ],
  "jiraUrl": "https://duelbits.atlassian.net/browse",
  "requiresTicketLink": true,
  "prTemplate": ".github/pull_request_template.md",
  "defaultBase": "master",
  "extends": "https://raw.githubusercontent.com/duelbits/ai-configs/main/pr-config.json"
}
````

**Schema explanation**:

- `organization`: Preset name or custom organization identifier
- `projectType`: Force specific project type (frontend/backend/chadmin)
- `baseBranchRules`: Array of branch pattern matching rules
    - `pattern`: Regex pattern to match branch names
    - `base`: Static base branch name (supports ${YYYYMMDD} template)
    - `baseByProject`: Map of project types to base branches
    - `requiresDate`: Whether to inject current date
- `jiraUrl`: Base URL for Jira ticket linking
- `requiresTicketLink`: Whether ticket links are required in PR
- `prTemplate`: Path to PR template file
- `defaultBase`: Fallback base branch if no rules match
- `extends`: URL to remote configuration file (loads and merges)

### Shared Organization Config

**Organization can host shared config**:

```javascript
// https://github.com/duelbits/ai-configs/blob/main/pr-config.json
{
  "organization": "duelbits",
  "baseBranchRules": [
    { "pattern": "MW-\\d+", "baseByProject": {...} },
    { "pattern": "(SUP|CORE)-\\d+", "base": "release/${YYYYMMDD}" }
  ],
  "jiraUrl": "https://duelbits.atlassian.net/browse",
  "requiresTicketLink": true
}
```

**Projects reference it**:

```json
{
	"extends": "https://raw.githubusercontent.com/duelbits/ai-configs/main/pr-config.json",
	"projectType": "frontend"
}
```

**Benefits**:

- ✅ Single source of truth for organization rules
- ✅ Projects only need to specify project type
- ✅ Updates propagate to all projects
- ✅ Version control for config changes

## Project Type Detection

**Detection methods** (in priority order):

### 1. Config File

```json
{
	"projectType": "frontend"
}
```

### 2. Package.json

```json
{
	"name": "duelbits-frontend",
	"ai-config": {
		"projectType": "frontend"
	}
}
```

### 3. Directory Structure Analysis

```typescript
function detectProjectType(): string {
	// Frontend indicators
	if (exists('src/components') || exists('src/views')) {
		if (hasReactImports() || hasVueImports()) {
			return 'frontend';
		}
	}

	// Backend indicators
	if (exists('src/controllers') || exists('src/services')) {
		if (hasNestJSModules()) {
			return 'backend';
		}
	}

	// Admin panel indicators
	if (exists('src/admin') || packageName.includes('admin')) {
		return 'chadmin';
	}

	return 'unknown';
}
```

### 4. Ask User

```
I couldn't determine the project type automatically.

Please select:
1. Frontend
2. Backend
3. Admin Panel (chadmin)
4. Other (will use generic rules)
```

## Uncertainty Handling

**Base branch cannot be determined**:

```
I couldn't determine the base branch automatically.

Current branch: {currentBranch}
Detected organization: {org}

Please provide the base branch (e.g., master, develop, release/20260402):
```

**Project type unclear**:

```
Project type detection failed. Please specify:
- frontend
- backend
- chadmin
- other
```

**PR template not found**:

```
⚠️ No PR template found at .github/pull_request_template.md

I'll use a generic template. You can customize it on GitHub after creation.
```

**Confidence requirement**: Must be 100% certain before creating PR. When in doubt, ask user.

## Output

### Success Output

```markdown
✅ Pull Request #142 created successfully!

🔗 https://github.com/duelbits/frontend/pull/142

**Details**:

- Title: "MW-142: Add wallet switcher component"
- Base: MW-143-FE-prerequisite ← MW-142-wallet-switcher
- Status: Open
- Draft: No

**Tickets**:

- MW-142: https://duelbits.atlassian.net/browse/MW-142

**Configuration**:

- Source: Duelbits preset (auto-detected from git remote)
- Project type: frontend (detected from package.json)

**Next Actions**:

1. ✅ Review PR on GitHub
2. 🔍 Request reviews from: @lead-developer @tech-lead
3. ⚙️ Monitor CI/CD pipeline
4. 💬 Address review comments if any
5. 🎉 Merge when approved
```

### Declined Output

````markdown
No problem! You can create the PR manually when ready.

**Recommended PR Settings**:

- **Base branch**: MW-143-FE-prerequisite
- **Head branch**: MW-142-wallet-switcher (current)
- **Title**: "MW-142: Add wallet switcher component"

**Using GitHub CLI**:

```bash
gh pr create \
  --base MW-143-FE-prerequisite \
  --title "MW-142: Add wallet switcher component" \
  --body-file .github/pr-description.md
```
````

**Using GitHub Web**:

1. Go to: https://github.com/duelbits/frontend/compare/MW-143-FE-prerequisite...MW-142-wallet-switcher
2. Click "Create pull request"
3. Fill in details using .github/pull_request_template.md

```

## Evals

- [ ] User confirmation obtained before creating PR
- [ ] GitHub platform detected successfully
- [ ] Project configuration loaded (file, preset, or generic)
- [ ] Project type determined (auto-detect or user input)
- [ ] Base branch correctly determined using rules
- [ ] Current branch name extracted
- [ ] No existing PR found for current branch
- [ ] PR template located and parsed
- [ ] Ticket numbers extracted from branch (if applicable)
- [ ] Ticket links formatted correctly for organization
- [ ] PR template filled with workflow information
- [ ] PR created successfully via GitHub MCP
- [ ] PR URL returned to user
- [ ] Configuration source documented in output
- [ ] Next steps provided to user

## Common Patterns

### Pattern 1: Duelbits Frontend Feature

```

Branch: MW-142-wallet-switcher
Remote: git@github.com:duelbits/frontend.git

Detection:
✓ Organization: duelbits (from remote)
✓ Project: frontend (from package.json)
✓ Base: MW-143-FE-prerequisite (from MW-\d+ rule)

PR:

- Title: "MW-142: Wallet switcher"
- Ticket: [MW-142](https://duelbits.atlassian.net/browse/MW-142)

```

### Pattern 2: Duelbits Backend Hotfix

```

Branch: CORE-456-fix-payment-bug
Remote: git@github.com:duelbits/backend.git

Detection:
✓ Organization: duelbits
✓ Project: backend
✓ Base: release/20260402 (from (SUP|CORE)-\d+ rule with date)

PR:

- Title: "CORE-456: Fix payment processing bug"
- Ticket: [CORE-456](https://duelbits.atlassian.net/browse/CORE-456)

```

### Pattern 3: Generic Open Source Project

```

Branch: feature/add-dark-mode
Remote: git@github.com:some-org/cool-project.git

Detection:
✓ Organization: generic (no known org detected)
✓ Project: N/A (not needed for generic)
✓ Base: main (from generic preset)

PR:

- Title: "Add dark mode support"
- No ticket links

```

### Pattern 4: Custom Config Override

```

Branch: hotfix-payment-critical
.github/ai-pr-config.json:
{
"baseBranchRules": [
{ "pattern": "hotfix-.*", "base": "production" }
]
}

Detection:
✓ Config: Custom (from .github/ai-pr-config.json)
✓ Base: production (from custom rule)

PR:

- Base: production (urgent hotfix)

```

## Error Handling

### GitHub MCP Not Available

```

❌ GitHub MCP tools are not available.

To create PRs automatically, you need:

1. GitHub Copilot with MCP support
2. GitHub MCP server configured

Manual alternative: Use GitHub CLI or web interface

```

### Authentication Error

```

❌ GitHub authentication failed.

Please authenticate:

```bash
gh auth login
```

Or check your GitHub token configuration.

```

### PR Creation Failed

```

❌ Failed to create pull request.

Error: {error message}

Troubleshooting:

1. Check if base branch exists: {baseBranch}
2. Verify you have write access to repository
3. Ensure current branch is pushed to remote

Manual creation: gh pr create --base {baseBranch}

```

## Future Enhancements

**Phase 2** (Not implemented yet):
- GitLab support
- Bitbucket support
- Azure DevOps support
- Auto-assign reviewers based on CODEOWNERS
- Auto-apply labels based on changes
- Link to CI/CD pipeline results

**Phase 3** (Ideas):
- AI-generated PR description from commits
- Screenshot upload for UI changes
- Performance impact analysis in PR body
- Security scan results in PR comments
```
