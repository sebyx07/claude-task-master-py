# CI/CD Integration Examples

Work with GitHub Actions and continuous integration using Claude Task Master.

## Example 1: Fix Failing CI

### Scenario
Pull request has failing tests.

### Command
```bash
claudetm start "Fix failing CI tests - address all test failures in the latest workflow run"
```

### Claude's Process
1. Checks CI status using GitHub API
2. Fetches failed run logs
3. Identifies specific test failures
4. Fixes the issues
5. Pushes fixes and waits for CI
6. Verifies tests pass

## Example 2: Add GitHub Actions Workflow

### Command
```bash
claudetm start "Add GitHub Actions workflow for running tests and linting on every push and PR"
```

### Generated Workflow
```yaml
# .github/workflows/test.yml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with ruff
      run: ruff check .

    - name: Type check with mypy
      run: mypy .

    - name: Run tests
      run: pytest --cov=src --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        files: ./coverage.xml
```

## Example 3: Monitor and Fix CI

### Workflow with claudetm

```bash
# Start feature development
claudetm start "Add user profile endpoints"

# Feature is implemented, PR is created
# CI runs and fails...

# Check CI status
claudetm ci-status

# View failure logs
claudetm ci-logs

# Claude automatically detects failures and can fix them
# Or manually resume to address CI failures
claudetm resume
```

## Example 4: Add Deploy Workflow

### Command
```bash
claudetm start "Add GitHub Actions workflow to deploy to production on release tags"
```

### Generated Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  release:
    types: [published]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Build package
      run: |
        pip install build
        python -m build

    - name: Publish to PyPI
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_API_TOKEN }}

    - name: Deploy to production
      run: |
        # Your deployment commands
        echo "Deploying version ${{ github.ref_name }}"
```

## Example 5: Multi-Environment CI

### Command
```bash
claudetm start "Add GitHub Actions matrix testing for Python 3.9, 3.10, and 3.11 on ubuntu and macos"
```

### Generated Workflow
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.9', '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest

    - name: Run tests
      run: pytest -v
```

## Example 6: Auto-fix Linting Issues

### Command
```bash
claudetm start "Fix all linting errors reported by ruff in CI"
```

### Claude's Approach
1. Runs ruff locally or checks CI logs
2. Identifies all linting violations
3. Fixes them automatically:
   - Import sorting
   - Unused imports
   - Line length
   - Code formatting
4. Commits and pushes
5. Waits for CI to pass

## Example 7: Add Coverage Requirements

### Command
```bash
claudetm start "Add test coverage check to CI - fail if coverage drops below 80%"
```

### Generated Workflow Addition
```yaml
- name: Run tests with coverage
  run: pytest --cov=src --cov-report=term-missing --cov-fail-under=80

- name: Coverage comment
  uses: py-cov-action/python-coverage-comment-action@v3
  with:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    MINIMUM_GREEN: 80
    MINIMUM_ORANGE: 60
```

## Example 8: Docker Build CI

### Command
```bash
claudetm start "Add CI workflow to build and test Docker image on every push"
```

### Generated Workflow
```yaml
name: Docker

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Build Docker image
      run: docker build -t myapp:test .

    - name: Test Docker image
      run: |
        docker run --rm myapp:test pytest

    - name: Login to DockerHub
      if: github.event_name == 'push'
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}

    - name: Push to DockerHub
      if: github.event_name == 'push'
      run: |
        docker tag myapp:test myorg/myapp:latest
        docker push myorg/myapp:latest
```

## Example 9: Security Scanning

### Command
```bash
claudetm start "Add security scanning to CI using bandit for Python and OWASP dependency check"
```

### Generated Workflow
```yaml
name: Security

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install bandit
      run: pip install bandit

    - name: Run security scan
      run: bandit -r src/ -f json -o bandit-report.json

    - name: Dependency check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'myproject'
        path: '.'
        format: 'ALL'

    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: security-reports
        path: |
          bandit-report.json
          dependency-check-report.html
```

## Example 10: Auto-merge on Success

### Command
```bash
claudetm start "Add workflow to auto-merge dependabot PRs when CI passes"
```

### Generated Workflow
```yaml
name: Auto-merge

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'

    steps:
    - name: Check CI status
      uses: fountainhead/action-wait-for-check@v1.1.0
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        checkName: test
        ref: ${{ github.event.pull_request.head.sha }}

    - name: Auto-merge
      uses: pascalgn/automerge-action@v0.15.6
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        MERGE_LABELS: dependencies
        MERGE_METHOD: squash
```

## Working with CI in claudetm

### Check CI Status
```bash
# View recent workflow runs
claudetm ci-status

# View specific run
claudetm ci-status -r 123456789

# View last 10 runs
claudetm ci-status -l 10
```

### View CI Logs
```bash
# Show logs from failed runs
claudetm ci-logs

# Show logs from specific run
claudetm ci-logs -r 123456789

# Show more lines
claudetm ci-logs -n 200
```

### PR Status
```bash
# View PR status including CI
claudetm pr-status 123

# View review comments
claudetm pr-comments 123
```

## CI Integration Best Practices

### 1. Let Claude Handle CI Failures
```bash
# Claude automatically waits for and handles CI
claudetm start "Add new feature" --auto-merge

# If CI fails, Claude will:
# 1. Detect the failure
# 2. Fetch logs
# 3. Identify the issue
# 4. Fix it
# 5. Push fix
# 6. Wait for CI again
```

### 2. Monitor Long-Running Tasks
```bash
# Terminal 1: Watch status
watch -n 10 claudetm status

# Terminal 2: Watch CI
watch -n 30 claudetm ci-status
```

### 3. Manual Intervention When Needed
```bash
# Start with auto-merge disabled for critical changes
claudetm start "Database migration" --no-auto-merge

# Review CI results manually
claudetm ci-status
gh pr checks

# Merge when satisfied
gh pr merge --squash
```

### 4. Pause for Review
```bash
# Pause after PR creation to review CI results
claudetm start "New feature" --pause-on-pr

# After PR created, check CI
claudetm ci-status
gh pr checks --watch

# Resume when ready
claudetm resume
```

## Common CI Scenarios

### Flaky Tests
```bash
claudetm start "Fix flaky test that fails intermittently in CI"
```

### Timeout Issues
```bash
claudetm start "Fix CI timeout - optimize slow tests and increase timeout limit"
```

### Environment-Specific Failures
```bash
claudetm start "Fix test that passes locally but fails in CI - ensure proper test isolation"
```

### Dependency Issues
```bash
claudetm start "Fix CI dependency installation failure - update requirements.txt and pin versions"
```

## Advanced CI Workflows

### Conditional Workflows
```bash
claudetm start "Add CI workflow that only runs integration tests when files in api/ directory change"
```

### Parallel Jobs
```bash
claudetm start "Split CI tests into parallel jobs to reduce total runtime"
```

### Caching
```bash
claudetm start "Add dependency caching to GitHub Actions to speed up CI runs"
```

### Notifications
```bash
claudetm start "Add Slack notification when CI fails on main branch"
```

## Troubleshooting CI

### CI Stuck
```bash
# Check status
claudetm ci-status

# If workflow is hung, you may need to manually cancel
gh run list --limit 5
gh run cancel <run-id>
```

### Cannot Reproduce Locally
```bash
claudetm start "Debug CI failure that cannot be reproduced locally - add more detailed logging and check environment differences"
```

### Too Slow
```bash
claudetm start "Optimize CI workflow - add caching, parallelize tests, and use faster actions"
```

## Next Steps

- [Advanced Workflows](./08-advanced-workflows.md) - Complex multi-step scenarios
