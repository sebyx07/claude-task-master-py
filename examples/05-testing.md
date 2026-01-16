# Testing Examples

Add comprehensive test coverage to your codebase using Claude Task Master.

## Example 1: Add Unit Tests

### Scenario
Function has no tests.

### Command
```bash
claudetm start "Add unit tests for calculate_discount function in utils/pricing.py - test normal cases, edge cases, and error handling"
```

### Generated Tests
```python
import pytest
from utils.pricing import calculate_discount

class TestCalculateDiscount:
    def test_basic_discount(self):
        result = calculate_discount(price=100, discount_percent=10)
        assert result == 90.0

    def test_zero_discount(self):
        result = calculate_discount(price=100, discount_percent=0)
        assert result == 100.0

    def test_full_discount(self):
        result = calculate_discount(price=100, discount_percent=100)
        assert result == 0.0

    def test_negative_price_raises_error(self):
        with pytest.raises(ValueError, match="Price cannot be negative"):
            calculate_discount(price=-10, discount_percent=10)

    def test_invalid_discount_percent_raises_error(self):
        with pytest.raises(ValueError, match="Discount must be between 0 and 100"):
            calculate_discount(price=100, discount_percent=150)

    @pytest.mark.parametrize("price,discount,expected", [
        (100, 10, 90),
        (50, 20, 40),
        (75.50, 15, 64.175),
        (0, 10, 0),
    ])
    def test_various_discount_calculations(self, price, discount, expected):
        result = calculate_discount(price, discount)
        assert result == pytest.approx(expected)
```

## Example 2: Integration Tests

### Scenario
API endpoint needs integration testing.

### Command
```bash
claudetm start "Add integration tests for POST /api/users endpoint - test successful creation, validation errors, duplicate email, and database rollback on failure"
```

### Generated Tests
```python
import pytest
from app import create_app, db
from models import User

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

class TestUserCreation:
    def test_create_user_success(self, client):
        response = client.post('/api/users', json={
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'securepass123',
        })
        assert response.status_code == 201
        data = response.get_json()
        assert data['email'] == 'john@example.com'
        assert 'password' not in data  # Password should not be in response

    def test_create_user_missing_required_fields(self, client):
        response = client.post('/api/users', json={
            'name': 'John Doe',
        })
        assert response.status_code == 400
        data = response.get_json()
        assert 'email' in data['errors']
        assert 'password' in data['errors']

    def test_create_user_invalid_email(self, client):
        response = client.post('/api/users', json={
            'name': 'John Doe',
            'email': 'not-an-email',
            'password': 'securepass123',
        })
        assert response.status_code == 400
        assert 'email' in response.get_json()['errors']

    def test_create_user_duplicate_email(self, client):
        # Create first user
        client.post('/api/users', json={
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'pass123',
        })

        # Try to create duplicate
        response = client.post('/api/users', json={
            'name': 'Jane Doe',
            'email': 'john@example.com',
            'password': 'pass456',
        })
        assert response.status_code == 409
        assert 'already exists' in response.get_json()['error']
```

## Example 3: Add Test Coverage

### Scenario
Entire module lacks tests.

### Command
```bash
claudetm start "Add comprehensive test coverage for services/auth.py - aim for 90%+ coverage including all branches"
```

### Claude's Approach
1. Analyzes auth.py to understand all functions
2. Identifies edge cases and error paths
3. Creates fixtures for common test data
4. Writes tests for:
   - Happy paths
   - Error cases
   - Edge cases
   - Boundary conditions
5. Runs coverage report
6. Adds missing tests until target reached

### Coverage Report
```
Name                    Stmts   Miss  Cover
-------------------------------------------
services/auth.py          125      8    94%
tests/test_auth.py        245      0   100%
-------------------------------------------
TOTAL                     370      8    98%
```

## Example 4: Test Fixtures

### Scenario
Tests have repetitive setup code.

### Command
```bash
claudetm start "Create pytest fixtures for common test data in tests/conftest.py - include user factory, database session, and API client"
```

### Generated Fixtures
```python
# tests/conftest.py
import pytest
from app import create_app, db
from models import User
from factory import Factory, Faker

class UserFactory(Factory):
    class Meta:
        model = User

    name = Faker('name')
    email = Faker('email')
    password = 'testpass123'

@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app

@pytest.fixture(scope='function')
def db_session(app):
    """Create clean database for each test."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app, db_session):
    """Test client with database."""
    return app.test_client()

@pytest.fixture
def user(db_session):
    """Create a test user."""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def authenticated_client(client, user):
    """Client with authenticated session."""
    client.post('/login', json={
        'email': user.email,
        'password': 'testpass123',
    })
    return client
```

