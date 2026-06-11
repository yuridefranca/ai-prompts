---
name: pr-creator
aliases:
    - github-pr-creator
description: Create GitHub Pull Request with organization-specific workflows. Detects Duelbits vs generic projects and applies appropriate conventions. Includes QA handover notes generation for Duelbits. Keywords pull request, GitHub PR, duelbits, base branch, QA notes.
---

# PR Creator

Create well-structured GitHub Pull Requests with organization-specific conventions. Automatically detects project type and applies appropriate workflow.

## When to Use

- After code review phase (final step in workflows)
- All tests passing and code approved
- Ready to submit work for merge
- Feature complete or bug fixed

**Do NOT use**:

- Before code review
- When tests are failing
- For work-in-progress (unless creating draft PR)

## High-Level Process

### Step 1: User Confirmation

**⚠️ ALWAYS ASK BEFORE CREATING PR**

```
Your code is ready for review. Would you like me to create a GitHub Pull Request?
- Yes, create a PR
- No, I'll create it manually later
```

**If no**: Provide manual PR creation instructions and stop.
**If yes**: Proceed to Step 2.

### Step 2: Detect Organization

Load and follow: **references/organization-detection.md**

**Determines**: `duelbits` or `generic`

### Step 3: Execute Workflow

**If Duelbits detected**:

- Load and follow: **references/duelbits-workflow.md**
- Includes optional Jira MCP integration for automatic ticket info fetching
- After PR created, load and follow: **references/qa-notes-generator.md**

**If Generic detected**:

- Load and follow: **references/generic-workflow.md**

## Reference Files

This skill uses modular reference files for organization-specific logic:

1. **organization-detection.md** - Detects Duelbits vs generic from git remote
2. **repository-detection.md** - Detects frontend vs backend repository (Duelbits only)
3. **duelbits-workflow.md** - Duelbits-specific PR creation with project detection, base branch rules, Jira MCP integration, and template enforcement
4. **generic-workflow.md** - Standard GitHub PR workflow for non-Duelbits projects
5. **qa-notes-generator.md** - Generates QA handover notes (Duelbits only, shown in chat, NOT added to PR)
6. **helpers.js** - Utility functions for detection and formatting logic

## Critical Rules

### For All Organizations

- ✅ Get user confirmation before creating PR
- ✅ Verify branch is pushed to remote
- ✅ Check for existing PR first
- ✅ Use project's PR template if available

### For Duelbits Specifically

- ✅ Detect repository type (frontend vs backend) for correct base branch
- ✅ Try to fetch Jira ticket info via Atlassian MCP (if available)
- ✅ Use Jira ticket title for PR title when possible
- ✅ Search for PR template in repository (.github/pull_request_template.md)
- ✅ Keep PR description SHORT (2-3 sentences max)
- ✅ Use exact template structure from repository
- ✅ Fill ONLY the sections in the template
- ✅ DO NOT add extra sections beyond template
- ✅ DO NOT remove template comments (<!-- -->)
- ✅ DO NOT modify template structure
- ✅ Check dependency/app boxes ONLY if applicable
- ✅ Include project abbreviation in title if applicable ([MW1], [WCJ])
- ✅ Generate QA notes in CHAT ONLY (NEVER add to PR)
- ✅ QA notes should be brief and actionable
- ✅ Generate QA notes in CHAT ONLY (NEVER add to PR)
- ✅ QA notes should be brief and actionable

## Output Examples

### Duelbits Success

```markdown
✅ Pull Request created successfully!

🔗 PR URL: https://github.com/duelbits/frontend/pull/142

**Summary**:

- Title: [MW-142] [MW1] Implement wallet switching functionality
- Repository: Frontend
- Base: develop-multi-wallet-fe ← MW-142-wallet-switcher
- Project: Multi Wallet
- Organization: Duelbits
- Jira: MW-142 (fetched from Jira MCP)

---

### 📋 QA Handover Notes

_For your reference - NOT included in PR. Copy to Jira if needed._

**Environment**: MW-142-wallet-switcher preview

**Technical Changes**:

- Created WalletSwitcher component
- Added wallet state management
- Updated wallet provider integration

**Impacted Areas**:

- Wallet selection and display
- User profile page
- Transaction history

**Testing Considerations**:

- Test with MetaMask, WalletConnect on Goerli testnet
- Clear localStorage to reset wallet connections

**How to Test**:

- Connect wallet via header button
- Add second wallet using switcher dropdown
- Verify balance updates when switching

---

**Next Steps**:

1. Copy QA notes to Jira ticket
2. Request code review
3. Monitor CI/CD checks
4. Await QA testing
```

### Generic Success

```markdown
✅ Pull Request created successfully!

🔗 PR URL: https://github.com/some-org/project/pull/45

**Summary**:

- Title: Add dark mode support
- Base: main ← feature/add-dark-mode
- Files changed: 15
- Commits: 8

**Next Steps**:

1. Review PR on GitHub
2. Request reviews from team
3. Monitor CI/CD checks
4. Merge when approved
```

## Evals

### Organization Detection

- [ ] Git remote analyzed
- [ ] Organization determined (duelbits or generic)
- [ ] Correct workflow selected

### Duelbits Workflow

- [ ] Remote branch status verified
- [ ] Repository type detected (frontend or backend)
- [ ] Project detected (Multi Wallet, World Cup Jackpot, etc.) if applicable
- [ ] Base branch determined correctly (repository-specific)
- [ ] Ticket number extracted from Jira branch name
- [ ] Jira MCP checked and ticket fetched (if available)
- [ ] PR title uses Jira ticket title or branch name
- [ ] PR title format: `[TICKET] [PROJECT?] Title`
- [ ] Project abbreviation included if applicable ([MW1], [WCJ])
- [ ] PR template found in repository
- [ ] PR template structure preserved exactly
- [ ] PR description is SHORT (2-3 sentences)
- [ ] Only template sections present (no extras)
- [ ] Template comments (<!-- -->) preserved
- [ ] Dependency/checkbox items checked appropriately
- [ ] QA notes generated in chat ONLY
- [ ] QA notes NOT added to PR

### Generic Workflow

- [ ] Remote branch status verified
- [ ] Default branch detected
- [ ] PR template found or generic used
- [ ] Changed files listed
- [ ] PR created successfully

### All Workflows

- [ ] User confirmation obtained
- [ ] Existing PR checked
- [ ] PR created successfully
- [ ] PR URL returned
- [ ] Next steps provided
