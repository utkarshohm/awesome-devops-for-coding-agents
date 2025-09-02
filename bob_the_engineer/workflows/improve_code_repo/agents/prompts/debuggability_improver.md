# Debuggability Improver Agent

## Objective
Enhance error handling, logging, and test feedback throughout the codebase to make debugging easier for coding agents and developers.

## Context
Coding agents struggle when errors are vague, logging is insufficient, or test failures don't provide clear guidance. This agent improves these aspects to enable more autonomous debugging and problem-solving.

## Process

### Phase 1: Analysis

#### 1.1 Analyze Error Handling Patterns
```bash
bob-the-engineer analyze-error-handling --repo-path .
```

Scan codebase for patterns in:
- Try-catch blocks
- Error throwing
- Error messages
- Stack trace handling
- Error propagation
- Recovery strategies

#### 1.2 Check Logging Coverage
```bash
bob-the-engineer check-logging-coverage --verbosity info
```

Evaluate logging:
- Entry/exit points
- Error logging
- Warning conditions
- Debug information
- Correlation IDs
- Structured vs unstructured

#### 1.3 Assess Test Quality
```bash
bob-the-engineer assess-test-quality --focus error-messages
```

Review tests for:
- Descriptive test names
- Clear assertion messages
- Helpful failure output
- Setup/teardown clarity
- Test organization

### Phase 2: Pattern Recognition

Identify good and bad patterns:

```markdown
# Debuggability Analysis Report

## Current State Assessment

### Error Handling Analysis

#### ❌ Bad Patterns Found (42 instances)

**Silent Exception Swallowing** (18 instances)
```javascript
// Found in: src/api/user.js:45
try {
  await saveUser(data);
} catch (e) {
  // Silent fail - AI can't debug this!
}
```

**Generic Error Messages** (15 instances)
```javascript
// Found in: src/utils/validation.js:23
if (!isValid) {
  throw new Error('Invalid input'); // What input? Why invalid?
}
```

**Lost Error Context** (9 instances)
```javascript
// Found in: src/services/payment.js:67
catch (error) {
  throw new Error('Payment failed'); // Original error lost
}
```

#### ✅ Good Patterns Found (23 instances)

**Contextual Error Messages**
```javascript
// Found in: src/auth/login.js:34
throw new Error(`Login failed for user ${email}: ${response.error}`);
```

**Preserved Stack Traces**
```javascript
// Found in: src/database/query.js:89
catch (error) {
  throw new DatabaseError('Query failed', { cause: error, query: sql });
}
```

### Logging Coverage Analysis

#### Current Coverage
- **Critical Paths**: 45% covered
- **Error Cases**: 67% logged
- **Entry/Exit**: 12% of functions
- **Structured Logging**: Not implemented

#### Missing Logging
- API endpoint entry/exit
- Database query execution
- External service calls
- Cache hits/misses
- Performance metrics

### Test Quality Analysis

#### Test Feedback Issues

**Cryptic Test Names** (89 tests)
```javascript
it('should work', () => { ... }); // What should work?
it('test 1', () => { ... }); // Meaningless name
```

**No Assertion Messages** (156 assertions)
```javascript
expect(result).toBe(true); // Why should it be true?
assert(user.id); // What are we asserting?
```

**Poor Failure Context** (67 tests)
```javascript
// When this fails, you get: "Expected true but got false"
expect(isValid(data)).toBe(true);
// Better would be: "Validation failed for: [data details]"
```

## Improvement Opportunities

### Priority 1: Critical Error Context
- 18 silent failures need error logging
- 15 generic messages need context
- 9 lost stack traces need preservation

### Priority 2: Logging Infrastructure
- Implement structured logging
- Add correlation IDs for request tracking
- Log all external service interactions

### Priority 3: Test Clarity
- Rename 89 tests with descriptive names
- Add messages to 156 assertions
- Improve failure output for 67 tests
```

### Phase 3: Generate Improvement Plan

Create a phased implementation plan:

```markdown
# Debuggability Improvement Plan

## Phase 1: Error Context Enhancement (Non-Breaking)

### Pattern 1: Add Context to Errors
```javascript
// Before
throw new Error('Invalid input');

// After
throw new Error(`Invalid input: ${field} must be ${requirement}, got ${value}`);
```

### Pattern 2: Preserve Original Errors
```javascript
// Before
catch (error) {
  throw new Error('Database error');
}

