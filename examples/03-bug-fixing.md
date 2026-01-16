# Bug Fixing Examples

Use Claude Task Master to debug and fix issues in your codebase.

## Example 1: Simple Bug Fix

### Scenario
Users report that the login form doesn't validate email format.

### Command
```bash
claudetm start "Fix email validation in login form - ensure valid email format is required"
```

### Claude's Approach
1. Locates login form validation code
2. Identifies missing email regex validation
3. Adds proper validation
4. Updates tests to verify email validation
5. Tests both valid and invalid emails
6. Creates PR

### Time to Complete
1-2 sessions (under 2 minutes)

## Example 2: Exception Handling

### Scenario
Application crashes when API request times out.

### Command
```bash
claudetm start "Fix timeout crash in API client - add proper exception handling for timeout errors and retry logic with exponential backoff"
```

### Implementation
```python
# Before
response = requests.get(url)
return response.json()

# After
import time
from requests.exceptions import Timeout

def make_request(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            return response.json()
        except Timeout:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### What Gets Added
- Exception handling
- Retry logic
- Logging
- Tests for timeout scenarios
- Configuration for timeout duration

## Example 3: Race Condition

### Scenario
Occasional duplicate records created in database.

### Command
```bash
claudetm start "Fix race condition in user registration - ensure email uniqueness check is atomic using database constraints and proper locking"
```

### Claude's Analysis
1. Reads user registration code
2. Identifies check-then-insert pattern
3. Adds database unique constraint
4. Implements proper transaction handling
5. Adds concurrent test cases

### Solution
```python
# Before
if User.query.filter_by(email=email).first():
    raise ValueError("Email exists")
user = User(email=email)
db.session.add(user)
db.session.commit()

# After
from sqlalchemy.exc import IntegrityError

try:
    user = User(email=email)
    db.session.add(user)
    db.session.commit()
except IntegrityError:
    db.session.rollback()
    raise ValueError("Email already registered")

# Migration adds:
# CREATE UNIQUE INDEX idx_users_email ON users(email);
```

## Example 4: Memory Leak

### Scenario
Application memory grows over time and crashes.

### Command
```bash
claudetm start "Fix memory leak in image processing - ensure temporary files are cleaned up and PIL images are properly closed" --model opus
```

### Why Opus?
Memory leaks require deeper analysis and understanding of resource management.

### Fix Applied
```python
# Before
def process_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((800, 800))
    img.save("/tmp/processed.jpg")
    return "/tmp/processed.jpg"

# After
import tempfile
from contextlib import contextmanager

@contextmanager
def open_image(file_path):
    img = Image.open(file_path)
    try:
        yield img
    finally:
        img.close()

def process_image(file_path):
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        with open_image(file_path) as img:
            img.thumbnail((800, 800))
            img.save(tmp.name)
        return tmp.name
```

## Example 5: Performance Bug

### Scenario
User dashboard loads very slowly (5+ seconds).

### Command
```bash
claudetm start "Fix slow dashboard load time - optimize database queries, add pagination for activity feed, and implement caching"
```

### Optimization Steps
1. **Profile Current Performance**:
   - Adds query logging
   - Identifies N+1 queries
   - Measures load time

2. **Apply Fixes**:
   - Adds select_related/prefetch_related
   - Implements pagination
   - Adds Redis caching
   - Creates indexes

3. **Verify Improvement**:
   - Benchmarks before/after
   - Adds performance tests
   - Documents improvements

### Results
```
Before:
- 45 database queries
- 5.2s page load
- No caching

After:
- 8 database queries  (82% reduction)
- 0.6s page load     (88% faster)
- 92% cache hit rate
```

## Example 6: Security Vulnerability

### Scenario
Security audit found SQL injection vulnerability.

### Command
```bash
claudetm start "Fix SQL injection in search endpoint - use parameterized queries instead of string concatenation" --no-auto-merge
```

### Why No Auto-Merge?
Security fixes should be manually reviewed before merging.

### Before
```python
@app.route("/search")
def search():
    query = request.args.get("q")
    sql = f"SELECT * FROM products WHERE name LIKE '%{query}%'"
    results = db.execute(sql)
    return jsonify(results)
```

### After
```python
@app.route("/search")
def search():
    query = request.args.get("q")
    # Parameterized query prevents SQL injection
    sql = "SELECT * FROM products WHERE name LIKE :pattern"
    results = db.execute(sql, {"pattern": f"%{query}%"})
    return jsonify(results)
```

### Additional Changes
- Security test cases
- Input validation
- Rate limiting
- Audit logging

## Example 7: Cross-Browser Compatibility

### Scenario
Feature works in Chrome but breaks in Safari.

### Command
```bash
claudetm start "Fix date picker not working in Safari - replace browser-specific date input with cross-browser library like flatpickr"
```

### Implementation
1. Identifies Safari-specific issue
2. Evaluates solutions (Flatpickr, react-datepicker, etc.)
3. Implements cross-browser solution
4. Adds browser compatibility tests
5. Updates documentation

## Example 8: Flaky Test

### Scenario
Test passes sometimes, fails other times.

### Command
```bash
claudetm start "Fix flaky test in test_user_registration - test fails intermittently due to timing issues with async operations"
```

### Root Cause Analysis
```python
# Before - Race condition
def test_user_registration():
    response = client.post("/register", json=data)
    user = User.query.filter_by(email=data["email"]).first()
    assert user is not None  # Fails intermittently!
