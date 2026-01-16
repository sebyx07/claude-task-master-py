# Code Refactoring Examples

Improve code quality, structure, and maintainability using Claude Task Master.

## Example 1: Extract Function

### Scenario
Long function with multiple responsibilities.

### Command
```bash
claudetm start "Refactor process_order function - extract payment processing, inventory update, and notification logic into separate functions"
```

### Before
```python
def process_order(order_id):
    order = Order.query.get(order_id)
    # 50 lines of payment processing...
    # 30 lines of inventory updates...
    # 20 lines of notification sending...
    return order
```

### After
```python
def process_order(order_id):
    order = Order.query.get(order_id)
    process_payment(order)
    update_inventory(order)
    send_notifications(order)
    return order

def process_payment(order):
    # Payment logic isolated
    ...

def update_inventory(order):
    # Inventory logic isolated
    ...

def send_notifications(order):
    # Notification logic isolated
    ...
```

### Benefits
- Each function has single responsibility
- Easier to test
- Reusable components
- Clearer code flow

## Example 2: Introduce Design Pattern

### Scenario
Multiple if/elif chains for different object types.

### Command
```bash
claudetm start "Refactor file processor to use Strategy pattern - replace if/elif chains with processor classes for each file type"
```

### Before
```python
def process_file(file_path):
    if file_path.endswith('.csv'):
        # CSV processing logic
        ...
    elif file_path.endswith('.json'):
        # JSON processing logic
        ...
    elif file_path.endswith('.xml'):
        # XML processing logic
        ...
```

### After
```python
from abc import ABC, abstractmethod

class FileProcessor(ABC):
    @abstractmethod
    def process(self, file_path):
        pass

class CSVProcessor(FileProcessor):
    def process(self, file_path):
        # CSV logic
        ...

class JSONProcessor(FileProcessor):
    def process(self, file_path):
        # JSON logic
        ...

class XMLProcessor(FileProcessor):
    def process(self, file_path):
        # XML logic
        ...

PROCESSORS = {
    '.csv': CSVProcessor(),
    '.json': JSONProcessor(),
    '.xml': XMLProcessor(),
}

def process_file(file_path):
    ext = Path(file_path).suffix
    processor = PROCESSORS.get(ext)
    if not processor:
        raise ValueError(f"Unsupported file type: {ext}")
    return processor.process(file_path)
```

## Example 3: Remove Code Duplication

### Scenario
Similar code repeated across multiple functions.

### Command
```bash
claudetm start "Remove duplication in user CRUD operations - extract common validation and database logic into base functions"
```

### Before
```python
def create_user(data):
    # Validate email
    if not re.match(EMAIL_REGEX, data['email']):
        raise ValueError("Invalid email")
    # Validate password
    if len(data['password']) < 8:
        raise ValueError("Password too short")
    # Create user
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id, data):
    # Validate email (duplicated!)
    if not re.match(EMAIL_REGEX, data['email']):
        raise ValueError("Invalid email")
    # Validate password (duplicated!)
    if 'password' in data and len(data['password']) < 8:
        raise ValueError("Password too short")
    # Update user
    user = User.query.get(user_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user
```

### After
```python
def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValueError("Invalid email")

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password too short")

def validate_user_data(data, is_update=False):
    if 'email' in data:
        validate_email(data['email'])
    if 'password' in data or not is_update:
        validate_password(data.get('password', ''))

def create_user(data):
    validate_user_data(data)
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user

def update_user(user_id, data):
    validate_user_data(data, is_update=True)
    user = User.query.get(user_id)
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user
```

## Example 4: Improve Naming

### Scenario
Unclear variable and function names.

### Command
```bash
claudetm start "Improve naming in api/utils.py - rename functions and variables to be more descriptive and follow Python conventions"
```

### Before
```python
def proc(d):
    r = []
    for x in d:
        if x['t'] == 'a':
            r.append(x)
    return r
```

### After
```python
def filter_active_users(users):
    active_users = []
    for user in users:
        if user['status'] == 'active':
            active_users.append(user)
    return active_users

# Or more Pythonic:
def filter_active_users(users):
    return [user for user in users if user['status'] == 'active']
```

