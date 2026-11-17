# Testing Best Practices

**Sources**:
- [JavaScript Testing Best Practices](https://github.com/goldbergyoni/javascript-testing-best-practices)
- [Test Pyramid (Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles/)

---

## Test Coverage

### Coverage Metrics

**Check**:
- [ ] Coverage >80% for new code?
- [ ] Critical paths 100% covered?
- [ ] Edge cases tested?
- [ ] Error scenarios tested?

```typescript
// ✅ GOOD: Aim for meaningful coverage
// Not just line coverage, but:
// - Statement coverage
// - Branch coverage (all if/else paths)
// - Function coverage
// - Integration coverage
```

### What to Test

**Check**:
- [ ] Unit tests for business logic?
- [ ] Integration tests for API endpoints?
- [ ] E2E tests for critical user flows?
- [ ] Edge cases and error conditions?

```typescript
// ✅ GOOD: Test structure
describe('UserService', () => {
  // Unit tests - business logic
  describe('createUser', () => {
    it('should hash password before saving');
    it('should throw error if email already exists');
    it('should send welcome email after creation');
  });
});

describe('UserController (e2e)', () => {
  // Integration tests - full flow
  it('POST /users should create user and return 201');
  it('POST /users should return 400 for invalid email');
});
```

---

## Test Quality

### Test Names

**Check**:
- [ ] Test names are descriptive?
- [ ] Test names describe expected behavior?
- [ ] Test names include context (given/when/then)?

```typescript
// ❌ BAD: Unclear test names
it('works');
it('returns data');
it('test user');

// ✅ GOOD: Descriptive names
it('should return active users when status is "active"');
it('should throw NotFoundException when user does not exist');
it('should send welcome email after successful registration');

// ✅ GOOD: Given/When/Then pattern
it('given invalid email, when creating user, then should throw ValidationError');
```

### AAA Pattern

**Principle**: Arrange, Act, Assert - structure tests in three clear sections.

**Check**:
- [ ] Tests follow AAA pattern?
- [ ] Setup, execution, and verification clearly separated?

```typescript
// ❌ BAD: Mixed arrangement, action, and assertion
it('creates user', async () => {
  const user = await service.create({ email: 'test@example.com' });
  const mockRepo = createMock();
  expect(user).toBeDefined();
  mockRepo.save.mockResolvedValue(user);
  expect(user.email).toBe('test@example.com');
});

// ✅ GOOD: AAA pattern
it('should create user with hashed password', async () => {
  // Arrange
  const dto = { email: 'test@example.com', password: 'Password123' };
  const mockRepo = createMockRepository();
  mockRepo.save.mockResolvedValue({ id: 1, ...dto });
  const service = new UserService(mockRepo);
  
  // Act
  const result = await service.create(dto);
  
  // Assert
  expect(result.password).not.toBe(dto.password);
  expect(result.email).toBe(dto.email);
  expect(mockRepo.save).toHaveBeenCalledTimes(1);
});
```

### Test Independence

**Check**:
- [ ] Tests can run in any order?
- [ ] Tests don't depend on each other?
- [ ] No shared mutable state between tests?
- [ ] Database/fixtures reset between tests?

```typescript
// ❌ BAD: Tests depend on each other
let userId: number;

it('should create user', async () => {
  const user = await service.create({ email: 'test@example.com' });
  userId = user.id; // Shared state!
});

it('should get user', async () => {
  const user = await service.findOne(userId); // Depends on previous test!
  expect(user).toBeDefined();
});

// ✅ GOOD: Independent tests
describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockRepository;
  
  beforeEach(() => {
    mockRepo = createMockRepository();
    service = new UserService(mockRepo);
  });
  
  it('should create user', async () => {
    const dto = { email: 'test@example.com', password: 'Pass123' };
    mockRepo.save.mockResolvedValue({ id: 1, ...dto });
    
    const result = await service.create(dto);
    
    expect(result.id).toBe(1);
  });
  
  it('should get user by id', async () => {
    const user = { id: 1, email: 'test@example.com' };
    mockRepo.findOne.mockResolvedValue(user);
    
    const result = await service.findOne(1);
    
    expect(result).toEqual(user);
  });
});
```

---

## Mocking & Test Doubles

### When to Mock

**Check**:
- [ ] External dependencies mocked (APIs, databases)?
- [ ] Time/date operations mockable?
- [ ] Random values controlled in tests?
- [ ] Not over-mocking (test real integrations where valuable)?

```typescript
// ✅ GOOD: Mock external dependencies
describe('PaymentService', () => {
  let service: PaymentService;
  let mockStripeAPI: jest.Mocked<StripeAPI>;
  
  beforeEach(() => {
    mockStripeAPI = {
      charge: jest.fn(),
      refund: jest.fn()
    } as any;
    
    service = new PaymentService(mockStripeAPI);
  });
  
  it('should process payment', async () => {
    mockStripeAPI.charge.mockResolvedValue({ id: 'ch_123', status: 'succeeded' });
    
    const result = await service.processPayment(100);
    
    expect(result.success).toBe(true);
    expect(mockStripeAPI.charge).toHaveBeenCalledWith(10000, 'USD');
  });
});

// ✅ GOOD: Mock time
import { useFakeTimers } from '@jest/globals';

it('should expire token after 1 hour', () => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-01T00:00:00Z'));
  
  const token = createToken();
  
  jest.setSystemTime(new Date('2024-01-01T01:00:01Z'));
  
  expect(token.isExpired()).toBe(true);
  
  jest.useRealTimers();
});
```

### Mock Quality

**Check**:
- [ ] Mocks behave like real objects?
- [ ] Mock assertions verify behavior, not implementation?
- [ ] Spies used to verify calls without changing behavior?

```typescript
// ❌ BAD: Testing implementation details
it('should call repository save method', async () => {
  const spy = jest.spyOn(mockRepo, 'save');
  
  await service.create(dto);
  
  expect(spy).toHaveBeenCalled(); // Testing implementation, not behavior
});

// ✅ GOOD: Testing behavior
it('should create user and return user with id', async () => {
  mockRepo.save.mockResolvedValue({ id: 1, ...dto });
  
  const result = await service.create(dto);
  
  expect(result).toHaveProperty('id');
  expect(result.email).toBe(dto.email);
});
```

---

## Assertions

### One Concept Per Test

**Check**:
- [ ] Each test verifies one concept?
- [ ] Multiple related assertions OK if testing same concept?
- [ ] Not testing multiple unrelated behaviors?

```typescript
// ❌ BAD: Testing multiple concepts
it('should handle user operations', async () => {
  // Creating user
  const user = await service.create(dto);
  expect(user).toBeDefined();
  
  // Updating user
  const updated = await service.update(user.id, { name: 'New Name' });
  expect(updated.name).toBe('New Name');
  
  // Deleting user
  await service.delete(user.id);
  const deleted = await service.findOne(user.id);
  expect(deleted).toBeNull();
});

// ✅ GOOD: Separate tests for each concept
describe('UserService', () => {
  it('should create user with hashed password', async () => {
    const user = await service.create(dto);
    
    expect(user).toBeDefined();
    expect(user.password).not.toBe(dto.password);
  });
  
  it('should update user name', async () => {
    mockRepo.findOne.mockResolvedValue({ id: 1, name: 'Old Name' });
    mockRepo.save.mockResolvedValue({ id: 1, name: 'New Name' });
    
    const updated = await service.update(1, { name: 'New Name' });
    
    expect(updated.name).toBe('New Name');
  });
  
  it('should delete user', async () => {
    mockRepo.delete.mockResolvedValue(undefined);
    mockRepo.findOne.mockResolvedValue(null);
    
    await service.delete(1);
    const deleted = await service.findOne(1);
    
    expect(deleted).toBeNull();
  });
});
```

### Precise Assertions

**Check**:
- [ ] Assertions are specific?
- [ ] Not using generic truthiness checks?
- [ ] Exact values checked when possible?

```typescript
// ❌ BAD: Vague assertions
it('returns user', async () => {
  const result = await service.findOne(1);
  
  expect(result).toBeTruthy(); // Too vague
  expect(result).toBeDefined(); // Too vague
});

// ✅ GOOD: Precise assertions
it('should return user with correct properties', async () => {
  mockRepo.findOne.mockResolvedValue({
    id: 1,
    email: 'test@example.com',
    name: 'Test User'
  });
  
  const result = await service.findOne(1);
  
  expect(result).toEqual({
    id: 1,
    email: 'test@example.com',
    name: 'Test User'
  });
  // Or check specific properties
  expect(result.id).toBe(1);
  expect(result.email).toBe('test@example.com');
});
```

---

## Edge Cases & Error Scenarios

### Happy Path vs Edge Cases

**Check**:
- [ ] Happy path tested?
- [ ] Edge cases tested (empty, null, undefined, max values)?
- [ ] Boundary conditions tested?
- [ ] Error scenarios tested?

```typescript
describe('calculateDiscount', () => {
  // Happy path
  it('should calculate 10% discount for regular users', () => {
    expect(calculateDiscount(100, 'regular')).toBe(10);
  });
  
  // Edge cases
  it('should return 0 discount for 0 price', () => {
    expect(calculateDiscount(0, 'regular')).toBe(0);
  });
  
  it('should handle negative prices', () => {
    expect(() => calculateDiscount(-100, 'regular')).toThrow('Invalid price');
  });
  
  it('should handle unknown user type', () => {
    expect(calculateDiscount(100, 'unknown')).toBe(0);
  });
  
  it('should handle very large prices', () => {
    expect(calculateDiscount(Number.MAX_SAFE_INTEGER, 'vip')).toBeLessThan(Infinity);
  });
  
  // Boundary conditions
  it('should handle price exactly at 1000', () => {
    expect(calculateDiscount(1000, 'regular')).toBe(100);
  });
  
  it('should handle price just below 1000', () => {
    expect(calculateDiscount(999.99, 'regular')).toBeCloseTo(99.99, 2);
  });
});
```

### Error Handling Tests

**Check**:
- [ ] Exceptions tested?
- [ ] Error messages validated?
- [ ] Error types checked?
- [ ] Cleanup happens on error?

```typescript
// ✅ GOOD: Test error scenarios
describe('UserService', () => {
  it('should throw NotFoundException when user not found', async () => {
    mockRepo.findOne.mockResolvedValue(null);
    
    await expect(service.findOne(999))
      .rejects
      .toThrow(NotFoundException);
  });
  
  it('should throw ConflictException when email already exists', async () => {
    mockRepo.findOne.mockResolvedValue({ id: 1, email: 'test@example.com' });
    
    await expect(service.create({ email: 'test@example.com', password: 'Pass123' }))
      .rejects
      .toThrow(ConflictException);
  });
  
  it('should rollback transaction on error', async () => {
    mockRepo.manager.transaction.mockImplementation(async (callback) => {
      try {
        await callback(mockRepo.manager);
      } catch (error) {
        // Verify rollback was called
        expect(mockRepo.manager.rollback).toHaveBeenCalled();
        throw error;
      }
    });
    
    // Test that error triggers rollback
  });
});
```

---

## Test Data

### Test Fixtures

**Check**:
- [ ] Test data is realistic?
- [ ] Factory functions for creating test data?
- [ ] Test data doesn't leak between tests?

```typescript
// ✅ GOOD: Factory functions for test data
export class UserFactory {
  static create(overrides?: Partial<User>): User {
    return {
      id: 1,
      email: 'test@example.com',
      name: 'Test User',
      password: 'hashedPassword',
      createdAt: new Date(),
      ...overrides
    };
  }
  
  static createMany(count: number): User[] {
    return Array.from({ length: count }, (_, i) => 
      this.create({ id: i + 1, email: `test${i}@example.com` })
    );
  }
}

// Usage
it('should find user by email', async () => {
  const user = UserFactory.create({ email: 'specific@example.com' });
  mockRepo.findOne.mockResolvedValue(user);
  
  const result = await service.findByEmail('specific@example.com');
  
  expect(result).toEqual(user);
});
```

---

## Integration & E2E Testing

### Test Database

**Check**:
- [ ] Separate test database used?
- [ ] Database reset between tests?
- [ ] Test data isolated per test?

```typescript
// ✅ GOOD: E2E test with test database
describe('UserController (e2e)', () => {
  let app: INestApplication;
  let db: TestDatabase;
  
  beforeAll(async () => {
    const moduleFixture = await Test.createTestingModule({
      imports: [AppModule]
    }).compile();
    
    app = moduleFixture.createNestApplication();
    await app.init();
    
    db = app.get(TestDatabase);
  });
  
  beforeEach(async () => {
    await db.reset(); // Clean database before each test
  });
  
  afterAll(async () => {
    await db.close();
    await app.close();
  });
  
  it('POST /users should create user', () => {
    return request(app.getHttpServer())
      .post('/users')
      .send({
        email: 'test@example.com',
        password: 'Password123'
      })
      .expect(201)
      .expect(res => {
        expect(res.body).toHaveProperty('id');
        expect(res.body.email).toBe('test@example.com');
        expect(res.body).not.toHaveProperty('password');
      });
  });
});
```

---

## Test Maintainability

### Avoid Test Fragility

**Check**:
- [ ] Tests don't rely on execution order?
- [ ] Tests not brittle to implementation changes?
- [ ] Tests focused on behavior, not implementation?

```typescript
// ❌ BAD: Fragile test - too tied to implementation
it('should call repository methods in correct order', async () => {
  const findSpy = jest.spyOn(mockRepo, 'findOne');
  const saveSpy = jest.spyOn(mockRepo, 'save');
  
  await service.updateUser(1, { name: 'New Name' });
  
  expect(findSpy).toHaveBeenCalledBefore(saveSpy); // Fragile!
  expect(findSpy).toHaveBeenCalledTimes(1);
  expect(saveSpy).toHaveBeenCalledTimes(1);
});

// ✅ GOOD: Test behavior, not implementation
it('should update user name', async () => {
  const existingUser = { id: 1, name: 'Old Name' };
  mockRepo.findOne.mockResolvedValue(existingUser);
  mockRepo.save.mockResolvedValue({ ...existingUser, name: 'New Name' });
  
  const result = await service.updateUser(1, { name: 'New Name' });
  
  expect(result.name).toBe('New Name');
});
```

### DRY in Tests

**Check**:
- [ ] Common setup extracted to beforeEach?
- [ ] Helper functions for repetitive test logic?
- [ ] Balance between DRY and test readability?

```typescript
// ✅ GOOD: Extract common setup
describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockRepository;
  let mockEmailService: MockEmailService;
  
  beforeEach(() => {
    mockRepo = createMockRepository();
    mockEmailService = createMockEmailService();
    service = new UserService(mockRepo, mockEmailService);
  });
  
  // Helper function for common assertions
  function expectUserToBeValid(user: User) {
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('email');
    expect(user).not.toHaveProperty('password');
  }
  
  it('should create user', async () => {
    mockRepo.save.mockResolvedValue({ id: 1, email: 'test@example.com' });
    
    const result = await service.create({ email: 'test@example.com', password: 'Pass123' });
    
    expectUserToBeValid(result);
  });
});
```

---

## Test Performance

### Fast Tests

**Check**:
- [ ] Unit tests run in milliseconds?
- [ ] Slow tests separated (e2e, integration)?
- [ ] Parallel execution enabled?
- [ ] No unnecessary waits/sleeps?

```typescript
// ❌ BAD: Unnecessary waits
it('should process data', async () => {
  await service.process(data);
  await new Promise(resolve => setTimeout(resolve, 1000)); // Why wait?
  expect(result).toBeDefined();
});

// ✅ GOOD: Fast, focused test
it('should process data', async () => {
  mockProcessor.process.mockResolvedValue(result);
  
  const output = await service.process(data);
  
  expect(output).toEqual(result);
});

// ✅ GOOD: Separate slow tests
// package.json
{
  "scripts": {
    "test": "jest --testPathIgnorePatterns=e2e", // Fast unit tests
    "test:e2e": "jest --testMatch=**/*.e2e-spec.ts", // Slow e2e tests
    "test:all": "jest" // All tests
  }
}
```
