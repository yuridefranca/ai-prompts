# Code Readability & Complexity

**Sources**:
- [Clean Code (Robert C. Martin)](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)
- [Code Complete (Steve McConnell)](https://www.microsoftpressstore.com/store/code-complete-9780735619678)
- [The Art of Readable Code](https://www.oreilly.com/library/view/the-art-of/9781449318482/)

---

## Naming Conventions

### Variable Names

**Principles**:
- Use descriptive, pronounceable names
- Avoid abbreviations unless universal
- Make distinctions meaningful
- Use searchable names

**Check**:
- [ ] Names are descriptive and clear?
- [ ] No single-letter variables (except loop counters)?
- [ ] No cryptic abbreviations?
- [ ] Boolean names indicate true/false?
- [ ] Names reveal intent?

```typescript
// ❌ BAD: Cryptic, abbreviated, unclear
const d = 86400;
const yyyymmdstr = formatDate(new Date());
const u = getUser();
const flag = checkStatus();

// ✅ GOOD: Clear, descriptive, searchable
const SECONDS_IN_DAY = 86400;
const currentDateFormatted = formatDate(new Date());
const activeUser = getUser();
const isUserActive = checkStatus();
const hasPermission = checkUserPermission();
```

### Function Names

**Check**:
- [ ] Function names are verbs or verb phrases?
- [ ] Names describe what function does?
- [ ] Consistent naming pattern?
- [ ] Names not too long (ideally <30 chars)?

```typescript
// ❌ BAD: Unclear, inconsistent
function data() { }          // What data?
function thing(u) { }        // What thing? What's u?
function process() { }       // Process what?

// ✅ GOOD: Clear, descriptive, consistent
function getUserById(id: number): User { }
function calculateTotalPrice(items: Item[]): number { }
function validateEmailFormat(email: string): boolean { }
function sendWelcomeEmail(user: User): Promise<void> { }
```

### Class Names

**Check**:
- [ ] Class names are nouns?
- [ ] Names describe what class represents?
- [ ] No generic names (Manager, Processor)?

```typescript
// ❌ BAD: Generic, unclear
class DataManager { }
class Processor { }
class Handler { }
class Utility { }

// ✅ GOOD: Specific, descriptive
class UserRepository { }
class EmailValidator { }
class PaymentProcessor { }
class OrderCalculator { }
```

### Constant Names

**Check**:
- [ ] Constants in UPPER_SNAKE_CASE?
- [ ] Magic numbers replaced with named constants?
- [ ] Purpose clear from name?

```typescript
// ❌ BAD: Magic numbers, unclear
if (age > 18) { }
setTimeout(callback, 3600000);
const tax = price * 0.0825;

// ✅ GOOD: Named constants
const MINIMUM_VOTING_AGE = 18;
const ONE_HOUR_IN_MS = 3600000;
const CALIFORNIA_SALES_TAX_RATE = 0.0825;

if (age > MINIMUM_VOTING_AGE) { }
setTimeout(callback, ONE_HOUR_IN_MS);
const tax = price * CALIFORNIA_SALES_TAX_RATE;
```

---

## Function Complexity

### Function Length

**Check**:
- [ ] Functions under 50 lines (ideally <20)?
- [ ] Each function does one thing?
- [ ] No long parameter lists (max 3-4)?
- [ ] Can understand function without scrolling?

```typescript
// ❌ BAD: Too long, does too much (80+ lines)
function processOrder(orderId, userId, items, discount, shipping, tax, payment) {
  // Validate user
  const user = getUser(userId);
  if (!user) throw new Error('User not found');
  if (!user.active) throw new Error('User inactive');
  
  // Validate items
  if (items.length === 0) throw new Error('No items');
  for (const item of items) {
    if (!item.id) throw new Error('Invalid item');
    const product = getProduct(item.id);
    if (!product) throw new Error('Product not found');
    if (product.stock < item.quantity) throw new Error('Out of stock');
  }
  
  // Calculate totals
  let subtotal = 0;
  for (const item of items) {
    subtotal += item.price * item.quantity;
  }
  const discountAmount = subtotal * discount;
  const taxAmount = (subtotal - discountAmount) * tax;
  const total = subtotal - discountAmount + taxAmount + shipping;
  
  // Process payment
  // ... 20 more lines
  
  // Update inventory
  // ... 20 more lines
  
  // Send notifications
  // ... 10 more lines
}

// ✅ GOOD: Broken into focused functions
function processOrder(request: OrderRequest): Order {
  const user = validateUser(request.userId);
  const validatedItems = validateOrderItems(request.items);
  const totals = calculateOrderTotals(validatedItems, request);
  const payment = processPayment(totals.total, request.paymentMethod);
  
  updateInventory(validatedItems);
  
  const order = createOrder({
    user,
    items: validatedItems,
    totals,
    payment
  });
  
  sendOrderConfirmation(order);
  
  return order;
}

function validateUser(userId: number): User {
  const user = userRepository.findById(userId);
  
  if (!user) {
    throw new NotFoundError('User not found');
  }
  
  if (!user.isActive) {
    throw new ValidationError('User account is inactive');
  }
  
  return user;
}

function validateOrderItems(items: OrderItemInput[]): ValidatedOrderItem[] {
  if (items.length === 0) {
    throw new ValidationError('Order must contain at least one item');
  }
  
  return items.map(validateOrderItem);
}

// ... other focused functions
```

### Cyclomatic Complexity

**Principle**: Reduce the number of independent paths through code.

**Check**:
- [ ] Complexity score < 10 (ideally < 5)?
- [ ] Not too many if/else branches?
- [ ] No deeply nested conditionals?
- [ ] Complex logic extracted to functions?

```typescript
// ❌ BAD: High complexity (complexity = 11)
function getDiscount(user, order, date) {
  if (user.isPremium) {
    if (order.total > 100) {
      if (date.getDay() === 0 || date.getDay() === 6) {
        return 0.25;
      } else if (user.loyaltyPoints > 1000) {
        return 0.20;
      } else {
        return 0.15;
      }
    } else if (order.total > 50) {
      if (user.loyaltyPoints > 500) {
        return 0.10;
      } else {
        return 0.05;
      }
    }
  } else {
    if (order.total > 200) {
      return 0.10;
    } else if (order.total > 100) {
      return 0.05;
    }
  }
  return 0;
}

// ✅ GOOD: Lower complexity with strategy pattern
interface DiscountStrategy {
  calculate(user: User, order: Order): number;
}

class PremiumWeekendDiscount implements DiscountStrategy {
  calculate(user: User, order: Order): number {
    if (!user.isPremium || !isWeekend()) return 0;
    if (order.total > 100) return 0.25;
    return 0;
  }
}

class PremiumLoyaltyDiscount implements DiscountStrategy {
  calculate(user: User, order: Order): number {
    if (!user.isPremium) return 0;
    
    if (order.total > 100 && user.loyaltyPoints > 1000) return 0.20;
    if (order.total > 100) return 0.15;
    if (order.total > 50 && user.loyaltyPoints > 500) return 0.10;
    if (order.total > 50) return 0.05;
    
    return 0;
  }
}

class StandardDiscount implements DiscountStrategy {
  calculate(user: User, order: Order): number {
    if (user.isPremium) return 0;
    
    if (order.total > 200) return 0.10;
    if (order.total > 100) return 0.05;
    
    return 0;
  }
}

class DiscountCalculator {
  private strategies: DiscountStrategy[] = [
    new PremiumWeekendDiscount(),
    new PremiumLoyaltyDiscount(),
    new StandardDiscount()
  ];
  
  calculate(user: User, order: Order): number {
    const discounts = this.strategies.map(s => s.calculate(user, order));
    return Math.max(...discounts);
  }
}
```

### Nesting Depth

**Check**:
- [ ] Nesting depth < 4 levels?
- [ ] Early returns used?
- [ ] Guard clauses at function start?
- [ ] Nested logic extracted to functions?

```typescript
// ❌ BAD: Deep nesting (5 levels)
function processPayment(order) {
  if (order) {
    if (order.items.length > 0) {
      if (order.total > 0) {
        if (order.user) {
          if (order.user.paymentMethod) {
            // Finally do something
            charge(order.user.paymentMethod, order.total);
          }
        }
      }
    }
  }
}

// ✅ GOOD: Guard clauses reduce nesting
function processPayment(order: Order): void {
  if (!order) {
    throw new ValidationError('Order is required');
  }
  
  if (order.items.length === 0) {
    throw new ValidationError('Order has no items');
  }
  
  if (order.total <= 0) {
    throw new ValidationError('Order total must be positive');
  }
  
  if (!order.user) {
    throw new ValidationError('Order must have a user');
  }
  
  if (!order.user.paymentMethod) {
    throw new ValidationError('User has no payment method');
  }
  
  charge(order.user.paymentMethod, order.total);
}
```

---

## Code Organization

### File Length

**Check**:
- [ ] Files under 300 lines (ideally <200)?
- [ ] Each file has single responsibility?
- [ ] Related code grouped together?
- [ ] Clear file organization?

```typescript
// ❌ BAD: Everything in one file (1000+ lines)
// user.ts
class User { }
class UserRepository { }
class UserService { }
class UserController { }
class UserValidator { }
class UserMapper { }
// ... 800 more lines

// ✅ GOOD: Organized into focused files
// user.model.ts
export class User { }

// user.repository.ts
export class UserRepository { }

// user.service.ts
export class UserService { }

// user.controller.ts
export class UserController { }

// user.validator.ts
export class UserValidator { }

// user.mapper.ts
export class UserMapper { }
```

### Import Organization

**Check**:
- [ ] Imports grouped logically?
- [ ] External imports separate from internal?
- [ ] Unused imports removed?
- [ ] Import order consistent?

```typescript
// ❌ BAD: Disorganized imports
import { User } from './models/user';
import express from 'express';
import { calculateTax } from './utils/tax';
import { z } from 'zod';
import { logger } from './logger';
import axios from 'axios';

// ✅ GOOD: Organized imports
// External dependencies
import express from 'express';
import axios from 'axios';
import { z } from 'zod';

// Internal utilities
import { logger } from './logger';
import { calculateTax } from './utils/tax';

// Models
import { User } from './models/user';
```

---

## Comments

### Comment Quality

**Principle**: Code should be self-documenting. Comments explain "why", not "what".

**Check**:
- [ ] Comments explain "why", not "what"?
- [ ] No obvious or redundant comments?
- [ ] No commented-out code?
- [ ] Complex logic explained?
- [ ] TODOs have ticket numbers?

```typescript
// ❌ BAD: Obvious comments
// Increment i by 1
i++;

// Create a new user
const user = new User();

// Loop through items
for (const item of items) {
  // Add item to cart
  cart.add(item);
}

// ❌ BAD: Commented-out code
function calculateTotal(items) {
  let total = 0;
  // const tax = 0.08;
  // const shipping = 5.99;
  for (const item of items) {
    total += item.price;
  }
  // total += shipping;
  return total;
}

// ✅ GOOD: Explains "why" and complex logic
function calculateDiscount(user: User, amount: number): number {
  // Business rule: Premium users get 20% discount on orders over $100
  // as per marketing campaign Q1-2024 (ticket: PROMO-123)
  if (user.isPremium && amount > 100) {
    return amount * 0.20;
  }
  
  // Legacy users (signed up before 2020) maintain old 15% discount
  // Cannot remove without migration (ticket: LEGACY-456)
  if (user.createdAt < new Date('2020-01-01')) {
    return amount * 0.15;
  }
  
  return 0;
}

// ✅ GOOD: Explain non-obvious algorithm
function calculateShipping(weight: number, distance: number): number {
  // Using USPS Zone-based pricing formula
  // Base rate + (weight factor * distance factor)
  // See: https://www.usps.com/business/prices.htm
  const baseRate = 5.00;
  const weightFactor = Math.ceil(weight / 16) * 0.50;  // Per pound
  const distanceFactor = Math.ceil(distance / 100) * 0.25;  // Per 100 miles
  
  return baseRate + (weightFactor * distanceFactor);
}
```

### Documentation Comments

**Check**:
- [ ] Public APIs documented?
- [ ] Parameters described?
- [ ] Return values described?
- [ ] Exceptions documented?
- [ ] Examples provided for complex APIs?

```typescript
// ✅ GOOD: Public API documentation
/**
 * Calculates the final price for an order including discounts and taxes.
 * 
 * @param items - Array of items in the order
 * @param user - User placing the order (affects discount eligibility)
 * @param shippingAddress - Shipping address (affects tax calculation)
 * @returns Final price breakdown with subtotal, discount, tax, and total
 * @throws {ValidationError} If items array is empty
 * @throws {NotFoundError} If user or any item doesn't exist
 * 
 * @example
 * ```typescript
 * const pricing = await calculateOrderPrice(
 *   [{ id: 1, quantity: 2 }],
 *   currentUser,
 *   { state: 'CA', zipCode: '90210' }
 * );
 * console.log(pricing.total); // 125.50
 * ```
 */
async function calculateOrderPrice(
  items: OrderItem[],
  user: User,
  shippingAddress: Address
): Promise<PriceBreakdown> {
  // Implementation
}
```

---

## Code Consistency

### Consistent Formatting

**Check**:
- [ ] Consistent indentation (2 or 4 spaces)?
- [ ] Consistent brace style?
- [ ] Consistent spacing?
- [ ] Formatter configured (Prettier, ESLint)?

```typescript
// ❌ BAD: Inconsistent formatting
function foo(x,y){
if(x>y){
return x
}
  else{
return y}}

// ✅ GOOD: Consistent formatting
function foo(x: number, y: number): number {
  if (x > y) {
    return x;
  } else {
    return y;
  }
}

// Or use formatter
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### Consistent Patterns

**Check**:
- [ ] Error handling consistent?
- [ ] Async patterns consistent (promises vs async/await)?
- [ ] Naming conventions consistent?
- [ ] Module structure consistent?

```typescript
// ❌ BAD: Inconsistent async handling
async function getUserById(id: number) {
  return db.users.findOne(id);  // Returns promise
}

function getOrders(userId: number) {
  db.orders.find(userId).then(orders => {  // Uses .then()
    return orders;
  });
}

function getProducts(categoryId: number, callback) {  // Uses callbacks!
  db.products.find(categoryId, (err, products) => {
    callback(err, products);
  });
}

// ✅ GOOD: Consistent async/await pattern
async function getUserById(id: number): Promise<User> {
  return await db.users.findOne(id);
}

async function getOrders(userId: number): Promise<Order[]> {
  return await db.orders.find(userId);
}

async function getProducts(categoryId: number): Promise<Product[]> {
  return await db.products.find(categoryId);
}
```

---

## Cognitive Load

### Reduce Mental Mapping

**Check**:
- [ ] No cryptic variable names?
- [ ] No mental translation needed?
- [ ] No encoded information in names?

```typescript
// ❌ BAD: Requires mental mapping
const arr = items.map(i => i.p * i.q);  // What's p? What's q?

// ✅ GOOD: Clear, no mapping needed
const itemTotals = items.map(item => item.price * item.quantity);
```

### One Thing Per Line

**Check**:
- [ ] One statement per line?
- [ ] No overly complex one-liners?
- [ ] Ternaries simple and clear?

```typescript
// ❌ BAD: Too much on one line
const result = users.filter(u => u.active && u.premium).map(u => ({...u, discount: u.total > 100 ? 0.2 : 0.1}));

// ✅ GOOD: Broken into readable steps
const activeUsers = users.filter(user => user.active && user.premium);

const usersWithDiscounts = activeUsers.map(user => ({
  ...user,
  discount: calculateDiscount(user.total)
}));

function calculateDiscount(total: number): number {
  return total > 100 ? 0.2 : 0.1;
}
```

---

## Duplication

### DRY Violations

**Check**:
- [ ] No copy-pasted code blocks?
- [ ] Shared logic extracted?
- [ ] Patterns abstracted?

```typescript
// ❌ BAD: Duplicated validation logic
function createUser(data) {
  if (!data.email || !data.email.includes('@')) {
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {
    throw new Error('Password too short');
  }
  // Create user
}

function updateUser(id, data) {
  if (!data.email || !data.email.includes('@')) {  // Duplicated!
    throw new Error('Invalid email');
  }
  if (!data.password || data.password.length < 8) {  // Duplicated!
    throw new Error('Password too short');
  }
  // Update user
}

// ✅ GOOD: Extract shared validation
function validateUserData(data: UserInput): void {
  if (!data.email || !data.email.includes('@')) {
    throw new ValidationError('Invalid email');
  }
  
  if (!data.password || data.password.length < 8) {
    throw new ValidationError('Password must be at least 8 characters');
  }
}

function createUser(data: UserInput): User {
  validateUserData(data);
  return userRepository.create(data);
}

function updateUser(id: number, data: UserInput): User {
  validateUserData(data);
  return userRepository.update(id, data);
}
```
