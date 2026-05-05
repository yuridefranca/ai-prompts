---
name: code-reviewer
description: Comprehensive code quality review covering security, performance, maintainability, anti-patterns, and regression risks. Used as final step in both feature and bugfix workflows before merge. Checks SOLID principles, best practices, test coverage, documentation, and prevents technical debt. Keywords code review, quality assurance, security review, performance review, maintainability, SOLID principles, anti-patterns, best practices, regression prevention.
---

# Code Reviewer

**Comprehensive code quality review** before merging. Final guardian against technical debt, security issues, and poor practices.

## When to Use

- Final step before merge (feature or bugfix)
- After post-fix review (for bugfixes)
- After refactoring phase (for features)
- Pull request review
- Critical/high-impact changes

## Workflow Artifact

This skill is invoked in all three workflows:

- **Feature Workflow Phase 8**: Produces `.ai-workflow/[feature-folder]/8-code-review.md`
- **Bug Workflow Phase 7**: Contributes to `.ai-workflow/[feature-folder]/7-post-fix-review.md` (alongside post-fix-reviewer)
- **Improvement Workflow Phase 7**: Produces `.ai-workflow/[feature-folder]/7-code-review.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, and all prior phase output files for full context of what's being reviewed.

## Core Principle

**Prevent Future Problems**: Catch issues now that would cause pain later. Balance thoroughness with pragmatism.

## Process

### Step 1: Understand the Change

**Read the context**:

- What's the goal? (feature/bugfix)
- What's the approach?
- How complex is it?

**Review scope**:

- Files changed
- Lines added/removed
- Components affected

**Document**:

```markdown
## Change Summary

**Type**: [Feature / Bugfix / Refactoring]
**Scope**: [Small / Medium / Large]
**Complexity**: [Low / Medium / High]

**Files Changed**: [N]

- `path/file1.ts` (+50, -10)
- `path/file2.ts` (+120, -30)

**Purpose**: [Brief description]
```

### Step 2: Security Review

**Check for vulnerabilities**:

#### Input Validation

- [ ] All user input validated?
- [ ] Type checking in place?
- [ ] Length limits enforced?
- [ ] Format validation (email, URL, etc.)?

#### SQL Injection

```typescript
// ❌ BAD
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ GOOD
const query = `SELECT * FROM users WHERE id = $1`;
db.query(query, [userId]);
```

#### XSS (Cross-Site Scripting)

```typescript
// ❌ BAD
element.innerHTML = userInput;

// ✅ GOOD
element.textContent = userInput;
// OR
element.innerHTML = sanitize(userInput);
```

#### Authentication & Authorization

- [ ] Authentication checked?
- [ ] Authorization enforced?
- [ ] Permissions validated?
- [ ] Token validation secure?

#### Sensitive Data

- [ ] Passwords hashed (not plain text)?
- [ ] Secrets not in code?
- [ ] PII properly handled?
- [ ] Logs don't expose sensitive data?

#### CSRF Protection

- [ ] State-changing operations protected?
- [ ] CSRF tokens used?
- [ ] SameSite cookies configured?

**Document findings**:

```markdown
## Security Issues

### Critical

**SEC-CRIT-1**: SQL injection vulnerability

- **Location**: `line 45 in user.service.ts`
- **Issue**: String concatenation in query
- **Fix**: Use parameterized queries
- **Impact**: Database compromise

### High

**SEC-HIGH-1**: Password stored in plain text

- **Location**: `line 120 in auth.service.ts`
- **Issue**: No bcrypt hashing
- **Fix**: Hash passwords before storage
- **Impact**: User account compromise
```

### Step 3: Performance Review

**Check for performance issues**:

#### Database Queries

```typescript
// ❌ BAD: N+1 query problem
for (const user of users) {
	const posts = await db.query('SELECT * FROM posts WHERE userId = $1', [user.id]);
}

// ✅ GOOD: Single query with JOIN
const usersWithPosts = await db.query(`
  SELECT u.*, p.* 
  FROM users u 
  LEFT JOIN posts p ON p.userId = u.id
`);
```

- [ ] No N+1 queries?
- [ ] Proper indexes used?
- [ ] Query limits in place?
- [ ] Pagination for large datasets?

#### Algorithms

- [ ] Time complexity reasonable? (avoid O(n²) if possible)
- [ ] Space complexity acceptable?
- [ ] Unnecessary loops avoided?
- [ ] Early returns used?

#### Caching

- [ ] Expensive operations cached?
- [ ] Cache invalidation handled?
- [ ] TTL set appropriately?

#### Async Operations

```typescript
// ❌ BAD: Sequential (slow)
const user = await getUser(id);
const posts = await getPosts(userId);
const comments = await getComments(userId);

