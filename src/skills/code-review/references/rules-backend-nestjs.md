# NestJS-Specific Review Rules

**Sources**:
- [NestJS Official Documentation](https://docs.nestjs.com/)
- [NestJS Best Practices](https://docs.nestjs.com/fundamentals/testing)
- [Enterprise NestJS Patterns](https://trilon.io/blog)

---

## Module Organization

### Module Structure

**Source**: [NestJS Modules](https://docs.nestjs.com/modules)

**Check**:
- [ ] Each feature has its own module?
- [ ] Shared functionality in shared/common module?
- [ ] No cross-feature imports (use module exports)?
- [ ] Module decorators properly configured?

```typescript
// ❌ BAD: Everything in one module
@Module({
  imports: [],
  controllers: [
    UserController,
    PostController,
    CommentController,
    AuthController
  ],
  providers: [
    UserService,
    PostService,
    CommentService,
    AuthService
  ]
})
export class AppModule {}

// ✅ GOOD: Feature modules
@Module({
  imports: [
    UsersModule,
    PostsModule,
    CommentsModule,
    AuthModule,
    DatabaseModule,
    ConfigModule.forRoot()
  ]
})
export class AppModule {}

// Feature module
@Module({
  imports: [DatabaseModule],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService] // Export for other modules
})
export class UsersModule {}
```

### Dynamic Modules

**Check**:
- [ ] Configuration modules use `.forRoot()` pattern?
- [ ] Async configuration uses `.forRootAsync()`?
- [ ] Feature modules use `.forFeature()` pattern?

```typescript
// ✅ GOOD: Dynamic module pattern
@Module({})
export class DatabaseModule {
  static forRoot(options: DatabaseOptions): DynamicModule {
    return {
      module: DatabaseModule,
      providers: [
        {
          provide: 'DATABASE_OPTIONS',
          useValue: options
        },
        DatabaseService
      ],
      exports: [DatabaseService]
    };
  }
  
  static forRootAsync(options: DatabaseAsyncOptions): DynamicModule {
    return {
      module: DatabaseModule,
      imports: options.imports || [],
      providers: [
        {
          provide: 'DATABASE_OPTIONS',
          useFactory: options.useFactory,
          inject: options.inject || []
        },
        DatabaseService
      ],
      exports: [DatabaseService]
    };
  }
}
```

---

## Dependency Injection

### Constructor Injection

**Source**: [NestJS Providers](https://docs.nestjs.com/providers)

**Check**:
- [ ] All dependencies use constructor injection?
- [ ] Dependencies use `private readonly` modifier?
- [ ] No circular dependencies?
- [ ] Providers registered in module?

```typescript
// ❌ BAD: Missing access modifier
@Injectable()
export class UserService {
  constructor(userRepository: UserRepository) {} // Won't be assigned!
}

// ❌ BAD: Not readonly
@Injectable()
export class UserService {
  constructor(private userRepository: UserRepository) {}
  
  someMethod() {
    this.userRepository = new UserRepository(); // Can be reassigned!
  }
}

// ✅ GOOD: Proper dependency injection
@Injectable()
export class UserService {
  constructor(
    private readonly userRepository: UserRepository,
    private readonly emailService: EmailService,
    private readonly logger: Logger
  ) {}
}
```

### Provider Scope

**Check**:
- [ ] Default scope (singleton) used unless there's a reason?
- [ ] Request-scoped providers only when necessary?
- [ ] Transient providers documented with reason?

```typescript
// ❌ BAD: Unnecessary request scope (performance impact)
@Injectable({ scope: Scope.REQUEST })
export class UserService {
  // This creates a new instance per request!
}

// ✅ GOOD: Request scope only when needed
@Injectable({ scope: Scope.REQUEST })
export class AuditService {
  constructor(
    @Inject(REQUEST) private readonly request: Request
  ) {}
  
  async log(action: string) {
    // Needs request context for user tracking
    const userId = this.request.user?.id;
    await this.saveAudit({ userId, action });
  }
}

// ✅ GOOD: Default singleton scope
@Injectable()
export class UserService {
  // Shared across all requests - efficient!
}
```

### Circular Dependencies

**Check**:
- [ ] No circular dependencies between modules?
- [ ] If circular dependency exists, uses `forwardRef()`?
- [ ] Circular dependencies are documented with justification?

```typescript
// ❌ BAD: Circular dependency
// user.service.ts
@Injectable()
export class UserService {
  constructor(private readonly postService: PostService) {}
}

// post.service.ts
@Injectable()
export class PostService {
  constructor(private readonly userService: UserService) {} // Circular!
}

// ✅ GOOD: Using forwardRef
// user.service.ts
@Injectable()
export class UserService {
  constructor(
    @Inject(forwardRef(() => PostService))
    private readonly postService: PostService
  ) {}
}

// ✅ BETTER: Refactor to remove circular dependency
@Injectable()
export class UserService {
  constructor(private readonly userRepository: UserRepository) {}
}

@Injectable()
export class PostService {
  constructor(
    private readonly postRepository: PostRepository,
    private readonly userRepository: UserRepository // Use repository instead
  ) {}
}
```

---

## Controllers

### Decorators

**Source**: [NestJS Controllers](https://docs.nestjs.com/controllers)

**Check**:
- [ ] Proper HTTP method decorators (@Get, @Post, etc.)?
- [ ] Route parameters use @Param()?
- [ ] Query parameters use @Query()?
- [ ] Request body uses @Body()?
- [ ] Custom decorators follow naming conventions?

```typescript
// ❌ BAD: Wrong parameter decorators
@Controller('users')
export class UserController {
  @Get(':id')
  getUser(@Body() id: string) {} // Wrong! Should be @Param
  
  @Get()
  listUsers(@Param() page: number) {} // Wrong! Should be @Query
}

// ✅ GOOD: Correct decorators
@Controller('users')
export class UserController {
  @Get(':id')
  getUser(@Param('id') id: string) {}
  
  @Get()
  listUsers(
    @Query('page') page: number = 1,
    @Query('limit') limit: number = 20
  ) {}
  
  @Post()
  createUser(@Body() dto: CreateUserDto) {}
}
```

### Validation

**Source**: [NestJS Validation](https://docs.nestjs.com/techniques/validation)

**Check**:
- [ ] Global validation pipe enabled?
- [ ] DTOs use class-validator decorators?
- [ ] Validation errors return proper status codes?
- [ ] Custom validators when needed?

```typescript
// main.ts - Enable global validation
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true, // Strip non-whitelisted properties
    forbidNonWhitelisted: true, // Throw error on unknown properties
    transform: true, // Auto-transform to DTO instances
    transformOptions: {
      enableImplicitConversion: true // Convert types automatically
    }
  })
);

// DTO with validation
import { IsEmail, IsString, MinLength, MaxLength, Matches } from 'class-validator';

export class CreateUserDto {
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

// ❌ BAD: No validation
@Post()
async create(@Body() data: any) {
  return this.userService.create(data);
}

// ✅ GOOD: DTO with validation
@Post()
async create(@Body() dto: CreateUserDto) {
  return this.userService.create(dto);
}
```

### Guards

**Source**: [NestJS Guards](https://docs.nestjs.com/guards)

**Check**:
- [ ] Authentication guards on protected routes?
- [ ] Authorization checks in place?
- [ ] Guards return boolean or throw exception?
- [ ] Guards registered at appropriate level (global/controller/route)?

```typescript
// ❌ BAD: No guards
@Controller('admin')
export class AdminController {
  @Get('users')
  getAllUsers() {} // Anyone can access!
}

// ✅ GOOD: Guards applied
@Controller('admin')
@UseGuards(AuthGuard('jwt'), RolesGuard)
export class AdminController {
  @Get('users')
  @Roles('admin')
  getAllUsers() {}
  
  @Get('settings')
  @Roles('admin', 'superadmin')
  getSettings() {}
}

// Guard implementation
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(),
      context.getClass()
    ]);
    
    if (!requiredRoles) {
      return true;
    }
    
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some(role => user.roles?.includes(role));
  }
}
```

### Interceptors

**Source**: [NestJS Interceptors](https://docs.nestjs.com/interceptors)

**Check**:
- [ ] Interceptors follow single responsibility?
- [ ] Transform logic in interceptors, not controllers?
- [ ] Proper use of `map` operator?
- [ ] Error handling in interceptors?

```typescript
// ✅ GOOD: Transform interceptor
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor<T, Response<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<Response<T>> {
    return next.handle().pipe(
      map(data => ({
        data,
        statusCode: context.switchToHttp().getResponse().statusCode,
        timestamp: new Date().toISOString()
      }))
    );
  }
}

// ✅ GOOD: Logging interceptor
@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  constructor(private readonly logger: Logger) {}

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url } = request;
    const now = Date.now();

    return next.handle().pipe(
      tap(() => {
        const response = context.switchToHttp().getResponse();
        const delay = Date.now() - now;
        
        this.logger.log(
          `${method} ${url} ${response.statusCode} - ${delay}ms`,
          'HTTP'
        );
      })
    );
  }
}
```

---

## Exception Handling

### Built-in Exceptions

**Source**: [NestJS Exception Filters](https://docs.nestjs.com/exception-filters)

**Check**:
- [ ] Uses NestJS built-in exceptions?
- [ ] Correct HTTP exception for each case?
- [ ] No generic `throw new Error()`?

```typescript
import {
  BadRequestException,
  NotFoundException,
  UnauthorizedException,
  ForbiddenException,
  ConflictException,
  InternalServerErrorException
} from '@nestjs/common';

// ❌ BAD: Generic errors
throw new Error('User not found'); // Returns 500
throw new Error('Invalid email'); // Returns 500

// ✅ GOOD: Specific exceptions
throw new NotFoundException('User not found'); // 404
throw new BadRequestException('Invalid email format'); // 400
throw new UnauthorizedException('Invalid credentials'); // 401
throw new ForbiddenException('Insufficient permissions'); // 403
throw new ConflictException('Email already exists'); // 409
```

### Custom Exception Filters

**Check**:
- [ ] Global exception filter configured?
- [ ] Custom filters for specific exceptions?
- [ ] Proper error response format?
- [ ] Errors logged with context?

```typescript
// ✅ GOOD: Custom exception filter
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  constructor(private readonly logger: Logger) {}

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse();
    const request = ctx.getRequest();

    const status = 
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR;

    const message =
      exception instanceof HttpException
        ? exception.getResponse()
        : 'Internal server error';

    this.logger.error(
      `HTTP ${status} - ${request.method} ${request.url}`,
      exception instanceof Error ? exception.stack : 'Unknown error'
    );

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message
    });
  }
}

// Register globally
app.useGlobalFilters(new AllExceptionsFilter(logger));
```

---

## Database Integration

### TypeORM Integration

**Source**: [NestJS TypeORM](https://docs.nestjs.com/techniques/database)

**Check**:
- [ ] Entities properly decorated?
- [ ] Repositories injected correctly?
- [ ] Transactions used for multi-step operations?
- [ ] Relations configured properly?

```typescript
// ✅ GOOD: Entity definition
@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @OneToMany(() => Post, post => post.user)
  posts: Post[];

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}

// ✅ GOOD: Repository injection
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>
  ) {}

  async findOne(id: number): Promise<User> {
    const user = await this.userRepository.findOne({ 
      where: { id },
      relations: ['posts']
    });
    
    if (!user) {
      throw new NotFoundException(`User ${id} not found`);
    }
    
    return user;
  }
}

// ✅ GOOD: Using transactions
async createUserWithProfile(dto: CreateUserDto) {
  return this.userRepository.manager.transaction(async manager => {
    const user = manager.create(User, dto);
    await manager.save(user);
    
    const profile = manager.create(Profile, { userId: user.id });
    await manager.save(profile);
    
    return user;
  });
}
```

---

## Configuration

### ConfigModule

**Source**: [NestJS Configuration](https://docs.nestjs.com/techniques/configuration)

**Check**:
- [ ] ConfigModule imported in root module?
- [ ] Environment variables validated?
- [ ] Configuration namespaced by feature?
- [ ] Type-safe configuration access?

```typescript
// ✅ GOOD: Configuration setup
// app.module.ts
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      validationSchema: Joi.object({
        NODE_ENV: Joi.string()
          .valid('development', 'production', 'test')
          .default('development'),
        PORT: Joi.number().default(3000),
        DATABASE_HOST: Joi.string().required(),
        DATABASE_PORT: Joi.number().required(),
        JWT_SECRET: Joi.string().min(32).required()
      })
    })
  ]
})
export class AppModule {}

// ✅ GOOD: Type-safe configuration
export const databaseConfig = registerAs('database', () => ({
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT, 10),
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME
}));

// Using in service
@Injectable()
export class DatabaseService {
  constructor(
    @Inject(databaseConfig.KEY)
    private config: ConfigType<typeof databaseConfig>
  ) {
    console.log(this.config.host); // Type-safe!
  }
}
```

---

## Testing

### Unit Testing

**Source**: [NestJS Testing](https://docs.nestjs.com/fundamentals/testing)

**Check**:
- [ ] Services have unit tests?
- [ ] Dependencies properly mocked?
- [ ] Test module uses `Test.createTestingModule()`?
- [ ] Tests are isolated?

```typescript
// ✅ GOOD: Unit test
describe('UserService', () => {
  let service: UserService;
  let repository: Repository<User>;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: {
            findOne: jest.fn(),
            save: jest.fn(),
            create: jest.fn()
          }
        }
      ]
    }).compile();

    service = module.get<UserService>(UserService);
    repository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  describe('findOne', () => {
    it('should return a user when found', async () => {
      const user = { id: 1, email: 'test@example.com' };
      jest.spyOn(repository, 'findOne').mockResolvedValue(user as User);

      const result = await service.findOne(1);

      expect(result).toEqual(user);
      expect(repository.findOne).toHaveBeenCalledWith({
        where: { id: 1 },
        relations: ['posts']
      });
    });

    it('should throw NotFoundException when user not found', async () => {
      jest.spyOn(repository, 'findOne').mockResolvedValue(null);

      await expect(service.findOne(1)).rejects.toThrow(NotFoundException);
    });
  });
});
```

### E2E Testing

**Check**:
- [ ] E2E tests for critical flows?
- [ ] Test database used (not production)?
- [ ] Tests clean up after themselves?
- [ ] Authentication tested?

```typescript
// ✅ GOOD: E2E test
describe('UserController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule]
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  afterAll(async () => {
    await app.close();
  });

  describe('/users (POST)', () => {
    it('should create a user', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'test@example.com',
          password: 'Password123',
          name: 'Test User'
        })
        .expect(201)
        .expect(res => {
          expect(res.body).toHaveProperty('id');
          expect(res.body.email).toBe('test@example.com');
          expect(res.body).not.toHaveProperty('password');
        });
    });

    it('should return 400 for invalid email', () => {
      return request(app.getHttpServer())
        .post('/users')
        .send({
          email: 'invalid-email',
          password: 'Password123'
        })
        .expect(400);
    });
  });
});
```

---

## Performance & Best Practices

### Async Operations

**Check**:
- [ ] Controllers use async/await?
- [ ] Services return Promises?
- [ ] No blocking operations?

```typescript
// ❌ BAD: Synchronous controller
@Get()
getUsers() {
  return this.userService.findAll(); // Blocks if service is slow
}

// ✅ GOOD: Async controller
@Get()
async getUsers() {
  return this.userService.findAll();
}
```

### DTOs for Type Safety

**Check**:
- [ ] Separate DTOs for create/update operations?
- [ ] Response DTOs exclude sensitive data?
- [ ] DTOs in dedicated files?

```typescript
// ✅ GOOD: Separate DTOs
// create-user.dto.ts
export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(8)
  password: string;
}

// update-user.dto.ts
export class UpdateUserDto extends PartialType(CreateUserDto) {}

// user-response.dto.ts
export class UserResponseDto {
  id: number;
  email: string;
  createdAt: Date;
  // No password field!
}

// Service
async create(dto: CreateUserDto): Promise<UserResponseDto> {
  const user = await this.userRepository.save(dto);
  return this.toResponseDto(user); // Exclude password
}
```

### Documentation with Swagger

**Source**: [NestJS OpenAPI](https://docs.nestjs.com/openapi/introduction)

**Check**:
- [ ] Swagger module configured?
- [ ] DTOs decorated with @ApiProperty()?
- [ ] Controllers have @ApiTags()?
- [ ] Endpoints have @ApiOperation() and @ApiResponse()?

```typescript
// ✅ GOOD: Swagger documentation
@ApiTags('users')
@Controller('users')
export class UserController {
  @Post()
  @ApiOperation({ summary: 'Create a new user' })
  @ApiResponse({ status: 201, description: 'User created', type: UserResponseDto })
  @ApiResponse({ status: 400, description: 'Invalid input' })
  @ApiResponse({ status: 409, description: 'Email already exists' })
  async create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.userService.create(dto);
  }
}

// DTO with Swagger
export class CreateUserDto {
  @ApiProperty({ example: 'user@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'SecurePass123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;
}
```
