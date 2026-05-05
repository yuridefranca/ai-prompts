---
name: minimal-impl-generator
description: Implement the simplest solution that makes tests pass, avoiding premature optimization and over-engineering. This is the "Green" phase of TDD. Always use during implementation phase after tests are written. Focus is on making tests pass, not on perfect code (refactoring comes later). Keywords minimal implementation, simple solution, YAGNI, green phase, TDD implementation, make tests pass, simplest code.
---

# Minimal Implementation Generator

Implement the **simplest possible solution** that makes tests pass. This is the "Green" phase of TDD - no optimization, no over-engineering, just working code.

## When to Use

- After tests are written (TDD approach)
- Implementation phase of feature workflow
- Need to make tests pass
- Following red-green-refactor cycle

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Feature Workflow Phase 5**: Produces `.ai-workflow/[feature-folder]/5-implementation.md`
- **Improvement Workflow Phase 5**: Produces `.ai-workflow/[feature-folder]/5-implementation.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, and the relevant prior phase outputs (spec, design, tests) before implementing.

## Core Principle: YAGNI

**You Aren't Gonna Need It**

- Don't add functionality not in tests
- Don't optimize prematurely
- Don't create abstractions for one use case
- Don't make it "flexible" without requirements

**If tempted to optimize**: STOP. That's Phase 6 (refactoring).

## Process

### Step 0: CRITICAL - Create Implementation Files

**⚠️ ENGINEER AGENTS MUST CREATE ACTUAL FILES** - Do NOT just output code in chat.

**When delegating to engineer agents**:

- Explicitly instruct them to use `create_file` or `replace_string_in_file` tools
- Specify exact file paths where code should be created
- Verify files are created in the workspace after delegation
- Code must be runnable and testable

**Why this matters**: Implementation that only exists in chat history cannot be tested or deployed.

### Step 1: Review Tests

**Understand what tests expect**:

- Read all test cases
- Identify success criteria
- Note edge cases
- Understand error scenarios

### Step 2: Implement Happy Path First

**Start with simplest test**:

```typescript
// Test expects:
it('should return sum of two numbers', () => {
	expect(add(2, 3)).toBe(5);
});

// Simplest implementation:
function add(a: number, b: number): number {
	return a + b; // That's it!
}
```

**Run test**: Should pass ✅

### Step 3: Add Edge Case Handling

**Only if tests require it**:

```typescript
// Test expects:
it('should handle null inputs', () => {
	expect(add(null, 3)).toBe(3);
});

// Add handling:
function add(a: number | null, b: number | null): number {
	return (a ?? 0) + (b ?? 0);
}
```

**Run tests**: Should pass ✅

### Step 4: Add Error Handling

**Only for scenarios in tests**:

```typescript
// Test expects:
it('should throw for invalid types', () => {
	expect(() => add('invalid', 3)).toThrow();
});

// Add validation:
function add(a: any, b: any): number {
	if (typeof a !== 'number' || typeof b !== 'number') {
		throw new TypeError('Arguments must be numbers');
	}
	return a + b;
}
```

### Step 5: Run Tests Continuously

**After each change**:

```bash
npm test
```

**If test fails**:

- Fix immediately
- Don't move forward
- Keep changes small

**If test passes**:

- Commit (optional)
- Move to next test

### Step 6: Resist Optimization Urges

**Common temptations** (AVOID):

- ❌ "Let me cache this" → Not in tests
- ❌ "This could be more efficient" → Not in tests
- ❌ "What if we need to support X?" → Not in tests
- ❌ "Let me refactor this" → Not yet, Phase 6

**Remember**: Premature optimization is the root of all evil

## Code Quality Rules

**During minimal implementation**:

✅ **DO**:

- Write code that makes tests pass
- Keep it simple and obvious
- Use clear variable names
- Add types (TypeScript/etc)
- Handle only tested scenarios

❌ **DON'T**:

- Optimize for performance (unless tested)
- Add abstractions (unless needed by tests)
- Write code for future requirements
- Refactor extensively (that's next phase)
- Add features not in tests

## Output

**Implementation code with**:

- All tests passing ✅
- Minimal complexity
- Clear logic
- Proper types
- Only tested scenarios handled

**Not required at this phase**:

- Performance optimization
- Design patterns
- Perfect abstractions
- Comprehensive error messages
- Extensive logging

## When Implementation is "Done"

**Checklist**:

- [ ] All tests pass
- [ ] All acceptance criteria met
- [ ] All edge cases handled
- [ ] All error scenarios handled
- [ ] Code is simple and understandable
- [ ] No added functionality beyond tests

**Next step**: Phase 6 (Refactoring)

## Examples

### Good Minimal Implementation

```typescript
// Tests expect basic CRUD operations
class UserService {
	create(data) {
		return this.db.insert(data);
	}
	get(id) {
		return this.db.findById(id);
	}
	update(id, data) {
		return this.db.update(id, data);
	}
	delete(id) {
		return this.db.delete(id);
	}
}

// ✅ Simple, passes tests, done
```

### Over-Engineered Implementation (AVOID)

```typescript
// Tests expect basic CRUD operations
class UserService {
	constructor(
		private db: IDatabase,
		private cache: ICache,
		private logger: ILogger,
		private eventBus: IEventBus,
	) {}

	async create(data: CreateUserDTO): Promise<User> {
		this.logger.info('Creating user', data);
		const validated = await this.validator.validate(data);
		const user = await this.db.transaction(async (tx) => {
			const created = await tx.users.insert(validated);
			await this.eventBus.emit('user.created', created);
			return created;
		});
		await this.cache.set(`user:${user.id}`, user, 3600);
		return user;
	}
	// ... more complexity
}

// ❌ Over-engineered, adds infrastructure not in tests
```

## Evals

- [ ] All tests pass
- [ ] Implementation is minimal (no extra code)
- [ ] No premature optimization
- [ ] No unused abstractions
- [ ] Code directly addresses test requirements