## Example 5: Mocking External Services

### Scenario
Code calls external API that shouldn't be hit in tests.

### Command
```bash
claudetm start "Add tests for payment service with mocked Stripe API - test successful payment, failed payment, and network errors"
```

### Generated Tests
```python
import pytest
from unittest.mock import Mock, patch
from services.payment import PaymentService
from stripe.error import CardError, APIConnectionError

@pytest.fixture
def payment_service():
    return PaymentService(api_key='test_key')

class TestPaymentService:
    @patch('stripe.PaymentIntent.create')
    def test_successful_payment(self, mock_create, payment_service):
        # Mock successful Stripe response
        mock_create.return_value = Mock(
            id='pi_123',
            status='succeeded',
            amount=1000,
        )

        result = payment_service.charge(amount=1000, currency='usd')

        assert result['status'] == 'succeeded'
        assert result['id'] == 'pi_123'
        mock_create.assert_called_once_with(
            amount=1000,
            currency='usd',
            automatic_payment_methods={'enabled': True},
        )

    @patch('stripe.PaymentIntent.create')
    def test_card_declined(self, mock_create, payment_service):
        # Mock card declined error
        mock_create.side_effect = CardError(
            message='Card declined',
            param='card',
            code='card_declined',
        )

        with pytest.raises(PaymentError) as exc_info:
            payment_service.charge(amount=1000, currency='usd')

        assert 'declined' in str(exc_info.value).lower()

    @patch('stripe.PaymentIntent.create')
    def test_network_error_retries(self, mock_create, payment_service):
        # Fail twice, succeed third time
        mock_create.side_effect = [
            APIConnectionError('Network error'),
            APIConnectionError('Network error'),
            Mock(id='pi_123', status='succeeded'),
        ]

        result = payment_service.charge(amount=1000, currency='usd')

        assert result['status'] == 'succeeded'
        assert mock_create.call_count == 3
```

## Example 6: End-to-End Tests

### Scenario
Need E2E tests for critical user flows.

### Command
```bash
claudetm start "Add E2E tests for user registration flow using Playwright - test complete signup, email verification, and first login"
```

### Generated Tests
```python
from playwright.sync_api import Page, expect

def test_complete_registration_flow(page: Page):
    # Visit signup page
    page.goto('http://localhost:3000/signup')

    # Fill registration form
    page.fill('#name', 'Test User')
    page.fill('#email', 'test@example.com')
    page.fill('#password', 'SecurePass123!')
    page.fill('#confirm-password', 'SecurePass123!')

    # Submit form
    page.click('button[type="submit"]')

    # Should redirect to verification page
    expect(page).to_have_url('http://localhost:3000/verify-email')
    expect(page.locator('.alert-success')).to_contain_text(
        'Please check your email'
    )

    # Get verification link from test email
    verification_link = get_test_email_verification_link('test@example.com')
    page.goto(verification_link)

    # Should be verified and logged in
    expect(page).to_have_url('http://localhost:3000/dashboard')
    expect(page.locator('.user-name')).to_contain_text('Test User')
```

## Example 7: Performance Tests

### Scenario
Need to ensure API response times are acceptable.

### Command
```bash
claudetm start "Add performance tests for user search endpoint - ensure response time under 200ms for 1000 users in database"
```

### Generated Tests
```python
import pytest
import time
from tests.factories import UserFactory

@pytest.fixture
def populate_users(db_session):
    """Create 1000 test users."""
    users = [UserFactory() for _ in range(1000)]
    db_session.bulk_save_objects(users)
    db_session.commit()

class TestSearchPerformance:
    def test_search_response_time(self, client, populate_users):
        start_time = time.time()
        response = client.get('/api/users/search?q=test')
        elapsed = time.time() - start_time

        assert response.status_code == 200
        assert elapsed < 0.2, f"Search took {elapsed:.3f}s (expected < 0.2s)"

    def test_pagination_performance(self, client, populate_users):
        start_time = time.time()
        response = client.get('/api/users?page=1&per_page=50')
        elapsed = time.time() - start_time

        assert response.status_code == 200
        assert elapsed < 0.1, f"Pagination took {elapsed:.3f}s (expected < 0.1s)"
        data = response.get_json()
        assert len(data['items']) == 50
```

## Example 8: Snapshot Tests

### Scenario
API response format should be stable.

