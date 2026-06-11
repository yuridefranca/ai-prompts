# Backend Review Rules

**Sources**:
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [Node.js Security Best Practices](https://nodejs.org/en/docs/guides/security/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

---

## Architecture & Structure

### Layered Architecture

**Check**:
- [ ] Clear separation between layers (controllers, services, repositories)?
- [ ] Business logic not in controllers?
- [ ] Controllers only handle HTTP concerns?
- [ ] Data access isolated in repository/data layer?

```typescript
// ❌ BAD: Business logic in controller
@Controller('users')
export class UsersController {
  @Post()
  async create(@Body() dto: CreateUserDto) {
    // Validation logic
    if (!dto.email.includes('@')) throw new Error('Invalid email');
    // Business logic
    const hashedPassword = await bcrypt.hash(dto.password, 10);
    // Data access
    const user = await this.db.query('INSERT INTO users...');
    // Email logic
    await this.emailService.sendWelcome(user);
    return user;
  }
}

// ✅ GOOD: Proper layering
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}
  
  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }
}
```

### Dependency Injection

**Check**:
- [ ] Dependencies injected, not created?
- [ ] No `new` keyword for services?
- [ ] Dependencies declared in constructor?
- [ ] Testable (can mock dependencies)?

```typescript
// ❌ BAD: Tight coupling
export class UserService {
  private emailService = new EmailService();
  private db = new Database();
}

// ✅ GOOD: Dependency injection
export class UserService {
  constructor(
    private readonly emailService: EmailService,
    private readonly db: Database
  ) {}
}
```

---

## Error Handling

### Centralized Error Handling

**Check**:
- [ ] Global error handler exists?
- [ ] Custom error classes for different types?
- [ ] Errors logged with context?
- [ ] Client-safe error messages (no stack traces in prod)?

```typescript
// ❌ BAD: Error handling in each route
app.get('/users/:id', async (req, res) => {
  try {
    const user = await getUser(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// ✅ GOOD: Centralized error handling
class UserNotFoundError extends Error {
  statusCode = 404;
  constructor(userId: string) {
    super(`User ${userId} not found`);
  }
}

app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  if (!user) throw new UserNotFoundError(req.params.id);
  res.json(user);
});

// Global error handler
app.use((err, req, res, next) => {
  logger.error('Request failed', { error: err, path: req.path });
  res.status(err.statusCode || 500).json({
    error: process.env.NODE_ENV === 'production' 
      ? 'Internal server error' 
      : err.message
  });
});
```

### Async Error Handling

**Check**:
- [ ] All async operations wrapped in try/catch or use error middleware?
- [ ] Promise rejections handled?
- [ ] No unhandled promise rejections?

```typescript
// ❌ BAD: Unhandled promise rejection
app.get('/users', async (req, res) => {
  const users = await getUsers(); // If this throws, server crashes
  res.json(users);
});

// ✅ GOOD: Proper async error handling
app.get('/users', asyncHandler(async (req, res) => {
  const users = await getUsers();
  res.json(users);
}));

// Or with explicit try/catch
app.get('/users', async (req, res, next) => {
  try {
    const users = await getUsers();
    res.json(users);
  } catch (error) {
    next(error);
  }
});
```

---

## Security

### Input Validation

**Source**: [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

**Check**:
- [ ] All user input validated?
- [ ] Validation happens server-side (not just client)?
- [ ] Type validation in place?
- [ ] Length limits enforced?
- [ ] Whitelist validation over blacklist?

```typescript
// ❌ BAD: No validation
@Post()
async createUser(@Body() data: any) {
  return this.db.save(data);
}

// ✅ GOOD: Proper validation
class CreateUserDto {
  @IsEmail()
  @MaxLength(255)
  email: string;

  @IsString()
  @MinLength(8)
  @MaxLength(100)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, {
    message: 'Password must contain uppercase, lowercase, and number'
  })
  password: string;

  @IsString()
  @MinLength(2)
  @MaxLength(50)
  name: string;
}

@Post()
async createUser(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}
```

### SQL Injection Prevention

**Source**: [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

**Check**:
- [ ] No string concatenation in queries?
- [ ] Parameterized queries or ORM used?
- [ ] Input sanitized before queries?

```typescript
// ❌ BAD: SQL injection vulnerability
async getUser(userId: string) {
  const query = `SELECT * FROM users WHERE id = '${userId}'`;
  return db.query(query);
}

// ❌ STILL BAD: Using template literals
async getUser(userId: string) {
  return db.query(`SELECT * FROM users WHERE id = '${userId}'`);
}

// ✅ GOOD: Parameterized query
async getUser(userId: string) {
  return db.query('SELECT * FROM users WHERE id = $1', [userId]);
}

// ✅ GOOD: Using ORM
async getUser(userId: string) {
  return this.userRepository.findOne({ where: { id: userId } });
}
```

### Authentication & Authorization

**Check**:
- [ ] Authentication checked for protected routes?
- [ ] Authorization enforced (user has permission)?
- [ ] JWT tokens validated properly?
- [ ] Token expiration implemented?
- [ ] Refresh token mechanism secure?

```typescript
// ❌ BAD: No auth check
@Get('admin/users')
async getAllUsers() {
  return this.usersService.findAll();
}

// ✅ GOOD: Auth and authorization
@Get('admin/users')
@UseGuards(AuthGuard, RolesGuard)
@Roles('admin')
async getAllUsers() {
  return this.usersService.findAll();
}
```

### Sensitive Data

**Check**:
- [ ] Passwords hashed (bcrypt, argon2)?
- [ ] No secrets in code or version control?
- [ ] Environment variables for sensitive config?
- [ ] No sensitive data in logs?
- [ ] PII properly masked/encrypted?

```typescript
// ❌ BAD: Plain text password
async createUser(dto: CreateUserDto) {
  return this.db.save({
    email: dto.email,
    password: dto.password // Plain text!
  });
}

// ❌ BAD: Secrets in code
const apiKey = 'sk_live_abc123xyz';

// ✅ GOOD: Hashed password
async createUser(dto: CreateUserDto) {
  const hashedPassword = await bcrypt.hash(dto.password, 10);
  return this.db.save({
    email: dto.email,
    password: hashedPassword
  });
}

// ✅ GOOD: Secrets in environment
const apiKey = process.env.STRIPE_API_KEY;
```

### Rate Limiting

**Source**: [Node.js Best Practices - Rate Limiting](https://github.com/goldbergyoni/nodebestpractices#6-security-best-practices)

**Check**:
- [ ] Rate limiting implemented?
- [ ] Different limits for authenticated vs anonymous?
- [ ] Stricter limits on sensitive endpoints (login, register)?

```typescript
// ✅ GOOD: Rate limiting
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests'
});

app.use('/api/', limiter);

// Stricter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts per 15 minutes
});

app.use('/api/auth/', authLimiter);
```

---

## Performance

### Database Queries

**Check**:
- [ ] No N+1 query problems?
- [ ] Eager loading used where appropriate?
- [ ] Indexes on frequently queried fields?
- [ ] Query limits for list endpoints?
- [ ] Pagination implemented?

```typescript
// ❌ BAD: N+1 query problem
async getUsersWithPosts() {
  const users = await this.userRepo.find();
  
  for (const user of users) {
    user.posts = await this.postRepo.find({ userId: user.id }); // Query in loop!
  }
  
  return users;
}

// ✅ GOOD: Single query with JOIN
async getUsersWithPosts() {
  return this.userRepo.find({
    relations: ['posts']
  });
}

// ✅ GOOD: Using query builder
async getUsersWithPosts() {
  return this.userRepo
    .createQueryBuilder('user')
    .leftJoinAndSelect('user.posts', 'post')
    .getMany();
}
```

### Pagination

**Check**:
- [ ] List endpoints return limited results?
- [ ] Pagination parameters validated?
- [ ] Default and max limits enforced?

```typescript
// ❌ BAD: No pagination (could return millions of records)
@Get('users')
async getUsers() {
  return this.userRepo.find();
}

// ✅ GOOD: Pagination with limits
@Get('users')
async getUsers(
  @Query('page') page: number = 1,
  @Query('limit') limit: number = 20
) {
  const maxLimit = 100;
  const safeLimit = Math.min(limit, maxLimit);
  const skip = (page - 1) * safeLimit;
  
  const [users, total] = await this.userRepo.findAndCount({
    skip,
    take: safeLimit
  });
  
  return {
    data: users,
    meta: {
      total,
      page,
      limit: safeLimit,
      totalPages: Math.ceil(total / safeLimit)
    }
  };
}
```

### Async Operations

**Check**:
- [ ] Independent operations run in parallel?
- [ ] No blocking operations on main thread?
- [ ] Streams used for large files?

```typescript
// ❌ BAD: Sequential (slow)
async getUserProfile(userId: string) {
  const user = await this.userRepo.findOne(userId);
  const posts = await this.postRepo.find({ userId });
  const comments = await this.commentRepo.find({ userId });
  
  return { user, posts, comments };
}

// ✅ GOOD: Parallel (fast)
async getUserProfile(userId: string) {
  const [user, posts, comments] = await Promise.all([
    this.userRepo.findOne(userId),
    this.postRepo.find({ userId }),
    this.commentRepo.find({ userId })
  ]);
  
  return { user, posts, comments };
}
```

### Caching

**Check**:
- [ ] Expensive operations cached?
- [ ] Cache invalidation strategy in place?
- [ ] TTL set appropriately?
- [ ] Cache keys properly namespaced?

```typescript
// ✅ GOOD: Caching expensive operations
async getPopularPosts() {
  const cacheKey = 'posts:popular';
  const cached = await this.cache.get(cacheKey);
  
  if (cached) {
    return JSON.parse(cached);
  }
  
  const posts = await this.postRepo.find({
    order: { views: 'DESC' },
    take: 10
  });
  
  await this.cache.set(cacheKey, JSON.stringify(posts), 'EX', 3600); // 1 hour
  
  return posts;
}
```

---

## API Design

### RESTful Conventions

**Source**: [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)

**Check**:
- [ ] Proper HTTP methods (GET, POST, PUT, PATCH, DELETE)?
- [ ] Correct status codes returned?
- [ ] Resource-based URLs (nouns, not verbs)?
- [ ] Consistent naming conventions?

```typescript
// ❌ BAD: Wrong methods and verbs in URLs
@Get('getUserById/:id')  // Should be just @Get(':id')
@Post('deleteUser/:id')  // Should be @Delete(':id')

// ✅ GOOD: RESTful design
@Get(':id')           // GET /users/123
@Post()               // POST /users
@Put(':id')           // PUT /users/123
@Patch(':id')         // PATCH /users/123
@Delete(':id')        // DELETE /users/123
```

### HTTP Status Codes

**Check**:
- [ ] 200 OK for successful GET, PUT, PATCH?
- [ ] 201 Created for successful POST?
- [ ] 204 No Content for successful DELETE?
- [ ] 400 Bad Request for validation errors?
- [ ] 401 Unauthorized for missing/invalid auth?
- [ ] 403 Forbidden for insufficient permissions?
- [ ] 404 Not Found for missing resources?
- [ ] 500 Internal Server Error for server issues?

```typescript
// ❌ BAD: Always 200
@Post()
async create(@Body() dto: CreateUserDto) {
  try {
    return await this.usersService.create(dto);
  } catch (error) {
    return { error: error.message }; // Still returns 200!
  }
}

// ✅ GOOD: Proper status codes
@Post()
@HttpCode(201)
async create(@Body() dto: CreateUserDto) {
  return this.usersService.create(dto);
}

@Delete(':id')
@HttpCode(204)
async delete(@Param('id') id: string) {
  await this.usersService.delete(id);
}
```

### Response Format

**Check**:
- [ ] Consistent response structure?
- [ ] Error responses follow standard format?
- [ ] Metadata included where appropriate?

```typescript
// ✅ GOOD: Consistent response format
interface ApiResponse<T> {
  data: T;
  meta?: {
    page?: number;
    total?: number;
    timestamp: string;
  };
}

interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: any;
  };
}
```

---

## Logging & Monitoring

**Source**: [Node.js Best Practices - Logging](https://github.com/goldbergyoni/nodebestpractices#2-error-handling-practices)

### Structured Logging

**Check**:
- [ ] Structured logs (JSON)?
- [ ] Appropriate log levels (debug, info, warn, error)?
- [ ] Context included (userId, requestId, etc.)?
- [ ] No sensitive data in logs?

```typescript
// ❌ BAD: Console.log with no structure
console.log('User logged in:', userId);

// ✅ GOOD: Structured logging
logger.info('User logged in', {
  userId,
  email: user.email,
  timestamp: new Date().toISOString(),
  ip: req.ip
});

// ✅ GOOD: Error logging with context
logger.error('Payment failed', {
  error: error.message,
  stack: error.stack,
  userId,
  orderId,
  amount
});
```

### Request Logging

**Check**:
- [ ] All requests logged?
- [ ] Request ID for tracing?
- [ ] Response time tracked?

```typescript
// ✅ GOOD: Request logging middleware
app.use((req, res, next) => {
  const startTime = Date.now();
  const requestId = uuidv4();
  
  req.id = requestId;
  
  res.on('finish', () => {
    const duration = Date.now() - startTime;
    
    logger.info('Request completed', {
      requestId,
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      userAgent: req.get('user-agent')
    });
  });
  
  next();
});
```

---

## Testing

### Test Coverage

**Check**:
- [ ] Unit tests for services?
- [ ] Integration tests for APIs?
- [ ] Error scenarios tested?
- [ ] Edge cases covered?
- [ ] Mocks used appropriately?

### Test Organization

```typescript
// ✅ GOOD: Well-organized tests
describe('UserService', () => {
  let service: UserService;
  let mockRepo: MockType<UserRepository>;
  
  beforeEach(() => {
    mockRepo = createMockRepository();
    service = new UserService(mockRepo);
  });
  
  describe('create', () => {
    it('should create a user with hashed password', async () => {
      const dto = { email: 'test@example.com', password: 'Password123' };
      mockRepo.save.mockResolvedValue({ id: 1, ...dto });
      
      const result = await service.create(dto);
      
      expect(result.password).not.toBe(dto.password);
      expect(mockRepo.save).toHaveBeenCalledWith(
        expect.objectContaining({ email: dto.email })
      );
    });
    
    it('should throw error if email already exists', async () => {
      mockRepo.findOne.mockResolvedValue({ id: 1 });
      
      await expect(
        service.create({ email: 'test@example.com', password: 'Pass123' })
      ).rejects.toThrow('Email already exists');
    });
  });
});
```

---

## Configuration Management

**Check**:
- [ ] Environment variables for all environments?
- [ ] Validation for required config?
- [ ] No hardcoded values?
- [ ] Different configs for dev/staging/prod?

```typescript
// ❌ BAD: Hardcoded config
const PORT = 3000;
const DB_HOST = 'localhost';

// ✅ GOOD: Environment-based config
import { z } from 'zod';

const configSchema = z.object({
  PORT: z.string().transform(Number),
  DB_HOST: z.string(),
  DB_PORT: z.string().transform(Number),
  DB_NAME: z.string(),
  JWT_SECRET: z.string().min(32),
  NODE_ENV: z.enum(['development', 'staging', 'production'])
});

export const config = configSchema.parse(process.env);
```

---

## Documentation

**Check**:
- [ ] API endpoints documented?
- [ ] Request/response examples provided?
- [ ] OpenAPI/Swagger spec exists?
- [ ] Error codes documented?

```typescript
// ✅ GOOD: API documentation
/**
 * Create a new user
 * 
 * @param dto User creation data
 * @returns Created user (without password)
 * @throws {ConflictException} Email already exists
 * @throws {BadRequestException} Invalid input data
 * 
 * @example
 * POST /users
 * Body: { "email": "user@example.com", "password": "SecurePass123" }
 * Response: { "id": 1, "email": "user@example.com", "createdAt": "2024-01-01T00:00:00Z" }
 */
@Post()
async create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
  return this.usersService.create(dto);
}
```
