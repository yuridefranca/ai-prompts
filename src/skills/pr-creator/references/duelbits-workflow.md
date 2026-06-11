# Duelbits PR Workflow

Handles PR creation for Duelbits organization with specific conventions for task categories, projects, and base branches.

## Task Categories

Duelbits uses the following task category prefixes in branch names:

- **CORE** - Core functionality tasks
- **SUP** - Support tasks
- **CAS** - Casino-related tasks
- **SPB** - Sportsbook-related tasks

## Projects

### Multi Wallet (MW)
- **Branch pattern**: Contains `mw` or `MW-` in the name
- **Project abbreviation**: `[MW1]` (used in PR title)
- **Example branches**: `MW-142-wallet-switcher`, `mw/feature-login`

### World Cup Jackpot (WCJ)
- **Branch pattern**: Contains `wcj` or `WCJ-` in the name
- **Project abbreviation**: `[WCJ]` (used in PR title)
- **Example branches**: `WCJ-45-jackpot-display`, `wcj/fix-timer`

## Jira Integration

Branches created using Jira utility have the ticket number as a prefix. This ticket number must be:
- Extracted from the branch name
- Included in the PR title
- Referenced in the PR body

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

### Step 2: Detect Repository Type

**Load and follow**: `repository-detection.md`

**Determines**: `frontend` or `backend`

This is critical because the same project may have different base branches for frontend and backend repositories.

**Examples**:
- `duelbits-frontend` → frontend
- `duelbits-backend` → backend

**Store result** as `repositoryType` for use in Step 4.

### Step 3: Detect Project

**Branch name pattern matching** (see `helpers.js` for implementation):

**Patterns**:
- Multi Wallet: `mw`, `MW-`, `multi-wallet`
- World Cup Jackpot: `wcj`, `WCJ-`, `world-cup`

**If pattern detected**: Ask user for confirmation

```
I detected this branch might be for the "{projectName}" project.

Is this correct?
- Yes, it's {projectName}
- No, it's a different project (specify)
- Not part of any specific project
```

**If no pattern detected**: Ask user

```
Which project is this PR for?
- Multi Wallet
- World Cup Jackpot
- Other (specify)
- Not part of any specific project
```

**Store result** as `project` for use in Step 4.

### Step 4: Determine Base Branch

**Base branch rules** (repository-specific, see `helpers.js` for implementation):

| Project | Frontend Base | Backend Base |
|---------|---------------|--------------|
| Multi Wallet | `develop-multi-wallet-fe` | `develop-multi-wallet-be` |
| World Cup Jackpot | `develop-wcj-fe` | `develop-wcj-be` |
| Default (no project) | `develop` | `develop` |

**Determine base branch**:
- Use `repositoryType` (from Step 2) + `project` (from Step 3)
- Look up in table above

**Examples**:
- Frontend + Multi Wallet → `develop-multi-wallet-fe`
- Backend + World Cup Jackpot → `develop-wcj-be`
- Frontend + No project → `develop`
 with user**:
```
I'll create a PR with these settings:
- Repository: {repositoryType}
- Current branch: {currentBranch}
- Base branch: {baseBranch}
- Project: {projectName}

Proceed?
- Yes
- No, change base branch to: _____
```

### Step 5: Extract Task Information

**Parse branch name for ticket** (Jira creates branches with ticket prefix)

See `helpers.js` → `extractTicket()` for implementation.

**Extraction logic**:
- Match pattern: `(CORE|SUP|CAS|SPB|MW|WCJ)-(\d+)`
- Extract category, number, and full ticket ID

**Example extractions**:
- `CORE-456-fix-payment` → `CORE-456`
- `MW-142-wallet-switcher` → `MW-142`
- `SUP-123-support-task` → `SUP-123`

**Store result** as `ticketNumber` for use in title and template.

### Step 5.1: Fetch Jira Ticket Information (Optional)

