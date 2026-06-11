---
name: site-rewrite-planner
description: >
    Plan and coordinate site rewrite migrations from React 17 to React 19 with new designs.
    Fetches Jira requirements via Atlassian MCP, maps Figma designs, inventories components
    across both repos (migrate, reuse, create), traces user flows and data flow differences,
    maps API calls and data fetching, raises unclear points and missing scenarios, and produces
    a detailed migration plan. Use this skill when migrating a React site to a new version,
    planning a full site rewrite, comparing legacy and new repos, or when Jira tickets and
    Figma designs need to be reconciled into an actionable migration contract. Keywords:
    site rewrite, React migration, React 17 to React 19, component inventory, migration plan,
    Jira requirements, Figma designs, contract.md, data flow mapping, API mapping.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-09'
    updated: '2026-06-09'
compatibility: >
    Atlassian MCP server and Figma MCP server recommended but not required (manual fallback available).
    Both legacy (React 17) and new (React 19) repos must be available locally.
---

# Site Rewrite Planner

Plan and coordinate a full site rewrite migration from React 17 to React 19, reconciling Jira requirements, Figma designs, and both codebases into a single actionable migration contract.

## When to Use

- Migrating a React site from an old version to a new one
- Planning a full site rewrite with new designs
- Need to reconcile Jira requirements with Figma designs and existing code
- Comparing legacy and new repos to identify migration work
- Creating a migration contract before starting implementation

## Prerequisites

- **Atlassian MCP server** configured for Jira access (fallback: manual input)
- **Figma MCP server** configured for design inspection (fallback: manual input)
- **Legacy repo** (React 17) available locally
- **New repo** (React 19) available locally
- Jira epic/ticket IDs for the rewrite initiative

## Output Directory Structure

All artifacts are organized under an **epic folder** with **feature subfolders**:

```
<output-root>/
└── <epic-name>/
    ├── contract.md
    ├── figma-inventory.md
    ├── gaps-and-assumptions.md
    ├── migration-plan.md
    └── <feature-name>/
        ├── component-inventory.md
        ├── flow-comparison.md
        └── api-mapping.md
```

- **`<epic-name>`** — kebab-case name from the Jira epic (e.g., `site-rewrite`, `betting-migration`)
- **`<feature-name>`** — kebab-case short name for each feature area within the epic (e.g., `auth-flow`, `bet-slip`, `user-profile`)
- Shared artifacts (contract, figma inventory, gaps, migration plan) live at the epic level
- Feature-specific artifacts (component inventory, flow comparison, API mapping) live in their feature subfolder

**Default output root**: `./docs` (relative to the workspace) if the user doesn't specify a path.

## Gotchas

- Jira tickets often lack implementation details — always cross-reference with Figma and legacy code
- Figma designs may not cover all states (loading, error, empty) — flag every missing state
- Components in the legacy repo may have undocumented side effects or shared state — trace dependencies carefully
- "Same component" across repos may have different APIs, props, or behavior — never assume equivalence
- Data fetching patterns differ significantly between React 17 (class components, lifecycle) and React 19 (hooks, RSC, suspense)
- Third-party libraries from React 17 may not have React 19 compatible versions — check early
- CSS-in-JS libraries (styled-components, emotion) may need migration to new patterns
- Legacy repo may have dead code that looks active — verify with git blame and import tracing
- Figma component names rarely match code component names — map both directions
- Requirements in Jira may reference outdated designs — always verify design version matches

## Process

### Step 0: Set Up Output Directory

Before generating any artifacts, establish where they'll live.

1. **Ask the user** where to place the output files:
    - "Where should I create the migration docs? (default: `./docs`)"
    - If the user doesn't specify or says "default", use `./docs`
2. **Determine the epic folder name**:
    - Derive from the Jira epic name (e.g., "Site Rewrite" → `site-rewrite`)
    - Convert to kebab-case (lowercase, hyphens, no spaces)
    - If no Jira epic name yet, ask the user for a short name
3. **Determine feature subfolders**:
    - Group Jira tickets by feature area (e.g., auth, betting, profile)
    - Each group becomes a kebab-case subfolder (e.g., `auth-flow`, `bet-slip`)
    - If only one feature area, skip subfolders and put everything at the epic level
