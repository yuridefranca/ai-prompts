---
name: test-generator
aliases:
    - tdd-test-generator
description: Write the phase 5 behavior contract and its failing tests BEFORE implementation (TDD red phase). Every behavior gets a C* clause ID, a test level (unit, integration, or e2e) picked from the clause kind, a test that cites the ID, and pasted red evidence. Reads the test framework and per-level commands from .ai-rules/project.md. Use when starting the TDD phase, before code exists. Keywords TDD, test-driven development, behavior contract, contract clauses, unit tests, integration tests, e2e, red-green-refactor, test first, mocking, phase 5.
---

# Test Generator

Write the **behavior contract** (`5-contract.md`) and the **failing tests** that pin it down, BEFORE implementation. Every test exists to prove one contract clause, at the level that clause needs.

## When to Use

- Phase 5 of every flow (backs [`tdd-engineer`](../../agents/tdd-engineer.agent.md))
- After the PRD/analysis is approved, BEFORE any code is written
- Driving API design and component boundaries through tests

**Do NOT use for**: testing existing code after the fact (tests come first), or the phase 8.3 Playwright specs written from the real DOM (that's `qa-automator`).

## Parameters

Read `{{phase}}`, `{{output}}`, and `{{inputs}}` from a [skill-params block](../../schemas/skill-params.md) (default: phase `5`, output `5-contract.md`).

## Where this runs

Phase 5. Reads `2-prd.md` (the `AC*` IDs) plus `3.4-tradeoffs.md` when phase 3 ran (in the debug flow, also `2.5-root-cause.md`). Writes `5-contract.md` per [contract-ids.md](../../schemas/contract-ids.md) — `[knowledge]` tier — and the test files themselves into the repo.

## TDD Philosophy

**Red → Green → Refactor**:

1. **Red**: write failing tests for every contract clause (this skill, phase 5)
2. **Green**: minimal code to pass (`minimal-impl-generator`, phases 6.1..n)
3. **Refactor**: improve while green (`refactor-optimizer`, end of each task)

Integration and e2e tests are written **now**, in the red phase, when a clause's level calls for them — not after implementation. A side effect "tested" with a mocked emitter tests the mock.

## Process

### Step 0: CRITICAL - Create Test Files

**⚠️ ALWAYS CREATE ACTUAL TEST FILES** - Do NOT just output test code in chat.

**Required actions**:

- Create the test files with your file-writing tool
- Follow the per-level `location` globs in `.ai-rules/project.md` §Test
- Verify files are created in the workspace
- Tests must be runnable with project's test command

**Why this matters**: Tests that only exist in chat history cannot be run. They must be committed to the repository.

### Step 1: Read the Test Setup from `.ai-rules/project.md`

Read the framework, per-level command, file location, and mocking policy from `.ai-rules/project.md` §Test — **never ask**. See [project-md-schema.md](../../schemas/project-md-schema.md).

- If project.md was declined for this run, inspect `package.json` and existing tests instead, and **say explicitly that the framework is a guess** before proceeding.
- Use the same framework at every level unless §Test names a different runner for that level.

### Step 2: Write the Contract Clauses

Turn the PRD into the clause table in [contract-ids.md](../../schemas/contract-ids.md#clause-table-schema-5-contractmd):

- Each `AC*` acceptance criterion → one or more clauses
- Each edge case, failure scenario, and business rule → a clause
- Debug flow: **`C1` is always the repro** — "given the repro steps, the system does X, not Y"

For each clause pick `Kind`, then the default `Level` from [the kind → level table](../../schemas/contract-ids.md#clause-kind--default-level):

| Kind | Level | How to test |
|---|---|---|
| Pure logic, calculation, validation, error mapping | unit | Steps 3–5 below: everything external mocked |
| Side effect (event emitted, row written, cache invalidated) | integration | Step 6: real dependencies |
| Cross-boundary contract (status code, response shape) | integration (API) | Step 6: real HTTP requests |
| User-visible flow | e2e | Step 6: drive the UI |

Overriding a default needs a one-line reason on the clause. A level the repo has no runner for is **downgraded with a note**, never silently dropped.

### Step 3: Unit Clauses — Edge Cases & Failures FIRST

**⚠️ CRITICAL: Write edge cases and failures BEFORE happy path**

**Why edge cases first?** They drive more robust design. When you think about edge cases early, you design better APIs and error handling from the start.

**Test individual functions/methods** - edge cases first:

```typescript
describe('FeatureName', () => {
	describe('methodName', () => {
		// EDGE CASES FIRST - Drive robust design
		it('should handle empty input gracefully', () => {
			expect(() => methodName('')).toThrow(ValidationError);
		});

		it('should handle null/undefined input', () => {
			expect(() => methodName(null)).toThrow(ValidationError);
		});

		it('should handle boundary values (max length)', () => {
			const longInput = 'a'.repeat(1000);
			expect(() => methodName(longInput)).toThrow(ValidationError);
		});

		it('should handle special characters', () => {
			const result = methodName('test@#$%');
			expect(result).toBeDefined();
		});

		// ERROR CASES
		it('should throw TypeError when input is wrong type', () => {
			expect(() => methodName(123)).toThrow(TypeError);
		});

		// HAPPY PATH LAST - Once edge cases inform the design
		it('should process valid input correctly', () => {
			// Arrange
			const input = 'valid input';
			const expected = 'expected output';

			// Act
			const result = methodName(input);

			// Assert
			expect(result).toEqual(expected);
		});
	});
});
```

**Test order priority**:

1. **Edge cases first**: Empty, null, undefined, boundary values
2. **Error cases**: Invalid types, validation failures, business rule violations
3. **Happy path last**: Normal expected behavior

### Step 4: Mock All External Dependencies

**⚠️ CRITICAL: Unit tests MUST isolate the unit under test**

**Why mock?** Unit tests verify ONE component in isolation. Real dependencies (databases, APIs, other classes) make tests slow, flaky, and test multiple things at once.

**Mock everything external**:

```typescript
describe('UserService', () => {
	let userService: UserService;
	let mockDatabase: jest.Mocked<Database>;
	let mockEmailService: jest.Mocked<EmailService>;

	beforeEach(() => {
		// Create mocks
		mockDatabase = {
			findUser: jest.fn(),
			saveUser: jest.fn(),
		} as any;

		mockEmailService = {
			sendWelcomeEmail: jest.fn(),
		} as any;

		// Inject mocks
		userService = new UserService(mockDatabase, mockEmailService);
	});

	it('should create user and send welcome email', async () => {
		// Arrange - configure mocks
		const newUser = { email: 'test@example.com', name: 'Test' };
		mockDatabase.saveUser.mockResolvedValue({ id: 1, ...newUser });
		mockEmailService.sendWelcomeEmail.mockResolvedValue(true);

		// Act - test the unit
		const result = await userService.createUser(newUser);

		// Assert - verify behavior
		expect(mockDatabase.saveUser).toHaveBeenCalledWith(newUser);
		expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith('test@example.com');
		expect(result).toEqual({ id: 1, ...newUser });
	});
});
```

**What to mock**:

- Database connections
- External APIs/HTTP clients
- File system
- Other services/classes
- Time/date functions
- Random number generators

**What NOT to mock**:

- Pure functions (no side effects)
- Simple utilities/helpers
- The unit under test itself

### Step 5: Setup Test Data & Fixtures

**Create reusable test data**:

```typescript
// Test fixtures
const validUser = { email: 'valid@example.com', name: 'Valid User' };
const invalidUser = { email: 'invalid', name: '' };
const mockUserId = 123;

// Mock return values
const mockDatabaseResponse = { id: mockUserId, ...validUser };
```

### Step 6: Integration and E2E Clauses

For clauses at `integration` or `e2e` level, test **real interactions**. See [references/integration-test-patterns.md](references/integration-test-patterns.md) for setup and examples.

- **Component integration**: services calling services, read-after-write, transaction rollback, error propagation, event publishing
- **API**: real HTTP requests to the app (supertest or similar)
- **Database**: concurrent operations, rollbacks, unique constraints, foreign keys
- **E2E**: a complete user journey, using the selector convention in `.ai-rules/project.md` §Browser

Mock only **external** APIs (Stripe, SendGrid — use nock/msw). Internal services stay real; that's what the test is for.

**Integration gotchas** — add to this list after fixing each mistake:

- Clean ALL tables between tests (`beforeEach`), or one test's data leaks into the next
- Run migrations before the suite, not during it — racing them makes tests flaky
- `NODE_ENV=test` doesn't automatically use the test database — configure it explicitly
- A shared test database breaks parallel runs — use `--runInBand` or one database per worker
- `beforeAll` database setup can time out — raise the timeout for integration suites
- Some ORMs auto-commit unless explicitly wrapped — verify transaction behavior
- `await` every async cleanup in `afterAll`, or it finishes before the work does
- Port conflicts from a stale test server — use random ports
- Docker test databases must be stopped AND removed

### Step 7: Cite the Clause in Every Test

Every test names the clause it asserts, in the test name or a leading comment — phase 6.x's contract diff greps for it:

```ts
// C2
it('rejects duplicate currency with 409', async () => { ... });
```

A citing test with zero assertions counts as **uncited**.

### Step 8: Run the Suite and Paste Red Evidence

Run each level's command from `.ai-rules/project.md` §Test. Every clause must fail, and you paste the **actual failure output** into its `Red evidence` column — not a description of what you expect to fail.

- **A clause with no red evidence means phase 5 did not complete.**
- **If a test passes before implementation**, the test is wrong (a tautology) or the behavior already exists — fix the test or drop the clause, and say which.

## Unit Test File Shape

**Test file structure**:

```typescript
import { describe, it, expect, beforeEach, jest } from '@testing-framework';
import { FeatureUnderTest } from './feature';
import type { Dependency } from './dependency';

describe('FeatureName', () => {
  // Setup with mocks
  let feature: FeatureUnderTest;
  let mockDependency: jest.Mocked<Dependency>;

  beforeEach(() => {
    // Create mocks
    mockDependency = {
      method: jest.fn(),
    } as any;

    // Inject mocks into unit under test
    feature = new FeatureUnderTest(mockDependency);
  });

  // Unit tests - edge cases FIRST
  describe('Unit Tests', () => {
    // Edge cases & error handling FIRST
    it('edge case test - empty input', () => { ... });
    it('edge case test - null input', () => { ... });
    it('error handling test - invalid type', () => { ... });

    // Happy path LAST
    it('happy path - valid input with mocked dependency', () => {
      // Arrange
      mockDependency.method.mockResolvedValue('mocked result');

      // Act
      const result = feature.process('valid input');

      // Assert
      expect(mockDependency.method).toHaveBeenCalledWith(...);
      expect(result).toEqual('expected output');
    });
  });
});
```

**Key points**:

- All external dependencies are mocked
- Tests focus on ONE unit in isolation
- Edge cases tested before happy path
- Mocks configured in beforeEach or individual tests

## Coverage Goals

- [ ] Every `AC*` in the PRD maps to at least one clause
- [ ] Every edge case, error scenario, and business rule has a clause
- [ ] Every clause has a test at its declared level, citing its ID
- [ ] Unit tests mock every external dependency; integration tests use real ones

**Quality indicators**: edge cases before happy path, tests isolated and independent, deterministic, unit tests fast (<100ms), descriptive names, Arrange-Act-Assert.

## Uncertainty Handling

**Clauses you couldn't test at their level**: list them in `5-contract.md` with the reason (missing runner, missing test environment).
**Confidence level**: % of `AC*` IDs covered by clauses with red evidence.

**If confidence < 70%**: list the missing scenarios as open questions in the return summary.

## Evals

- [ ] Framework and commands read from `.ai-rules/project.md` (or the guess stated explicitly)
- [ ] Every clause has `Kind`, `Level`, and pasted red evidence
- [ ] Level overrides carry a one-line reason
- [ ] Every test cites its `C*` ID and has at least one real assertion
- [ ] Debug flow: `C1` is the repro
- [ ] Unit tests mock all external dependencies; integration tests mock only third-party APIs
- [ ] Edge cases and failures written BEFORE happy path tests
- [ ] Test files exist in the repo, not just in chat

## Related

- [../../schemas/contract-ids.md](../../schemas/contract-ids.md) — clause schema, levels, the 6.x contract diff
- [../../agents/tdd-engineer.agent.md](../../agents/tdd-engineer.agent.md)
