# Design Patterns & Anti-Patterns

**Sources**:
- [Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)](https://www.amazon.com/Design-Patterns-Elements-Reusable-Object-Oriented/dp/0201633612)
- [Refactoring.guru - Design Patterns](https://refactoring.guru/design-patterns)
- [SourceMaking - Anti-patterns](https://sourcemaking.com/antipatterns)

---

## Common Anti-Patterns to Avoid

### God Object / God Class

**Anti-pattern**: A class that knows too much or does too much. It has too many responsibilities and dependencies.

**Check**:
- [ ] No single class doing everything?
- [ ] Classes have focused responsibilities?
- [ ] Class has reasonable number of methods (<20)?
- [ ] Class has reasonable number of dependencies (<5)?

```typescript
// ❌ BAD: God object
class Application {
  // Database operations
  connectToDatabase() {}
  executeQuery() {}
  
  // User management
  createUser() {}
  deleteUser() {}
  authenticateUser() {}
  
  // Email operations
  sendEmail() {}
  validateEmail() {}
  
  // File operations
  readFile() {}
  writeFile() {}
  
  // Payment processing
  processPayment() {}
  refundPayment() {}
  
  // Reporting
  generateReport() {}
  exportToPDF() {}
  
  // ... 50 more methods
}

// ✅ GOOD: Separated responsibilities
class DatabaseService { }
class UserService { }
class EmailService { }
class FileService { }
class PaymentService { }
class ReportService { }
```

### Callback Hell / Pyramid of Doom

**Anti-pattern**: Deeply nested callbacks that make code hard to read and maintain.

**Check**:
- [ ] No deep callback nesting?
- [ ] Uses async/await or Promises?
- [ ] Sequential operations are flat?

```typescript
// ❌ BAD: Callback hell
getData(userId, (error, user) => {
  if (error) {
    handleError(error);
  } else {
    getPosts(user.id, (error, posts) => {
      if (error) {
        handleError(error);
      } else {
        getComments(posts[0].id, (error, comments) => {
          if (error) {
            handleError(error);
          } else {
            updateCache(comments, (error, result) => {
              if (error) {
                handleError(error);
              } else {
                // Finally done!
              }
            });
          }
        });
      }
    });
  }
});

// ✅ GOOD: Async/await
try {
  const user = await getData(userId);
  const posts = await getPosts(user.id);
  const comments = await getComments(posts[0].id);
  await updateCache(comments);
} catch (error) {
  handleError(error);
}
```

### Premature Optimization

**Anti-pattern**: Optimizing code before knowing if there's a performance problem.

**Check**:
- [ ] Optimization justified by profiling data?
- [ ] No complex optimizations for imaginary problems?
- [ ] Code clarity not sacrificed for minor gains?

```typescript
// ❌ BAD: Premature optimization
class DataCache {
  private cache: Map<string, WeakRef<any>>;
  private pool: ObjectPool;
  private mutex: Mutex;
  
  async get(key: string): Promise<any> {
    await this.mutex.lock();
    try {
      const ref = this.cache.get(key);
      const obj = ref?.deref();
      if (obj) {
        return this.pool.clone(obj); // Complex pooling for simple cache
      }
    } finally {
      this.mutex.unlock();
    }
  }
}

// ✅ GOOD: Simple solution first, optimize if needed
class DataCache {
  private cache = new Map<string, any>();
  
  get(key: string): any | undefined {
    return this.cache.get(key);
  }
  
  set(key: string, value: any): void {
    this.cache.set(key, value);
  }
}
```

### Big Ball of Mud

**Anti-pattern**: System with no recognizable structure. Haphazardly structured code with tangled dependencies.

**Check**:
- [ ] Clear architectural layers?
- [ ] Defined module boundaries?
- [ ] Dependencies flow in one direction?
- [ ] No circular dependencies?

```typescript
// ❌ BAD: Everything depends on everything
// user.service.ts
import { PostService } from './post.service';
import { OrderService } from './order.service';

// post.service.ts
import { UserService } from './user.service';
import { CommentService } from './comment.service';

// order.service.ts
import { UserService } from './user.service';
import { ProductService } from './product.service';

// Circular dependencies, no clear structure

// ✅ GOOD: Layered architecture
// Domain Layer
class User { }
class Post { }
class Order { }

// Repository Layer (depends on Domain)
class UserRepository { }
class PostRepository { }
class OrderRepository { }

// Service Layer (depends on Repository)
class UserService {
  constructor(private userRepo: UserRepository) {}
}

class PostService {
  constructor(private postRepo: PostRepository) {}
}

// Controller Layer (depends on Service)
class UserController {
  constructor(private userService: UserService) {}
}
```

### Spaghetti Code

**Anti-pattern**: Code with complex and tangled control structures. Difficult to follow the program flow.

**Check**:
- [ ] Clear, linear flow?
- [ ] No goto-like behavior?
- [ ] No excessive branching?
- [ ] Function calls are logical?

```typescript
// ❌ BAD: Spaghetti code
let state = 1;
function process(data: any) {
  if (state === 1) {
    state = 2;
    if (data.type === 'A') {
      state = 3;
      doSomething();
      state = 1;
    } else {
      state = 4;
      doOtherThing();
      if (data.flag) {
        state = 1;
      } else {
        state = 5;
      }
    }
  } else if (state === 2) {
    // ... more tangled logic
  }
  // Impossible to follow!
}

// ✅ GOOD: Clear state machine or simple flow
enum ProcessState {
  INITIAL,
  PROCESSING,
  COMPLETED
}

class DataProcessor {
  private state = ProcessState.INITIAL;
  
  process(data: any): void {
    this.validateInput(data);
    this.processData(data);
    this.finalizeProcessing();
  }
  
  private validateInput(data: any): void {
    // Clear validation logic
  }
  
  private processData(data: any): void {
    // Clear processing logic
  }
  
  private finalizeProcessing(): void {
    this.state = ProcessState.COMPLETED;
  }
}
```

### Tight Coupling

**Anti-pattern**: Components are so dependent on each other that changes ripple throughout the system.

**Check**:
- [ ] Components loosely coupled?
- [ ] Dependencies injected rather than created?
- [ ] Uses interfaces/abstractions?
- [ ] Changes to one component don't force changes to many others?

```typescript
// ❌ BAD: Tight coupling
class EmailService {
  private smtp = new SMTPClient('smtp.example.com', 587);
  
  send(to: string, message: string) {
    this.smtp.send(to, message);
  }
}

class UserService {
  private emailService = new EmailService(); // Tightly coupled!
  
  register(user: User) {
    // User service knows about email implementation
    this.emailService.send(user.email, 'Welcome!');
  }
}

// ✅ GOOD: Loose coupling
interface EmailSender {
  send(to: string, message: string): Promise<void>;
}

class SMTPEmailService implements EmailSender {
  async send(to: string, message: string) {
    // SMTP implementation
  }
}

class SendGridEmailService implements EmailSender {
  async send(to: string, message: string) {
    // SendGrid implementation
  }
}

class UserService {
  constructor(private emailSender: EmailSender) {} // Loosely coupled!
  
  async register(user: User) {
    await this.emailSender.send(user.email, 'Welcome!');
  }
}
```

---

## Useful Design Patterns

### Strategy Pattern

**Use when**: You need to define a family of algorithms and make them interchangeable.

```typescript
// Define strategy interface
interface PricingStrategy {
  calculatePrice(basePrice: number): number;
}

// Concrete strategies
class RegularPricing implements PricingStrategy {
  calculatePrice(basePrice: number): number {
    return basePrice;
  }
}

class MemberPricing implements PricingStrategy {
  calculatePrice(basePrice: number): number {
    return basePrice * 0.9; // 10% discount
  }
}

class VIPPricing implements PricingStrategy {
  calculatePrice(basePrice: number): number {
    return basePrice * 0.8; // 20% discount
  }
}

// Context
class ShoppingCart {
  constructor(private pricingStrategy: PricingStrategy) {}
  
  setPricingStrategy(strategy: PricingStrategy) {
    this.pricingStrategy = strategy;
  }
  
  calculateTotal(items: Item[]): number {
    const basePrice = items.reduce((sum, item) => sum + item.price, 0);
    return this.pricingStrategy.calculatePrice(basePrice);
  }
}

// Usage
const cart = new ShoppingCart(new RegularPricing());
cart.calculateTotal(items);

cart.setPricingStrategy(new VIPPricing());
cart.calculateTotal(items); // Now with VIP discount
```

### Factory Pattern

**Use when**: Object creation logic is complex or you need to decouple object creation from usage.

```typescript
// Product interface
interface Database {
  connect(): Promise<void>;
  query(sql: string): Promise<any>;
}

// Concrete products
class PostgreSQLDatabase implements Database {
  async connect() { /* PostgreSQL connection */ }
  async query(sql: string) { /* PostgreSQL query */ }
}

class MySQLDatabase implements Database {
  async connect() { /* MySQL connection */ }
  async query(sql: string) { /* MySQL query */ }
}

class MongoDBDatabase implements Database {
  async connect() { /* MongoDB connection */ }
  async query(sql: string) { /* MongoDB query */ }
}

// Factory
class DatabaseFactory {
  static create(type: string, config: any): Database {
    switch (type) {
      case 'postgresql':
        return new PostgreSQLDatabase(config);
      case 'mysql':
        return new MySQLDatabase(config);
      case 'mongodb':
        return new MongoDBDatabase(config);
      default:
        throw new Error(`Unknown database type: ${type}`);
    }
  }
}

// Usage
const db = DatabaseFactory.create(process.env.DB_TYPE, config);
await db.connect();
```

### Singleton Pattern

**Use when**: You need exactly one instance of a class (use sparingly!).

**Note**: Often better to use dependency injection instead of singleton.

```typescript
// ✅ Singleton (use cautiously)
class DatabaseConnection {
  private static instance: DatabaseConnection;
  private connection: any;
  
  private constructor() {
    // Private constructor prevents direct instantiation
  }
  
  static getInstance(): DatabaseConnection {
    if (!DatabaseConnection.instance) {
      DatabaseConnection.instance = new DatabaseConnection();
    }
    return DatabaseConnection.instance;
  }
  
  async connect() {
    if (!this.connection) {
      this.connection = await createConnection();
    }
    return this.connection;
  }
}

// Usage
const db1 = DatabaseConnection.getInstance();
const db2 = DatabaseConnection.getInstance();
// db1 === db2 (same instance)

// ✅ BETTER: Dependency injection (in most cases)
@Injectable({ scope: Scope.DEFAULT }) // Singleton scope
class DatabaseConnection {
  private connection: any;
  
  async connect() {
    if (!this.connection) {
      this.connection = await createConnection();
    }
    return this.connection;
  }
}
```

### Repository Pattern

**Use when**: You need to abstract data access logic from business logic.

```typescript
// Domain entity
class User {
  constructor(
    public id: number,
    public email: string,
    public name: string
  ) {}
}

// Repository interface
interface UserRepository {
  findById(id: number): Promise<User | null>;
  findAll(): Promise<User[]>;
  save(user: User): Promise<User>;
  delete(id: number): Promise<void>;
}

// Concrete implementation
class TypeORMUserRepository implements UserRepository {
  constructor(
    @InjectRepository(UserEntity)
    private repo: Repository<UserEntity>
  ) {}
  
  async findById(id: number): Promise<User | null> {
    const entity = await this.repo.findOne({ where: { id } });
    return entity ? this.toDomain(entity) : null;
  }
  
  async findAll(): Promise<User[]> {
    const entities = await this.repo.find();
    return entities.map(e => this.toDomain(e));
  }
  
  async save(user: User): Promise<User> {
    const entity = this.toEntity(user);
    const saved = await this.repo.save(entity);
    return this.toDomain(saved);
  }
  
  async delete(id: number): Promise<void> {
    await this.repo.delete(id);
  }
  
  private toDomain(entity: UserEntity): User {
    return new User(entity.id, entity.email, entity.name);
  }
  
  private toEntity(user: User): UserEntity {
    const entity = new UserEntity();
    entity.id = user.id;
    entity.email = user.email;
    entity.name = user.name;
    return entity;
  }
}

// Service uses repository interface
class UserService {
  constructor(private userRepository: UserRepository) {}
  
  async getUser(id: number): Promise<User> {
    const user = await this.userRepository.findById(id);
    if (!user) {
      throw new NotFoundException('User not found');
    }
    return user;
  }
}
```

### Decorator Pattern

**Use when**: You need to add behavior to objects dynamically without affecting other objects.

```typescript
// Component interface
interface Coffee {
  cost(): number;
  description(): string;
}

// Concrete component
class SimpleCoffee implements Coffee {
  cost(): number {
    return 2;
  }
  
  description(): string {
    return 'Simple coffee';
  }
}

// Decorator base
abstract class CoffeeDecorator implements Coffee {
  constructor(protected coffee: Coffee) {}
  
  abstract cost(): number;
  abstract description(): string;
}

// Concrete decorators
class MilkDecorator extends CoffeeDecorator {
  cost(): number {
    return this.coffee.cost() + 0.5;
  }
  
  description(): string {
    return `${this.coffee.description()}, milk`;
  }
}

class SugarDecorator extends CoffeeDecorator {
  cost(): number {
    return this.coffee.cost() + 0.2;
  }
  
  description(): string {
    return `${this.coffee.description()}, sugar`;
  }
}

// Usage
let coffee: Coffee = new SimpleCoffee();
console.log(coffee.description(), coffee.cost()); // "Simple coffee" 2

coffee = new MilkDecorator(coffee);
console.log(coffee.description(), coffee.cost()); // "Simple coffee, milk" 2.5

coffee = new SugarDecorator(coffee);
console.log(coffee.description(), coffee.cost()); // "Simple coffee, milk, sugar" 2.7
```

### Observer Pattern

**Use when**: You need to notify multiple objects about state changes.

```typescript
// Subject
interface Subject {
  attach(observer: Observer): void;
  detach(observer: Observer): void;
  notify(): void;
}

// Observer
interface Observer {
  update(subject: Subject): void;
}

// Concrete subject
class StockPrice implements Subject {
  private observers: Observer[] = [];
  private _price: number = 0;
  
  get price(): number {
    return this._price;
  }
  
  set price(value: number) {
    this._price = value;
    this.notify();
  }
  
  attach(observer: Observer): void {
    this.observers.push(observer);
  }
  
  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer);
    if (index > -1) {
      this.observers.splice(index, 1);
    }
  }
  
  notify(): void {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }
}

// Concrete observers
class EmailAlert implements Observer {
  update(subject: Subject): void {
    if (subject instanceof StockPrice) {
      console.log(`Email: Stock price changed to ${subject.price}`);
    }
  }
}

class SMSAlert implements Observer {
  update(subject: Subject): void {
    if (subject instanceof StockPrice) {
      console.log(`SMS: Stock price changed to ${subject.price}`);
    }
  }
}

// Usage
const stock = new StockPrice();
const emailAlert = new EmailAlert();
const smsAlert = new SMSAlert();

stock.attach(emailAlert);
stock.attach(smsAlert);

stock.price = 100; // Both observers notified
stock.price = 150; // Both observers notified
```

### Adapter Pattern

**Use when**: You need to make incompatible interfaces work together.

```typescript
// Target interface (what we want)
interface PaymentProcessor {
  processPayment(amount: number): Promise<PaymentResult>;
}

// Adaptee (third-party service with different interface)
class StripeAPI {
  async charge(amountInCents: number, currency: string): Promise<any> {
    // Stripe-specific implementation
    return { id: 'ch_123', status: 'succeeded' };
  }
}

// Adapter
class StripeAdapter implements PaymentProcessor {
  constructor(private stripeAPI: StripeAPI) {}
  
  async processPayment(amount: number): Promise<PaymentResult> {
    const amountInCents = Math.round(amount * 100);
    const result = await this.stripeAPI.charge(amountInCents, 'USD');
    
    return {
      success: result.status === 'succeeded',
      transactionId: result.id
    };
  }
}

// Another adaptee
class PayPalAPI {
  async makePayment(dollars: number): Promise<any> {
    // PayPal-specific implementation
    return { paymentId: 'pp_456', state: 'approved' };
  }
}

// Another adapter
class PayPalAdapter implements PaymentProcessor {
  constructor(private paypalAPI: PayPalAPI) {}
  
  async processPayment(amount: number): Promise<PaymentResult> {
    const result = await this.paypalAPI.makePayment(amount);
    
    return {
      success: result.state === 'approved',
      transactionId: result.paymentId
    };
  }
}

// Usage - same interface for different payment providers
class CheckoutService {
  constructor(private paymentProcessor: PaymentProcessor) {}
  
  async checkout(amount: number) {
    return this.paymentProcessor.processPayment(amount);
  }
}

// Can use either adapter
const stripeCheckout = new CheckoutService(new StripeAdapter(new StripeAPI()));
const paypalCheckout = new CheckoutService(new PayPalAdapter(new PayPalAPI()));
```