4. **Create the directory structure**:
    ```
    mkdir -p <output-root>/<epic-name>/<feature-name-a>
    mkdir -p <output-root>/<epic-name>/<feature-name-b>
    ```
5. **Store the paths** — use `<OUTPUT_ROOT>` and `<EPIC_NAME>` as variables in subsequent steps

**Example**:

```
./docs/
└── site-rewrite/
    ├── contract.md
    ├── figma-inventory.md
    ├── gaps-and-assumptions.md
    ├── migration-plan.md
    ├── auth-flow/
    │   ├── component-inventory.md
    │   ├── flow-comparison.md
    │   └── api-mapping.md
    └── bet-slip/
        ├── component-inventory.md
        ├── flow-comparison.md
        └── api-mapping.md
```

### Step 1: Fetch Jira Requirements → contract.md

**Primary**: Use the Atlassian MCP to fetch all tickets for the rewrite epic.

**Fallback**: If Atlassian MCP is not available, ask the user to provide requirements manually (see fallback instructions below).

1. **Identify the epic** — get the Jira epic key from the user
2. **Fetch all child tickets** — use Atlassian MCP to list tickets under the epic
3. **Extract per-ticket details**:
    - Title, description, acceptance criteria
    - Linked Figma URLs (if any)
    - Priority and status
    - Labels/components for grouping
4. **Produce `contract.md`** using the template in [assets/contract-template.md](assets/contract-template.md)

**Validation**: Every Jira ticket MUST appear in contract.md. If a ticket lacks acceptance criteria, flag it as `[MISSING: acceptance criteria]`.

#### Fallback: Manual Requirements Input

If Atlassian MCP is unavailable:

1. **Ask the user** to provide requirements in one of these formats:
    - Paste Jira ticket details directly (title, description, acceptance criteria)
    - Provide a CSV/JSON export from Jira
    - Share a screenshot or text dump of the epic board
    - Describe the requirements in freeform text
2. **Parse the input** — extract ticket-like structures (title, description, acceptance criteria) from whatever format the user provides
3. **Flag gaps** — any information that would normally come from Jira fields (priority, status, labels) but is missing from user input should be flagged as `[MISSING: <field>]` in contract.md
4. **Proceed** — continue with the same contract.md template, filling in what's available and flagging what's not

**Important**: Do NOT skip or delay the workflow because MCP is unavailable. The manual path produces the same output format with explicit gaps flagged.

### Step 2: Inspect Figma Designs

**Primary**: Use the Figma MCP to inspect design files referenced in Jira tickets.

**Fallback**: If Figma MCP is not available, ask the user to provide design information manually (see fallback instructions below).

1. **Collect all Figma URLs** from Jira tickets and any additional links provided
2. **For each design page/frame**:
    - List all components and their variants
    - Identify breakpoints (mobile, tablet, desktop, wide)
    - Note design tokens (colors, spacing, typography)
    - Flag missing states (loading, error, empty, disabled)
3. **Produce `figma-inventory.md`** using the template in [assets/figma-inventory-template.md](assets/figma-inventory-template.md)

**Validation**: Every Figma URL from Jira MUST be inspected. Missing states MUST be flagged.

#### Fallback: Manual Design Input

If Figma MCP is unavailable:

1. **Ask the user** to provide design information in one of these formats:
    - Share Figma URLs for the agent to open in a browser (if browser tools are available)
    - Paste exported design specs (Figma Dev Mode export, CSS, or design tokens JSON)
    - Provide screenshots of the designs with annotations
    - Describe the components, layouts, and states in freeform text
2. **Extract what you can** — identify components, variants, breakpoints, and tokens from the provided input
3. **Flag gaps** — any design information that cannot be extracted (missing states, unclear breakpoints, unknown tokens) should be flagged in figma-inventory.md
4. **Proceed** — continue with the same figma-inventory.md template, filling in what's available and flagging what's not

**Important**: Do NOT skip or delay the workflow because MCP is unavailable. The manual path produces the same output format with explicit gaps flagged.

