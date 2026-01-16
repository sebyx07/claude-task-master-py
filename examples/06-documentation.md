# Documentation Examples

Generate and maintain documentation using Claude Task Master.

## Example 1: Add Docstrings

### Command
```bash
claudetm start "Add comprehensive docstrings to all functions in api/users.py following Google style guide"
```

### Before
```python
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        raise NotFoundException()
    return user
```

### After
```python
def get_user(user_id: int) -> User:
    """Retrieve a user by their ID.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        User object containing user data.

    Raises:
        NotFoundException: If user with given ID doesn't exist.

    Example:
        >>> user = get_user(123)
        >>> print(user.email)
        'john@example.com'
    """
    user = User.query.get(user_id)
    if not user:
        raise NotFoundException(f"User {user_id} not found")
    return user
```

## Example 2: API Documentation

### Command
```bash
claudetm start "Generate OpenAPI/Swagger documentation for all REST endpoints in api/ directory"
```

### Generated Documentation
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
  description: API for user management

paths:
  /api/users/{userId}:
    get:
      summary: Get user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: User found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          description: User not found
```

## Example 3: README Updates

### Command
```bash
claudetm start "Update README.md to include new authentication system - add setup instructions, configuration options, and usage examples"
```

### Generated Sections
```markdown
## Authentication

### Setup

1. Install dependencies:
   ```bash
   pip install pyjwt cryptography
   ```

2. Configure environment variables:
   ```bash
   export JWT_SECRET_KEY="your-secret-key"
   export JWT_EXPIRATION_HOURS=24
   ```

### Usage

#### Login
```python
from auth import login

token = login(email="user@example.com", password="secret")
print(f"Token: {token}")
```

#### Protected Routes
```python
from auth import require_auth

@app.route('/protected')
@require_auth
def protected_route():
    return {"message": "Authenticated!"}
```
```

## Example 4: Inline Comments

### Command
```bash
claudetm start "Add explanatory comments to complex algorithm in utils/sorting.py"
```

### Before
```python
def quicksort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort(arr, low, pi - 1)
        quicksort(arr, high + 1, high)
```

### After
```python
def quicksort(arr, low, high):
    """Sort array using quicksort algorithm.

    Time complexity: O(n log n) average, O(n²) worst case
    Space complexity: O(log n) for recursion stack
    """
    # Base case: array with 0 or 1 element is already sorted
    if low < high:
        # Partition array and get pivot index
        # Elements < pivot are on left, elements > pivot are on right
        pi = partition(arr, low, high)

        # Recursively sort left partition (elements before pivot)
        quicksort(arr, low, pi - 1)

        # Recursively sort right partition (elements after pivot)
        quicksort(arr, low, pi + 1, high)
```

## Example 5: Architecture Documentation

### Command
```bash
claudetm start "Create ARCHITECTURE.md documenting system design, component relationships, and data flow"
```

### Generated File
```markdown
# Architecture

## Overview
This application follows a layered architecture pattern with clear separation of concerns.

## Layers

### 1. Presentation Layer (API)
- **Location**: `api/`
- **Responsibility**: HTTP request/response handling
- **Components**:
  - Route handlers
  - Request validation
  - Response formatting

### 2. Business Logic Layer (Services)
- **Location**: `services/`
- **Responsibility**: Core business logic
- **Components**:
  - User service
  - Order service
  - Payment service

### 3. Data Access Layer (Models)
- **Location**: `models/`
- **Responsibility**: Database interaction
- **Components**:
  - ORM models
  - Query builders
  - Migrations

## Data Flow

```
Client Request
    ↓
API Handler (validates request)
    ↓
Service Layer (business logic)
    ↓
Model Layer (database query)
    ↓
Database
    ↓
Response (formatted and returned to client)
```

## Component Relationships

- API depends on Services
- Services depend on Models
- Models depend on Database
- No circular dependencies
```

## Example 6: Tutorial/Guide

### Command
```bash
claudetm start "Create TUTORIAL.md with step-by-step guide for building a todo app using our framework"
```

### Generated Tutorial
```markdown
# Building a Todo App

This tutorial walks you through creating a todo application from scratch.

