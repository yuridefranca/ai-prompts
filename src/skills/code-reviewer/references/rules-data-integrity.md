# Data Integrity & Validation

**Sources**:
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
- [Data Validation Best Practices](https://martinfowler.com/articles/domain-oriented-observability.html)
- [Database Constraints Best Practices](https://use-the-index-luke.com/)

---

## Input Validation

### Validation Strategy

**Principle**: Validate early, validate thoroughly, fail fast.

**Check**:
- [ ] All user input validated?
- [ ] Validation at API boundary?
- [ ] Whitelist approach (allow known good)?
- [ ] Validation before business logic?
- [ ] Clear validation error messages?

```typescript
// ❌ BAD: No validation, processing invalid data
function createUser(data: any) {
  // Directly using unvalidated input
  return database.users.create(data);
}

// ✅ GOOD: Validate at entry point
function createUser(data: unknown) {
  // Validate first
  const validated = UserSchema.parse(data); // Throws if invalid
  
  // Now safe to use
  return database.users.create(validated);
}

// ✅ GOOD: With detailed errors
function createUser(data: unknown) {
  const result = UserSchema.safeParse(data);
  
  if (!result.success) {
    throw new ValidationError('Invalid user data', {
      errors: result.error.errors.map(e => ({
        field: e.path.join('.'),
        message: e.message,
        code: e.code
      }))
    });
  }
  
  return database.users.create(result.data);
}
```

### Schema Validation

**Check**:
- [ ] Schema-based validation used?
- [ ] Type checking enforced?
- [ ] Required fields validated?
- [ ] Field formats validated?
- [ ] Custom validation rules applied?

```typescript
// ✅ GOOD: Comprehensive schema (using Zod example)
const UserSchema = z.object({
  email: z.string()
    .email('Must be valid email')
    .max(255, 'Email too long'),
  
  age: z.number()
    .int('Must be integer')
    .min(18, 'Must be 18 or older')
    .max(120, 'Invalid age'),
  
  password: z.string()
    .min(8, 'Minimum 8 characters')
    .regex(/[A-Z]/, 'Must contain uppercase')
    .regex(/[a-z]/, 'Must contain lowercase')
    .regex(/[0-9]/, 'Must contain number'),
  
  role: z.enum(['admin', 'user', 'guest'], {
    errorMap: () => ({ message: 'Invalid role' })
  }),
  
  phone: z.string()
    .regex(/^\+?[1-9]\d{1,14}$/, 'Invalid phone format')
    .optional(),
  
  metadata: z.record(z.string(), z.unknown())
    .optional()
    .default({})
});
```

---

## Data Type Safety

### Type Coercion

**Check**:
- [ ] No automatic type coercion?
- [ ] Explicit type conversion?
- [ ] Type mismatches caught early?

```typescript
// ❌ BAD: Automatic coercion causes bugs
function processAge(age) {
  if (age > 18) {  // "100" > 18 is true (string coercion)
    // ...
  }
}
processAge("100");  // Accidentally passes string

// ✅ GOOD: Strict type checking
function processAge(age: unknown) {
  if (typeof age !== 'number') {
    throw new TypeError('Age must be a number');
  }
  
  if (age > 18) {
    // Now safe
  }
}
```

### Null/Undefined Handling

**Check**:
- [ ] Null/undefined explicitly handled?
- [ ] No implicit null coercion?
- [ ] Optional vs required fields clear?
- [ ] Default values documented?

```typescript
// ❌ BAD: Undefined behavior
function getDisplayName(user) {
  return user.firstName + ' ' + user.lastName;
  // What if firstName is undefined?
}

// ✅ GOOD: Explicit handling
function getDisplayName(user: User): string {
  const firstName = user.firstName ?? '';
  const lastName = user.lastName ?? '';
  
  if (!firstName && !lastName) {
    return user.email;  // Fallback
  }
  
  return `${firstName} ${lastName}`.trim();
}

// ✅ GOOD: Type system enforces
interface User {
  firstName: string | null;  // Explicit nullable
  lastName: string | null;
  email: string;             // Required, non-null
}
```

---

## Boundary Validation

### String Length Limits

**Check**:
- [ ] Maximum length enforced?
- [ ] Minimum length enforced (where needed)?
- [ ] Database column sizes matched?
- [ ] No buffer overflows possible?

```typescript
// ❌ BAD: No length validation
const comment = { text: userInput };
await db.comments.create(comment);
// Database column is VARCHAR(500), but userInput could be 10,000 chars

// ✅ GOOD: Enforce limits
function validateComment(text: string): void {
  if (text.length < 1) {
    throw new ValidationError('Comment cannot be empty');
  }
  
  if (text.length > 500) {
    throw new ValidationError('Comment must be 500 characters or less');
  }
}
```

### Numeric Ranges

**Check**:
- [ ] Minimum values enforced?
- [ ] Maximum values enforced?
- [ ] Integer vs decimal specified?
- [ ] Precision specified?
- [ ] Negative values handled?

```typescript
// ❌ BAD: No range validation
function setDiscount(percentage: number) {
  const discount = price * (percentage / 100);
  // What if percentage is -100? Or 1000?
}

// ✅ GOOD: Range validation
function setDiscount(percentage: number): number {
  if (!Number.isFinite(percentage)) {
    throw new ValidationError('Discount must be a finite number');
  }
  
  if (percentage < 0 || percentage > 100) {
    throw new ValidationError('Discount must be between 0 and 100');
  }
  
  return price * (percentage / 100);
}
```

### Array/Collection Limits

**Check**:
- [ ] Maximum array size enforced?
- [ ] Empty arrays handled?
- [ ] Array element validation?

```typescript
// ❌ BAD: No array size limits
function processTags(tags: string[]) {
  tags.forEach(tag => addTag(tag));
  // User could send 1 million tags
}

// ✅ GOOD: Array validation
function processTags(tags: unknown): void {
  if (!Array.isArray(tags)) {
    throw new ValidationError('Tags must be an array');
  }
  
  if (tags.length === 0) {
    throw new ValidationError('At least one tag required');
  }
  
  if (tags.length > 10) {
    throw new ValidationError('Maximum 10 tags allowed');
  }
  
  // Validate each element
  tags.forEach((tag, index) => {
    if (typeof tag !== 'string') {
      throw new ValidationError(`Tag at index ${index} must be a string`);
    }
    
    if (tag.length > 50) {
      throw new ValidationError(`Tag at index ${index} is too long (max 50 chars)`);
    }
  });
  
  tags.forEach(tag => addTag(tag));
}
```

---

## Data Sanitization

### HTML/Script Injection Prevention

**Check**:
- [ ] User input sanitized before display?
- [ ] HTML tags escaped?
- [ ] No raw HTML insertion?
- [ ] XSS prevention in place?

```typescript
// ❌ BAD: Unsanitized output
element.innerHTML = userComment;  // XSS vulnerability!

// ✅ GOOD: Sanitize or escape
element.textContent = userComment;  // Automatically escapes
// OR
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userComment);
```

### SQL Injection Prevention

**Check**:
- [ ] Parameterized queries used?
- [ ] No string concatenation in queries?
- [ ] ORM used safely?

```typescript
// ❌ BAD: SQL injection vulnerability
const query = `SELECT * FROM users WHERE id = ${userId}`;
await db.query(query);

// ✅ GOOD: Parameterized query
const query = 'SELECT * FROM users WHERE id = $1';
await db.query(query, [userId]);

// ✅ GOOD: ORM with type safety
const user = await db.users.findOne({ where: { id: userId } });
```

---

## Referential Integrity

### Foreign Key Validation

**Check**:
- [ ] Foreign keys validated before use?
- [ ] Referenced entities exist?
- [ ] Cascade deletes configured correctly?
- [ ] Orphan records prevented?

```typescript
// ❌ BAD: No validation of foreign key
async function createOrder(userId: number, items: Item[]) {
  // Assumes user exists, but doesn't check
  return db.orders.create({ userId, items });
}

// ✅ GOOD: Validate foreign key
async function createOrder(userId: number, items: Item[]) {
  // Verify user exists
  const user = await db.users.findOne(userId);
  
  if (!user) {
    throw new NotFoundError(`User ${userId} not found`);
  }
  
  // Verify all product IDs exist
  const productIds = items.map(i => i.productId);
  const products = await db.products.findMany({
    where: { id: { in: productIds } }
  });
  
  if (products.length !== productIds.length) {
    throw new ValidationError('One or more products not found');
  }
  
  return db.orders.create({ userId, items });
}
```

---

## Data Consistency

### Transaction Boundaries

**Check**:
- [ ] Related operations in single transaction?
- [ ] Rollback on partial failure?
- [ ] ACID properties maintained?
- [ ] Isolation level appropriate?

```typescript
// ❌ BAD: No transaction, inconsistent state possible
async function transferMoney(fromId: number, toId: number, amount: number) {
  await accounts.decrease(fromId, amount);
  // If this fails, money is lost!
  await accounts.increase(toId, amount);
}

// ✅ GOOD: Transaction ensures consistency
async function transferMoney(fromId: number, toId: number, amount: number) {
  await db.transaction(async (tx) => {
    // Both operations succeed or both fail
    await tx.accounts.decrease(fromId, amount);
    await tx.accounts.increase(toId, amount);
  });
  // Automatic rollback if any operation fails
}
```

### Optimistic Locking

**Check**:
- [ ] Concurrent updates handled?
- [ ] Version numbers or timestamps used?
- [ ] Conflict detection in place?

```typescript
// ❌ BAD: Last write wins (lost updates)
async function updateInventory(productId: number, quantity: number) {
  const product = await db.products.findOne(productId);
  product.quantity = quantity;
  await db.products.update(productId, product);
  // Another request might have updated in between
}

// ✅ GOOD: Optimistic locking with version
async function updateInventory(productId: number, quantity: number, version: number) {
  const result = await db.products.update(
    { id: productId, version: version },
    { quantity, version: version + 1 }
  );
  
  if (result.rowsAffected === 0) {
    throw new ConflictError('Product was modified by another request. Please retry.');
  }
}
```

---

## Invariant Enforcement

### Business Rule Validation

**Check**:
- [ ] Business invariants enforced?
- [ ] Domain rules validated?
- [ ] State transitions validated?
- [ ] Constraints at domain level?

```typescript
// ❌ BAD: Allows invalid state
class Order {
  status: string;
  items: Item[];
  
  cancel() {
    this.status = 'cancelled';
    // But items might already be shipped!
  }
}

// ✅ GOOD: Enforce business rules
class Order {
  private _status: OrderStatus;
  private _items: Item[];
  
  get status(): OrderStatus {
    return this._status;
  }
  
  cancel(): void {
    // Enforce: can't cancel shipped orders
    if (this._status === 'shipped') {
      throw new InvalidOperationError('Cannot cancel shipped order');
    }
    
    // Enforce: can't cancel empty orders
    if (this._items.length === 0) {
      throw new InvalidOperationError('Cannot cancel empty order');
    }
    
    this._status = 'cancelled';
  }
}
```

### State Machine Validation

**Check**:
- [ ] Valid state transitions defined?
- [ ] Invalid transitions prevented?
- [ ] State transition logged?

```typescript
// ✅ GOOD: State machine with validation
class OrderStateMachine {
  private static validTransitions = {
    'pending': ['confirmed', 'cancelled'],
    'confirmed': ['processing', 'cancelled'],
    'processing': ['shipped', 'cancelled'],
    'shipped': ['delivered'],
    'delivered': [],
    'cancelled': []
  };
  
  static canTransition(from: OrderStatus, to: OrderStatus): boolean {
    return this.validTransitions[from]?.includes(to) ?? false;
  }
  
  transition(order: Order, newStatus: OrderStatus): void {
    if (!OrderStateMachine.canTransition(order.status, newStatus)) {
      throw new InvalidTransitionError(
        `Cannot transition from ${order.status} to ${newStatus}`
      );
    }
    
    order.status = newStatus;
    this.logTransition(order.id, order.status, newStatus);
  }
}
```

---

## Data Transformation

### Parse vs Transform

**Check**:
- [ ] Parsing errors handled?
- [ ] Invalid data rejected early?
- [ ] Transformation reversible (if needed)?
- [ ] Data loss prevented?

```typescript
// ❌ BAD: Silent data loss
function parseDate(input: string): Date {
  return new Date(input);  // Returns "Invalid Date" for bad input
}

// ✅ GOOD: Explicit validation
function parseDate(input: string): Date {
  const date = new Date(input);
  
  if (isNaN(date.getTime())) {
    throw new ValidationError(`Invalid date format: ${input}`);
  }
  
  return date;
}

// ✅ GOOD: Safe parsing
function parseDate(input: string): Date | null {
  try {
    const date = new Date(input);
    return isNaN(date.getTime()) ? null : date;
  } catch {
    return null;
  }
}
```

### Normalization

**Check**:
- [ ] Data normalized before storage?
- [ ] Case sensitivity handled?
- [ ] Whitespace trimmed?
- [ ] Unicode normalization applied?

```typescript
// ❌ BAD: No normalization
function createUser(email: string) {
  return db.users.create({ email });
  // "User@Example.com" and "user@example.com" are different
}

// ✅ GOOD: Normalize before storage
function createUser(email: string) {
  const normalized = email.trim().toLowerCase();
  
  // Check for duplicates with normalized value
  const existing = await db.users.findOne({ email: normalized });
  
  if (existing) {
    throw new ConflictError('Email already registered');
  }
  
  return db.users.create({ email: normalized });
}
```

---

## Unique Constraints

### Uniqueness Validation

**Check**:
- [ ] Unique constraints at database level?
- [ ] Duplicate checks before insert?
- [ ] Race conditions handled?
- [ ] Clear error messages for duplicates?

```typescript
// ❌ BAD: Only application-level check (race condition)
async function createUser(email: string) {
  const existing = await db.users.findOne({ email });
  
  if (existing) {
    throw new ConflictError('Email already exists');
  }
  
  // Another request could insert here!
  return db.users.create({ email });
}

// ✅ GOOD: Database constraint + application check
// In migration:
// CREATE UNIQUE INDEX users_email_unique ON users(email);

async function createUser(email: string) {
  try {
    return await db.users.create({ email });
  } catch (error) {
    if (error.code === 'UNIQUE_VIOLATION') {
      throw new ConflictError('Email already registered');
    }
    throw error;
  }
}
```

---

## Data Privacy

### PII Handling

**Check**:
- [ ] PII fields identified?
- [ ] PII not logged?
- [ ] PII encrypted at rest?
- [ ] PII minimization applied?

```typescript
// ❌ BAD: Logging PII
logger.info('User login', {
  email: user.email,
  password: password,  // Never log passwords!
  ssn: user.ssn        // Never log SSN!
});

// ✅ GOOD: Redact PII from logs
logger.info('User login', {
  userId: user.id,
  email: redactEmail(user.email),  // user@example.com -> u***@example.com
  ip: request.ip
});

function redactEmail(email: string): string {
  const [local, domain] = email.split('@');
  return `${local[0]}***@${domain}`;
}
```

---

## Date/Time Handling

### Timezone Safety

**Check**:
- [ ] Dates stored in UTC?
- [ ] Timezone conversion explicit?
- [ ] Date formats consistent (ISO 8601)?
- [ ] Timestamp precision defined?

```typescript
// ❌ BAD: Ambiguous date handling
const createdAt = new Date();  // Local timezone
await db.users.create({ createdAt });

// ✅ GOOD: Explicit UTC
const createdAt = new Date();  // Stores in UTC
await db.users.create({
  createdAt: createdAt.toISOString()  // "2024-01-15T10:30:00.000Z"
});

// ✅ GOOD: Timezone-aware display
function displayDate(date: Date, userTimezone: string): string {
  return date.toLocaleString('en-US', {
    timeZone: userTimezone,
    dateStyle: 'medium',
    timeStyle: 'short'
  });
}
```