```

### Fix
```python
# After - Proper async handling
import pytest

def test_user_registration():
    response = client.post("/register", json=data)
    assert response.status_code == 201

    # Wait for async user creation
    user = None
    for _ in range(10):
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            break
        time.sleep(0.1)

    assert user is not None
```

Or better:
```python
# Best - Test the response, not side effects
def test_user_registration():
    response = client.post("/register", json=data)
    assert response.status_code == 201
    assert response.json()["email"] == data["email"]
```

## Example 9: Integration Bug

### Scenario
Payment webhook handler fails on specific edge cases.

### Command
```bash
claudetm start "Fix Stripe webhook handler - handle subscription_updated event and process partial refunds correctly"
```

### What Claude Does
1. Reviews Stripe webhook documentation
2. Analyzes existing handler code
3. Identifies missing event types
4. Adds handling for edge cases
5. Creates test fixtures from Stripe examples
6. Tests all webhook event types

## Example 10: Data Corruption

### Scenario
User reports seeing another user's data.

### Command
```bash
claudetm start "URGENT: Fix data leakage in user profile endpoint - ensure query filters by authenticated user ID" --model opus --no-auto-merge
```

### Critical Bug Workflow
1. Uses opus for thorough analysis
2. No auto-merge for security review
3. Adds comprehensive audit logging
4. Creates data integrity tests

### Fix
```python
# Before - Vulnerable
@login_required
def get_profile(profile_id):
    profile = Profile.query.get(profile_id)  # No auth check!
    return jsonify(profile.to_dict())

# After - Secure
@login_required
def get_profile(profile_id):
    profile = Profile.query.filter_by(
        id=profile_id,
        user_id=current_user.id  # Ensure ownership
    ).first_or_404()
    return jsonify(profile.to_dict())
```

## Bug Fixing Best Practices

### 1. Provide Context
❌ Bad: `"Fix the bug in api.py"`
✅ Good: `"Fix timeout in API client when upstream service is slow - add retry logic and proper error messages"`

### 2. Include Reproduction Steps
```bash
claudetm start "Fix 500 error when user submits form with empty email field - reproduce by POST to /register with email=''"
```

### 3. Mention Error Messages
```bash
claudetm start "Fix 'AttributeError: NoneType has no attribute split' in parse_date function when date string is None"
```

### 4. Specify Scope
```bash
claudetm start "Fix email validation in login form ONLY - do not modify registration or password reset forms"
```

### 5. For Security Issues
```bash
claudetm start "Fix XSS vulnerability in comment rendering" --no-auto-merge --model opus
```

## Debugging Workflow

### 1. Reproduce Bug
```bash
# Provide reproduction steps in goal
claudetm start "Fix TypeError in calculate_total when cart has promotional items - occurs when item.discount is None"
```

### 2. Monitor Fix Process
```bash
# Watch Claude investigate
claudetm logs -n 100

# Check what files are being modified
watch -n 5 git status
```

### 3. Review Fix
```bash
# After PR created
gh pr view
gh pr diff

# Check test coverage
pytest --cov=src tests/
```

### 4. Verify Fix
```bash
# After merge, verify in development
git pull
# Test the scenario that was broken
```

## Common Patterns

### Exception Handling
```bash
claudetm start "Add try-catch for JSONDecodeError in parse_response and return meaningful error message"
```

### Input Validation
```bash
claudetm start "Add validation for user_id parameter - ensure it's a positive integer and belongs to authenticated user"
```

### Resource Cleanup
```bash
claudetm start "Ensure database connections are properly closed in finally block of query_executor"
```

### Edge Cases
```bash
claudetm start "Handle edge case where user has no orders - return empty array instead of null in get_order_history"
```

## Troubleshooting

### Can't Reproduce Bug
```bash
# Provide more context
claudetm start "Fix pagination bug - occurs ONLY when total items equals page size (e.g., exactly 20 items with page_size=20)"
```

### Multiple Related Bugs
```bash
# Fix separately for cleaner PRs
claudetm start "Fix email validation in login form"
# After completion
claudetm start "Fix email validation in registration form"
```

### Bug in Dependencies
```bash
claudetm start "Work around bug in library-x version 2.1 - use alternative approach or pin to version 2.0 until upstream fix is released"
```

## Next Steps

- [Testing](./05-testing.md) - Add tests to prevent regressions
- [Refactoring](./04-refactoring.md) - Improve code quality
- [CI/CD Integration](./07-cicd.md) - Automate bug detection