## Prerequisites
- Python 3.10+
- PostgreSQL running locally

## Step 1: Project Setup

Create a new project:
```bash
mkdir todo-app
cd todo-app
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Define the Model

Create `models/todo.py`:
```python
from db import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    completed = Column(Boolean, default=False)
```

[... continues with full tutorial ...]
```

## Example 7: Changelog

### Command
```bash
claudetm start "Update CHANGELOG.md with all changes from the last release to current HEAD"
```

### Generated Changelog
```markdown
# Changelog

## [1.2.0] - 2024-01-15

### Added
- JWT authentication system with token refresh
- User profile avatar upload
- Email verification flow
- Rate limiting on API endpoints

### Changed
- Updated password hashing to bcrypt
- Improved error messages for validation failures
- Database migration to add email_verified field

### Fixed
- Race condition in user registration
- Memory leak in image processing
- CORS headers for OPTIONS requests

### Security
- Fixed SQL injection vulnerability in search endpoint
- Added input sanitization for user-generated content
```

## Example 8: Code Examples

### Command
```bash
claudetm start "Add usage examples to docstrings in services/payment.py"
```

### Generated Documentation
```python
class PaymentService:
    """Service for processing payments.

    Examples:
        Basic payment processing:
        >>> service = PaymentService()
        >>> result = service.charge(amount=1000, currency='usd')
        >>> print(result['status'])
        'succeeded'

        Handling payment errors:
        >>> try:
        ...     service.charge(amount=1000, currency='usd')
        ... except PaymentError as e:
        ...     print(f"Payment failed: {e}")

        Refunding a payment:
        >>> refund = service.refund(payment_id='pi_123', amount=500)
        >>> print(refund['status'])
        'succeeded'
    """
```

## Example 9: Contributing Guide

### Command
```bash
claudetm start "Create CONTRIBUTING.md with guidelines for code style, testing, and PR process"
```

### Generated Guide
```markdown
# Contributing Guide

## Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use black for formatting

## Testing

All PRs must include tests:
```bash
# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=term-missing
```

Minimum coverage: 80%

## Pull Request Process

1. Create a feature branch
   ```bash
   git checkout -b feature/my-feature
   ```

2. Make your changes with clear commits
   ```bash
   git commit -m "feat: Add user authentication"
   ```

3. Push and create PR
   ```bash
   git push origin feature/my-feature
   gh pr create
   ```

4. Wait for CI checks
5. Address review comments
6. PR will be merged by maintainers
```

## Example 10: Type Annotations

### Command
```bash
claudetm start "Add type annotations to all functions in api/ directory following PEP 484"
```

### Before
```python
def create_user(data):
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user
```

### After
```python
from typing import Dict, Any
from models import User

def create_user(data: Dict[str, Any]) -> User:
    """Create a new user.

    Args:
        data: Dictionary containing user fields (name, email, password).

    Returns:
        Created User instance.

    Raises:
        ValidationError: If data is invalid.
    """
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user
```

## Documentation Best Practices

### 1. Be Specific About Style
```bash
claudetm start "Add docstrings following Google style guide with examples"
claudetm start "Add JSDoc comments to all functions in src/"
```

### 2. Target Specific Audience
```bash
claudetm start "Create beginner-friendly tutorial for setting up development environment"
claudetm start "Add API reference for advanced users with all configuration options"
```

### 3. Include Examples
```bash
claudetm start "Add code examples to README showing common use cases"
```

### 4. Keep It Updated
```bash
claudetm start "Update documentation to reflect changes in authentication system"
```

## Common Documentation Commands

### Generate API Docs
```bash
claudetm start "Generate Sphinx documentation from docstrings"
```

### Update README
```bash
claudetm start "Update README with new installation instructions and configuration options"
```

### Add Migration Guides
```bash
claudetm start "Create MIGRATION.md for upgrading from v1 to v2"
```

### Document Configuration
```bash
claudetm start "Document all environment variables in .env.example with descriptions and default values"
```

## Next Steps

- [CI/CD Integration](./07-cicd.md) - Automate documentation builds
- [Advanced Workflows](./08-advanced-workflows.md) - Complex documentation scenarios
