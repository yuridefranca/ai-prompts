# Repository Detection (Duelbits)

Detects whether the repository is frontend or backend to determine appropriate base branch and PR template.

## Purpose

Different repositories (frontend/backend) may have different base branches for the same project. Repository type detection ensures the correct base branch and PR template are used.

## Detection Methods

**Priority order** (first match wins):

1. **Package.json name**
2. **Directory structure analysis**
3. **Ask user**

## Process

### Method 1: Check Package.json

**Look for repository type in package name**:

```bash
# Read package.json
cat package.json | grep '"name"'
```

**Detection patterns**:
- Contains `frontend`, `fe`, `client` → **Frontend**
- Contains `backend`, `be`, `server`, `api` → **Backend**

**Examples**:
- `"name": "duelbits-frontend"` → Frontend
- `"name": "@duelbits/backend"` → Backend
- `"name": "duelbits-client"` → Frontend

### Method 2: Directory Structure Analysis

**Frontend indicators**:
- Has `src/components/` directory
- Has `src/views/` or `src/pages/` directory
- Has `public/` directory
- Has React/Vue/Angular dependencies in package.json

**Backend indicators**:
- Has `src/controllers/` directory
- Has `src/services/` directory
- Has `src/models/` directory
- Has NestJS/Express dependencies in package.json

**Check directory structure**:
```bash
# Frontend check
[ -d "src/components" ] && echo "frontend"

# Backend check
[ -d "src/controllers" ] && echo "backend"
```

### Method 3: Ask User

If both methods fail:

```
I couldn't determine if this is a frontend or backend repository.

Which repository type is this?
- Frontend
- Backend
- Other
```

## Output

Returns one of:
- `frontend` → Use frontend base branch and template
- `backend` → Use backend base branch and template

## Base Branch Mapping

Once repository type is detected, use with project to determine base branch:

| Project | Frontend Base | Backend Base |
|---------|---------------|--------------|
| Multi Wallet | `develop-multi-wallet-fe` | `develop-multi-wallet-be` |
| World Cup Jackpot | `develop-wcj-fe` | `develop-wcj-be` |
| Default (no project) | `develop` | `develop` |

## PR Template Selection

**Frontend**: Use frontend PR template (see `pr-template-frontend.md`)
**Backend**: Use backend PR template (see `pr-template-backend.md`)

## Helper Function Reference

See `helpers.js` for implementation:
- `detectRepositoryType(workspace)` - Main detection logic
- `determineBaseBranch(repositoryType, project)` - Base branch selection

## Examples

### Example 1: Frontend with Multi Wallet

```
Repository: duelbits-frontend
Branch: MW-142-wallet-switcher
Detection: frontend (from package.json name)
Project: multi-wallet (from branch pattern)
Base Branch: develop-multi-wallet-fe
Template: Frontend PR template
```

### Example 2: Backend with World Cup Jackpot

```
Repository: duelbits-backend
Branch: WCJ-45-jackpot-api
Detection: backend (from directory structure)
Project: world-cup-jackpot (from branch pattern)
Base Branch: develop-wcj-be
Template: Backend PR template
```

### Example 3: Backend CORE task

```
Repository: duelbits-api
Branch: CORE-456-fix-payment
Detection: backend (from package.json name)
Project: null (no project pattern)
Base Branch: develop
Template: Backend PR template
```
