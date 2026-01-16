# Feature Development Examples

Build complete features from scratch using Claude Task Master.

## Example 1: Add API Endpoint

### Goal
Add a REST API endpoint to retrieve user profile information.

### Command
```bash
cd my-api-project
claudetm start "Add GET /api/v1/users/:id/profile endpoint that returns user profile with avatar, bio, and settings"
```

### What Claude Does

1. **Planning**:
   - Analyzes existing API structure
   - Identifies patterns (routing, controllers, models)
   - Creates task breakdown

2. **Implementation**:
   - Creates/updates route handler
   - Adds controller method
   - Implements data validation
   - Adds error handling
   - Writes integration tests
   - Updates API documentation
   - Creates PR

3. **Verification**:
   - Runs tests
   - Checks linting
   - Ensures CI passes

### Example Plan Output
```markdown
- [x] Create profile route in routes/users.py
- [x] Add get_profile controller method
- [x] Add ProfileResponse model with validation
- [x] Implement avatar URL generation
- [x] Add error handling for missing users
- [ ] Write integration tests
- [ ] Update OpenAPI schema
- [ ] Create PR
```

## Example 2: Database Migration

### Goal
Add email verification to user model.

### Command
```bash
claudetm start "Add email_verified boolean field and verified_at timestamp to User model with migration"
```

### Implementation Details

Claude will:
1. Create database migration file
2. Update User model class
3. Add migration for existing users (default: False)
4. Update API response schemas
5. Add verification endpoint
6. Write migration tests
7. Update documentation

### Files Modified
- `models/user.py`
- `migrations/0023_add_email_verification.py`
- `schemas/user.py`
- `tests/test_user_model.py`
- `tests/test_migrations.py`
- `docs/api.md`

## Example 3: Authentication System

### Goal
Add JWT-based authentication from scratch.

### Command
```bash
claudetm start "Implement JWT authentication system with login, logout, and protected routes" --max-sessions 20
```

### Why Max Sessions?
Large features may need many iterations. Set a limit to prevent infinite loops.

### What Gets Built

1. **Auth Module**:
   ```
   auth/
   ├── __init__.py
   ├── jwt.py          # Token generation/validation
   ├── middleware.py   # Auth middleware
   ├── models.py       # Token/Session models
   └── routes.py       # Login/logout endpoints
   ```

2. **Tests**:
   ```
   tests/auth/
   ├── test_jwt.py
   ├── test_middleware.py
   ├── test_login.py
   └── test_logout.py
   ```

3. **Documentation**:
   - API usage examples
   - Configuration guide
   - Security considerations

### Expected Sessions
10-15 sessions to complete fully.

## Example 4: Frontend Component

### Goal
Add a reusable modal component in React.

### Command
```bash
cd my-react-app
claudetm start "Create a reusable Modal component with props for title, content, onClose, and footer buttons. Include animations and accessibility features."
```

### Deliverables

```
src/components/Modal/
├── Modal.tsx           # Main component
├── Modal.module.css    # Styles with animations
├── Modal.test.tsx      # Unit tests
├── Modal.stories.tsx   # Storybook stories
└── index.ts            # Export
```

### Features Implemented
- ESC key to close
- Click outside to close
- ARIA attributes
- Focus trap
- Smooth animations
- Mobile responsive
- TypeScript types

## Example 5: CLI Command

### Goal
Add a new CLI command to your Python package.

### Command
```bash
claudetm start "Add 'export' command to CLI that exports data to JSON or CSV format with --format flag"
```

### Implementation

1. **Command Module**:
   ```python
   # cli/commands/export.py
   @app.command()
   def export(
       format: str = typer.Option("json", help="Output format: json or csv"),
       output: Path = typer.Option(None, help="Output file path"),
   ):
       """Export data to file."""
       ...
   ```

2. **Tests**:
   ```python
   # tests/cli/test_export.py
   def test_export_json():
       result = runner.invoke(app, ["export", "--format", "json"])
       assert result.exit_code == 0
   ```

3. **Documentation**:
   - Update README with example usage
   - Add docstrings
   - Update CLI help text

## Example 6: Multi-Step Feature with Pause

### Goal
Large feature that you want to review mid-way.

### Command
```bash
claudetm start "Add complete shopping cart system with add/remove items, quantity updates, and checkout flow" --pause-on-pr --max-sessions 15
```

### Workflow