// After
catch (error) {
  throw new Error(`Database error: ${error.message}`, { cause: error });
}
```

### Pattern 3: Log Before Throwing
```javascript
// After
catch (error) {
  logger.error('Payment processing failed', {
    error: error.message,
    userId: user.id,
    amount: payment.amount,
    stack: error.stack
  });
  throw new PaymentError('Payment processing failed', { cause: error });
}
```

## Phase 2: Logging Infrastructure (Backwards Compatible)

### Add Structured Logging Library
```bash
npm install winston winston-transport
```

### Create Logging Utility
```javascript
// src/utils/logger.js
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.simple()
    })
  ]
});

// Add correlation ID middleware
logger.correlate = (req, res, next) => {
  req.correlationId = req.headers['x-correlation-id'] || uuid();
  logger.defaultMeta = { correlationId: req.correlationId };
  next();
};

module.exports = logger;
```

### Add Entry/Exit Logging
```javascript
// High-value functions to instrument
function processPayment(data) {
  logger.info('Processing payment', { amount: data.amount, method: data.method });

  try {
    const result = // ... processing logic
    logger.info('Payment processed successfully', { transactionId: result.id });
    return result;
  } catch (error) {
    logger.error('Payment processing failed', { error: error.message, data });
    throw error;
  }
}
```

## Phase 3: Test Enhancement (Test-Only Changes)

### Improve Test Names
```javascript
// Before
describe('User', () => {
  it('should work', () => {});
  it('test 1', () => {});
});

// After
describe('User', () => {
  it('should create a new user with valid email and password', () => {});
  it('should reject user creation when email already exists', () => {});
});
```

### Add Assertion Messages
```javascript
// Before
expect(result.status).toBe(200);
expect(user.email).toBeDefined();

// After
expect(result.status).toBe(200,
  `Expected successful response but got ${result.status}: ${result.error}`);
expect(user.email).toBeDefined(
  'User email should be set after registration');
```

### Enhance Test Helpers
```javascript
// Create custom matchers for better messages
expect.extend({
  toBeValidUser(received) {
    const pass = received.id && received.email && received.name;
    return {
      pass,
      message: () => pass
        ? `Expected user to be invalid but got valid user: ${JSON.stringify(received)}`
        : `Expected valid user but missing: ${
            !received.id ? 'id ' : ''
          }${!received.email ? 'email ' : ''}${!received.name ? 'name' : ''}`
    };
  }
});

// Usage
expect(user).toBeValidUser();
```
```

### Phase 4: Implementation

Execute improvements in order of impact:

#### 4.1 Quick Wins (Immediate Impact)
```bash
# Add context to error messages
bob-the-engineer enhance-error-context --pattern generic --add-context

# Add logging to error catches
bob-the-engineer add-error-logging --unlogged-catches

# Fix test names
bob-the-engineer improve-test-names --pattern cryptic
```

#### 4.2 Infrastructure Setup
```bash
# Install logging library
npm install winston winston-transport

# Create logger utility
bob-the-engineer create-logger --type structured

# Add correlation ID middleware
bob-the-engineer add-correlation-tracking
```

#### 4.3 Systematic Improvements
```bash
# Instrument critical paths
bob-the-engineer add-entry-exit-logging --critical-paths

# Enhance test assertions
bob-the-engineer add-assertion-messages --missing

# Add debug helpers
bob-the-engineer create-debug-utils
```

### Phase 5: Verification and Report

Verify improvements:

```bash
# Run tests with enhanced messages
npm test -- --verbose

# Check error handling
bob-the-engineer test-error-scenarios

# Validate logging output
bob-the-engineer analyze-log-output --sample
```

Generate final report:

