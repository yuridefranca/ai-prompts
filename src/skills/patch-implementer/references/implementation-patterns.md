# Implementation Checklist Template

```markdown
## Implementation Checklist

### Must Fix (Blocking)
- [ ] [Issue 1]
- [ ] [Issue 2]

### Should Fix (High Priority)
- [ ] [Issue 3]
- [ ] [Issue 4]

### Can Defer (Low Priority)
- [ ] [Issue 5]
```

# TDD Implementation Pattern

## 1. Create Failing Test First

```typescript
it('should [expected behavior]', () => {
  // Arrange
  const input = [test data];
  
  // Act
  const result = functionToFix(input);
  
  // Assert
  expect(result).toBe(expected);
});
```

## 2. Run Test (Should Fail)

```bash
npm test
# Expect: FAIL - Test demonstrates the bug
```

## 3. Implement Minimal Fix

- Write simplest code that makes test pass
- Don't add features
- Don't refactor yet
- Handle critique concerns (edge cases, performance, security)

## 4. Run Tests Again (Should Pass)

```bash
npm test
# Expect: PASS - All tests green
```

## 5. Refactor If Needed

- Improve code quality
- Extract duplicated logic
- Rename for clarity
- Keep tests passing

# Fix Documentation Template

```markdown
## Fix Summary

**Bug**: [Description]
**Root Cause**: [From root cause analysis]
**Solution**: [Brief description]

## Changes Made

**Files Modified**:
- `path/to/file.ts`: [What changed]
- `path/to/test.spec.ts`: [Tests added]

**Critique Concerns Addressed**:
- ✅ FAILURE-1: [How addressed]
- ✅ EDGE-1: [How handled]
- ✅ PERF-1: [How optimized]

## Test Evidence

**Before Fix**:
```
FAIL src/module.spec.ts
  ✗ should handle edge case (12ms)
```

**After Fix**:
```
PASS src/module.spec.ts
  ✓ should handle edge case (8ms)
  ✓ should handle null input (5ms)
  ✓ should handle empty array (4ms)
```

## Verification

- ✅ Original bug fixed
- ✅ All critique concerns addressed
- ✅ All tests passing
- ✅ No regressions
```

# Common Fix Patterns

## Pattern: Input Validation

```typescript
// Before (buggy)
function process(data) {
  return data.map(item => item.value);
}

// After (fixed)
function process(data) {
  if (!data || !Array.isArray(data)) {
    return [];
  }
  return data.map(item => item?.value ?? null).filter(v => v !== null);
}
```

## Pattern: Error Handling

```typescript
// Before (buggy)
async function fetchUser(id) {
  const user = await db.findUser(id);
  return user;
}

// After (fixed)
async function fetchUser(id) {
  try {
    const user = await db.findUser(id);
    if (!user) {
      throw new NotFoundError(`User ${id} not found`);
    }
    return user;
  } catch (error) {
    if (error instanceof NotFoundError) throw error;
    throw new DatabaseError('Failed to fetch user', error);
  }
}
```

## Pattern: Race Condition Fix

```typescript
// Before (buggy)
let counter = 0;
function increment() {
  counter = counter + 1;
}

// After (fixed)
let counter = 0;
const lock = new Mutex();
async function increment() {
  await lock.acquire();
  try {
    counter = counter + 1;
  } finally {
    lock.release();
  }
}
```

## Pattern: Performance Optimization

```typescript
// Before (N+1 query problem)
async function getOrdersWithUsers(orderIds) {
  const orders = await db.orders.findMany({ id: orderIds });
  for (const order of orders) {
    order.user = await db.users.findOne(order.userId); // N queries
  }
  return orders;
}

// After (fixed with JOIN)
async function getOrdersWithUsers(orderIds) {
  return await db.orders.findMany({
    where: { id: orderIds },
    include: { user: true } // 1 query
  });
}
```