**If Atlassian MCP is available**, try to fetch ticket details from Jira.

**Check for Atlassian MCP**:
```bash
# MCP should be configured in .vscode/mcp.json or similar
# com.atlassian/atlassian-mcp-server
```

**If MCP is available and running**:

1. **Fetch ticket details** using the ticket number from Step 5:
   - Ticket title/summary
   - Ticket description
   - Ticket status
   - Ticket type (Bug, Story, Task, etc.)

2. **Use fetched data**:
   - Use Jira ticket title for PR title (more accurate than branch name)
   - Optionally suggest using Jira description for PR description (if concise)
   - Verify ticket exists and is valid

3. **Handle errors gracefully**:
   - If MCP fails or ticket not found, fall back to branch name extraction
   - If MCP not configured, skip this step silently

**If MCP not available**:
- Skip to Step 6 (use branch name for title generation)

**Example Jira fetch**:
```
Fetching Jira ticket: MW-142...
✓ Found: "Implement wallet switching functionality"
  Type: Story
  Status: In Progress
  
Using Jira title for PR.
```

**Benefits of Jira MCP**:
- ✅ Accurate ticket titles (no guessing from branch names)
- ✅ Can copy ticket description if it's concise
- ✅ Validates ticket exists before creating PR
- ✅ Gets ticket type to potentially auto-fill PR template sections

### Step 6: Create PR Title

**Format**: `[TICKET-NUMBER] [PROJECT-ABBREV?] {Title}`

See `helpers.js` → `generatePRTitle()` for implementation.

**Components**:
- `[TICKET-NUMBER]` - Required (e.g., `[SUP-123]`, `[MW-142]`)
- `[PROJECT-ABBREV]` - Optional, only for project-specific tickets
  - Multi Wallet → `[MW1]`
  - World Cup Jackpot → `[WCJ]`
- `{Title}` - Jira ticket title or concise branch description

**Title generation strategy** (in priority order):
1. **Use Jira ticket title** (from Step 5.1 if MCP available)
2. Extract from branch name (see `helpers.js` → `branchToTitle()`)
3. Ask user for concise title if unclear

**Examples**:
- Jira fetch: `MW-142` → "Implement wallet switching functionality" → `[MW-142] [MW1] Implement wallet switching functionality`
- Branch extraction: `SUP-123-support-issue` → `[SUP-123] Support issue`
- Branch extraction: `SPB-456-wcj-jackpot` → `[SPB-456] [WCJ] Jackpot display`
- Branch extraction: `CORE-789-api-fix` → `[CORE-789] API fix`

### Step 7: Find and Fill PR Template

**Search for PR template in repository**:

```bash
# Check common template locations
.github/pull_request_template.md
.github/PULL_REQUEST_TEMPLATE.md
docs/pull_request_template.md
PULL_REQUEST_TEMPLATE.md
pull_request_template.md
```

**If template found**: Read it and use its exact structure

**If no template found**: Ask user if there's a custom location or use generic template

**CRITICAL RULES FOR ALL TEMPLATES**:

1. ✅ Keep description SHORT (2-3 sentences max)
2. ✅ Fill ONLY the sections in the template
3. ✅ DO NOT add extra sections
4. ✅ DO NOT remove template comments (<!-- -->)
5. ✅ DO NOT modify template structure
6. ✅ Check dependency/checkbox items ONLY if applicable
7. ✅ Keep it concise and relevant

**Description format**:
```
This PR implements [feature/fix] by [approach].
```

**Common template sections** (Duelbits):

**Frontend templates typically have**:
- Related Tickets
- Description
- Dependencies (BE/Contentful/Translation)
- Screenshots

**Backend templates typically have**:
- Related Tickets
- Description
- Apps Affected (microservices list)
- Database migrations checkbox
- Dependencies (FE/Translation)

**Smart description filling**:
- If Jira description was fetched (Step 5.1) and is concise (< 3 sentences), suggest using it
- Otherwise, write a new SHORT description (2-3 sentences)
- User can always override with custom description

