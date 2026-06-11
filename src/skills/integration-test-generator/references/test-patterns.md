# Integration Test Patterns and Examples

This document contains detailed code examples for different integration test patterns.

## Test Environment Setup Patterns

### Database Setup

```typescript
import { setupTestDatabase, teardownTestDatabase } from './test-helpers';

describe('User Registration Integration', () => {
	beforeAll(async () => {
		// Setup real test database
		await setupTestDatabase();
	});

	afterAll(async () => {
		// Cleanup
		await teardownTestDatabase();
	});

	beforeEach(async () => {
		// Clear data between tests
		await clearAllTables();
	});

	it('should create user in database and send welcome email', async () => {
		// Test uses REAL database connection
		const userService = new UserService(realDatabase, realEmailService);

		const newUser = await userService.register({
			email: 'test@example.com',
			password: 'secure123',
		});

		// Verify in actual database
		const dbUser = await realDatabase.users.findOne({ email: 'test@example.com' });
		expect(dbUser).toBeDefined();
		expect(dbUser.id).toEqual(newUser.id);
	});
});
```

### Common Setup Patterns

- **Test databases**: PostgreSQL, MongoDB, Redis
- **Test API servers**: start/stop in beforeAll/afterAll
- **Test message queues**: RabbitMQ, Kafka test instances
- **Mock external APIs only**: use nock, msw
- **File system fixtures**: setup/teardown temp directories

## Component Integration Tests

Test real interactions between your components:

```typescript
describe('Order Checkout Integration', () => {
	it('should process complete checkout flow', async () => {
		// Real services with real dependencies
		const inventoryService = new InventoryService(realDatabase);
		const paymentService = new PaymentService(realPaymentGateway);
		const orderService = new OrderService(realDatabase, inventoryService, paymentService);

		// Test actual workflow
		const order = await orderService.checkout({
			userId: testUserId,
			items: [{ productId: 123, quantity: 2 }],
			payment: { method: 'credit_card', token: 'test_token' },
		});

		// Verify side effects in real systems
		expect(order.status).toBe('completed');

		// Check inventory actually decreased
		const product = await inventoryService.getProduct(123);
		expect(product.stock).toBe(originalStock - 2);

		// Check payment actually processed
		const payment = await paymentService.getPayment(order.paymentId);
		expect(payment.status).toBe('captured');
	});
});
```

**Test patterns**:
- Services calling services
- Read-after-write verification
- Transaction rollback scenarios
- Error propagation across boundaries
- Event publishing and handling

## API/HTTP Integration Tests

Test actual HTTP endpoints:

```typescript
import request from 'supertest';
import { app } from '../app';

describe('API Integration Tests', () => {
	it('should create user via POST /api/users', async () => {
		const response = await request(app).post('/api/users').send({
			email: 'newuser@example.com',
			name: 'New User',
		});

		expect(response.status).toBe(201);
		expect(response.body).toMatchObject({
			email: 'newuser@example.com',
			name: 'New User',
		});

		// Verify user exists via GET
		const getResponse = await request(app).get(`/api/users/${response.body.id}`);

		expect(getResponse.status).toBe(200);
		expect(getResponse.body.email).toBe('newuser@example.com');
	});

	it('should return 400 for invalid email', async () => {
		const response = await request(app).post('/api/users').send({
			email: 'invalid-email',
			name: 'Test',
		});

		expect(response.status).toBe(400);
		expect(response.body.error).toBeDefined();
	});
});
```

## Database Integration Tests

Test actual database operations:

```typescript
describe('Database Integration', () => {
	it('should handle concurrent user creation', async () => {
		const email = 'concurrent@example.com';

		// Simulate concurrent requests
		const promises = [
			userService.create({ email, name: 'User 1' }), 
			userService.create({ email, name: 'User 2' })
		];

		// One should succeed, one should fail (unique constraint)
		const results = await Promise.allSettled(promises);

		const successful = results.filter((r) => r.status === 'fulfilled');
		const failed = results.filter((r) => r.status === 'rejected');

		expect(successful).toHaveLength(1);
		expect(failed).toHaveLength(1);
		expect(failed[0].reason.message).toContain('unique constraint');
	});

	it('should rollback transaction on error', async () => {
		const userId = 123;

		try {
			await database.transaction(async (trx) => {
				await trx.users.update(userId, { status: 'active' });
				await trx.orders.create({ userId, total: 100 });
				throw new Error('Simulated error');
			});
		} catch (error) {
			// Expected error
		}

		// Verify rollback - user status unchanged
		const user = await database.users.findOne(userId);
		expect(user.status).toBe('inactive'); // Original status
	});
});
```

