# Performance Review Rules

**Sources**:
- [Web.dev Performance](https://web.dev/performance/)
- [Node.js Best Practices - Performance](https://github.com/goldbergyoni/nodebestpractices#6-performance-best-practices)
- [Use The Index, Luke](https://use-the-index-luke.com/) (SQL Performance)

---

## Database Query Performance

### N+1 Query Problem

**Check**:
- [ ] No queries inside loops?
- [ ] Eager loading used where appropriate?
- [ ] Relations loaded efficiently?

```typescript
// ❌ BAD: N+1 query problem
async getUsersWithPosts() {
  const users = await this.userRepo.find(); // 1 query
  
  for (const user of users) {
    user.posts = await this.postRepo.find({ userId: user.id }); // N queries!
  }
  // Total: 1 + N queries (if 100 users = 101 queries!)
  
  return users;
}

// ❌ BAD: Sequential queries
async getUserProfile(userId: string) {
  const user = await this.userRepo.findOne(userId);
  const posts = await this.postRepo.find({ userId }); // Wait for user
  const comments = await this.commentRepo.find({ userId }); // Wait for posts
  
  return { user, posts, comments };
}

// ✅ GOOD: Eager loading
async getUsersWithPosts() {
  return this.userRepo.find({
    relations: ['posts'] // Single query with JOIN
  });
}

// ✅ GOOD: Query builder with JOIN
async getUsersWithPosts() {
  return this.userRepo
    .createQueryBuilder('user')
    .leftJoinAndSelect('user.posts', 'post')
    .getMany(); // Single optimized query
}

// ✅ GOOD: Parallel queries (when JOIN not possible)
async getUserProfile(userId: string) {
  const [user, posts, comments] = await Promise.all([
    this.userRepo.findOne(userId),
    this.postRepo.find({ userId }),
    this.commentRepo.find({ userId })
  ]); // All queries run in parallel!
  
  return { user, posts, comments };
}
```

### Database Indexes

**Check**:
- [ ] Indexes on frequently queried fields?
- [ ] Foreign keys indexed?
- [ ] Composite indexes for multi-column queries?
- [ ] Indexes not overdone (they slow writes)?

```typescript
// ✅ GOOD: Proper indexing
@Entity()
@Index(['email']) // Single column index
@Index(['lastName', 'firstName']) // Composite index for name searches
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  @Index() // Unique index automatically created
  email: string;

  @Column()
  firstName: string;

  @Column()
  lastName: string;

  @Column()
  @Index() // Index for filtering active users
  isActive: boolean;

  @CreateDateColumn()
  @Index() // Index for date range queries
  createdAt: Date;
}

// Supports queries like:
// SELECT * FROM users WHERE email = 'x'; -- Uses email index
// SELECT * FROM users WHERE lastName = 'Smith' AND firstName = 'John'; -- Uses composite
// SELECT * FROM users WHERE isActive = true; -- Uses isActive index
// SELECT * FROM users WHERE createdAt > '2024-01-01'; -- Uses createdAt index
```

### Pagination

**Check**:
- [ ] List endpoints use pagination?
- [ ] Default and maximum limits enforced?
- [ ] Cursor-based pagination for large datasets?
- [ ] Metadata included (total count, page info)?

```typescript
// ❌ BAD: No pagination
@Get('users')
async getUsers() {
  return this.userRepo.find(); // Could return millions!
}

// ❌ BAD: No limit validation
@Get('users')
async getUsers(@Query('limit') limit: number) {
  return this.userRepo.find({ take: limit }); // User can request 1 million!
}

// ✅ GOOD: Offset pagination with limits
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
    take: safeLimit,
    order: { createdAt: 'DESC' }
  });
  
  return {
    data: users,
    meta: {
      total,
      page,
      limit: safeLimit,
      totalPages: Math.ceil(total / safeLimit),
      hasNextPage: page < Math.ceil(total / safeLimit),
      hasPrevPage: page > 1
    }
  };
}

// ✅ BETTER: Cursor-based pagination (for real-time data)
@Get('posts')
async getPosts(
  @Query('cursor') cursor?: string,
  @Query('limit') limit: number = 20
) {
  const safeLimit = Math.min(limit, 100);
  
  const query = this.postRepo
    .createQueryBuilder('post')
    .orderBy('post.createdAt', 'DESC')
    .take(safeLimit + 1); // Take one extra to know if there's more
  
  if (cursor) {
    query.where('post.createdAt < :cursor', { cursor: new Date(cursor) });
  }
  
  const posts = await query.getMany();
  const hasMore = posts.length > safeLimit;
  
  if (hasMore) {
    posts.pop(); // Remove the extra
  }
  
  return {
    data: posts,
    meta: {
      nextCursor: hasMore ? posts[posts.length - 1].createdAt : null,
      hasMore
    }
  };
}
```

### Query Optimization

**Check**:
- [ ] SELECT only needed columns?
- [ ] WHERE clauses use indexed columns?
- [ ] JOINs are necessary?
- [ ] Query execution plan analyzed for slow queries?

```typescript
// ❌ BAD: Fetching all columns
async getUserEmails() {
  const users = await this.userRepo.find(); // Fetches all columns!
  return users.map(u => u.email);
}

// ✅ GOOD: Select only needed columns
async getUserEmails() {
  return this.userRepo
    .createQueryBuilder('user')
    .select(['user.id', 'user.email']) // Only fetch what's needed
    .getMany();
}

// ❌ BAD: Inefficient filtering
async getActiveUsers() {
  const allUsers = await this.userRepo.find();
  return allUsers.filter(u => u.isActive); // Filtering in application!
}

// ✅ GOOD: Filter in database
async getActiveUsers() {
  return this.userRepo.find({
    where: { isActive: true } // Let database filter
  });
}
```

---

## Caching

### Strategy

**Check**:
- [ ] Expensive operations cached?
- [ ] Cache TTL set appropriately?
- [ ] Cache invalidation strategy in place?
- [ ] Cache keys properly namespaced?

```typescript
// ❌ BAD: No caching
async getPopularPosts() {
  // Expensive query run on every request
  return this.postRepo
    .createQueryBuilder('post')
    .leftJoinAndSelect('post.comments', 'comment')
    .leftJoinAndSelect('post.likes', 'like')
    .orderBy('like.count', 'DESC')
    .take(10)
    .getMany();
}

// ✅ GOOD: With caching
@Injectable()
export class PostService {
  constructor(
    private postRepo: Repository<Post>,
    @Inject('CACHE_MANAGER') private cacheManager: Cache
  ) {}
  
  async getPopularPosts(): Promise<Post[]> {
    const cacheKey = 'posts:popular';
    
    // Try cache first
    const cached = await this.cacheManager.get<Post[]>(cacheKey);
    if (cached) {
      return cached;
    }
    
    // Cache miss - query database
    const posts = await this.postRepo
      .createQueryBuilder('post')
      .leftJoinAndSelect('post.comments', 'comment')
      .leftJoinAndSelect('post.likes', 'like')
      .orderBy('like.count', 'DESC')
      .take(10)
      .getMany();
    
    // Store in cache for 5 minutes
    await this.cacheManager.set(cacheKey, posts, 300);
    
    return posts;
  }
  
  async createPost(dto: CreatePostDto): Promise<Post> {
    const post = await this.postRepo.save(dto);
    
    // Invalidate cache when new post is created
    await this.cacheManager.del('posts:popular');
    
    return post;
  }
}
```

### Cache Layers

**Check**:
- [ ] Multiple cache layers considered (memory, Redis, CDN)?
- [ ] Cache warming for predictable loads?
- [ ] Cache stampede protection?

```typescript
// ✅ GOOD: Multi-layer caching
export class CacheService {
  private memoryCache = new Map<string, { data: any; expires: number }>();
  
  constructor(
    @Inject('REDIS') private redis: Redis
  ) {}
  
  async get<T>(key: string): Promise<T | null> {
    // Layer 1: Memory cache (fastest)
    const memCached = this.memoryCache.get(key);
    if (memCached && memCached.expires > Date.now()) {
      return memCached.data;
    }
    
    // Layer 2: Redis cache
    const redisCached = await this.redis.get(key);
    if (redisCached) {
      const data = JSON.parse(redisCached);
      
      // Populate memory cache
      this.memoryCache.set(key, {
        data,
        expires: Date.now() + 60000 // 1 minute in memory
      });
      
      return data;
    }
    
    return null;
  }
  
  async set(key: string, value: any, ttlSeconds: number): Promise<void> {
    // Set in both layers
    this.memoryCache.set(key, {
      data: value,
      expires: Date.now() + Math.min(ttlSeconds * 1000, 60000)
    });
    
    await this.redis.setex(key, ttlSeconds, JSON.stringify(value));
  }
}
```

---

## Async Operations & Concurrency

### Parallel Execution

**Check**:
- [ ] Independent operations run in parallel?
- [ ] Promise.all used for concurrent operations?
- [ ] Batch operations where possible?

```typescript
// ❌ BAD: Sequential execution
async function processUserData(userId: string) {
  const user = await fetchUser(userId); // Wait
  const posts = await fetchPosts(userId); // Wait
  const comments = await fetchComments(userId); // Wait
  const likes = await fetchLikes(userId); // Wait
  
  return { user, posts, comments, likes };
  // Total time: time(user) + time(posts) + time(comments) + time(likes)
}

// ✅ GOOD: Parallel execution
async function processUserData(userId: string) {
  const [user, posts, comments, likes] = await Promise.all([
    fetchUser(userId),
    fetchPosts(userId),
    fetchComments(userId),
    fetchLikes(userId)
  ]);
  
  return { user, posts, comments, likes };
  // Total time: max(time(user), time(posts), time(comments), time(likes))
}

// ✅ GOOD: Batch processing
async function processUsers(userIds: string[]) {
  // Instead of looping and making N requests
  const users = await this.userRepo.findByIds(userIds); // Single query
  
  return users;
}
```

### Rate Limiting External APIs

**Check**:
- [ ] External API calls rate-limited?
- [ ] Retry logic with exponential backoff?
- [ ] Circuit breaker pattern for failing services?

```typescript
// ✅ GOOD: Rate limiting with p-queue
import PQueue from 'p-queue';

export class ExternalAPIService {
  private queue = new PQueue({
    concurrency: 5, // Max 5 concurrent requests
    interval: 1000, // Per second
    intervalCap: 10 // Max 10 requests per interval
  });
  
  async fetchData(id: string): Promise<any> {
    return this.queue.add(() => this.makeRequest(id));
  }
  
  private async makeRequest(id: string): Promise<any> {
    // Actual API call
  }
}

// ✅ GOOD: Retry with exponential backoff
async function fetchWithRetry(url: string, maxRetries = 3): Promise<any> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fetch(url);
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      
      const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s, 8s...
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}
```

---

## Algorithm Efficiency

### Time Complexity

**Check**:
- [ ] No O(n²) nested loops when avoidable?
- [ ] Appropriate data structures used?
- [ ] Early returns to avoid unnecessary work?

```typescript
// ❌ BAD: O(n²) complexity
function findDuplicates(arr: number[]): number[] {
  const duplicates: number[] = [];
  
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  
  return duplicates;
}

// ✅ GOOD: O(n) complexity
function findDuplicates(arr: number[]): number[] {
  const seen = new Set<number>();
  const duplicates = new Set<number>();
  
  for (const num of arr) {
    if (seen.has(num)) {
      duplicates.add(num);
    } else {
      seen.add(num);
    }
  }
  
  return Array.from(duplicates);
}

// ❌ BAD: O(n) search every time
function findUser(users: User[], id: number): User | undefined {
  return users.find(u => u.id === id); // Linear search
}

// ✅ GOOD: O(1) lookup
const userMap = new Map(users.map(u => [u.id, u]));
function findUser(id: number): User | undefined {
  return userMap.get(id); // Constant time
}
```

### Space Complexity

**Check**:
- [ ] No unnecessary copies of large data?
- [ ] Streams used for large files?
- [ ] Memory released when no longer needed?

```typescript
// ❌ BAD: Loading entire file into memory
async function processLargeFile(filePath: string) {
  const content = await fs.readFile(filePath, 'utf-8'); // Could be gigabytes!
  const lines = content.split('\n');
  
  for (const line of lines) {
    await processLine(line);
  }
}

// ✅ GOOD: Streaming
import { createReadStream } from 'fs';
import * as readline from 'readline';

async function processLargeFile(filePath: string) {
  const fileStream = createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });
  
  for await (const line of rl) {
    await processLine(line); // Process one line at a time
  }
}
```

---

## Blocking Operations

### Non-Blocking I/O

**Check**:
- [ ] No synchronous file operations in request handlers?
- [ ] No blocking CPU-intensive work on main thread?
- [ ] Worker threads for heavy computation?

```typescript
// ❌ BAD: Blocking file read
import * as fs from 'fs';

@Get('file')
getFile() {
  const data = fs.readFileSync('./large-file.json'); // BLOCKS entire server!
  return JSON.parse(data.toString());
}

// ✅ GOOD: Non-blocking
import { promises as fs } from 'fs';

@Get('file')
async getFile() {
  const data = await fs.readFile('./large-file.json', 'utf-8');
  return JSON.parse(data);
}

// ❌ BAD: CPU-intensive work blocking requests
@Post('process')
processData(@Body() data: any) {
  // Heavy computation blocks all requests
  for (let i = 0; i < 1000000000; i++) {
    // Complex calculation
  }
  return result;
}

// ✅ GOOD: Offload to worker thread
import { Worker } from 'worker_threads';

@Post('process')
async processData(@Body() data: any) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./processor-worker.js');
    worker.postMessage(data);
    
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}
```

---

## Memory Management

### Memory Leaks

**Check**:
- [ ] Event listeners removed when no longer needed?
- [ ] Timers cleared?
- [ ] Large objects not held in closures?
- [ ] Circular references avoided?

```typescript
// ❌ BAD: Memory leak - listeners not removed
export class UserService {
  constructor(private eventEmitter: EventEmitter) {
    this.eventEmitter.on('user:created', this.handleUserCreated);
    // Listener never removed, keeps reference even when service destroyed
  }
  
  handleUserCreated(user: User) {
    // Handle event
  }
}

// ✅ GOOD: Cleanup listeners
export class UserService implements OnDestroy {
  private listener: (user: User) => void;
  
  constructor(private eventEmitter: EventEmitter) {
    this.listener = this.handleUserCreated.bind(this);
    this.eventEmitter.on('user:created', this.listener);
  }
  
  onDestroy() {
    this.eventEmitter.off('user:created', this.listener);
  }
  
  handleUserCreated(user: User) {
    // Handle event
  }
}

// ❌ BAD: Timer not cleared
setInterval(() => {
  checkStatus();
}, 1000); // Runs forever!

// ✅ GOOD: Clear timers
const interval = setInterval(() => {
  checkStatus();
}, 1000);

// Later, when done
clearInterval(interval);
```

---

## Response Size Optimization

### Payload Size

**Check**:
- [ ] Only return necessary data?
- [ ] Pagination for large result sets?
- [ ] Compression enabled (gzip, brotli)?
- [ ] Field selection supported?

```typescript
// ❌ BAD: Returning too much data
@Get('users/:id')
async getUser(@Param('id') id: string) {
  const user = await this.userRepo.findOne(id, {
    relations: ['posts', 'comments', 'likes', 'followers', 'following']
  });
  // Returns EVERYTHING including nested relations
  return user;
}

// ✅ GOOD: Return only what's needed
@Get('users/:id')
async getUser(@Param('id') id: string) {
  const user = await this.userRepo.findOne(id);
  
  return {
    id: user.id,
    name: user.name,
    email: user.email,
    avatar: user.avatar
    // Exclude sensitive fields, nested relations
  };
}

// ✅ BETTER: Field selection
@Get('users/:id')
async getUser(
  @Param('id') id: string,
  @Query('fields') fields?: string
) {
  const selectedFields = fields?.split(',') || ['id', 'name', 'email'];
  
  return this.userRepo
    .createQueryBuilder('user')
    .select(selectedFields.map(f => `user.${f}`))
    .where('user.id = :id', { id })
    .getOne();
}

// ✅ GOOD: Enable compression
import * as compression from 'compression';

app.use(compression()); // Automatically compress responses
```
