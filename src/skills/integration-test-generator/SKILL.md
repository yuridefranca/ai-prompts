---
name: integration-test-generator
description: >
    Generate integration and E2E tests AFTER implementation to verify components work together 
    correctly. Tests use real dependencies (databases, APIs) not mocks. Always use after 
    implementation is complete and unit tests pass. Validates architecture design and acceptance 
    criteria end-to-end. Keywords: integration tests, E2E tests, end-to-end, acceptance testing, 
    system testing, component integration, real dependencies.
metadata:
    author: yuridefranca
    version: '1.0'
    created: '2026-06-01'
    updated: '2026-06-01'
---

# Integration & E2E Test Generator

Generate integration and end-to-end tests AFTER implementation to verify real component interactions and validate acceptance criteria. Uses real dependencies, not mocks.

## When to Use

- After implementation complete (Phase 5)
- Unit tests passing
- Need to verify components work together
- Validate architecture design from Phase 2
- Test acceptance criteria end-to-end
- Verify real database operations
- Test actual API endpoints

**Do NOT use**:

- Before implementation exists
- For unit tests (use `test-generator`)
- When dependencies can be mocked (use unit tests instead)

## Workflow Artifact

This skill is invoked in multiple workflows:

- **Feature Workflow Phase 6**: Produces `.ai-workflow/[feature-folder]/6-integration-tests.md`
- **Improvement Workflow Phase 6**: Produces `.ai-workflow/[feature-folder]/6-integration-tests.md`

**Context**: Read `0-startpoint.md`, `0.1-grill-me.md`, and the relevant prior phase outputs before generating integration tests.

## Gotchas

Environment-specific facts that defy assumptions - add to this list after fixing each mistake:

- Integration tests need real database cleanup between tests - forgetting this causes random failures
- Docker containers for test databases must be stopped AND removed, not just stopped
- Test database migrations must run before tests, not during - race conditions cause flaky tests
- `NODE_ENV=test` doesn't automatically use test database - must explicitly configure
- Parallel test execution breaks with shared test database - use `--runInBand` or separate DB per worker
- `beforeAll` database setup can timeout - increase Jest timeout to 30000ms for integration tests
- Mock external APIs (Stripe, SendGrid) but not internal services - integration tests verify internal integrations
- Test isolation failures: Previous test's data affects next test - always clean ALL tables in beforeEach
- Port conflicts: Test server already running from previous test run - use random ports or kill stale processes
- Transaction tests: Some ORMs auto-commit unless explicitly wrapped - verify transaction behavior
- Async cleanup: `afterAll` can finish before async operations complete - use `await` on all cleanup
- CI environment: Database connection strings differ from local - use environment variables

## Integration vs Unit Tests

| Aspect          | Unit Tests            | Integration Tests       |
| --------------- | --------------------- | ----------------------- |
| When            | Before implementation | After implementation    |
| Dependencies    | All mocked            | Real dependencies       |
| Speed           | Fast (<100ms)         | Slower (seconds)        |
| Scope           | One function/class    | Multiple components     |
| Purpose         | Drive design          | Verify integration      |
| Failures reveal | Logic bugs            | Contract/interface bugs |

## Process

### Step 0: CRITICAL - Create Test Files

**⚠️ ALWAYS CREATE ACTUAL TEST FILES** - Do NOT just output test code in chat.

**Required actions**:

- Use `create_file` tool to create test files
- Follow project's integration test naming conventions (e.g., `*.integration.spec.ts`, `*.e2e.spec.ts`)
- Place tests in appropriate directories (e.g., `test/integration/`, `e2e/`, `__tests__/integration/`)
- Include test environment setup (databases, test servers)
- Verify tests are runnable with project's test command

**Why this matters**: Integration tests validate real system behavior. They must be committed and run in CI/CD.

### Step 1: Use Same Testing Framework as Unit Tests

**⚠️ CONSISTENCY IS CRITICAL**

Use the same testing framework identified in Phase 4:

- If unit tests use Jest, use Jest
- If unit tests use Vitest, use Vitest
- If unit tests use node:test, use node:test
- If unit tests use Bun, use Bun

**Check existing test configuration** for setup patterns.

### Step 2: Identify Integration Points

**From Phase 2 architecture design**:

- Component boundaries (service → service)
- Database operations (ORM → database)
- External APIs (app → third-party API)
- Message queues (publisher → subscriber)
- File system operations
- Authentication/authorization flows
- Caching layers

**Document each integration point to test**.

### Step 3: Setup Test Environment

See [references/test-patterns.md](references/test-patterns.md) for detailed setup examples.

**Quick setup checklist**:

- Real test database (PostgreSQL, MongoDB, Redis)
- Test API servers (start/stop in beforeAll/afterAll)
- Mock only external APIs (use nock, msw)
- File system fixtures if needed
- Environment variables for test config

### Step 4: Generate Component Integration Tests

Test real interactions between components. See [references/test-patterns.md](references/test-patterns.md#component-integration-tests) for detailed examples.

**Test patterns**:

- Services calling services
- Read-after-write verification
- Transaction rollback scenarios
- Error propagation across boundaries
- Event publishing and handling

### Step 5: Generate API/HTTP Integration Tests

Test actual HTTP endpoints. See [references/test-patterns.md](references/test-patterns.md#api-http-integration-tests) for detailed examples.

**Use supertest or similar** to make real HTTP requests to your API.

### Step 6: Generate Database Integration Tests

Test actual database operations. See [references/test-patterns.md](references/test-patterns.md#database-integration-tests) for detailed examples.

**Focus on**:

- Concurrent operations (race conditions)
- Transaction rollbacks
- Unique constraints
- Foreign key relationships

### Step 7: Generate E2E Tests

Test complete user workflows. See [references/test-patterns.md](references/test-patterns.md#e2e-tests) for detailed examples.

**E2E tests simulate real user journeys** from start to finish.

### Step 8: Run and Verify Integration Tests

**Execute tests**:

```bash
npm run test:integration
# or
npm run test:e2e
```

**Expected behavior**:

- Tests may be slower than unit tests (that's OK)
- Tests should pass if implementation is correct
- Failures indicate real integration issues

**If tests fail**:

1. Check if unit tests still pass (isolate the issue)
2. Review component contracts (Phase 2 architecture)
3. Fix integration bugs in implementation
4. Re-run unit tests to ensure no regression

## Output Format

See [references/test-patterns.md](references/test-patterns.md#integration-test-file-structure-template) for complete file structure template.

**Integration test files should include**:

- Real dependency setup in beforeAll/afterAll
- Data cleanup in beforeEach
- Organized test suites (Happy Path, Error Scenarios, Performance)
- Tests that verify actual database/API state

**File naming conventions**:

- `*.integration.spec.ts` or `*.integration.test.ts`
- `*.e2e.spec.ts` or `*.e2e.test.ts`

**Directory structure**:

- `test/integration/` or `__tests__/integration/`
- `e2e/` or `test/e2e/`

## Test Coverage Goals

**Integration coverage checklist**:

- [ ] All component boundaries tested
- [ ] All database operations verified
- [ ] All API endpoints tested end-to-end
- [ ] Acceptance criteria validated
- [ ] Error propagation tested
- [ ] Transaction rollbacks verified
- [ ] Concurrent operations tested (if applicable)

**Quality indicators**:

- Tests use real dependencies (no mocks for internal components)
- Tests verify actual database state
- Tests validate architecture contracts from Phase 2
- Tests are idempotent (can run multiple times)
- Tests clean up after themselves
- Tests can run in CI/CD environment
- Test setup is automated

## Uncertainty Handling

**Integration test gaps**: Document external dependencies that can't be tested in CI/CD (e.g., third-party APIs)

**Confidence level**: % of architecture contracts verified

**If confidence < 80%**: List missing integration scenarios

## Reference Files

- [Test Patterns and Examples](references/test-patterns.md) - Detailed code examples for all integration test patterns

## Evals

- [ ] Uses same testing framework as unit tests
- [ ] All component boundaries tested
- [ ] Real dependencies used (databases, not mocks)
- [ ] Database operations verified
- [ ] API endpoints tested end-to-end
- [ ] Acceptance criteria validated
- [ ] Transaction handling tested
- [ ] Error propagation verified
- [ ] Test environment setup automated
- [ ] Tests clean up after themselves
- [ ] Tests can run in CI/CD
- [ ] Integration tests created AFTER implementation (not before)
