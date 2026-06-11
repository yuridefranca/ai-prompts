# Edge Case Identification Guide

Think through **boundary conditions and unusual scenarios**:

## Data Edge Cases

- Empty inputs (null, "", [])
- Extreme values (very large, very small, negative)
- Invalid formats (malformed data)
- Special characters (unicode, emojis, SQL injection attempts)
- Missing required fields

## Timing Edge Cases

- Race conditions (concurrent requests)
- Timeouts (slow external services)
- Out-of-order events
- Duplicate requests

## State Edge Cases

- Resource doesn't exist (404 scenarios)
- Resource already exists (conflict scenarios)
- Unauthorized access attempts
- Expired sessions/tokens

## Volume Edge Cases

- Pagination with zero results
- Pagination with millions of results
- Bulk operations (1 item vs 10,000 items)
- Rate limiting scenarios

## Integration Edge Cases

- External service down
- External service returns unexpected data
- Network failures
- Partial failures

## Format

```
EDGE-[N]: [Scenario] → [Expected Behavior]
Example: EDGE-1: User submits order with invalid payment → Return 400 error with clear message
```
