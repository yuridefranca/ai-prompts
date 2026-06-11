# General Security Review Rules

**Sources**:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CWE (Common Weakness Enumeration)](https://cwe.mitre.org/)

---

## Input Validation

**Source**: [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)

**Check**:
- [ ] All user input validated?
- [ ] Validation happens server-side (not just client)?
- [ ] Type checking in place?
- [ ] Length limits enforced?
- [ ] Whitelist validation over blacklist?
- [ ] Format validation (email, URL, phone, etc.)?

```typescript
// ❌ BAD: No validation
@Post()
async createUser(@Body() data: any) {
  return this.db.save(data); // Accepts anything!
}

// ❌ BAD: Client-side only
// Only validates in frontend - easy to bypass

// ✅ GOOD: Server-side validation with whitelist
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
  @Matches(/^[a-zA-Z\s'-]+$/) // Whitelist allowed characters
  name: string;

  @IsInt()
  @Min(18)
  @Max(120)
  age: number;
}

@Post()
async createUser(@Body() dto: CreateUserDto) {
  return this.userService.create(dto);
}
```

---

## SQL Injection Prevention

**Source**: [OWASP SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

**Check**:
- [ ] No string concatenation in queries?
- [ ] Parameterized queries or ORM used?
- [ ] Input sanitized before queries?
- [ ] Stored procedures use parameterized calls?

```typescript
// ❌ CRITICAL: SQL injection vulnerability
async getUser(userId: string) {
  const query = `SELECT * FROM users WHERE id = '${userId}'`;
  return db.query(query);
}
// User can inject: userId = "1' OR '1'='1" to get all users
// Or: userId = "1'; DROP TABLE users; --" to delete data

// ❌ STILL BAD: Template literals
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

// ✅ GOOD: Query builder
async getUser(userId: string) {
  return this.userRepository
    .createQueryBuilder('user')
    .where('user.id = :id', { id: userId })
    .getOne();
}
```

---

## XSS (Cross-Site Scripting) Prevention

**Source**: [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

**Check**:
- [ ] User input escaped before rendering?
- [ ] No direct innerHTML with user data?
- [ ] Content Security Policy (CSP) headers set?
- [ ] HTML sanitization library used when needed?

```typescript
// ❌ BAD: XSS vulnerability
function displayComment(comment: string) {
  document.getElementById('comment').innerHTML = comment;
  // User can inject: <script>alert('XSS')</script>
  // Or: <img src=x onerror="alert('XSS')">
}

// ✅ GOOD: Use textContent
function displayComment(comment: string) {
  document.getElementById('comment').textContent = comment;
  // Scripts won't execute, displayed as text
}

// ✅ GOOD: React automatically escapes
function CommentComponent({ comment }: { comment: string }) {
  return <div>{comment}</div>; // Safe by default
}

// ⚠️ CAUTION: dangerouslySetInnerHTML requires sanitization
import DOMPurify from 'dompurify';

function CommentComponent({ html }: { html: string }) {
  const sanitized = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: sanitized }} />;
}

// ✅ GOOD: Set CSP headers
app.use((req, res, next) => {
  res.setHeader(
    'Content-Security-Policy',
    "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
  );
  next();
});
```

---

## Authentication & Authorization

**Source**: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### Authentication

**Check**:
- [ ] Authentication checked for protected routes?
- [ ] Strong password requirements enforced?
- [ ] Multi-factor authentication available for sensitive operations?
- [ ] Account lockout after failed attempts?
- [ ] Session timeout implemented?

```typescript
// ❌ BAD: No authentication
@Get('admin/users')
async getAllUsers() {
  return this.usersService.findAll(); // Anyone can access!
}

// ❌ BAD: Weak password requirements
class CreateUserDto {
  @IsString()
  @MinLength(1) // Too short!
  password: string;
}

// ✅ GOOD: Authentication guard
@Get('admin/users')
@UseGuards(AuthGuard('jwt'))
async getAllUsers() {
  return this.usersService.findAll();
}

// ✅ GOOD: Strong password requirements
class CreateUserDto {
  @IsString()
  @MinLength(12)
  @MaxLength(128)
  @Matches(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])/, {
    message: 'Password must contain uppercase, lowercase, number, and special character'
  })
  password: string;
}

// ✅ GOOD: Rate limiting for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per window
  message: 'Too many login attempts, please try again later'
});

app.use('/api/auth/login', authLimiter);
```

### Authorization

**Check**:
- [ ] Authorization enforced (user has permission)?
- [ ] Role-based access control (RBAC) implemented?
- [ ] Permissions validated on server-side?
- [ ] No authorization logic in client-side only?

```typescript
// ❌ BAD: No authorization check
@Delete('users/:id')
@UseGuards(AuthGuard)
async deleteUser(@Param('id') id: string) {
  return this.usersService.delete(id); // Any logged-in user can delete any user!
}

// ✅ GOOD: Role-based authorization
@Delete('users/:id')
@UseGuards(AuthGuard, RolesGuard)
@Roles('admin')
async deleteUser(@Param('id') id: string) {
  return this.usersService.delete(id);
}

// ✅ GOOD: Resource ownership check
@Delete('posts/:id')
@UseGuards(AuthGuard)
async deletePost(
  @Param('id') id: string,
  @CurrentUser() user: User
) {
  const post = await this.postsService.findOne(id);
  
  if (post.authorId !== user.id && !user.roles.includes('admin')) {
    throw new ForbiddenException('You can only delete your own posts');
  }
  
  return this.postsService.delete(id);
}
```

---

## Sensitive Data Handling

**Source**: [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

### Password Storage

**Check**:
- [ ] Passwords hashed (bcrypt, argon2, scrypt)?
- [ ] Never stored in plain text?
- [ ] Salt used (automatic with bcrypt/argon2)?
- [ ] Appropriate cost factor (10+ for bcrypt)?

```typescript
// ❌ CRITICAL: Plain text password
async createUser(dto: CreateUserDto) {
  return this.db.save({
    email: dto.email,
    password: dto.password // NEVER STORE PLAIN TEXT!
  });
}

// ❌ BAD: Weak hashing (MD5, SHA1)
async createUser(dto: CreateUserDto) {
  const hashed = crypto.createHash('md5').update(dto.password).digest('hex');
  return this.db.save({ email: dto.email, password: hashed });
}

// ✅ GOOD: bcrypt with appropriate cost
import * as bcrypt from 'bcrypt';

async createUser(dto: CreateUserDto) {
  const saltRounds = 12; // Higher = more secure, but slower
  const hashedPassword = await bcrypt.hash(dto.password, saltRounds);
  
  return this.db.save({
    email: dto.email,
    password: hashedPassword
  });
}

async validatePassword(plainPassword: string, hashedPassword: string): Promise<boolean> {
  return bcrypt.compare(plainPassword, hashedPassword);
}

// ✅ BETTER: argon2 (more secure)
import * as argon2 from 'argon2';

async createUser(dto: CreateUserDto) {
  const hashedPassword = await argon2.hash(dto.password);
  
  return this.db.save({
    email: dto.email,
    password: hashedPassword
  });
}
```

### Secrets Management

**Check**:
- [ ] No secrets in code or version control?
- [ ] Environment variables for sensitive config?
- [ ] Secrets stored in secure vault (AWS Secrets Manager, HashiCorp Vault)?
- [ ] API keys rotated regularly?

```typescript
// ❌ BAD: Secrets in code
const apiKey = 'sk_live_abc123xyz789'; // NEVER!
const dbPassword = 'MyP@ssw0rd123'; // NEVER!

// ❌ BAD: Committed to git
// .env file committed to repository

// ✅ GOOD: Environment variables
const apiKey = process.env.STRIPE_API_KEY;
const dbPassword = process.env.DATABASE_PASSWORD;

// ✅ GOOD: Validate required secrets
import { z } from 'zod';

const envSchema = z.object({
  STRIPE_API_KEY: z.string().min(1),
  DATABASE_PASSWORD: z.string().min(1),
  JWT_SECRET: z.string().min(32)
});

const env = envSchema.parse(process.env);

// ✅ BEST: Secrets manager
import { SecretsManager } from '@aws-sdk/client-secrets-manager';

async function getSecret(secretName: string) {
  const client = new SecretsManager({ region: 'us-east-1' });
  const response = await client.getSecretValue({ SecretId: secretName });
  return JSON.parse(response.SecretString);
}
```

### PII (Personally Identifiable Information)

**Check**:
- [ ] PII encrypted at rest?
- [ ] PII encrypted in transit (HTTPS)?
- [ ] PII masked in logs?
- [ ] PII not exposed in error messages?

```typescript
// ❌ BAD: PII in logs
logger.info('User logged in', {
  email: user.email, // PII exposed
  ssn: user.ssn, // Very sensitive!
  creditCard: user.creditCard // Very sensitive!
});

// ✅ GOOD: Masked PII in logs
logger.info('User logged in', {
  userId: user.id, // Use ID instead
  emailDomain: user.email.split('@')[1] // Only domain
});

// ✅ GOOD: Mask sensitive data
function maskEmail(email: string): string {
  const [local, domain] = email.split('@');
  return `${local.substring(0, 2)}***@${domain}`;
}

function maskCreditCard(card: string): string {
  return `****-****-****-${card.slice(-4)}`;
}

logger.info('Payment processed', {
  userId: user.id,
  email: maskEmail(user.email),
  card: maskCreditCard(payment.card)
});
```

---

## CSRF Protection

**Source**: [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

**Check**:
- [ ] State-changing operations protected?
- [ ] CSRF tokens used for forms?
- [ ] SameSite cookie attribute set?
- [ ] Origin/Referer header validation?

```typescript
// ❌ BAD: No CSRF protection
@Post('transfer-money')
async transfer(@Body() dto: TransferDto) {
  return this.bankService.transfer(dto);
  // Attacker can create malicious form that submits to this endpoint
}

// ✅ GOOD: CSRF protection with token
import * as csurf from 'csurf';

const csrfProtection = csurf({ cookie: true });

app.use(csrfProtection);

// ✅ GOOD: SameSite cookies
app.use(session({
  secret: process.env.SESSION_SECRET,
  cookie: {
    httpOnly: true,
    secure: true, // HTTPS only
    sameSite: 'strict' // Prevents CSRF
  }
}));

// ✅ GOOD: Origin validation
app.use((req, res, next) => {
  const origin = req.get('origin');
  const allowedOrigins = ['https://example.com', 'https://app.example.com'];
  
  if (origin && !allowedOrigins.includes(origin)) {
    return res.status(403).json({ error: 'Forbidden origin' });
  }
  
  next();
});
```

---

## Security Headers

**Source**: [OWASP Secure Headers Project](https://owasp.org/www-project-secure-headers/)

**Check**:
- [ ] Helmet.js or equivalent security headers middleware used?
- [ ] HTTPS enforced (HSTS header)?
- [ ] Content-Type sniffing disabled?
- [ ] Clickjacking protection (X-Frame-Options)?

```typescript
// ✅ GOOD: Security headers with Helmet
import helmet from 'helmet';

app.use(helmet());

// Or configure individually
app.use(
  helmet({
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
    hsts: {
      maxAge: 31536000, // 1 year
      includeSubDomains: true,
      preload: true,
    },
    frameguard: {
      action: 'deny', // Prevent clickjacking
    },
    noSniff: true, // Prevent MIME sniffing
    xssFilter: true, // Enable XSS filter
  })
);

// ✅ GOOD: Force HTTPS
app.use((req, res, next) => {
  if (req.header('x-forwarded-proto') !== 'https' && process.env.NODE_ENV === 'production') {
    return res.redirect(`https://${req.header('host')}${req.url}`);
  }
  next();
});
```

---

## Rate Limiting

**Source**: [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)

**Check**:
- [ ] Rate limiting implemented?
- [ ] Different limits for authenticated vs anonymous?
- [ ] Stricter limits on sensitive endpoints (login, register)?
- [ ] DDoS protection in place?

```typescript
// ✅ GOOD: General rate limiting
import rateLimit from 'express-rate-limit';

const generalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  message: 'Too many requests from this IP, please try again later',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', generalLimiter);

// ✅ GOOD: Strict rate limiting for auth
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // Only 5 login attempts
  skipSuccessfulRequests: true, // Don't count successful logins
});

app.use('/api/auth/login', authLimiter);
app.use('/api/auth/register', authLimiter);

// ✅ GOOD: Per-user rate limiting
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import Redis from 'ioredis';

const redis = new Redis();

const userLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: async (req) => {
    // Premium users get higher limits
    const user = req.user;
    return user?.isPremium ? 1000 : 100;
  },
  keyGenerator: (req) => req.user?.id || req.ip,
  store: new RedisStore({
    client: redis,
    prefix: 'rl:',
  }),
});
```

---

## File Upload Security

**Check**:
- [ ] File type validated (not just extension)?
- [ ] File size limits enforced?
- [ ] Files scanned for malware?
- [ ] Uploaded files stored outside webroot?
- [ ] Unique, non-guessable filenames?

```typescript
// ❌ BAD: No validation
@Post('upload')
@UseInterceptors(FileInterceptor('file'))
async upload(@UploadedFile() file: Express.Multer.File) {
  return { filename: file.originalname }; // Accepts anything!
}