### Step 3: Component Inventory — Legacy vs New

Map all components across both repos to classify them.

1. **Inventory legacy repo (React 17)**:
    - Pages and routes
    - UI components (shared + page-specific)
    - Custom hooks
    - Context providers and consumers
    - Utility functions and helpers
    - Third-party dependencies

2. **Inventory new repo (React 19)**:
    - Same categories as above
    - Design system components already in place

3. **Classify each component**:

| Component | Legacy Path      | New Repo Path               | Classification | Notes             |
| --------- | ---------------- | --------------------------- | -------------- | ----------------- |
| Header    | `src/Header.tsx` | `src/components/Header.tsx` | Migrate        | API changed       |
| Button    | `src/Button.tsx` | `src/ui/Button.tsx`         | Exists         | Different styling |
| Dashboard | —                | —                           | Create         | New page in Figma |

**Classifications**:

- **Migrate** — exists in legacy, needs porting to React 19
- **Exists** — already in new repo, verify compatibility
- **Create** — new component per Figma, no legacy equivalent
- **Delete** — legacy component no longer needed

4. **Produce `component-inventory.md`** in each feature subfolder (`<OUTPUT_ROOT>/<EPIC_NAME>/<feature-name>/`) using the template in [assets/component-inventory-template.md](assets/component-inventory-template.md)

**Note**: If the epic has multiple feature areas, produce one `component-inventory.md` per feature subfolder. If only one feature area, produce it at the epic root.

**Validation**: Every page/route in legacy repo MUST appear in the inventory. Every component in Figma MUST map to a classification.

### Step 4: Map User Flows and Data Flow

Compare user flows and data flow between legacy and new implementations.

1. **Map legacy user flows**:
    - Identify all user journeys (auth, browse, transact, etc.)
    - Trace data flow for each journey (API calls → state → UI)
    - Document state management patterns (Redux, Context, local state)

2. **Map new user flows** (from Figma + Jira):
    - Same journeys, noting changes in flow or UI
    - Identify new flows not in legacy
    - Identify removed flows

3. **Compare and diff**:

```markdown
## Flow: User Login

| Aspect   | Legacy (React 17)            | New (React 19)              | Delta                |
| -------- | ---------------------------- | --------------------------- | -------------------- |
| Entry    | `/login` route               | `/auth/login` route         | Route changed        |
| State    | Redux store                  | Server components + RSC     | Architecture changed |
| API      | `POST /api/auth`             | `POST /api/v2/auth`         | Version bump         |
| Redirect | `history.push('/dashboard')` | `router.push('/dashboard')` | Library change       |
```

4. **Produce `flow-comparison.md`** in each feature subfolder (`<OUTPUT_ROOT>/<EPIC_NAME>/<feature-name>/`) using the template in [assets/flow-comparison-template.md](assets/flow-comparison-template.md)

**Note**: If the epic has multiple feature areas, produce one `flow-comparison.md` per feature subfolder. If only one feature area, produce it at the epic root.

**Validation**: Every user flow in legacy MUST be accounted for (migrated, changed, or removed). New flows from Figma MUST be documented.

### Step 5: Map API Calls and Data Fetching

Compare API integration patterns between repos.

1. **Inventory legacy API calls**:
    - All endpoints called (method, path, params, response shape)
    - Data fetching patterns (axios, fetch, SWR, React Query)
    - Authentication/authorization flow
    - Error handling patterns

2. **Inventory new API expectations** (from Jira + Figma):
    - Endpoints needed for new features
    - Data shape expectations from designs
    - New API versions or changes

3. **Compare and classify**:

| Endpoint               | Legacy Usage        | New Usage   | Status  | Notes          |
| ---------------------- | ------------------- | ----------- | ------- | -------------- |
| `GET /api/user`        | `useEffect` + axios | RSC `fetch` | Migrate | Pattern change |
| `POST /api/v2/bet`     | —                   | New feature | Create  | New endpoint   |
| `GET /api/legacy-feed` | Redux action        | —           | Delete  | Deprecated     |