```markdown
# Debuggability Improvements - Completion Report

## Implemented Enhancements

### ✅ Error Handling Improvements
- **Before**: 18 silent failures
- **After**: All failures logged with context
- **Example**:
  ```javascript
  // Before
  catch (e) { }

  // After
  catch (error) {
    logger.error('User save failed', {
      error: error.message,
      userId: user.id,
      operation: 'CREATE_USER'
    });
    throw new UserCreationError(`Failed to create user: ${error.message}`, { cause: error });
  }
  ```

### ✅ Logging Infrastructure
- **Implemented**: Winston with structured logging
- **Coverage**: 85% of critical paths
- **Features**:
  - Correlation IDs for request tracking
  - Error stack traces preserved
  - Performance metrics logged
  - External API calls tracked

### ✅ Test Clarity Improvements
- **Renamed**: 89 tests with descriptive names
- **Enhanced**: 156 assertions with failure messages
- **Added**: Custom matchers for domain objects

## Before/After Examples

### Error Debugging
**Before AI Experience**:
"Error: Invalid input"
- No context about which input
- No information about why it's invalid
- Stack trace points to error throw, not cause

**After AI Experience**:
"ValidationError: Invalid user email: 'notanemail' failed regex /^[^@]+@[^@]+$/"
- Clear what failed
- Shows actual vs expected
- Full stack trace with cause chain

### Test Failures
**Before**:
```
✗ should work
  Expected: true
  Received: false
```

**After**:
```
✗ should validate email format and reject invalid addresses
  Expected: Email 'not.an.email' to be rejected
  Received: Validation passed unexpectedly
  Debug: Regex pattern might be incorrect
```

### Log Output
**Before**:
```
Error occurred
Processing...
Done
```

**After**:
```json
{
  "timestamp": "2024-01-10T10:30:45Z",
  "level": "error",
  "message": "Payment processing failed",
  "correlationId": "abc-123-def",
  "userId": "user_456",
  "amount": 99.99,
  "error": "Gateway timeout after 30s",
  "stack": "Error: Gateway timeout..."
}
```

## Metrics

### Debugging Efficiency
- **Time to identify error cause**: Reduced by 65%
- **AI success rate in debugging**: Increased from 45% to 87%
- **False error reports**: Reduced by 80%

### Code Quality Metrics
- **Error handling coverage**: 95% (was 45%)
- **Logged error paths**: 100% (was 67%)
- **Test assertion clarity**: 92% (was 34%)

## New Debugging Utilities

### Debug Commands Available
```bash
# Trace error through system
bob-the-engineer trace-error --correlation-id abc-123

# Analyze log patterns
bob-the-engineer analyze-logs --timeframe 1h --level error

# Test error scenarios
bob-the-engineer test-error-handling --component user-service
```

### Helper Functions Added
```javascript
// Debug utility for development
const debug = require('./utils/debug');

// Detailed object inspection
debug.inspect(complexObject);

// Performance tracking
debug.time('operation-name');
// ... code ...
debug.timeEnd('operation-name');

// Conditional debug logging
debug.log('Detailed state:', { ...state });
```

## Best Practices Established

1. **Every error must include context**
2. **All external calls must be logged**
3. **Test names must describe behavior**
4. **Assertions must explain expectations**
5. **Stack traces must be preserved**

## Next Steps

1. Add monitoring dashboard for logs
2. Implement error tracking service
3. Create runbook for common errors
4. Add performance profiling
5. Set up alert thresholds
```

## Available Tools

```bash
# Analysis
bob-the-engineer analyze-error-handling --repo-path .
bob-the-engineer check-logging-coverage --verbosity [error|warn|info|debug]
bob-the-engineer assess-test-quality --focus error-messages

# Pattern Detection
bob-the-engineer find-silent-catches
bob-the-engineer find-generic-errors
bob-the-engineer find-missing-logs --critical-paths

# Implementation
bob-the-engineer enhance-error-context --pattern [generic|silent|lost]
bob-the-engineer add-error-logging --unlogged-catches
bob-the-engineer improve-test-names --pattern [cryptic|numbered|generic]
bob-the-engineer add-assertion-messages --missing

# Infrastructure
bob-the-engineer create-logger --type [structured|simple]
bob-the-engineer add-correlation-tracking
bob-the-engineer add-entry-exit-logging --critical-paths

# Verification
bob-the-engineer test-error-scenarios
bob-the-engineer analyze-log-output --sample
bob-the-engineer validate-test-clarity
```

## Success Criteria

✅ No silent error catches
✅ All errors include context
✅ Critical paths have entry/exit logging
✅ Test failures provide clear guidance
✅ Stack traces preserved throughout
✅ Correlation IDs for request tracking
✅ Structured logging implemented

## Important Guidelines

1. **Don't Break Working Code**: Enhancements only
2. **Preserve Performance**: Don't over-log
3. **Security First**: Don't log sensitive data
4. **Backward Compatible**: Existing logs still work
5. **Team Alignment**: Agree on logging standards
