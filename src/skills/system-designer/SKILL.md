---
name: system-designer
description: Design system architecture for new features including domain model, data structures, API contracts, event flows, and scaling considerations. Always use this skill when designing technical solutions, planning system changes, or whenarchitecture decisions need to be made. Addresses domain changes, data models, API design, concurrency, state management, and scalability. Keywords architecture, system design, API design, data model, domain model, technical design, scalability, event flow, state transitions, component design.
---

# System Designer

This skill designs comprehensive system architecture for new features, covering domain model, data structures, APIs, event flows, state management, concurrency, and scaling considerations.

## When to Use This Skill

- After specification extraction (spec is approved)
- Designing technical solution for new feature
- Making architecture decisions
- Planning system changes
- Need to evaluate technical approaches

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Feature Workflow Phase 2**: Produces `.ai-workflow/[feature-folder]/2-architecture.md`
- **Improvement Workflow Phase 2**: Contributes to `.ai-workflow/[feature-folder]/2-tradeoff-and-design.md` (design section)

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, and `1-specification.md` (Feature) or `1-component-map.md` (Improvement) before designing.

## Input Requirements

- Approved specification document (from spec-extractor)
- Understanding of existing system architecture
- Knowledge of technology stack
- Performance/scaling targets

## Process

### Step 1: Analyze Domain Changes

**Identify new domain concepts**:

- What new entities/aggregates are needed?
- What new value objects?
- What new domain events?
- What business rules must be enforced?

**Map to existing domain**:

- How do new concepts relate to existing ones?
- What bounded contexts are affected?
- Any domain model refactoring needed?

### Step 2: Design Data Model Changes

**Database schema changes**:

- New tables/collections
- New columns/fields
- Relationships (1:1, 1:N, M:N)
- Indexes for performance
- Constraints for data integrity

**Data migration considerations**:

- Breaking changes?
- Backward compatibility?
- Migration strategy?

### Step 3: Define API Contracts

**For each endpoint**:

```
POST /api/v1/resources
Request:
{
  "field1": "type + validation rules",
  "field2": "type + validation rules"
}

Response (200):
{
  "id": "uuid",
  "field1": "value",
  "created_at": "iso8601"
}

Response (400): { "error": "message", "field": "field1" }
Response (401): { "error": "unauthorized" }
```

**Define** :

- HTTP methods (GET/POST/PUT/DELETE/PATCH)
- URL patterns (/resource/:id)
- Request schemas with validation
- Response schemas (success + errors)
- Status codes
- Headers (auth, content-type, etc.)

### Step 4: Map Event Flow

**Identify events**:

- What triggers the feature?
- What events does feature emit?
- What events does feature consume?

**Create simple flow diagram** (text-based):

```
User → API: Request
API → Service: Process
Service → Database: Query
Database → Service: Result
Service → EventBus: Emit event
Service → API: Response
API → User: Result
```

### Step 5: Design State Transitions

**If feature has state machine**:

- List all states
- Define valid transitions
- Identify transition triggers
- Document side effects per transition

**Example**:

```
States: [Draft, Pending, Approved, Rejected, Completed]

Transitions:
Draft → Pending: on submit()
Pending → Approved: on approve()
Pending → Rejected: on reject()
Approved → Completed: on complete()
```

### Step 6: Analyze Concurrency Impact

**Questions to answer**:

- Can multiple requests modify same resource?
- Race condition risks?
- Locking strategy (optimistic/pessimistic)?
- Idempotency required?
- Transaction boundaries?

**Document strategy**:

- How to handle concurrent updates
- Conflict resolution approach
- Retry logic

### Step 7: Address Scaling Considerations

**Bottleneck analysis**:

- What will be slowest part? (Database? External API?)
- What will consume most resources?
- What will limit throughput?

**Scaling strategy**:

- Caching (what, where, TTL?)
- Async processing (queues, workers?)
- Read replicas?
- Sharding strategy?
- Rate limiting?

## Output Format

````markdown
# System Design: [Feature Name]

## Domain Model Changes

### New Entities

- **EntityName**: [Description]
    - Properties: [List]
    - Business Rules: [List]

### New Value Objects

- **ValueObjectName**: [Description]

### New Domain Events

- **EventName**: [When emitted, payload]

## Data Model Changes

### New Tables/Collections

```sql
CREATE TABLE table_name (
  id UUID PRIMARY KEY,
  field1 VARCHAR(255) NOT NULL,
  field2 INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  INDEX idx_field1 (field1)
);
```
````

### Schema Modifications

- Table X: Add column Y (migration: [strategy])

## API Contracts

### POST /api/v1/resources

**Purpose**: [What it does]

**Request**:

```json
{
	"field1": "string (required, max 255 chars)",
	"field2": "number (optional, min 0)"
}
```

**Response 200**:

```json
{
	"id": "uuid",
	"field1": "string",
	"created_at": "iso8601"
}
```

**Response 400**: Validation errors
**Response 401**: Unauthorized
**Response 409**: Conflict (already exists)

## Event Flow

```
Step 1: User → API: [Request type]
Step 2: API → Service: [Process action]
Step 3: Service → Database: [Query/Update]
Step 4: Database → Service: [Result]
Step 5: Service → EventBus: [Event emitted]
Step 6: Service → API: [Response]
Step 7: API → User: [Result]

Alternate Paths:
- Error Path 1: [When and what happens]
- Error Path 2: [When and what happens]
```

```

**Key flows**:

1. [Flow description]
2. [Flow description]

## State Transitions

**States**: [List]

**Transitions**:

```

State A → State B: Trigger (side effects)

```

## Concurrency Strategy

**Potential race conditions**:

- [Scenario 1]: [Mitigation]
- [Scenario 2]: [Mitigation]

**Locking approach**: [Optimistic/Pessimistic]

**Idempotency**: [How ensured]

## Scaling Considerations

### Bottlenecks

1. [Bottleneck]: [Impact]

### Caching Strategy

- **What**: [What to cache]
- **Where**: [Redis/In-memory/CDN]
- **TTL**: [Duration]
- **Invalidation**: [Strategy]

### Async Processing

- **What operations**: [List]
- **Queue**: [Technology]
- **Workers**: [Count, scaling]

### Database Optimization

- **Indexes**: [List new indexes]
- **Query optimization**: [Strategies]
- **Read replicas**: [Yes/No, why]

## Assumptions

### Technical Assumptions

- ASSUM P-1: [Assumption]

### Scaling Assumptions

- ASSUMPTION-2: [Traffic pattern, growth rate]

### Confidence Level

**[X]%** - [Justification]

### Open Questions

- QUESTION-1: [Unresolved technical decision]

```

## Evals

### Completeness (35%)

- [ ] Domain model fully specified
- [ ] Data model with schema
- [ ] API contracts with all responses
- [ ] Event flow diagram
- [ ] Concurrency strategy defined
- [ ] Scaling approach documented

### Correctness (30%)

- [ ] Design aligns with spec requirements
- [ ] No obvious technical flaws
- [ ] Handles edge cases from spec
- [ ] Addresses NFRs (performance, security)

### Clarity (20%)

- [ ] Component boundaries clear
- [ ] Data flow understandable
- [ ] API contracts complete
- [ ] Diagrams aid understanding

### Scalability (15%)

- [ ] Bottlenecks identified
- [ ] Scaling strategy practical
- [ ] Performance targets achievable
- [ ] Resource implications considered

```

```
