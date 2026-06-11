# Business Logic Quality

**Sources**:
- [Domain-Driven Design (Eric Evans)](https://www.domainlanguage.com/ddd/)
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Enterprise Application Architecture (Martin Fowler)](https://martinfowler.com/eaaCatalog/)

---

## Domain Modeling

### Ubiquitous Language

**Principle**: Code should speak the language of the business domain.

**Check**:
- [ ] Domain terms used consistently?
- [ ] Technical jargon avoided in domain layer?
- [ ] Business concepts clearly named?
- [ ] Terms match business documentation?

```typescript
// ❌ BAD: Technical/generic names, unclear domain concepts
class Record {
  data: any;
  process() { }
}

function handleSubmission(obj: any) {
  const items = obj.list;
  const val = calc(items);
  return val;
}

// ✅ GOOD: Domain language, clear business concepts
class Order {
  items: OrderItem[];
  customer: Customer;
  
  calculateTotal(): Money {
    return this.items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.zero()
    );
  }
}

class OrderItem {
  product: Product;
  quantity: Quantity;
  
  get lineTotal(): Money {
    return this.product.price.multiply(this.quantity.value);
  }
}

function processCheckout(cart: ShoppingCart): CheckoutResult {
  const order = cart.convertToOrder();
  const total = order.calculateTotal();
  return new CheckoutResult(order, total);
}
```

### Value Objects

**Check**:
- [ ] Domain values modeled as value objects?
- [ ] Value objects immutable?
- [ ] Validation in value object constructor?
- [ ] Equality based on value, not identity?

```typescript
// ❌ BAD: Primitive obsession
function createProduct(name: string, price: number, currency: string) {
  if (price < 0) throw new Error('Invalid price');
  if (currency.length !== 3) throw new Error('Invalid currency');
  // Business logic mixed with validation
}

// ✅ GOOD: Value objects encapsulate domain concepts
class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: Currency
  ) {
    if (amount < 0) {
      throw new ValidationError('Amount cannot be negative');
    }
  }
  
  static of(amount: number, currency: Currency): Money {
    return new Money(amount, currency);
  }
  
  add(other: Money): Money {
    if (!this.currency.equals(other.currency)) {
      throw new InvalidOperationError('Cannot add different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }
  
  multiply(factor: number): Money {
    return new Money(this.amount * factor, this.currency);
  }
  
  equals(other: Money): boolean {
    return this.amount === other.amount && 
           this.currency.equals(other.currency);
  }
}

class EmailAddress {
  private constructor(private readonly value: string) {
    if (!this.isValid(value)) {
      throw new ValidationError('Invalid email address');
    }
  }
  
  static of(value: string): EmailAddress {
    return new EmailAddress(value.trim().toLowerCase());
  }
  
  private isValid(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
  
  toString(): string {
    return this.value;
  }
}

// Now business logic is clean
function createProduct(
  name: ProductName,
  price: Money,
  category: Category
): Product {
  return new Product(name, price, category);
}
```

---

## Business Rules

### Rule Encapsulation

**Check**:
- [ ] Business rules in domain objects, not services?
- [ ] Rules close to data they operate on?
- [ ] Rules not scattered across layers?
- [ ] Rules testable in isolation?

```typescript
// ❌ BAD: Business rules in service layer
class OrderService {
  placeOrder(order: Order): void {
    // Business rules scattered in service
    if (order.items.length === 0) {
      throw new Error('Order must have items');
    }
    
    let total = 0;
    for (const item of order.items) {
      total += item.price * item.quantity;
    }
    
    if (order.customer.isPremium && total > 100) {
      total *= 0.9;  // 10% discount
    }
    
    if (order.customer.country === 'US') {
      total *= 1.08;  // Sales tax
    }
    
    order.total = total;
    this.repository.save(order);
  }
}

// ✅ GOOD: Business rules in domain objects
class Order {
  private _items: OrderItem[] = [];
  private _customer: Customer;
  private _status: OrderStatus = OrderStatus.Draft;
  
  constructor(customer: Customer) {
    this._customer = customer;
  }
  
  addItem(item: OrderItem): void {
    if (this._status !== OrderStatus.Draft) {
      throw new InvalidOperationError('Cannot modify submitted order');
    }
    
    this._items.push(item);
  }
  
  calculateTotal(): Money {
    if (this._items.length === 0) {
      throw new InvalidOperationError('Cannot calculate total for empty order');
    }
    
    const subtotal = this._items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.zero()
    );
    
    const discounted = this._customer.applyDiscount(subtotal);
    const withTax = this._customer.applyTax(discounted);
    
    return withTax;
  }
  
  submit(): void {
    if (this._items.length === 0) {
      throw new InvalidOperationError('Cannot submit empty order');
    }
    
    if (this._status !== OrderStatus.Draft) {
      throw new InvalidOperationError('Order already submitted');
    }
    
    this._status = OrderStatus.Submitted;
  }
}

class Customer {
  applyDiscount(amount: Money): Money {
    if (this.isPremium && amount.greaterThan(Money.of(100, 'USD'))) {
      return amount.multiply(0.9);  // 10% premium discount
    }
    return amount;
  }
  
  applyTax(amount: Money): Money {
    const taxRate = this.getTaxRateForCountry();
    return amount.multiply(1 + taxRate);
  }
  
  private getTaxRateForCountry(): number {
    return this.country === 'US' ? 0.08 : 0.0;
  }
}
```

### Invariant Enforcement

**Check**:
- [ ] Invariants enforced at all times?
- [ ] No invalid states possible?
- [ ] Validation in constructors?
- [ ] Setters validate or removed?

```typescript
// ❌ BAD: Allows invalid states
class BankAccount {
  balance: number = 0;  // Public, can be set to anything
  overdraftLimit: number = 0;
  
  withdraw(amount: number) {
    this.balance -= amount;  // Could go negative without limit check
  }
}

// Usage creates invalid state
const account = new BankAccount();
account.balance = -1000;  // Invalid!
account.overdraftLimit = -500;  // Invalid!

// ✅ GOOD: Invariants always enforced
class BankAccount {
  private _balance: Money;
  private _overdraftLimit: Money;
  
  constructor(initialBalance: Money, overdraftLimit: Money) {
    if (initialBalance.isNegative()) {
      throw new ValidationError('Initial balance cannot be negative');
    }
    
    if (overdraftLimit.isNegative()) {
      throw new ValidationError('Overdraft limit cannot be negative');
    }
    
    this._balance = initialBalance;
    this._overdraftLimit = overdraftLimit;
  }
  
  get balance(): Money {
    return this._balance;
  }
  
  withdraw(amount: Money): void {
    if (amount.isNegative() || amount.isZero()) {
      throw new ValidationError('Withdrawal amount must be positive');
    }
    
    const newBalance = this._balance.subtract(amount);
    const minimumAllowed = this._overdraftLimit.negate();
    
    if (newBalance.lessThan(minimumAllowed)) {
      throw new InsufficientFundsError(
        `Withdrawal would exceed overdraft limit. Available: ${this._balance.add(this._overdraftLimit)}`
      );
    }
    
    this._balance = newBalance;
  }
  
  deposit(amount: Money): void {
    if (amount.isNegative() || amount.isZero()) {
      throw new ValidationError('Deposit amount must be positive');
    }
    
    this._balance = this._balance.add(amount);
  }
}
```

---

## State Management

### State Machines

**Check**:
- [ ] Valid state transitions defined?
- [ ] Invalid transitions prevented?
- [ ] State-specific behavior encapsulated?
- [ ] Current state always clear?

```typescript
// ❌ BAD: No clear state machine, allows invalid transitions
class Order {
  status: string = 'pending';
  
  ship() {
    this.status = 'shipped';  // What if already cancelled?
  }
  
  cancel() {
    this.status = 'cancelled';  // What if already shipped?
  }
}

// ✅ GOOD: Explicit state machine
enum OrderStatus {
  Draft = 'draft',
  Submitted = 'submitted',
  Confirmed = 'confirmed',
  Shipped = 'shipped',
  Delivered = 'delivered',
  Cancelled = 'cancelled'
}

class Order {
  private _status: OrderStatus = OrderStatus.Draft;
  
  private static readonly validTransitions: Record<OrderStatus, OrderStatus[]> = {
    [OrderStatus.Draft]: [OrderStatus.Submitted, OrderStatus.Cancelled],
    [OrderStatus.Submitted]: [OrderStatus.Confirmed, OrderStatus.Cancelled],
    [OrderStatus.Confirmed]: [OrderStatus.Shipped, OrderStatus.Cancelled],
    [OrderStatus.Shipped]: [OrderStatus.Delivered],
    [OrderStatus.Delivered]: [],
    [OrderStatus.Cancelled]: []
  };
  
  get status(): OrderStatus {
    return this._status;
  }
  
  submit(): void {
    this.transitionTo(OrderStatus.Submitted);
  }
  
  confirm(): void {
    this.transitionTo(OrderStatus.Confirmed);
  }
  
  ship(): void {
    this.transitionTo(OrderStatus.Shipped);
  }
  
  deliver(): void {
    this.transitionTo(OrderStatus.Delivered);
  }
  
  cancel(): void {
    this.transitionTo(OrderStatus.Cancelled);
  }
  
  private transitionTo(newStatus: OrderStatus): void {
    const validNextStatuses = Order.validTransitions[this._status];
    
    if (!validNextStatuses.includes(newStatus)) {
      throw new InvalidStateTransitionError(
        `Cannot transition from ${this._status} to ${newStatus}`
      );
    }
    
    this._status = newStatus;
  }
}
```

---

## Separation of Concerns

### Domain vs Infrastructure

**Check**:
- [ ] Domain logic independent of infrastructure?
- [ ] No database queries in domain objects?
- [ ] No HTTP/framework code in domain?
- [ ] Dependency direction: Infrastructure → Domain?

```typescript
// ❌ BAD: Domain logic mixed with infrastructure
class Order {
  async save() {
    // Domain object knows about database!
    await db.orders.insert(this);
  }
  
  async sendConfirmationEmail() {
    // Domain object knows about email service!
    await emailService.send({
      to: this.customer.email,
      subject: 'Order confirmed'
    });
  }
}

// ✅ GOOD: Domain separated from infrastructure
// Domain layer (pure business logic)
class Order {
  private _items: OrderItem[];
  private _customer: Customer;
  
  calculateTotal(): Money {
    return this._items.reduce(
      (sum, item) => sum.add(item.lineTotal),
      Money.zero()
    );
  }
  
  submit(): OrderSubmittedEvent {
    if (this._items.length === 0) {
      throw new InvalidOperationError('Cannot submit empty order');
    }
    
    this._status = OrderStatus.Submitted;
    
    // Return domain event instead of side effect
    return new OrderSubmittedEvent(this);
  }
}

// Infrastructure layer (handles persistence, external services)
class OrderRepository {
  async save(order: Order): Promise<void> {
    await this.db.orders.insert(this.toDatabase(order));
  }
  
  async findById(id: string): Promise<Order | null> {
    const data = await this.db.orders.findOne(id);
    return data ? this.toDomain(data) : null;
  }
}

class OrderEventHandler {
  async handle(event: OrderSubmittedEvent): Promise<void> {
    await this.emailService.sendOrderConfirmation(event.order);
    await this.inventoryService.reserveItems(event.order.items);
  }
}
```

### Service Layer

**Check**:
- [ ] Services coordinate, don't contain business logic?
- [ ] Transaction boundaries at service level?
- [ ] Services thin, domain objects rich?

```typescript
// ❌ BAD: Anemic domain, fat services
class Order {
  items: OrderItem[];
  total: number;
  status: string;
}

class OrderService {
  // All business logic in service
  async createOrder(customerId: number, items: OrderItem[]) {
    const customer = await this.customerRepo.findById(customerId);
    
    let total = 0;
    for (const item of items) {
      total += item.price * item.quantity;
    }
    
    if (customer.isPremium && total > 100) {
      total *= 0.9;
    }
    
    const order = new Order();
    order.items = items;
    order.total = total;
    order.status = 'pending';
    
    await this.orderRepo.save(order);
    await this.emailService.send(customer.email, 'Order created');
  }
}

// ✅ GOOD: Rich domain, thin services
class Order {
  // Business logic in domain
  constructor(customer: Customer) { }
  addItem(item: OrderItem): void { }
  calculateTotal(): Money { }
  submit(): OrderSubmittedEvent { }
}

class OrderService {
  // Service coordinates, doesn't implement business logic
  async createOrder(
    customerId: CustomerId,
    itemsData: CreateOrderItemDTO[]
  ): Promise<Order> {
    return await this.db.transaction(async () => {
      const customer = await this.customerRepo.findById(customerId);
      
      if (!customer) {
        throw new NotFoundError('Customer not found');
      }
      
      // Domain object handles business logic
      const order = new Order(customer);
      
      for (const itemData of itemsData) {
        const product = await this.productRepo.findById(itemData.productId);
        const item = OrderItem.create(product, itemData.quantity);
        order.addItem(item);
      }
      
      const event = order.submit();
      
      await this.orderRepo.save(order);
      await this.eventBus.publish(event);
      
      return order;
    });
  }
}
```

---

## Edge Cases

### Business Edge Cases

**Check**:
- [ ] Zero values handled?
- [ ] Boundary values tested?
- [ ] Unusual combinations considered?
- [ ] Edge cases documented?

```typescript
// ❌ BAD: Edge cases not handled
class DiscountCalculator {
  calculate(orderTotal: number, discountPercent: number): number {
    return orderTotal * (discountPercent / 100);
    // What if discountPercent is 0? 100? -10? 1000?
    // What if orderTotal is 0? Negative?
  }
}

// ✅ GOOD: Edge cases explicitly handled
class DiscountCalculator {
  calculate(orderTotal: Money, discountPercent: Percentage): Money {
    // Handle zero order total
    if (orderTotal.isZero()) {
      return Money.zero();
    }
    
    // Validation happens in Percentage value object
    // - Can't be negative
    // - Can't be > 100
    // - Can be 0 (no discount)
    
    // Handle 100% discount (free order)
    if (discountPercent.isOneHundred()) {
      return orderTotal;
    }
    
    return orderTotal.multiply(discountPercent.asDecimal());
  }
}

class Percentage {
  private constructor(private readonly value: number) {
    if (value < 0 || value > 100) {
      throw new ValidationError('Percentage must be between 0 and 100');
    }
  }
  
  static of(value: number): Percentage {
    return new Percentage(value);
  }
  
  isZero(): boolean {
    return this.value === 0;
  }
  
  isOneHundred(): boolean {
    return this.value === 100;
  }
  
  asDecimal(): number {
    return this.value / 100;
  }
}
```

---

## Business Logic Testing

### Test Business Rules

**Check**:
- [ ] Business rules have unit tests?
- [ ] Edge cases tested?
- [ ] Invalid operations tested?
- [ ] Tests use domain language?

```typescript
// ✅ GOOD: Business logic tested with domain language
describe('Order', () => {
  describe('applying premium discount', () => {
    it('should apply 10% discount for premium customers when order total exceeds $100', () => {
      const premiumCustomer = Customer.createPremium('john@example.com');
      const order = new Order(premiumCustomer);
      
      order.addItem(OrderItem.create(
        Product.create('Widget', Money.of(60, 'USD')),
        Quantity.of(2)  // Total: $120
      ));
      
      const total = order.calculateTotal();
      
      expect(total).toEqual(Money.of(108, 'USD'));  // 120 - 12 (10%)
    });
    
    it('should not apply discount when order total is below $100', () => {
      const premiumCustomer = Customer.createPremium('john@example.com');
      const order = new Order(premiumCustomer);
      
      order.addItem(OrderItem.create(
        Product.create('Widget', Money.of(40, 'USD')),
        Quantity.of(2)  // Total: $80
      ));
      
      const total = order.calculateTotal();
      
      expect(total).toEqual(Money.of(80, 'USD'));  // No discount
    });
    
    it('should not apply discount for regular customers', () => {
      const regularCustomer = Customer.createRegular('jane@example.com');
      const order = new Order(regularCustomer);
      
      order.addItem(OrderItem.create(
        Product.create('Widget', Money.of(60, 'USD')),
        Quantity.of(2)  // Total: $120
      ));
      
      const total = order.calculateTotal();
      
      expect(total).toEqual(Money.of(120, 'USD'));  // No discount
    });
  });
  
  describe('state transitions', () => {
    it('should not allow shipping a cancelled order', () => {
      const order = createOrder();
      order.submit();
      order.cancel();
      
      expect(() => order.ship()).toThrow(InvalidStateTransitionError);
    });
  });
});
```

---

## Documentation

### Business Rule Documentation

**Check**:
- [ ] Complex business rules documented?
- [ ] Business rationale explained?
- [ ] References to business requirements?
- [ ] Examples provided?

```typescript
/**
 * Calculates shipping cost based on USPS Priority Mail rates.
 * 
 * Business Rules:
 * - Domestic orders: Base rate $7.50 + $0.50 per pound
 * - International orders: Base rate $25.00 + $2.00 per pound
 * - Free shipping for orders over $100 (domestic only)
 * - Premium members always get free domestic shipping
 * 
 * See: Business Requirements Document PRD-2024-001
 * 
 * @throws {ValidationError} If weight is negative or zero
 */
class ShippingCalculator {
  calculate(
    order: Order,
    destination: Address,
    weight: Weight
  ): Money {
    // Implementation
  }
}
```