## E2E Tests

Test complete user workflows:

```typescript
describe('E2E: User Registration and First Purchase', () => {
	it('should complete full user journey', async () => {
		// 1. Register
		const registerResponse = await request(app).post('/api/auth/register').send({
			email: 'e2e@example.com',
			password: 'secure123',
			name: 'E2E User',
		});

		expect(registerResponse.status).toBe(201);
		const { token, userId } = registerResponse.body;

		// 2. Login
		const loginResponse = await request(app).post('/api/auth/login').send({
			email: 'e2e@example.com',
			password: 'secure123',
		});

		expect(loginResponse.status).toBe(200);

		// 3. Browse products
		const productsResponse = await request(app)
			.get('/api/products')
			.set('Authorization', `Bearer ${token}`);

		expect(productsResponse.status).toBe(200);
		const productId = productsResponse.body[0].id;

		// 4. Add to cart
		const cartResponse = await request(app)
			.post('/api/cart')
			.set('Authorization', `Bearer ${token}`)
			.send({ productId, quantity: 1 });

		expect(cartResponse.status).toBe(200);

		// 5. Checkout
		const checkoutResponse = await request(app)
			.post('/api/checkout')
			.set('Authorization', `Bearer ${token}`)
			.send({
				payment: { method: 'credit_card', token: 'test_token' },
			});

		expect(checkoutResponse.status).toBe(200);
		expect(checkoutResponse.body.order.status).toBe('completed');

		// 6. Verify order in database
		const order = await database.orders.findOne({ userId });
		expect(order).toBeDefined();
		expect(order.status).toBe('completed');
	});
});
```

## Common Integration Test Patterns

### Pattern 1: Repository Integration

```typescript
it('should save and retrieve entity', async () => {
	const repository = new UserRepository(realDatabase);

	const user = await repository.save({ email: 'test@example.com' });
	const retrieved = await repository.findById(user.id);

	expect(retrieved).toEqual(user);
});
```

### Pattern 2: Service Layer Integration

```typescript
it('should orchestrate multiple repositories', async () => {
	const orderService = new OrderService(realDb);

	const order = await orderService.createOrder({
		userId: 1,
		items: [{ productId: 10, quantity: 2 }],
	});

	expect(order.total).toBe(expectedTotal);

	// Verify inventory decreased
	const product = await realDb.products.findOne(10);
	expect(product.stock).toBe(originalStock - 2);
});
```

### Pattern 3: API Endpoint Integration

```typescript
it('should handle authentication flow', async () => {
	const loginResponse = await request(app)
		.post('/api/auth/login')
		.send({ email: 'user@test.com', password: 'pass' });

	const { token } = loginResponse.body;

	const protectedResponse = await request(app)
		.get('/api/profile')
		.set('Authorization', `Bearer ${token}`);

	expect(protectedResponse.status).toBe(200);
});
```

## Integration Test File Structure Template

```typescript
import request from 'supertest';
import { setupTestDatabase, teardownTestDatabase } from './test-helpers';
import { app } from '../app';
import { database } from '../database';

describe('Feature Integration Tests', () => {
	// Setup real dependencies
	beforeAll(async () => {
		await setupTestDatabase();
		await app.listen(0); // Random port
	});

	afterAll(async () => {
		await app.close();
		await teardownTestDatabase();
	});

	beforeEach(async () => {
		await database.clearAll();
	});

	describe('Happy Path Integration', () => {
		it('should complete workflow end-to-end', async () => {
			// Test with real dependencies
		});
	});

	describe('Error Scenarios Integration', () => {
		it('should handle errors across boundaries', async () => {
			// Test error propagation
		});
	});

	describe('Performance and Concurrency', () => {
		it('should handle concurrent operations', async () => {
			// Test race conditions
		});
	});
});
```
