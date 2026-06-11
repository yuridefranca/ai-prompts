# PR Creator Reference Files

This directory contains modular reference files used by the PR Creator skill. Each file handles a specific aspect of the PR creation workflow.

## File Structure

### organization-detection.md
**Purpose**: Detects whether the repository belongs to Duelbits or uses generic GitHub workflows.

**Key responsibilities**:
- Analyzes git remote URL
- Identifies organization from remote path
- Returns `duelbits` or `generic`

**When loaded**: First step after user confirms PR creation

---

### repository-detection.md
**Purpose**: Detects whether the Duelbits repository is frontend or backend.

**Key responsibilities**:
- Checks package.json name
- Analyzes directory structure
- Returns `frontend` or `backend`

**When loaded**: When organization detection returns `duelbits` (Step 2 of Duelbits workflow)

---

### duelbits-workflow.md
**Purpose**: Handles PR creation for Duelbits organization with specific conventions.

**Key responsibilities**:
- Verifies branch pushed to remote
- Detects repository type (frontend/backend)
- Detects project (Multi Wallet, World Cup Jackpot, etc.)
- Determines base branch based on repository + project
- Extracts task category and ticket number
- Selects appropriate PR template
- Creates short, direct PR descriptions
- Enforces template rules (no modifications)

**When loaded**: When organization detection returns `duelbits`

**Important rules**:
- Keep PR description SHORT (2-3 sentences)
- DO NOT modify template structure or comments
- DO NOT add extra sections
- Generate QA notes separately (see qa-notes-generator.md)
- Try to fetch Jira ticket info via Atlassian MCP if available
- Gracefully degrade if MCP not available

---

### generic-workflow.md
**Purpose**: Standard GitHub PR workflow for non-Duelbits projects.

**Key responsibilities**:
- Verifies branch pushed to remote
- Auto-detects default branch (main/master)
- Finds and fills PR template
- Lists changed files
- Creates comprehensive PR description

**When loaded**: When organization detection returns `generic`

---

### qa-notes-generator.md
**Purpose**: Generates QA handover notes for Duelbits projects following their QA process guidelines.

**Key responsibilities**:
- Lists technical changes
- Identifies impacted areas
- Provides testing considerations
- Includes HOW to test instructions
- Requests verification evidence

**When loaded**: AFTER PR is created (Duelbits only)

**⚠️ CRITICAL**: QA notes are ONLY shown in the chat for developer reference. They are NEVER added to the PR description.

---

### helpers.js
**Purpose**: Utility functions for PR creation logic (detection, formatting, etc.)

**Key responsibilities**:
- `detectRepositoryType()` - Detects frontend vs backend from package.json or directory structure
- `detectProject()` - Detects project from branch name patterns
- `extractTicket()` - Extracts Jira ticket number from branch name
- `determineBaseBranch()` - Determines base branch based on repository type and project
- `generatePRTitle()` - Generates formatted PR title with proper brackets
- `branchToTitle()` - Converts branch name to readable title

**When loaded**: Referenced throughout Duelbits workflow for implementation details

**Note**: These are reference implementations. Adapt the logic as needed for your AI workflow.

---

## Usage Flow

```
User requests PR creation
         ↓
Load: organization-detection.md
         ↓
    Duelbits?
    /        \
  Yes        No
   ↓          ↓
repository- generic-
detection.md workflow.md
   ↓
duelbits-
workflow.md
   ↓
Extract ticket number
from branch name
   ↓
Try to fetch from Jira MCP
(if available)
   ├─ Success: Use Jira title & description
   └─ Not available: Use branch name
   ↓
Search for PR template
in repository
(.github/pull_request_template.md)
   ↓
Fill template with
project-specific data
   ↓
PR created
   ↓
qa-notes-
generator.md
(chat only)
```

## Maintenance

When updating PR creation logic:

1. **Organization-specific changes**: Update `duelbits-workflow.md` or `generic-workflow.md`
2. **Detection logic changes**: Update `organization-detection.md` or `repository-detection.md`
3. **QA notes changes**: Update `qa-notes-generator.md`
4. **Helper function changes**: Update `helpers.js`
5. **New organization support**: Create new workflow file and update main SKILL.md
6. **New project support**: Update project detection in `helpers.js` and add base branch rules

## Testing Checklist

When making changes, verify:

- [ ] Organization detection works for all remotes
- [ ] Repository detection works for frontend and backend
- [ ] Base branch correctly determined for repo type + project
- [ ] Jira MCP integration checked (graceful degradation if not available)
- [ ] Jira ticket fetching works when MCP is available
- [ ] Fallback to branch name parsing when Jira MCP unavailable
- [ ] PR title uses Jira ticket title when available
- [ ] PR template found in repository (not hardcoded)
- [ ] Duelbits workflow enforces all critical rules
- [ ] Generic workflow handles standard GitHub repos
- [ ] QA notes generated in chat only (never in PR)
- [ ] Helper functions are referenced (not duplicated) in markdown files
- [ ] All file references in main SKILL.md are correct