4. **Produce `api-mapping.md`** in each feature subfolder (`<OUTPUT_ROOT>/<EPIC_NAME>/<feature-name>/`) using the template in [assets/api-mapping-template.md](assets/api-mapping-template.md)

**Note**: If the epic has multiple feature areas, produce one `api-mapping.md` per feature subfolder. If only one feature area, produce it at the epic root.

**Validation**: Every API call in legacy MUST be classified. New endpoints from requirements MUST be listed.

### Step 6: Raise Unclear Points and Missing Scenarios

Systematically identify gaps and assumptions.

1. **Cross-reference all artifacts**:
    - Jira tickets vs Figma designs (missing screens?)
    - Figma designs vs legacy code (missing states?)
    - Legacy flows vs new requirements (removed features?)
    - API expectations vs documented endpoints

2. **For each gap, document**:

```markdown
## GAP-001: Missing error state for Bet Slip

- **Source**: Figma design has no error state for bet slip component
- **Legacy**: Has retry UI with "Try Again" button
- **Impact**: Users cannot recover from failed bet placement
- **Assumption**: New design will use toast notifications for errors
- **Action**: Confirm with design team
- **Priority**: HIGH — blocks bet slip implementation
```

3. **Produce `gaps-and-assumptions.md`** using the template in [assets/gaps-template.md](assets/gaps-template.md)

**Validation**: ALL assumptions MUST be explicitly stated. Every gap MUST have an action item and priority.

### Step 7: Create Migration Plan

Synthesize all artifacts into an actionable migration plan.

1. **Group work into phases** based on dependencies:
    - Phase 0: Foundation (design system, shared utilities, auth)
    - Phase 1: Core pages (homepage, navigation, auth flows)
    - Phase 2: Feature pages (per Jira epic grouping)
    - Phase 3: Polish (animations, edge cases, performance)

2. **For each phase, list**:
    - Components to migrate/create
    - API changes needed
    - Figma designs to implement
    - Jira tickets covered
    - Dependencies on other phases
    - Estimated complexity (S/M/L)

3. **Produce `migration-plan.md`** using the template in [assets/migration-plan-template.md](assets/migration-plan-template.md)

**Validation**: Every Jira ticket MUST map to a phase. Every component classification MUST appear in a phase. All gaps MUST be resolved or explicitly deferred with justification.

## Output Files

All output files go in `<OUTPUT_ROOT>/<EPIC_NAME>/` (default: `./docs/<epic-name>/`):

| File                      | Step | Location          | Purpose                                  |
| ------------------------- | ---- | ----------------- | ---------------------------------------- |
| `contract.md`             | 1    | Epic root         | Jira requirements as structured contract |
| `figma-inventory.md`      | 2    | Epic root         | Design components and states             |
| `component-inventory.md`  | 3    | Feature subfolder | Component classification across repos    |
| `flow-comparison.md`      | 4    | Feature subfolder | User flow and data flow diff             |
| `api-mapping.md`          | 5    | Feature subfolder | API call comparison                      |
| `gaps-and-assumptions.md` | 6    | Epic root         | Unclear points and assumptions           |
| `migration-plan.md`       | 7    | Epic root         | Phased migration plan                    |

## Progress Checklist

- [ ] Step 0: Set up output directory → `<OUTPUT_ROOT>/<EPIC_NAME>/`
- [ ] Step 1: Fetch Jira requirements → `contract.md`
- [ ] Step 2: Inspect Figma designs → `figma-inventory.md`
- [ ] Step 3: Component inventory → `<feature>/component-inventory.md`
- [ ] Step 4: Map user flows and data flow → `<feature>/flow-comparison.md`
- [ ] Step 5: Map API calls → `<feature>/api-mapping.md`
- [ ] Step 6: Raise gaps and assumptions → `gaps-and-assumptions.md`
- [ ] Step 7: Create migration plan → `migration-plan.md`

## Validation Loop

After completing all steps:

1. Run cross-reference check: every Jira ticket → contract.md → migration plan phase
2. Run gap check: every gap has an action item and is not BLOCKING without resolution
3. Run assumption check: no implicit assumptions — all stated in `gaps-and-assumptions.md`
4. If any check fails, return to the relevant step and fix before proceeding
