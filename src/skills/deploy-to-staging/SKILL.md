---
name: deploy-to-staging
description: Update feature branch with master/main and merge to staging across multi-repo projects (backend, frontend, chadmin-frontend). Use when syncing feature branches with master/main, resolving merge conflicts, preparing staging deployments, or when user mentions backmerge, update from master, sync with main, merge to staging, or deploy to staging. Handles repository-specific workflows and intelligently manages merge conflicts. Keywords backmerge, master sync, main sync, staging merge, merge conflicts, multi-repo deployment, branch sync, feature branch update, conflict resolution, import conflicts.
---

# Deploy to Staging

This skill orchestrates the process of updating a feature branch with the latest changes from master/main and merging it to staging. It handles different workflows for backend, frontend, and chadmin-frontend repositories, and provides intelligent conflict resolution guidance.

## When to Use This Skill

Use this skill when you need to:
- Update a feature branch with the latest changes from master/main (backmerge)
- Prepare a feature branch for staging deployment
- Sync feature branch with main repository changes before testing
- Resolve merge conflicts between master/main and feature branches
- Deploy updated feature branch to staging environment

## Repository Identification

First, identify which repository you're working in by checking the current directory name or asking the user. The three supported repositories are:

1. **backend** - Uses `master` as base branch, no staging merge
2. **frontend** - Uses `master` as base branch, merges to staging
3. **chadmin-frontend** - Uses `main` as base branch, merges to staging

If the repository doesn't match any of these three, ask the user to specify which workflow pattern to follow.

## Workflow by Repository

### Backend Repository

```bash
git checkout master
git pull
git checkout <feature-branch>
git pull
git merge origin/master
git push
```

**Key points:**
- Backend does NOT deploy to staging in this workflow
- Only syncs feature branch with master
- Stops after pushing updated feature branch

### Frontend Repository

```bash
git checkout master
git pull
git checkout <feature-branch>
git pull
git merge origin/master
git push
git checkout staging
git pull
git merge origin/<feature-branch>
git push
```

**Key points:**
- Uses `master` as base branch
- Merges updated feature branch to staging
- Two merge points: master→feature, then feature→staging

### Chadmin-Frontend Repository

```bash
git checkout main
git pull
git checkout <feature-branch>
git pull
git merge origin/main
git push
git checkout staging
git pull
git merge origin/<feature-branch>
git push
```

**Key points:**
- Uses `main` as base branch (not master)
- Otherwise identical to frontend workflow
- Two merge points: main→feature, then feature→staging

## Conflict Resolution Strategy

Merge conflicts most commonly occur when merging master/main into the feature branch. When conflicts occur, follow this analysis process:

### Import-Only Conflicts

**Identification:**
- Conflict markers appear only in import statements
- No code logic is conflicted
- Both sides are adding/removing/reordering imports

**Resolution:**
Accept both changes and automatically clean up:
1. Accept both import sets from both branches
2. Remove duplicate imports
3. Remove unused imports (imports with no references in the file)
4. Sort imports according to project conventions
5. Resolve the conflict and continue the merge

### Code Logic Conflicts

**Identification:**
- Conflict markers appear in actual code logic, not just imports
- Functions, classes, or logic blocks are in conflict
- Changes affect the same code paths or logic

**Resolution:** 
DO NOT automatically resolve. Instead, create a detailed analysis report with:

1. **Conflict Location:** File path and line numbers
2. **Master/Main Changes:** What was changed in master/main and why (infer from git history if needed)
3. **Feature Branch Changes:** What was changed in the feature branch and why
4. **Conflict Type:** Classification (e.g., "competing implementations", "refactor vs feature", "deletion vs modification")
5. **Recommendation:** Which version should likely be kept, OR how to merge both approaches
6. **Reasoning:** Why this recommendation makes sense (consider feature intent, code quality, breaking changes)
7. **Risk Assessment:** What could break if wrong choice is made

**Report Format:**

```markdown
## Merge Conflict Analysis Report

### Conflict 1: [File Path]

**Location:** `path/to/file.ts` lines X-Y

**Master/Main Changes:**
- [Describe what changed and why]

**Feature Branch Changes:**
- [Describe what changed and why]

**Conflict Type:** [Classification]

**Recommendation:** [Keep master | Keep feature | Merge both with modifications]

**Reasoning:**
[Explain the thinking behind the recommendation, considering:
- Feature requirements and intent
- Code quality and maintainability
- Breaking changes and backwards compatibility
- Business logic correctness
]

**Risk Assessment:**
[Describe potential issues if resolved incorrectly]

---

[Repeat for each conflict]
```

After presenting the report, explicitly state: "Please review the analysis and manually resolve these conflicts. I cannot auto-resolve code logic conflicts."

## Execution Steps

Follow these steps in order:

1. **Identify Repository**
   - Check current directory or ask user
   - Confirm which workflow to use

2. **Identify Feature Branch**
   - If not provided by user, check current branch or ask
   - Verify branch exists remotely

3. **Execute Base Branch Sync**
   - Checkout master/main
   - Pull latest changes
   - Checkout feature branch
   - Pull latest changes

4. **Merge Base into Feature**
   - Execute `git merge origin/master` (or origin/main)
   - If successful, push and continue
   - If conflicts, analyze using strategy above

5. **Staging Merge (Frontend & Chadmin only)**
   - If backend, stop here and report completion
   - Checkout staging
   - Pull latest changes
   - Merge feature branch into staging
   - If conflicts, analyze using strategy above
   - Push staging

6. **Report Completion**
   - Summarize what was done
   - Report any conflicts that need manual resolution
   - Confirm staging is updated (if applicable)

## Important Principles

**Never Skip Pulling:** Always pull before merging to ensure you have latest changes. This prevents unnecessary conflicts.

**Conflict Analysis Over Auto-Resolution:** When code conflicts occur, err on the side of caution. It's better to provide a thorough analysis than to make incorrect automatic decisions that could break functionality.

**Import Conflicts Are Safe:** Import-only conflicts can be resolved automatically because they don't affect logic. Worst case, an unused import remains (linting catches this).

**Respect Repository Patterns:** Each repository has its own branching strategy (main vs master, staging vs no staging). Always follow the established pattern.

**Git History Context:** When analyzing conflicts, use git log or git show to understand the intent behind changes. Commit messages provide valuable context.

## Example Interaction

**User:** "Update my feature branch with master and deploy to staging"

**Assistant:**
1. Identifies repository (e.g., frontend)
2. Asks for feature branch name if not obvious from current branch
3. Executes frontend workflow
4. If import conflicts: Resolves automatically and reports
5. If code conflicts: Creates detailed analysis report and requests manual resolution
6. Reports final status
