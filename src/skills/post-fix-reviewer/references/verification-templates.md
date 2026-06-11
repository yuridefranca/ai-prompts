# Verification Templates

## Bug Fix Verification Template

```markdown
## Bug Fix Verification

**Original Issue**: [Description]

**Reproduction Steps**:
1. [Step]
2. [Step]

**Result**:
- ✅ Bug no longer occurs
- ✅ Expected behavior observed
- ✅ No error messages

**Evidence**: [Screenshot/log/test output]
```

## Test Results Template

```markdown
## Test Results

**Unit Tests**: ✅ 152/152 passing
**Integration Tests**: ✅ 43/43 passing
**E2E Tests**: ✅ 12/12 passing

**Coverage**:
- Before: 87.3%
- After: 88.1%
- Delta: +0.8%

**New Tests Added**: 5
- bug-reproduction.spec.ts
- edge-cases.spec.ts (3 tests)
- regression.spec.ts
```

## Edge Case Validation Template

```markdown
## Edge Case Validation

### EDGE-1: Null Input
- **Test**: Pass null to function
- **Expected**: Return empty string
- **Actual**: ✅ Returns empty string
- **Test**: `edge-cases.spec.ts:12`

### EDGE-2: Empty Array
- **Test**: Pass [] to function
- **Expected**: Return [] without error
- **Actual**: ✅ Returns []
- **Test**: `edge-cases.spec.ts:18`

### EDGE-3: Concurrent Requests
- **Test**: Send 10 simultaneous requests
- **Expected**: All succeed, no race conditions
- **Actual**: ✅ All succeed
- **Test**: `concurrency.spec.ts:25`
```

## Regression Checks Template

```markdown
## Regression Checks

### Feature 1: User Login
- **Status**: ✅ Works normally
- **Tested**: Login flow, session creation

### Feature 2: Password Reset
- **Status**: ✅ Works normally
- **Tested**: Email sending, token validation

### Feature 3: Profile Update
- **Status**: ✅ Works normally
- **Tested**: Form submission, validation
```

## Performance Validation Template

```markdown
## Performance Validation

**PERF-1**: N+1 Query Issue
- **Before**: 50 queries per request
- **After**: 2 queries per request
- **Status**: ✅ Fixed

**Response Time**:
- **Before**: 450ms average
- **After**: 85ms average
- **Target**: <100ms
- **Status**: ✅ Meets target
```

## Security Validation Template

```markdown
## Security Validation

**SEC-1**: SQL Injection
- **Attack**: `'; DROP TABLE users--`
- **Result**: ✅ Parameterized query prevents injection
- **Test**: `security.spec.ts:10`

**SEC-2**: XSS
- **Attack**: `<script>alert('xss')</script>`
- **Result**: ✅ Input sanitized
- **Test**: `security.spec.ts:20`
```

## Code Quality Notes Template

```markdown
## Code Quality Notes

**✅ Good**:
- Clean variable names
- Proper error handling
- Good test coverage

**⚠️ Minor Concerns**:
- Function could be split (lines 45-80)
- Magic number on line 67 (should be constant)

**🛑 Must Fix**:
- [None]
```

## Documentation Check Template

```markdown
## Documentation Check

- ✅ Code comments added (lines 45, 67)
- ✅ Commit message follows format
- ✅ AGENTS.md updated (if schema changed)
- ✅ CHANGELOG.md entry added
- ❌ API docs (not needed for internal fix)
```
