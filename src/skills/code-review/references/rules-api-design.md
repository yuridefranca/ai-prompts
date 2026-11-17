# API Design Best Practices

**Sources**:
- [REST API Design Best Practices](https://restfulapi.net/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [GraphQL Best Practices](https://graphql.org/learn/best-practices/)
- [API Security Checklist](https://github.com/shieldfy/API-Security-Checklist)

---

## RESTful Resource Design

### Resource Naming

**Principles**:
- Use nouns, not verbs
- Use plural for collections
- Use kebab-case for multi-word resources
- Be consistent across the API

**Check**:
- [ ] Resource names are nouns?
- [ ] Collections use plural names?
- [ ] Consistent naming convention?
- [ ] No verbs in URLs?

```typescript
// ❌ BAD: Verbs in URLs, inconsistent naming
GET  /getUsers
POST /createNewUser
GET  /user/123/fetchOrders
PUT  /updateUserProfile/123

// ✅ GOOD: Nouns, plural collections, consistent
GET    /users
POST   /users
GET    /users/123/orders
PUT    /users/123
DELETE /users/123
```

### Resource Hierarchy

**Check**:
- [ ] Resources properly nested (max 2-3 levels)?
- [ ] Parent-child relationships clear?
- [ ] Not over-nesting?

```typescript
// ❌ BAD: Over-nested, confusing hierarchy
GET /organizations/123/departments/456/teams/789/members/012/tasks/345

// ✅ GOOD: Flatter structure, clear relationships
GET /teams/789/members
GET /members/012/tasks
// Or use query params
GET /tasks?memberId=012&teamId=789
```

---

## HTTP Methods & Status Codes

### Proper HTTP Verb Usage

**Check**:
- [ ] GET for retrieval (safe, idempotent)?
- [ ] POST for creation?
- [ ] PUT for full update (idempotent)?
- [ ] PATCH for partial update?
- [ ] DELETE for removal (idempotent)?

```typescript
// ❌ BAD: Wrong methods
GET  /users/123/delete  // GET should not modify
POST /users/123/update  // Should be PUT/PATCH
POST /users/123         // Should be PUT for update

// ✅ GOOD: Correct HTTP methods
GET    /users/123       // Retrieve user
POST   /users           // Create new user
PUT    /users/123       // Full update (replace)
PATCH  /users/123       // Partial update
DELETE /users/123       // Delete user
```

### Status Codes

**Check**:
- [ ] 2xx for success (200, 201, 204)?
- [ ] 4xx for client errors (400, 401, 403, 404)?
- [ ] 5xx for server errors (500, 502, 503)?
- [ ] Specific codes used appropriately?

```typescript
// ❌ BAD: Always 200, even for errors
return { status: 200, data: { error: 'User not found' } };

// ✅ GOOD: Appropriate status codes
// Success
200 OK              // Successful GET, PUT, PATCH
201 Created         // Successful POST
204 No Content      // Successful DELETE
202 Accepted        // Async operation started

// Client errors
400 Bad Request     // Invalid input
401 Unauthorized    // Not authenticated
403 Forbidden       // Not authorized
404 Not Found       // Resource doesn't exist
409 Conflict        // Duplicate or state conflict
422 Unprocessable   // Validation failed
429 Too Many Req    // Rate limit exceeded

// Server errors
500 Internal Error  // Server bug
502 Bad Gateway     // Upstream service error
503 Service Unavail // Temporary downtime
```

---

## Request & Response Format

### Request Validation

**Check**:
- [ ] All inputs validated?
- [ ] Clear validation error messages?
- [ ] Schema-based validation?
- [ ] Field-level error details?

```typescript
// ❌ BAD: Vague error message
{
  "error": "Invalid request"
}

// ✅ GOOD: Detailed validation errors
{
  "error": "Validation failed",
  "details": [
    {
      "field": "email",
      "message": "Must be a valid email address",
      "code": "INVALID_FORMAT"
    },
    {
      "field": "age",
      "message": "Must be between 18 and 120",
      "code": "OUT_OF_RANGE"
    }
  ]
}
```

### Response Consistency

**Check**:
- [ ] Consistent response structure?
- [ ] Consistent field naming (camelCase or snake_case)?
- [ ] Consistent date/time format?
- [ ] Consistent error format?

```typescript
// ❌ BAD: Inconsistent responses
GET /users/123
{ id: 123, user_name: "John", created: "2024-01-15" }

GET /products/456
{ productId: 456, name: "Widget", createdAt: "15/01/2024" }

// ✅ GOOD: Consistent structure and naming
GET /users/123
{
  "id": 123,
  "username": "John",
  "createdAt": "2024-01-15T10:30:00Z"
}

GET /products/456
{
  "id": 456,
  "name": "Widget",
  "createdAt": "2024-01-15T14:20:00Z"
}
```

### Envelope vs Direct Response

**Check**:
- [ ] Response format chosen and consistent?
- [ ] Metadata included when needed (pagination, etc.)?

```typescript
// ✅ OPTION 1: Direct response (simpler)
GET /users
[
  { "id": 1, "name": "John" },
  { "id": 2, "name": "Jane" }
]

// ✅ OPTION 2: Enveloped (better for metadata)
GET /users
{
  "data": [
    { "id": 1, "name": "John" },
    { "id": 2, "name": "Jane" }
  ],
  "meta": {
    "total": 150,
    "page": 1,
    "perPage": 20
  }
}
```

---

## Pagination

### Pagination Strategy

**Check**:
- [ ] Pagination implemented for collections?
- [ ] Default page size reasonable (10-100)?
- [ ] Maximum page size enforced?
- [ ] Pagination metadata provided?

```typescript
// ❌ BAD: No pagination (could return millions of records)
GET /users
// Returns all users in database

// ✅ GOOD: Offset-based pagination
GET /users?page=2&limit=20
{
  "data": [...],
  "meta": {
    "page": 2,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}

// ✅ GOOD: Cursor-based pagination (better for large datasets)
GET /users?cursor=eyJpZCI6MTIzfQ&limit=20
{
  "data": [...],
  "meta": {
    "nextCursor": "eyJpZCI6MTQzfQ",
    "hasMore": true
  }
}
```

---

## Filtering, Sorting, Searching

### Query Parameters

**Check**:
- [ ] Filtering supported with query params?
- [ ] Sorting supported?
- [ ] Searching supported?
- [ ] Consistent query param naming?

```typescript
// ✅ GOOD: Comprehensive query capabilities
GET /users?
  status=active&
  role=admin&
  sort=-createdAt,name&
  search=john&
  limit=20

// Response includes applied filters
{
  "data": [...],
  "meta": {
    "filters": {
      "status": "active",
      "role": "admin"
    },
    "sort": ["-createdAt", "name"],
    "search": "john"
  }
}
```

---

## Versioning

### API Versioning Strategy

**Check**:
- [ ] Versioning strategy chosen and applied?
- [ ] Version clearly indicated?
- [ ] Backward compatibility maintained?
- [ ] Deprecation policy defined?

```typescript
// ✅ OPTION 1: URL versioning (most common)
GET /v1/users
GET /v2/users

// ✅ OPTION 2: Header versioning
GET /users
Headers: API-Version: 1

// ✅ OPTION 3: Content negotiation
GET /users
Headers: Accept: application/vnd.myapi.v1+json

// ❌ BAD: No versioning
GET /users  // What happens when we need breaking changes?
```

### Deprecation

**Check**:
- [ ] Deprecated endpoints marked?
- [ ] Deprecation warnings in responses?
- [ ] Sunset date communicated?
- [ ] Migration guide provided?

```typescript
// ✅ GOOD: Clear deprecation warning
GET /v1/users
Response Headers:
  Deprecation: true
  Sunset: Sat, 31 Dec 2024 23:59:59 GMT
  Link: <https://api.example.com/docs/v2-migration>; rel="deprecation"

Response:
{
  "data": [...],
  "meta": {
    "deprecationWarning": "This endpoint is deprecated. Please migrate to /v2/users by Dec 31, 2024."
  }
}
```

---

## Error Handling

### Error Response Format

**Check**:
- [ ] Consistent error format?
- [ ] Error codes/types included?
- [ ] Human-readable messages?
- [ ] No sensitive data in errors?
- [ ] Request ID for tracing?

```typescript
// ❌ BAD: Inconsistent, exposing internals
{
  "error": "SqlException: duplicate key value violates unique constraint users_email_key"
}

// ✅ GOOD: Consistent, safe, informative
{
  "error": {
    "type": "DUPLICATE_RESOURCE",
    "message": "A user with this email already exists",
    "statusCode": 409,
    "requestId": "req-abc-123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// ✅ GOOD: With field-level details
{
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "statusCode": 422,
    "requestId": "req-abc-124",
    "details": [
      {
        "field": "email",
        "message": "Email is already registered",
        "code": "DUPLICATE_EMAIL"
      }
    ]
  }
}
```

---

## Rate Limiting

### Rate Limit Headers

**Check**:
- [ ] Rate limiting implemented?
- [ ] Rate limit headers included?
- [ ] Clear 429 response?
- [ ] Retry-After header provided?

```typescript
// ✅ GOOD: Rate limit headers
GET /users
Response Headers:
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 999
  X-RateLimit-Reset: 1640000000

// When limit exceeded
429 Too Many Requests
Headers:
  Retry-After: 3600
  X-RateLimit-Limit: 1000
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1640000000

Response:
{
  "error": {
    "type": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again in 1 hour.",
    "retryAfter": 3600
  }
}
```

---

## Idempotency

### Idempotent Operations

**Check**:
- [ ] GET, PUT, DELETE are idempotent?
- [ ] POST operations handle duplicates?
- [ ] Idempotency keys used for critical operations?

```typescript
// ✅ GOOD: Idempotency key for payment
POST /payments
Headers:
  Idempotency-Key: unique-request-id-123

Body:
{
  "amount": 1000,
  "orderId": "order-456"
}

// Duplicate request with same key returns cached result
// Instead of charging twice
```

---

## GraphQL Specific

### Query Complexity

**Check**:
- [ ] Query complexity limits enforced?
- [ ] Depth limiting in place?
- [ ] N+1 query prevention (DataLoader)?
- [ ] Query cost analysis?

```typescript
// ❌ BAD: No depth limit, allows expensive queries
query {
  users {
    posts {
      comments {
        author {
          posts {
            comments {
              // Infinite nesting possible
            }
          }
        }
      }
    }
  }
}

// ✅ GOOD: Implement query complexity limits
// In schema configuration:
{
  validationRules: [
    depthLimit(5),
    createComplexityLimitRule(1000)
  ]
}
```

### Mutations

**Check**:
- [ ] Mutations return updated object?
- [ ] Clear input types defined?
- [ ] Errors properly handled?

```graphql
# ✅ GOOD: Clear mutation structure
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    user {
      id
      email
      createdAt
    }
    errors {
      field
      message
    }
  }
}
```

---

## API Documentation

### Documentation Requirements

**Check**:
- [ ] All endpoints documented?
- [ ] Request/response examples provided?
- [ ] Authentication requirements clear?
- [ ] Error responses documented?
- [ ] OpenAPI/Swagger spec available?

```yaml
# ✅ GOOD: OpenAPI documentation
openapi: 3.0.0
paths:
  /users:
    get:
      summary: List all users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              examples:
                default:
                  value:
                    data: [...]
                    meta: {...}
```

---

## Backward Compatibility

### Breaking Changes

**Check**:
- [ ] No removal of fields without deprecation?
- [ ] No changing field types?
- [ ] No changing URL structure?
- [ ] New required fields avoided?
- [ ] Default values for new optional fields?

```typescript
// ❌ BAD: Breaking changes
// v1
{ "id": 123, "name": "John" }

// v2 - BREAKING!
{ "userId": 123, "fullName": "John" }  // Renamed fields

// ✅ GOOD: Backward compatible changes
// v1
{ "id": 123, "name": "John" }

// v2 - COMPATIBLE
{
  "id": 123,
  "name": "John",
  "firstName": "John",      // New optional field
  "lastName": "Doe",        // New optional field
  "email": "john@example.com"  // New optional field
}
```

---

## Security Headers

### Required Headers

**Check**:
- [ ] Authentication header validated?
- [ ] CORS headers configured?
- [ ] Content-Type validated?
- [ ] Security headers present?

```typescript
// ✅ GOOD: Security headers in responses
Response Headers:
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'
```

---

## Caching

### Cache Headers

**Check**:
- [ ] Cache-Control headers set?
- [ ] ETags used for conditional requests?
- [ ] Last-Modified headers included?
- [ ] Cache invalidation considered?

```typescript
// ✅ GOOD: Caching headers
GET /users/123
Response Headers:
  Cache-Control: private, max-age=300
  ETag: "686897696a7c876b7e"
  Last-Modified: Tue, 15 Jan 2024 10:30:00 GMT

// Conditional request
GET /users/123
Headers:
  If-None-Match: "686897696a7c876b7e"

// Response
304 Not Modified  // Data hasn't changed
```

---

## API Performance

### Response Size

**Check**:
- [ ] Field selection supported (sparse fieldsets)?
- [ ] No over-fetching?
- [ ] Compression enabled?
- [ ] Large responses paginated?

```typescript
// ✅ GOOD: Field selection
GET /users/123?fields=id,name,email
{
  "id": 123,
  "name": "John",
  "email": "john@example.com"
  // Not including 50 other fields
}

// ✅ GOOD: Compression
Response Headers:
  Content-Encoding: gzip
```