// ✅ GOOD: Proper validation
import { FileInterceptor } from '@nestjs/platform-express';
import { diskStorage } from 'multer';
import * as path from 'path';
import * as crypto from 'crypto';

@Post('upload')
@UseInterceptors(
  FileInterceptor('file', {
    limits: {
      fileSize: 5 * 1024 * 1024, // 5MB max
    },
    fileFilter: (req, file, cb) => {
      // Validate MIME type
      const allowedMimes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!allowedMimes.includes(file.mimetype)) {
        return cb(new Error('Invalid file type'), false);
      }
      cb(null, true);
    },
    storage: diskStorage({
      destination: './uploads', // Outside webroot
      filename: (req, file, cb) => {
        // Generate unique filename
        const randomName = crypto.randomBytes(16).toString('hex');
        const ext = path.extname(file.originalname);
        cb(null, `${randomName}${ext}`);
      },
    }),
  })
)
async upload(@UploadedFile() file: Express.Multer.File) {
  // Additional validation: check file signature (magic bytes)
  const fileBuffer = await fs.readFile(file.path);
  const fileType = await FileType.fromBuffer(fileBuffer);
  
  if (!fileType || !['image/jpeg', 'image/png'].includes(fileType.mime)) {
    await fs.unlink(file.path); // Delete invalid file
    throw new BadRequestException('Invalid file type');
  }
  
  return { filename: file.filename };
}
```
