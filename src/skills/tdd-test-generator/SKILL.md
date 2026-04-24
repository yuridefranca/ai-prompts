---
name: tdd-test-generator
description: Generate unit tests BEFORE implementation following TDD (Test-Driven Development) principles. Creates ONLY unit tests with mocked dependencies that initially fail. Integration and E2E tests come later after implementation. Always use when starting TDD phase before code exists. Tests must be written before code. Keywords TDD, test-driven development, unit tests, test coverage, testing, red-green-refactor, test first, mocking.
---

# TDD Test Generator (Unit Tests Only)

Generate comprehensive failing UNIT tests BEFORE implementation to drive design and API boundaries. Follows TDD red-green-refactor cycle. **Does NOT create integration or E2E tests** - those come after implementation.

## When to Use

- Before implementing feature (TDD approach)
- After architecture approved, BEFORE any code written
- Need to drive API design through tests
- Implementing critical functionality
- Want to define component boundaries

**Do NOT use for**:

- Integration tests (use `integration-test-generator` after implementation)
- E2E tests (use `integration-test-generator` after implementation)
- Testing existing code (tests should come first)

## Workflow Artifact

This skill is invoked in multiple phases across both workflows:

- **Feature Workflow Phase 4**: Produces `.ai-workflow/[feature-folder]/4-unit-tests.md`
- **Improvement Workflow Phase 5**: Produces `.ai-workflow/[feature-folder]/5-tdd-tests.md`

**Context**: Read `0-startpoint.md` for initial requirements. Read `1-specification.md` (Feature) or `2-root-cause-analysis.md` (Improvement) for what needs to be tested.

## TDD Philosophy

**Red-Green-Refactor-Integration Cycle**:

1. **Red**: Write failing UNIT test (this skill)
2. **Green**: Write minimal code to pass (implementation phase)
3. **Integration**: Write integration tests (after implementation)
4. **Refactor**: Improve code quality (refactoring phase)

**This skill handles "Red" phase** - writing unit tests that fail because no implementation exists yet.

## Process

### Step 0: CRITICAL - Create Test Files

**⚠️ ALWAYS CREATE ACTUAL TEST FILES** - Do NOT just output test code in chat.

**Required actions**:

- Use `create_file` tool to create test files
- Follow project's test file naming conventions (e.g., `*.spec.ts`, `*.test.ts`)
- Place tests in appropriate directories (e.g., `test/`, `__tests__/`, `src/**/*.spec.ts`)
- Verify files are created in the workspace
- Tests must be runnable with project's test command

**Why this matters**: Tests that only exist in chat history cannot be run. They must be committed to the repository.

### Step 1: Identify Testing Framework

**⚠️ ALWAYS CONFIRM TESTING TOOL BEFORE WRITING TESTS**

**Ask user or check project configuration**:

- Which testing framework should be used?
    - **Node.js native**: `node:test` API (Node 18+)
    - **Bun native**: Bun's built-in test runner
    - **Jest**: Popular testing framework with mocking
    - **Vitest**: Fast Vite-native test runner
    - **Other**: Mocha, AVA, Tape, etc.

**Discovery methods**:

1. Check `package.json` for test dependencies
2. Look for existing test files and their imports
3. Check test scripts in `package.json`
4. If unclear, **ASK THE USER**

**Use the confirmed framework consistently** across all generated tests.

### Step 2: Extract Test Scenarios

**From specification**:

- Each acceptance criterion = test(s)
- Each edge case = test
- Each failure scenario = test
- Each business rule = test

### Step 3: Generate Edge Case & Failure Tests FIRST

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

### Step 6: Verify Tests Fail

**Run test suite** - all tests should FAIL:

```bash
npm test
# Expected: X failing tests (red phase)
```

**If tests pass**: Tests are wrong or feature already exists

**Why tests must fail initially**: Confirms tests are actually testing something. If they pass before implementation exists, the tests are broken.

## Output Format

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

## Test Coverage Goals

**Minimum coverage** (unit level):

- [ ] All acceptance criteria have unit tests
- [ ] All edge cases covered at unit level
- [ ] All error scenarios have tests
- [ ] All business rules validated in isolation
- [ ] All external dependencies are mocked

**Quality indicators**:

- Edge cases and error handling written before happy path (drives robust design)
- All external dependencies properly mocked
- Tests are isolated (testing ONE unit only)
- Tests are independent (no interdependencies)
- Tests are deterministic (no randomness)
- Tests are fast (<100ms for unit tests)
- Test names describe expected behavior
- Tests use AAA pattern (Arrange-Act-Assert)
- Mock setup is clear and understandable

## Uncertainty Handling

**Test coverage gaps**: Document scenarios that can't be tested at unit level (save for integration tests)
**Confidence level**: % of requirements covered by unit tests

**If confidence < 70%**: List missing test scenarios

**Note**: Some scenarios can only be tested with integration tests after implementation. That's OK - document them for Phase 6.

## Evals

- [ ] Testing framework identified and confirmed (node:test, Bun, Jest, Vitest, etc.)
- [ ] All functional requirements have unit tests
- [ ] All edge cases covered at unit level
- [ ] Error scenarios tested
- [ ] **All external dependencies are mocked** (databases, APIs, file system, etc.)
- [ ] Edge cases and failures written BEFORE happy path tests
- [ ] Tests fail initially (red phase)
- [ ] Test names are descriptive
- [ ] Tests are fast (<100ms each)
- [ ] No integration or E2E tests created (those come in Phase 6)
- [ ] Tests are independent
