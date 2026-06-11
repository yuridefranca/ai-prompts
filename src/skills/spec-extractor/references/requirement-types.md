# Requirement Types and Categories

## Functional Requirements

Identify explicit and implicit **what the system must do**:

**Questions to answer**:
- What user actions must be supported?
- What data must be created/read/updated/deleted?
- What business rules must be enforced?
- What integrations are required?
- What outputs/responses are expected?

**Format each requirement**:
```
REQ-[N]: [Action] [Object] [Condition]
Example: REQ-1: User can create a new order with valid payment method
```

**Requirements should be**:
- **Specific**: No ambiguous language
- **Measurable**: Can determine if satisfied
- **Testable**: Can write automated test
- **Independent**: Not duplicating other requirements

## Non-Functional Requirements (NFRs)

Identify quality attributes and constraints:

### Performance Requirements

- Response time targets (e.g., "API responds in <200ms")
- Throughput targets (e.g., "handles 1000 req/sec")
- Resource limits (e.g., "uses <512MB RAM")

### Security Requirements

- Authentication needs (who can access?)
- Authorization rules (what can they do?)
- Data sensitivity (PII, financial, etc.)
- Compliance needs (GDPR, HIPAA, etc.)

### Reliability Requirements

- Uptime targets (e.g., "99.9% availability")
- Failure handling (what happens when things break?)
- Data integrity (how to prevent data corruption?)

### Scalability Requirements

- Expected growth (users, data, traffic)
- Scaling approach (horizontal/vertical)
- Load patterns (steady/spiky)

### Usability Requirements

- User experience expectations
- Accessibility standards
- Internationalization needs

## Constraints

Document limitations that restrict implementation choices:

### Technical Constraints

- Technology stack (must use X framework)
- Existing architecture (must integrate with Y)
- Infrastructure limitations (on-prem, specific cloud)
- Browser/device support requirements

### Business Constraints

- Budget limits
- Timeline requirements
- Resource availability (team size, skills)
- Legal/regulatory constraints

### Operational Constraints

- Deployment windows
- Maintenance windows
- Support requirements
- Monitoring/observability needs