## Example 5: Modernize Code

### Scenario
Old Python 2 style code needs updating.

### Command
```bash
claudetm start "Modernize user_service.py to Python 3.10+ - use type hints, dataclasses, pathlib, and f-strings"
```

### Before
```python
def get_user_info(user_id):
    user = db.get_user(user_id)
    return {
        'name': user.name,
        'email': user.email,
        'age': user.age,
    }

def format_greeting(name):
    return "Hello, %s!" % name
```

### After
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class UserInfo:
    name: str
    email: str
    age: int

def get_user_info(user_id: int) -> Optional[UserInfo]:
    user = db.get_user(user_id)
    if not user:
        return None
    return UserInfo(
        name=user.name,
        email=user.email,
        age=user.age,
    )

def format_greeting(name: str) -> str:
    return f"Hello, {name}!"
```

## Example 6: Split Large File

### Scenario
Single file has grown to 2000+ lines.

### Command
```bash
claudetm start "Split api/views.py into separate modules - group by resource type (users, orders, products) and move to api/views/ directory"
```

### Before
```
api/
└── views.py  (2000 lines)
```

### After
```
api/
└── views/
    ├── __init__.py
    ├── users.py      (400 lines)
    ├── orders.py     (600 lines)
    ├── products.py   (500 lines)
    └── common.py     (300 lines)
```

## Example 7: Async/Await Migration

### Scenario
Blocking I/O operations need to be async.

### Command
```bash
claudetm start "Convert API client to async/await - use aiohttp instead of requests and make all HTTP calls non-blocking"
```

### Before
```python
import requests