// ✅ GOOD: Parallel (fast)
const [user, posts, comments] = await Promise.all([getUser(id), getPosts(userId), getComments(userId)]);
```

#### Blocking Operations

- [ ] No blocking I/O on main thread?
- [ ] Heavy computation offloaded?
- [ ] Streams used for large files?

**Document findings**:

```markdown
## Performance Issues

### High

**PERF-HIGH-1**: N+1 query in user list

- **Location**: `line 67 in user.controller.ts`
- **Issue**: Fetching posts in loop
- **Fix**: Use JOIN or dataloader
- **Impact**: Slow response (<500ms SLA breach)

### Medium

**PERF-MED-1**: No pagination

- **Location**: `line 120 in post.service.ts`
- **Issue**: Returns all posts (could be 10,000+)
- **Fix**: Add limit/offset pagination
- **Impact**: Memory issues, slow responses
```

### Step 4: Code Quality & Maintainability

**Check SOLID principles**:

#### Single Responsibility

```typescript
// ❌ BAD: Class does too much
class UserService {
  createUser() { ... }
  sendWelcomeEmail() { ... }
  generateReport() { ... }
  logActivity() { ... }
}

// ✅ GOOD: Separate responsibilities
class UserService {
  createUser() { ... }
}
class EmailService {
  sendWelcomeEmail() { ... }
}
class ReportService {
  generateReport() { ... }
}
```

#### Open/Closed Principle

- [ ] Extensible without modification?
- [ ] Uses interfaces/abstract classes?
- [ ] Strategy pattern where appropriate?

#### Liskov Substitution

- [ ] Subtypes behave like base types?
- [ ] No broken inheritance?

#### Interface Segregation

- [ ] Interfaces are focused?
- [ ] No "fat" interfaces?

#### Dependency Inversion

- [ ] Depends on abstractions, not concretions?
- [ ] Uses dependency injection?

**Check for DRY violations**:

```typescript
// ❌ BAD: Duplication
function validateEmail(email: string) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
function validateUserEmail(email: string) {
	return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// ✅ GOOD: Single source of truth
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
function validateEmail(email: string) {
	return EMAIL_REGEX.test(email);
}
```

**Check for code smells**:

- [ ] No magic numbers (use constants)
- [ ] No overly long functions (>50 lines)
- [ ] No deep nesting (>3 levels)
- [ ] No commented-out code
- [ ] No TODO/FIXME without tickets
- [ ] Descriptive variable names
- [ ] Consistent naming conventions

### Step 5: Error Handling

**Check error handling practices**:

```typescript
// ❌ BAD: Silent failure
try {
	await processPayment();
} catch (error) {
	// Ignored
}

// ✅ GOOD: Proper error handling
try {
	await processPayment();
} catch (error) {
	logger.error('Payment processing failed', { error, userId });
	throw new PaymentError('Payment failed', { cause: error });
}
```

- [ ] All errors caught?
- [ ] Errors logged appropriately?
- [ ] User-friendly error messages?
- [ ] No sensitive data in error messages?
- [ ] Proper error types used?
- [ ] Transactions rolled back on error?

### Step 6: Testing

**Check test coverage**:

- [ ] Unit tests for new code?
- [ ] Integration tests for API changes?
- [ ] Edge cases covered?
- [ ] Error scenarios tested?
- [ ] Mocks used appropriately?
- [ ] Tests are deterministic (no flakiness)?

**Test quality**:

```typescript
// ❌ BAD: Unclear test
it('works', () => {
	const result = func(data);
	expect(result).toBeTruthy();
});

// ✅ GOOD: Clear test
it('should return active users when status is "active"', () => {
	const users = [
		{ id: 1, status: 'active' },
		{ id: 2, status: 'inactive' },
	];
	const result = filterActiveUsers(users);
	expect(result).toEqual([{ id: 1, status: 'active' }]);
});
```

- [ ] Test names are descriptive?
- [ ] Tests follow AAA pattern (Arrange, Act, Assert)?
- [ ] One assertion per test (ideally)?
- [ ] Tests are independent?

**Coverage metrics**:

- [ ] Coverage >80% for new code?
- [ ] Critical paths covered?
- [ ] Edge cases tested?

### Step 7: Documentation

**Check documentation**:

#### Code Comments

```typescript
// ❌ BAD: Obvious comment
const total = price + tax; // Add price and tax

// ✅ GOOD: Explains "why"
// Tax must be calculated before discounts per IRS regulation 2023-45
const total = price + calculateTax(price);
```

- [ ] Complex logic explained?
- [ ] "Why" documented, not "what"?
- [ ] No outdated comments?
- [ ] Public APIs documented?

#### Function/Class Documentation

```typescript
/**
 * Processes payment for an order
 *
 * @param orderId - Unique order identifier
 * @param amount - Payment amount in cents
 * @returns Payment confirmation ID
 * @throws PaymentError if payment fails
 * @throws ValidationError if amount is invalid
 */
async function processPayment(orderId: string, amount: number): Promise<string>;
```

#### External Documentation

- [ ] README updated (if needed)?
- [ ] AGENTS.md updated (if schema/API changed)?
- [ ] CHANGELOG entry added?
- [ ] Migration guide (if breaking changes)?

### Step 8: Regression Risk

**Check for regression potential**:

**High-risk changes**:

- Modified shared utilities
- Changed core business logic
- Altered database schema
- Modified authentication/authorization
- Changed API contracts

**Questions**:

- What features use this code?
- What could break?
- Are there tests proving it won't break?

**Document**:

```markdown
## Regression Risk Assessment

**Risk Level**: [Low / Medium / High / Critical]

**Affected Features**:

1. User login - \u26a0\ufe0f Modified auth flow
2. Payment processing - \u26a0\ufe0f Uses changed validation
3. Reporting - ✅ No impact

**Mitigations**:

- \u2705 Comprehensive test suite
- \u2705 Regression tests added
- \u26a0\ufe0f Manual testing recommended for auth flow
```

### Step 9: Anti-Patterns

**Check for common anti-patterns**:

#### God Object

- [ ] No single class doing everything?

#### Premature Optimization

- [ ] Optimization justified by profiling?
- [ ] Not optimizing for imaginary problems?

#### Callback Hell

```typescript
// ❌ BAD
getData((data) => {
	processData(data, (result) => {
		saveData(result, (saved) => {
			notify(saved, () => {
				// Done
			});
		});
	});
});

// ✅ GOOD
const data = await getData();
const result = await processData(data);
const saved = await saveData(result);
await notify(saved);
```

#### Tight Coupling

- [ ] Components loosely coupled?
- [ ] Dependencies injected?
- [ ] Interfaces used?

### Step 10: Best Practices

**Language-specific best practices**:

#### TypeScript

- [ ] Strict mode enabled?
- [ ] No `any` types (unless justified)?
- [ ] Enums used for string unions?
- [ ] Null checks in place?

#### Node.js

- [ ] Environment variables for config?
- [ ] Async/await used (not callbacks)?
- [ ] Promises handled (.catch or try/catch)?
- [ ] No blocking operations?

#### React (if applicable)

- [ ] Hooks used correctly?
- [ ] Keys on list items?
- [ ] No unnecessary re-renders?
- [ ] PropTypes or TypeScript types?

## Output Format

````markdown
# Code Review: [Feature/Issue]

## Executive Summary

**Overall Quality**: [Excellent / Good / Needs Improvement / Poor]

**Recommendation**:

- ✅ **APPROVE** - Ready to merge
- ⚠️ **APPROVE WITH COMMENTS** - Minor issues, can fix later
- 🔧 **REQUEST CHANGES** - Issues must be fixed before merge
- 🛑 **REJECT** - Significant rework needed

**Confidence**: [X]%

## Change Overview

**Type**: Feature
**Complexity**: Medium
**Files Changed**: 5
**Lines**: +230, -45

**Purpose**: Add discount code functionality to checkout

## Issues Found

### 🛑 Critical (Must fix before merge)

1. **SEC-CRIT-1**: SQL injection vulnerability
    - **File**: `src/checkout.service.ts:45`
    - **Issue**: Using string concatenation in query
    - **Fix**: Use parameterized queries

### ⚠️ High Priority (Should fix before merge)

1. **PERF-HIGH-1**: N+1 query problem
    - **File**: `src/checkout.controller.ts:67`
    - **Issue**: Loading discounts in loop
    - **Fix**: Use JOIN or eager loading

### 📌 Medium Priority (Fix soon)

1. **MAINTAIN-MED-1**: Function too long
    - **File**: `src/discount.service.ts:120-180`
    - **Issue**: 60-line function with multiple responsibilities
    - **Fix**: Extract helper functions

### 💡 Low Priority (Nice to have)

1. **STYLE-LOW-1**: Magic number
    - **File**: `src/discount.service.ts:145`
    - **Issue**: Hardcoded `30` without explanation
    - **Fix**: Extract to named constant

## Detailed Analysis

### Security ✅ 1 Critical, 0 High

**SEC-CRIT-1**: SQL Injection Vulnerability

```typescript
// Line 45 in checkout.service.ts
const query = `SELECT * FROM discounts WHERE code = '${code}'`;
```
````

**Fix**:

```typescript
const query = 'SELECT * FROM discounts WHERE code = $1';
const result = await db.query(query, [code]);
```

### Performance ⚠️ 1 High, 1 Medium

**PERF-HIGH-1**: N+1 Query Problem

- **Impact**: Slow response for users with many items
- **Current**: 1 query per cart item (up to 50 queries)
- **Target**: Single query with JOIN
- **Priority**: HIGH

### Code Quality ✅ Good overall

**Strengths**:

- Clean variable naming
- Good separation of concerns
- Proper TypeScript types
- Error handling present

**Issues**:

- One function too long (60 lines)
- Minor DRY violation (validation duplicated)

### Testing ⚠️ Needs improvement

**Coverage**: 75% (target: 80%)

**Missing Tests**:

- Edge case: Empty discount code
- Edge case: Expired discount
- Error case: Invalid discount format

**Existing Tests**: Well-written, clear naming

### Documentation ✅ Good

- [ x Code comments adequate
- [x] Function documentation present
- [x] CHANGELOG updated
- [x] AGENTS.md updated (discount schema added)

### Regression Risk 🟡 Medium

**Affected Features**:

1. Checkout flow - Modified validation
2. Cart calculation - Added discount logic

**Mitigations**:

- \u2705 Tests cover happy path
- ⚠️ Needs tests for edge cases
- ⚠️ Recommend manual QA for checkout

## Positive Highlights

1. **Excellent error handling** - All error paths covered
2. **Clean architecture** - Good separation of concerns
3. **Type safety** - Strong TypeScript usage
4. **Readable code** - Easy to follow logic

## Action Items

### Must Fix (Blocking)

- [ ] SEC-CRIT-1: Fix SQL injection (checkout.service.ts:45)

### Should Fix (Before merge)

- [ ] PERF-HIGH-1: Fix N+1 query (checkout.controller.ts:67)
- [ ] Add tests for edge cases (empty/expired discounts)

### Can Fix Later (Create tickets)

- [ ] #1234: Extract long function (discount.service.ts:120-180)
- [ ] #1235: Extract magic number constant (discount.service.ts:145)
- [ ] #1236: Improve test coverage to 80%

## Recommendation

**🔧 REQUEST CHANGES**

One critical security issue must be fixed before merge. After fixing SEC-CRIT-1, please also address PERF-HIGH-1 to prevent performance issues in production.

Other issues are minor and can be addressed in follow-up PRs.

**Estimated Fix Time**: 30-60 minutes

**Confidence**: 90%

```

## Severity Guidelines

**Critical** 🛑:
- Security vulnerabilities
- Data loss potential
- System crashes
- Production incidents guaranteed

**High** ⚠️:
- Performance issues affecting UX
- Logic errors causing incorrect behavior
- Missing critical error handling
- Significant technical debt

**Medium** 📌:
- Code maintainability issues
- Missing tests for important scenarios
- Documentation gaps
- Minor performance concerns

**Low** 💡:
- Code style inconsistencies
- Minor refactoring opportunities
- Non-critical documentation
- Optimization suggestions

## When to Approve

**Approve** ✅ if:
- Zero critical issues
- Zero high-priority issues
- Tests passing
- Documentation adequate

**Approve with Comments** ⚠️ if:
- Zero critical issues
- Minor high-priority issues (can fix immediately)
- Medium/low issues present
- Overall quality good

**Request Changes** 🔧 if:
- Critical issues present
- Multiple high-priority issues
- Significant quality concerns
- Tests inadequate

**Reject** 🛑 if:
- Multiple critical issues
- Fundamental design flaws
- Massive technical debt introduced
- Requires complete rework

## Evals

- [ ] Security vulnerabilities checked
- [ ] Performance issues identified
- [ ] Code quality assessed (SOLID, DRY, KISS)
- [ ] Error handling reviewed
- [ ] Test coverage evaluated
- [ ] Documentation checked
- [ ] Regression risk assessed
- [ ] Anti-patterns identified
- [ ] Clear recommendation provided
- [ ] Action items prioritized
```