### Step 8: Generate QA Notes (For Chat Only)

**⚠️ IMPORTANT: QA Notes are ONLY shown in the chat, NEVER added to the PR description**

Generate QA handover notes following the guidelines from the Duelbits QA process and display them in the chat for the developer to copy if needed.

See `qa-notes-generator.md` for detailed generation rules.

**Output in chat**:
```markdown
✅ Pull Request created successfully!

🔗 PR URL: {prUrl}

---

### QA Handover Notes (for your reference - NOT included in PR)

**Environment**: Dev environment ({branchName} preview)

**Technical Changes**:
{List key technical changes}

**Impacted Areas**:
{List affected components/features}

**Testing Considerations**:
{Any special testing requirements or limitations}

**Verification**:
{Screenshot or recording showing core functionality working}

---

You can copy these notes to add as a comment on the Jira ticket if needed.
```

## Evals

- [ ] Remote branch status verified (branch pushed)
- [ ] Repository type detected (frontend or backend)
- [ ] Project detected or user confirmed (if applicable)
- [ ] Base branch determined correctly (repository-specific)
- [ ] Ticket number extracted from Jira branch name
- [ ] Jira MCP checked for availability (if configured)
- [ ] Jira ticket fetched successfully (if MCP available) or gracefully skipped
- [ ] PR title follows format: `[TICKET] [PROJECT?] Title`
- [ ] PR title uses Jira ticket title if available, branch name otherwise
- [ ] Project abbreviation included if applicable ([MW1], [WCJ])
- [ ] PR template found in repository
- [ ] PR template structure preserved exactly
- [ ] PR description is SHORT (2-3 sentences max)
- [ ] PR description uses Jira description if concise, or written manually
- [ ] Only template sections present (no extras)
- [ ] Template comments (<!-- -->) preserved
- [ ] Dependency/checkbox items checked appropriately
- [ ] QA notes generated in chat ONLY
- [ ] QA notes NOT added to PR description
## Jira MCP Integration

This workflow supports optional Jira integration via Atlassian MCP server.

**Configuration**: Check for MCP server at `com.atlassian/atlassian-mcp-server` in `.vscode/mcp.json`

**Benefits**:
- Automatic ticket title retrieval (more accurate than branch names)
- Ticket description for PR description suggestions
- Ticket type validation
- Ticket status verification

**Graceful degradation**: If MCP is not available or fails, the workflow falls back to:
- Branch name parsing for titles
- Manual description writing
- No ticket validation

**MCP Tools** (if available):
- Search for and load Jira MCP tools before attempting to fetch
- Use ticket search/fetch functionality
- Handle authentication errors gracefully

## Helper Scripts

Code functions have been moved to `helpers.js` for better maintainability:

- `detectRepositoryType()` - Detects frontend vs backend
- `detectProject()` - Detects project from branch name
- `extractTicket()` - Extracts Jira ticket from branch
- `determineBaseBranch()` - Determines base branch by repo type and project
- `generatePRTitle()` - Generates formatted PR title
- `branchToTitle()` - Converts branch name to readable title

## Evals

- [ ] Remote branch status verified (branch pushed)
- [ ] Repository type detected (frontend or backend)
- [ ] Project detected or user confirmed (if applicable)
- [ ] Base branch determined correctly (repository-specific)
- [ ] Ticket number extracted from Jira branch name
- [ ] PR title follows format: `[TICKET] [PROJECT?] Title`
- [ ] Project abbreviation included if applicable ([MW1], [WCJ])
- [ ] Correct PR template used (frontend vs backend)
- [ ] PR description is SHORT (2-3 sentences max)
- [ ] Only template sections present (no extras)
- [ ] Template structure NOT modified
- [ ] Template comments preserved
- [ ] Dependency boxes checked appropriately
- [ ] Apps Affected checked (backend only)