class APIClient:
    def get_user(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        return response.json()

    def get_orders(self, user_id):
        response = requests.get(f"{self.base_url}/orders?user={user_id}")
        return response.json()
```

### After
```python
import aiohttp
from typing import Dict, List

class APIClient:
    async def get_user(self, user_id: int) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/users/{user_id}") as response:
                return await response.json()

    async def get_orders(self, user_id: int) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/orders?user={user_id}") as response:
                return await response.json()

    async def get_user_with_orders(self, user_id: int) -> Dict:
        # Now we can parallelize!
        user, orders = await asyncio.gather(
            self.get_user(user_id),
            self.get_orders(user_id),
        )
        return {**user, 'orders': orders}
```

## Example 8: Database Query Optimization

### Scenario
N+1 query problem in ORM usage.

### Command
```bash
claudetm start "Fix N+1 queries in get_users_with_orders - use select_related and prefetch_related to load data efficiently"
```

### Before (Django)
```python
def get_users_with_orders():
    users = User.objects.all()
    result = []
    for user in users:
        result.append({
            'user': user,
            'orders': user.orders.all(),  # N+1 query!
            'profile': user.profile,       # N+1 query!
        })
    return result
```

### After
```python
def get_users_with_orders():
    users = User.objects.select_related('profile').prefetch_related('orders')
    return [
        {
            'user': user,
            'orders': user.orders.all(),  # No extra query!
            'profile': user.profile,       # No extra query!
        }
        for user in users
    ]
```

## Example 9: Error Handling Refactor

### Scenario
Inconsistent error handling across codebase.

### Command
```bash
claudetm start "Standardize error handling - create custom exception classes and unified error response format for all API endpoints"
```

### Before
```python
@app.route('/api/users/<id>')
def get_user(id):
    try:
        user = User.query.get(id)
        if not user:
            return {"error": "not found"}, 404
        return user.to_dict()
    except Exception as e:
        return {"error": str(e)}, 500
```

### After
```python
# exceptions.py
class APIException(Exception):
    status_code = 500
    message = "Internal server error"

    def __init__(self, message=None, status_code=None):
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

class NotFoundException(APIException):
    status_code = 404
    message = "Resource not found"

class ValidationException(APIException):
    status_code = 400
    message = "Invalid input"

# error_handler.py
@app.errorhandler(APIException)
def handle_api_exception(error):
    return {
        "error": {
            "message": error.message,
            "status_code": error.status_code,
        }
    }, error.status_code

# views.py
@app.route('/api/users/<id>')
def get_user(id):
    user = User.query.get(id)
    if not user:
        raise NotFoundException(f"User {id} not found")
    return user.to_dict()
```

## Example 10: Test Refactoring

### Scenario
Tests are slow and have lots of duplication.

### Command
```bash
claudetm start "Refactor test suite - use fixtures for common setup, parametrize similar tests, and add factory pattern for test data"
```

### Before
```python
def test_create_user():
    user = User(name="John", email="john@example.com", age=30)
    db.session.add(user)
    db.session.commit()
    assert user.id is not None

def test_update_user():
    user = User(name="Jane", email="jane@example.com", age=25)
    db.session.add(user)
    db.session.commit()
    user.name = "Jane Doe"
    db.session.commit()
    assert user.name == "Jane Doe"
```

### After
```python
import pytest
from factory import Factory, Faker

class UserFactory(Factory):
    class Meta:
        model = User

    name = Faker('name')
    email = Faker('email')
    age = Faker('pyint', min_value=18, max_value=100)

@pytest.fixture
def user(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    return user

def test_create_user(db_session):
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    assert user.id is not None

def test_update_user(user, db_session):
    user.name = "Jane Doe"
    db_session.commit()
    assert user.name == "Jane Doe"

@pytest.mark.parametrize("age,expected", [
    (17, False),
    (18, True),
    (50, True),
])
def test_is_adult(age, expected):
    user = UserFactory(age=age)
    assert user.is_adult() == expected
```

## Refactoring Best Practices

### 1. Keep It Focused
❌ Bad: `"Refactor the entire application"`
✅ Good: `"Refactor authentication module - extract validation logic and use dependency injection"`

### 2. Preserve Behavior
```bash
claudetm start "Refactor calculate_discount function to be more readable - ensure all existing tests still pass"
```

### 3. One Pattern at a Time
```bash
# Do separately
claudetm start "Add type hints to user_service.py"
# Then
claudetm start "Extract user validation into separate validator class"
```

### 4. Specify Testing Requirements
```bash
claudetm start "Refactor payment processing - ensure all existing tests pass and add new tests for extracted functions"
```

### 5. Mention Performance
```bash
claudetm start "Refactor data processing pipeline to use generators instead of lists - reduce memory usage for large datasets"
```

## Safe Refactoring Checklist

Before refactoring:
- [ ] All tests pass
- [ ] Code is committed
- [ ] Branch is up to date

During refactoring (Claude handles):
- [ ] Tests still pass after each change
- [ ] Behavior is preserved
- [ ] Code coverage maintained or improved
- [ ] Linting passes

After refactoring:
- [ ] Review the diff carefully
- [ ] Run full test suite
- [ ] Check performance if relevant
- [ ] Update documentation

## Common Refactoring Patterns

### Extract Method
```bash
claudetm start "Extract method - split complex_calculation into smaller functions with single responsibilities"
```

### Rename
```bash
claudetm start "Rename getData to fetch_user_profile across entire codebase for clarity"
```

### Move Method
```bash
claudetm start "Move email sending logic from User model to separate EmailService class"
```

### Replace Conditional with Polymorphism
```bash
claudetm start "Replace type checking conditionals with polymorphic classes for different payment methods"
```

### Introduce Parameter Object
```bash
claudetm start "Replace multiple parameters in create_user with UserData dataclass"
```

## Monitoring Refactoring Progress

```bash
# Check what's being changed
git diff

# Ensure tests still pass
pytest

# Check code quality
ruff check .
mypy .

# View refactoring plan
claudetm plan
```

## Troubleshooting

### Tests Failing After Refactor
Claude will:
1. Identify failing tests
2. Update tests to match new structure
3. Ensure behavior is preserved

### Too Many Changes at Once
```bash
# Interrupt if scope is too large
^C

# Review and possibly split
claudetm clean -f
claudetm start "Refactor auth module - part 1: extract validation only"
```

## Next Steps

- [Testing](./05-testing.md) - Improve test coverage
- [Documentation](./06-documentation.md) - Update docs after refactoring
- [Advanced Workflows](./08-advanced-workflows.md) - Complex scenarios
