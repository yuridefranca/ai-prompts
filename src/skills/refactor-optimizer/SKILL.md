---
name: refactor-optimizer
description: Improve code quality, architecture alignment, and performance while keeping tests green. This is the "Refactor" phase of TDD. Always use after minimal implementation is complete and tests pass. Focus on readability, SOLID principles, DRY, performance, and maintainability. Keywords refactoring, code quality, performance optimization, SOLID principles, DRY, code improvement, clean code, technical debt reduction.
---

# Refactor Optimizer

Improve code quality and performance **after tests pass**. This is the "Refactor" phase of TDD - make code better while keeping tests green.

## When to Use

- After minimal implementation (tests passing)
- Code works but isn't clean
- Performance optimization needed
- Architecture alignment required
- Technical debt reduction

## Workflow Artifact

This skill is invoked as **Phase 7** of the Feature Workflow. It MUST produce an output file in the workflow folder.

**Output File**: `.ai-workflow/[feature-folder]/7-refactoring.md`

**Context**: Read `0-startpoint.md` for initial requirements, `2-architecture.md` for the design, and `5-implementation.md` for what was implemented.

## Core Principle

**Tests must stay green** - If refactoring breaks tests, revert and try different approach.

## Process

### Step 1: Improve Readability

**Extract magic numbers**:

```typescript
// Before
if (user.age >= 18) { ... }

// After
const LEGAL_AGE = 18;
if (user.age >= LEGAL_AGE) { ... }
```

**Extract complex conditions**:

```typescript
// Before
if (user.role === 'admin' || user.role === 'superadmin') { ... }

// After
const isAdmin = () => ['admin', 'superadmin'].includes(user.role);
if (isAdmin()) { ... }
```

**Rename for clarity**:

```typescript
// Before
const d = new Date();
const x = calculateThing(d);

// After
const currentDate = new Date();
const expirationTimestamp = calculateExpiration(currentDate);
```

### Step 2: Architecture Alignment

**Follow project patterns**:

- Use established service patterns
- Match existing file structure
- Follow naming conventions
- Use project utilities/helpers

**Apply SOLID principles**:

- **Single Responsibility**: One class, one job
- **Open/Closed**: Extend via composition
- **Liskov Substitution**: Subtypes are substitutable
- **Interface Segregation**: Small, focused interfaces
- **Dependency Inversion**: Depend on abstractions

### Step 3: Remove Duplication (DRY)

**Extract repeated code**:

```typescript
// Before
function processOrderA(order) {
	validate(order);
	save(order);
	notify(order);
}

function processOrderB(order) {
	validate(order);
	save(order);
	notify(order);
}

// After
function processOrder(order, type) {
	validate(order);
	save(order);
	notify(order);
}
```

**Extract to shared utilities** (if used 3+ times)

### Step 4: Query Optimization

**Reduce N+1 queries**:

```typescript
// Before
for (const user of users) {
	user.posts = await fetchPosts(user.id); // N queries
}

// After
const userIds = users.map((u) => u.id);
const posts = await fetchPostsByUsers(userIds); // 1 query
users.forEach((user) => {
	user.posts = posts.filter((p) => p.userId === user.id);
});
```

**Add indexes** (if queries are slow):

```sql
CREATE INDEX idx_user_email ON users(email);
```

**Use caching** (if appropriate):

```typescript
const cached = await cache.get(key);
if (cached) return cached;

const result = await expensiveOperation();
await cache.set(key, result, ttl);
return result;
```

### Step 5: Performance Improvements

**Only if**:

- Performance tests exist
- Or measured bottleneck
- Or requirement in spec

**Common optimizations**:

- Replace O(n²) with O(n log n)
- Use Set/Map instead of Array.find()
- Batch operations
- Lazy loading
- Pagination

**Always measure**: Don't optimize without profiling

### Step 6: Validate Tests Still Pass

**After EACH refactoring**:

```bash
npm test
```

**If tests fail**:

1. Revert the refactoring
2. Analyze why test broke
3. Fix test if needed (rare)
4. Try different refactoring approach

**If tests pass**:

- Commit refactoring
- Move to next improvement

## Refactoring Patterns

### Extract Method

```typescript
// Before
function processUser(user) {
	// 50 lines of complex logic
}

// After
function processUser(user) {
	const validated = validateUser(user);
	const enriched = enrichWithDefaults(validated);
	return saveUser(enriched);
}
```

### Extract Class

```typescript
// Before
class OrderService {
	// Order logic + payment logic + shipping logic
}

// After
class OrderService {
	constructor(
		private paymentService: PaymentService,
		private shippingService: ShippingService,
	) {}
}
```

### Replace Conditional with Polymorphism

```typescript
// Before
if (type === 'email') {
	sendEmail();
} else if (type === 'sms') {
	sendSMS();
} else if (type === 'push') {
	sendPush();
}

// After
const notifier = NotifierFactory.create(type);
notifier.send();
```

## What NOT to Refactor

❌ **Don't refactor**:

- Code unrelated to current feature
- Code without tests
- Code you don't understand
- Working code that's "ugly" but clear

**"While I'm here" syndrome** leads to regressions

## Output

**Refactored code with**:

- All tests still passing ✅
- Improved readability
- Better architecture alignment
- Removed duplication
- Optimized queries (if needed)
- Better performance (if measured)

## Evals

- [ ] Tests still pass after each refactoring
- [ ] Code is more readable than before
- [ ] Follows SOLID principles
- [ ] No duplication (DRY)
- [ ] Architecture patterns consistent
- [ ] Performance same or better