### Command
```bash
claudetm start "Add snapshot tests for API responses - ensure user, order, and product endpoints return consistent JSON structure"
```

### Generated Tests
```python
import pytest
from syrupy.assertion import SnapshotAssertion

class TestAPISnapshots:
    def test_user_response_structure(
        self,
        client,
        user,
        snapshot: SnapshotAssertion
    ):
        response = client.get(f'/api/users/{user.id}')
        data = response.get_json()

        # First run creates snapshot, subsequent runs compare
        assert data == snapshot

    def test_order_list_structure(
        self,
        client,
        authenticated_client,
        snapshot: SnapshotAssertion
    ):
        response = authenticated_client.get('/api/orders')
        data = response.get_json()

        assert data == snapshot
```

## Example 9: Property-Based Tests

### Scenario
Function should work for wide range of inputs.

### Command
```bash
claudetm start "Add property-based tests for slug generation function using Hypothesis - test with various string inputs"
```

### Generated Tests
```python
from hypothesis import given, strategies as st
from utils.text import slugify

class TestSlugify:
    @given(st.text())
    def test_slugify_always_lowercase(self, text):
        result = slugify(text)
        assert result == result.lower()

    @given(st.text())
    def test_slugify_no_special_chars(self, text):
        result = slugify(text)
        assert result.replace('-', '').replace('_', '').isalnum()

    @given(st.text(min_size=1))
    def test_slugify_not_empty_for_valid_input(self, text):
        if any(c.isalnum() for c in text):
            result = slugify(text)
            assert len(result) > 0

    @given(st.lists(st.text(), min_size=2, max_size=10))
    def test_slugify_unique_inputs_unique_outputs(self, texts):
        # Remove duplicates from input
        unique_texts = list(set(texts))
        if len(unique_texts) < 2:
            return

        slugs = [slugify(t) for t in unique_texts]
        # Most inputs should produce unique slugs
        assert len(set(slugs)) > len(slugs) * 0.8
```

## Example 10: Test Documentation

### Scenario
Tests exist but lack documentation.

### Command
```bash
claudetm start "Add docstrings to all tests in tests/test_auth.py explaining what each test validates and why"
```

## Testing Best Practices

### 1. Be Specific About Coverage
```bash
claudetm start "Add tests for user authentication - cover login, logout, token refresh, and session expiry"
```

### 2. Specify Test Types
```bash
claudetm start "Add unit tests for validation functions - no database or external dependencies"
```

### 3. Include Edge Cases
```bash
claudetm start "Add tests for payment processing including edge cases: zero amount, negative amount, invalid currency, and network timeouts"
```

### 4. Request Specific Patterns
```bash
claudetm start "Add tests using pytest fixtures and parametrize for multiple test cases"
```

### 5. Set Coverage Goals
```bash
claudetm start "Add tests to bring auth.py coverage from 60% to 90%+"
```

## Testing Patterns

### AAA Pattern (Arrange-Act-Assert)
```python
def test_user_creation():
    # Arrange
    user_data = {'name': 'John', 'email': 'john@example.com'}

    # Act
    user = create_user(user_data)

    # Assert
    assert user.name == 'John'
    assert user.email == 'john@example.com'
```

### Given-When-Then (BDD)
```python
def test_user_login():
    # Given: User exists in database
    user = UserFactory(password='secret123')

    # When: User attempts login
    response = client.post('/login', json={
        'email': user.email,
        'password': 'secret123',
    })

    # Then: Login succeeds
    assert response.status_code == 200
    assert 'token' in response.get_json()
```

## Common Test Commands

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html
```

### Run Specific Test
```bash
pytest tests/test_auth.py::TestLogin::test_successful_login
```

### Run Tests Matching Pattern
```bash
pytest -k "test_user"
```

### Run in Parallel
```bash
pytest -n auto
```

## Troubleshooting

### Tests Too Slow
```bash
claudetm start "Optimize test suite - use fixtures efficiently, mock external services, and add pytest-xdist for parallel execution"
```

### Flaky Tests
```bash
claudetm start "Fix flaky tests in test_async_operations.py - add proper async handling and remove timing dependencies"
```

### Low Coverage Areas
```bash
# Check coverage
pytest --cov=src --cov-report=term-missing

# Target specific low coverage file
claudetm start "Add tests for error_handler.py to increase coverage from 45% to 90%"
```

## Next Steps

- [Documentation](./06-documentation.md) - Document your tested code
- [CI/CD Integration](./07-cicd.md) - Automate test execution
- [Advanced Workflows](./08-advanced-workflows.md) - Complex testing scenarios