1. **First Run**:
   ```bash
   claudetm start "..." --pause-on-pr
   ```
   - Claude plans and implements
   - Creates first PR
   - **Pauses automatically**

2. **Review PR**:
   ```bash
   gh pr view
   gh pr diff
   ```

3. **Continue**:
   ```bash
   claudetm resume
   ```
   - Claude waits for CI
   - Handles review comments if any
   - Merges when ready
   - Continues with remaining tasks

## Example 7: Integration with External Service

### Goal
Add Stripe payment integration.

### Command
```bash
claudetm start "Integrate Stripe payment processing with checkout flow, webhook handling, and payment status tracking" --no-auto-merge
```

### Why No Auto-Merge?
- External service integration needs careful review
- API keys and secrets require manual verification
- Testing in staging environment first

### Implementation Checklist

Claude creates:
- [ ] Stripe client wrapper
- [ ] Payment intent creation
- [ ] Webhook endpoint
- [ ] Signature verification
- [ ] Payment status updates
- [ ] Error handling
- [ ] Retry logic
- [ ] Tests with mocked Stripe API
- [ ] Environment variables documentation
- [ ] Security audit checklist

### Manual Steps After PR
```bash
# Review the PR
gh pr view

# Test in staging
git checkout <pr-branch>
# ... test with Stripe test mode ...

# Merge when satisfied
gh pr merge --squash
```

## Example 8: Performance Optimization

### Goal
Optimize database queries in user dashboard.

### Command
```bash
claudetm start "Optimize user dashboard queries - add database indexes, implement query result caching, and reduce N+1 queries"
```

### Claude's Approach

1. **Analysis**:
   - Reads existing dashboard code
   - Identifies slow queries
   - Checks for N+1 patterns

2. **Optimization**:
   - Adds select_related/prefetch_related (Django)
   - Creates database indexes
   - Implements caching layer
   - Adds query monitoring

3. **Verification**:
   - Benchmarks before/after
   - Runs performance tests
   - Checks cache hit rates

### Metrics Tracked
```python
# Claude adds benchmarking
Before: 2.3s average page load
After: 0.4s average page load
Cache hit rate: 87%
Database queries reduced: 45 → 8
```

## Best Practices for Feature Development

### 1. Be Specific
❌ Bad: `"Add user management"`
✅ Good: `"Add user management with CRUD operations, role assignment, and activity logging"`

### 2. Mention Related Systems
```bash
claudetm start "Add webhook system for order updates that integrates with existing notification service and logs to audit trail"
```

### 3. Specify Technologies
```bash
claudetm start "Add real-time chat using WebSockets (socket.io), store messages in PostgreSQL, and cache recent messages in Redis"
```

### 4. Include Testing Requirements
```bash
claudetm start "Add payment processing with Stripe - include unit tests, integration tests with mocked API, and error handling tests"
```

### 5. Set Appropriate Limits
- Simple feature: default (no limit)
- Medium feature: `--max-sessions 10`
- Complex feature: `--max-sessions 20`
- Very complex: `--max-sessions 30` (review plan first)

### 6. Use Right Model
- **opus**: Complex features, architectural decisions
- **sonnet**: Standard features, well-defined requirements
- **haiku**: Simple additions, clear patterns exist

## Monitoring Large Features

```bash
# Terminal 1: Watch status
watch -n 5 claudetm status

# Terminal 2: Follow logs
tail -f .claude-task-master/logs/run-*.txt

# Terminal 3: Monitor git
watch -n 5 git status
```

## Troubleshooting

### Feature Too Large
If Claude struggles with scope:
```bash
# Break into smaller pieces
claudetm clean -f
claudetm start "Add shopping cart - Part 1: Add/remove items only"
# After completion
claudetm start "Add shopping cart - Part 2: Quantity updates and subtotal"
```

### Wrong Direction
```bash
# Interrupt with Ctrl+C
^C

# Review what was done
git status
git diff

# Decide: resume or start over
claudetm clean -f  # Start over
# OR
claudetm resume    # Continue
```

### Session Limit Reached
```bash
# Check progress
claudetm plan
claudetm progress

# If making progress, increase limit and resume
claudetm resume  # Will continue despite previous limit
```

## Next Steps

- [Bug Fixing](./03-bug-fixing.md) - Fix issues in code
- [Testing](./05-testing.md) - Add comprehensive tests
- [Advanced Workflows](./08-advanced-workflows.md) - Complex scenarios
