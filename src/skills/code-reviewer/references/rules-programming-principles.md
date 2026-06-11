# Programming Principles & Paradigms

**Sources**:
- [Clean Code (Robert C. Martin)](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)
- [SOLID Principles](https://www.digitalocean.com/community/conceptual-articles/s-o-l-i-d-the-first-five-principles-of-object-oriented-design)
- [Refactoring.guru](https://refactoring.guru/refactoring/what-is-refactoring)

---

## SOLID Principles

### Single Responsibility Principle (SRP)

**Principle**: A class should have one, and only one, reason to change. Each class should have a single, well-defined purpose.

**Check**:
- [ ] Each class has one clear responsibility?
- [ ] Changes to one feature don't require changes to unrelated classes?
- [ ] Class name clearly indicates its purpose?

```typescript
// ❌ BAD: Class does too much
class UserService {
  createUser() { /* User creation logic */ }
  sendWelcomeEmail() { /* Email logic */ }
  generateReport() { /* Reporting logic */ }
  logActivity() { /* Logging logic */ }
}

// ✅ GOOD: Separate responsibilities
class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService,
    private readonly activityLogger: ActivityLogger
  ) {}
  
  async createUser(dto: CreateUserDto) {
    const user = await this.userRepository.save(dto);
    await this.emailService.sendWelcomeEmail(user);
    await this.activityLogger.log('user_created', user.id);
    return user;
  }
}

class EmailService {
  sendWelcomeEmail(user: User) { /* Email logic */ }
}

class ReportService {
  generateReport() { /* Reporting logic */ }
}

class ActivityLogger {
  log(action: string, userId: number) { /* Logging logic */ }
}
```

### Open/Closed Principle (OCP)

**Principle**: Software entities should be open for extension, but closed for modification. You should be able to add new functionality without changing existing code.

**Check**:
- [ ] Can add new features without modifying existing code?
- [ ] Uses interfaces/abstract classes for extension points?
- [ ] Strategy pattern used where appropriate?

```typescript
// ❌ BAD: Must modify class to add new payment types
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.type === 'credit_card') {
      // Process credit card
    } else if (payment.type === 'paypal') {
      // Process PayPal
    } else if (payment.type === 'bitcoin') {
      // Process Bitcoin - had to modify existing code!
    }
  }
}

// ✅ GOOD: Open for extension, closed for modification
interface PaymentMethod {
  process(amount: number): Promise<PaymentResult>;
}

class CreditCardPayment implements PaymentMethod {
  async process(amount: number) {
    // Credit card logic
  }
}

class PayPalPayment implements PaymentMethod {
  async process(amount: number) {
    // PayPal logic
  }
}

class BitcoinPayment implements PaymentMethod {
  async process(amount: number) {
    // Bitcoin logic - no modification to existing code!
  }
}

class PaymentProcessor {
  constructor(private paymentMethod: PaymentMethod) {}
  
  async process(amount: number) {
    return this.paymentMethod.process(amount);
  }
}
```

### Liskov Substitution Principle (LSP)

**Principle**: Objects of a superclass should be replaceable with objects of a subclass without breaking the application. Subtypes must be substitutable for their base types.

**Check**:
- [ ] Subtypes behave like base types?
- [ ] No broken inheritance?
- [ ] Subclasses don't remove functionality?
- [ ] Preconditions not strengthened in subclasses?
- [ ] Postconditions not weakened in subclasses?

```typescript
// ❌ BAD: Square violates LSP for Rectangle
class Rectangle {
  constructor(protected width: number, protected height: number) {}
  
  setWidth(width: number) {
    this.width = width;
  }
  
  setHeight(height: number) {
    this.height = height;
  }
  
  area(): number {
    return this.width * this.height;
  }
}

class Square extends Rectangle {
  setWidth(width: number) {
    this.width = width;
    this.height = width; // Violates expectations!
  }
  
  setHeight(height: number) {
    this.width = height;
    this.height = height; // Violates expectations!
  }
}

// This breaks with Square
function resizeRectangle(rect: Rectangle) {
  rect.setWidth(5);
  rect.setHeight(4);
  console.assert(rect.area() === 20); // Fails for Square!
}

// ✅ GOOD: Separate hierarchies
interface Shape {
  area(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  
  area(): number {
    return this.width * this.height;
  }
}

class Square implements Shape {
  constructor(private side: number) {}
  
  area(): number {
    return this.side * this.side;
  }
}
```

### Interface Segregation Principle (ISP)

**Principle**: No client should be forced to depend on methods it does not use. Many specific interfaces are better than one general-purpose interface.

**Check**:
- [ ] Interfaces are focused and cohesive?
- [ ] No "fat" interfaces forcing unnecessary implementations?
- [ ] Clients depend only on methods they use?

```typescript
// ❌ BAD: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class HumanWorker implements Worker {
  work() { /* Work */ }
  eat() { /* Eat */ }
  sleep() { /* Sleep */ }
}

class RobotWorker implements Worker {
  work() { /* Work */ }
  eat() { /* Robots don't eat - forced to implement! */ }
  sleep() { /* Robots don't sleep - forced to implement! */ }
}

// ✅ GOOD: Segregated interfaces
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class HumanWorker implements Workable, Eatable, Sleepable {
  work() { /* Work */ }
  eat() { /* Eat */ }
  sleep() { /* Sleep */ }
}

class RobotWorker implements Workable {
  work() { /* Work */ }
  // Only implements what it needs!
}
```

### Dependency Inversion Principle (DIP)

**Principle**: High-level modules should not depend on low-level modules. Both should depend on abstractions. Abstractions should not depend on details. Details should depend on abstractions.

**Check**:
- [ ] Depends on abstractions (interfaces), not concretions (classes)?
- [ ] Uses dependency injection?
- [ ] High-level code not coupled to low-level implementation details?

```typescript
// ❌ BAD: High-level depends on low-level
class MySQLDatabase {
  save(data: any) {
    // MySQL-specific code
  }
}

class UserService {
  private db = new MySQLDatabase(); // Tightly coupled!
  
  saveUser(user: User) {
    this.db.save(user);
  }
}

// ✅ GOOD: Both depend on abstraction
interface Database {
  save(data: any): Promise<void>;
}

class MySQLDatabase implements Database {
  async save(data: any) {
    // MySQL-specific code
  }
}

class PostgreSQLDatabase implements Database {
  async save(data: any) {
    // PostgreSQL-specific code
  }
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction!
  
  async saveUser(user: User) {
    await this.db.save(user);
  }
}

// Can easily swap implementations
const service1 = new UserService(new MySQLDatabase());
const service2 = new UserService(new PostgreSQLDatabase());
```

---

## DRY (Don't Repeat Yourself)

**Principle**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**Source**: [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)

**Check**:
- [ ] No duplicated code?
- [ ] No duplicated logic?
- [ ] Shared functionality extracted into utilities?
- [ ] Constants defined once?

```typescript
// ❌ BAD: Duplication
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateUserEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); // Duplicated regex!
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); // Duplicated again!
}

// ✅ GOOD: Single source of truth
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function validateEmail(email: string): boolean {
  return EMAIL_REGEX.test(email);
}

// Or as a utility module
export class EmailValidator {
  private static readonly EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
  static validate(email: string): boolean {
    return this.EMAIL_REGEX.test(email);
  }
}
```

```typescript
// ❌ BAD: Duplicated business logic
class OrderService {
  calculateTotal(items: Item[]) {
    let total = 0;
    for (const item of items) {
      total += item.price * item.quantity;
      total += item.price * item.quantity * 0.1; // Tax
    }
    return total;
  }
}

class InvoiceService {
  generateInvoice(items: Item[]) {
    let total = 0;
    for (const item of items) {
      total += item.price * item.quantity;
      total += item.price * item.quantity * 0.1; // Duplicated tax logic!
    }
    return { total, items };
  }
}

// ✅ GOOD: Extract shared logic
class PriceCalculator {
  private static readonly TAX_RATE = 0.1;
  
  static calculateItemTotal(item: Item): number {
    return item.price * item.quantity;
  }
  
  static calculateTax(subtotal: number): number {
    return subtotal * this.TAX_RATE;
  }
  
  static calculateTotal(items: Item[]): number {
    const subtotal = items.reduce(
      (sum, item) => sum + this.calculateItemTotal(item),
      0
    );
    return subtotal + this.calculateTax(subtotal);
  }
}

class OrderService {
  calculateTotal(items: Item[]) {
    return PriceCalculator.calculateTotal(items);
  }
}

class InvoiceService {
  generateInvoice(items: Item[]) {
    return {
      total: PriceCalculator.calculateTotal(items),
      items
    };
  }
}
```

---

## KISS (Keep It Simple, Stupid)

**Principle**: Most systems work best if they are kept simple rather than made complicated. Simplicity should be a key goal in design.

**Check**:
- [ ] Solution is as simple as possible?
- [ ] No over-engineering?
- [ ] No premature optimization?
- [ ] Clear and straightforward logic?

```typescript
// ❌ BAD: Over-complicated
class UserNameFormatter {
  private readonly strategies: Map<string, NameFormattingStrategy>;
  
  constructor() {
    this.strategies = new Map([
      ['uppercase', new UppercaseStrategy()],
      ['lowercase', new LowercaseStrategy()],
      ['titlecase', new TitlecaseStrategy()]
    ]);
  }
  
  format(name: string, strategy: string): string {
    const formatter = this.strategies.get(strategy);
    if (!formatter) {
      throw new Error('Unknown strategy');
    }
    return formatter.format(name);
  }
}

// ✅ GOOD: Simple and clear
function formatUserName(name: string, format: 'upper' | 'lower' | 'title'): string {
  switch (format) {
    case 'upper':
      return name.toUpperCase();
    case 'lower':
      return name.toLowerCase();
    case 'title':
      return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
  }
}
```

```typescript
// ❌ BAD: Premature optimization
class DataProcessor {
  private cache: Map<string, any> = new Map();
  private pool: WorkerPool;
  
  constructor() {
    this.pool = new WorkerPool(10); // Complex worker pool for simple task
  }
  
  async process(data: string): Promise<any> {
    const cacheKey = this.generateCacheKey(data);
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }
    
    const result = await this.pool.execute(() => JSON.parse(data));
    this.cache.set(cacheKey, result);
    return result;
  }
  
  private generateCacheKey(data: string): string {
    // Complex hashing algorithm
  }
}

// ✅ GOOD: Simple solution
class DataProcessor {
  process(data: string): any {
    return JSON.parse(data); // Optimize only if performance issue is proven
  }
}
```

---

## YAGNI (You Aren't Gonna Need It)

**Principle**: Don't add functionality until it's necessary. Avoid implementing things based on speculation about future needs.

**Source**: [Extreme Programming](http://www.extremeprogramming.org/rules/early.html)

**Check**:
- [ ] All code serves current requirements?
- [ ] No "just in case" features?
- [ ] No speculative abstractions?

```typescript
// ❌ BAD: YAGNI violation
interface User {
  id: number;
  name: string;
  email: string;
  // Adding fields we "might need someday"
  phoneNumber?: string;
  address?: Address;
  preferences?: UserPreferences;
  metadata?: Record<string, any>;
  customFields?: CustomField[];
}

class UserService {
  // Methods we don't need yet
  async updatePreferences(userId: number, prefs: UserPreferences) {}
  async addCustomField(userId: number, field: CustomField) {}
  async exportUserData(userId: number, format: 'json' | 'xml' | 'csv') {}
  async importUserData(data: any, format: 'json' | 'xml' | 'csv') {}
}

// ✅ GOOD: Only what's needed now
interface User {
  id: number;
  name: string;
  email: string;
}

class UserService {
  async create(dto: CreateUserDto): Promise<User> {}
  async findById(id: number): Promise<User> {}
  async update(id: number, dto: UpdateUserDto): Promise<User> {}
  // Add more methods when actually needed
}
```

---

## Separation of Concerns (SoC)

**Principle**: Separate a program into distinct sections, each addressing a separate concern. A concern is a set of information that affects the code.

**Check**:
- [ ] Business logic separated from presentation?
- [ ] Data access separated from business logic?
- [ ] Cross-cutting concerns (logging, auth) properly isolated?

```typescript
// ❌ BAD: Mixed concerns
@Controller('users')
export class UserController {
  @Post()
  async create(@Body() dto: CreateUserDto) {
    // Validation (should be middleware)
    if (!dto.email.includes('@')) {
      throw new Error('Invalid email');
    }
    
    // Business logic (should be in service)
    const hashedPassword = await bcrypt.hash(dto.password, 10);
    
    // Data access (should be in repository)
    const user = await db.query(
      'INSERT INTO users (email, password) VALUES ($1, $2)',
      [dto.email, hashedPassword]
    );
    
    // Email sending (should be in email service)
    await sendEmail(user.email, 'Welcome!');
    
    // Logging (should be in logger/interceptor)
    console.log('User created:', user.id);
    
    return user;
  }
}

// ✅ GOOD: Separated concerns
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}
  
  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.userService.create(dto);
  }
}

@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService,
    private readonly logger: Logger
  ) {}
  
  async create(dto: CreateUserDto): Promise<User> {
    const hashedPassword = await this.hashPassword(dto.password);
    const user = await this.userRepository.create({
      email: dto.email,
      password: hashedPassword
    });
    
    await this.emailService.sendWelcome(user);
    this.logger.log('User created', { userId: user.id });
    
    return user;
  }
  
  private async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, 10);
  }
}
```

---

## Composition Over Inheritance

**Principle**: Favor object composition over class inheritance. Compose objects to achieve polymorphic behavior and code reuse.

**Check**:
- [ ] Uses composition when possible?
- [ ] Inheritance used only for true "is-a" relationships?
- [ ] No deep inheritance hierarchies (>3 levels)?

```typescript
// ❌ BAD: Inheritance abuse
class Animal {
  eat() {}
  sleep() {}
}

class FlyingAnimal extends Animal {
  fly() {}
}

class SwimmingAnimal extends Animal {
  swim() {}
}

// What about a duck that flies AND swims? Multiple inheritance problem!
class Duck extends FlyingAnimal {
  swim() {} // Duplicating swimming logic
}

// ✅ GOOD: Composition
interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

interface Flyable {
  fly(): void;
}

interface Swimmable {
  swim(): void;
}

class Duck implements Eatable, Sleepable, Flyable, Swimmable {
  private flyBehavior = new FlyBehavior();
  private swimBehavior = new SwimBehavior();
  
  eat() { /* Eat behavior */ }
  sleep() { /* Sleep behavior */ }
  fly() { this.flyBehavior.fly(); }
  swim() { this.swimBehavior.swim(); }
}

class Penguin implements Eatable, Sleepable, Swimmable {
  private swimBehavior = new SwimBehavior();
  
  eat() { /* Eat behavior */ }
  sleep() { /* Sleep behavior */ }
  swim() { this.swimBehavior.swim(); }
  // No fly - doesn't implement Flyable
}
```

---

## Law of Demeter (Principle of Least Knowledge)

**Principle**: A unit should have limited knowledge about other units. Only talk to your immediate friends, don't talk to strangers.

**Check**:
- [ ] No method chaining through multiple objects?
- [ ] Objects don't reach through other objects?
- [ ] Uses appropriate abstractions?

```typescript
// ❌ BAD: Violates Law of Demeter
class ShoppingCart {
  checkout() {
    const user = this.session.getUser();
    const address = user.getProfile().getAddress();
    const country = address.getCountry();
    const taxRate = country.getTaxRate(); // Too many levels!
    
    // Chain of dependencies: cart -> session -> user -> profile -> address -> country
  }
}

// ✅ GOOD: Proper encapsulation
class ShoppingCart {
  constructor(private readonly taxService: TaxService) {}
  
  checkout() {
    const taxRate = this.taxService.getTaxRateForCurrentUser();
    // Single dependency, proper abstraction
  }
}

class TaxService {
  constructor(private readonly sessionService: SessionService) {}
  
  getTaxRateForCurrentUser(): number {
    const user = this.sessionService.getCurrentUser();
    return user.getTaxRate(); // User encapsulates the complexity
  }
}

class User {
  getTaxRate(): number {
    // Internally handles profile -> address -> country -> tax rate
    return this.profile.address.country.taxRate;
  }
}
```

---

## Code Smells

Common indicators of poor code quality that should be refactored.

### Magic Numbers/Strings

**Check**:
- [ ] No hardcoded numbers without explanation?
- [ ] Constants defined with meaningful names?

```typescript
// ❌ BAD
function calculateDiscount(price: number, customerType: number) {
  if (customerType === 1) {
    return price * 0.1;
  } else if (customerType === 2) {
    return price * 0.2;
  }
  return 0;
}

// What does 1, 2, 0.1, 0.2 mean?

// ✅ GOOD
enum CustomerType {
  REGULAR = 1,
  PREMIUM = 2,
  VIP = 3
}

const DISCOUNT_RATES = {
  [CustomerType.REGULAR]: 0.1,
  [CustomerType.PREMIUM]: 0.2,
  [CustomerType.VIP]: 0.3
} as const;

function calculateDiscount(price: number, customerType: CustomerType) {
  const discountRate = DISCOUNT_RATES[customerType] ?? 0;
  return price * discountRate;
}
```

### Long Functions

**Check**:
- [ ] Functions under 50 lines?
- [ ] Each function does one thing well?
- [ ] Complex functions broken into smaller helpers?

```typescript
// ❌ BAD: 100+ line function
function processOrder(order: Order) {
  // Validate order (20 lines)
  // Calculate totals (15 lines)
  // Apply discounts (25 lines)
  // Process payment (30 lines)
  // Update inventory (20 lines)
  // Send notifications (20 lines)
}

// ✅ GOOD: Small, focused functions
function processOrder(order: Order) {
  validateOrder(order);
  const total = calculateTotal(order);
  processPayment(order, total);
  updateInventory(order);
  sendNotifications(order);
}

function validateOrder(order: Order) {
  // 10 lines max
}

function calculateTotal(order: Order): number {
  const subtotal = calculateSubtotal(order.items);
  const discount = calculateDiscount(order, subtotal);
  return subtotal - discount;
}
```

### Deep Nesting

**Check**:
- [ ] Nesting depth < 3 levels?
- [ ] Early returns used?
- [ ] Guard clauses used?

```typescript
// ❌ BAD: Deep nesting
function processUser(user: User) {
  if (user) {
    if (user.isActive) {
      if (user.hasPermission('write')) {
        if (user.quota > 0) {
          // Do something
        }
      }
    }
  }
}

// ✅ GOOD: Guard clauses
function processUser(user: User) {
  if (!user) return;
  if (!user.isActive) return;
  if (!user.hasPermission('write')) return;
  if (user.quota <= 0) return;
  
  // Do something
}
```

### Long Parameter Lists

**Check**:
- [ ] Functions have < 4 parameters?
- [ ] Related parameters grouped in objects?

```typescript
// ❌ BAD: Too many parameters
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  password: string,
  age: number,
  country: string,
  city: string,
  zipCode: string,
  phoneNumber: string
) {}

// ✅ GOOD: Parameter object
interface CreateUserDto {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  age: number;
  address: {
    country: string;
    city: string;
    zipCode: string;
  };
  phoneNumber: string;
}

function createUser(dto: CreateUserDto) {}
```
