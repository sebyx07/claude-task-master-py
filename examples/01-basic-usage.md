# Basic Usage Examples

Learn the fundamentals of Claude Task Master with these simple examples.

## Example 1: Add a Simple Function

### Goal
Add a utility function to calculate the factorial of a number.

### Command
```bash
cd my-python-project
claudetm start "Add a factorial function to utils/math.py with tests"
```

### What Happens
1. **Planning Phase**: Claude creates a task list:
   - Create or update utils/math.py
   - Add factorial function with proper error handling
   - Write unit tests in tests/test_math.py
   - Run tests to verify

2. **Execution Phase**: Claude implements each task:
   - Writes the function
   - Adds comprehensive tests
   - Runs pytest to verify
   - Creates a PR with descriptive title and summary

3. **PR & CI**:
   - PR is created automatically
   - CI runs tests
   - PR auto-merges when CI passes (default behavior)

### Check Progress
```bash
# While it's running
claudetm status
claudetm plan
claudetm logs -n 50
```

## Example 2: Fix a Typo

### Goal
Fix a typo in the README file.

### Command
```bash
claudetm start "Fix typo: change 'installtion' to 'installation' in README.md"
```

### Expected Result
- Claude identifies the typo
- Updates the file
- Creates a PR titled "fix: Correct typo in README.md"
- Auto-merges after CI passes

### Time
Should complete in 1-2 sessions (under a minute).

## Example 3: Add Environment Variable

### Goal
Add support for a new environment variable in your config.

### Command
```bash
claudetm start "Add DATABASE_TIMEOUT env var to config.py with default value of 30 seconds"
```

### What Gets Updated
- `config.py` - adds new variable
- `.env.example` - documents the variable
- `README.md` - updates configuration docs
- Tests - verifies the config loading

## Example 4: Status Monitoring

### Scenario
You started a task and want to check its progress.

```bash
# Start a task
claudetm start "Add logging to the API client"

# In another terminal, check status
claudetm status
```

### Output
```
Task Status

Goal: Add logging to the API client
Status: working
Model: opus
Current Task: 2
Sessions: 3
Run ID: 1234567890

Options:
  Auto-merge: True
  Max sessions: unlimited
  Pause on PR: False
```

```bash
# View the plan
claudetm plan
```

### Output
```
Task Plan

- [x] Add logging import to api/client.py
- [ ] Configure logger with appropriate level
- [ ] Add debug logs for request/response
- [ ] Add error logs for failures
- [ ] Update tests to verify logging
- [ ] Create PR
```

## Example 5: Interrupt and Resume

### Scenario
You need to stop the task temporarily.

```bash
# Start task
claudetm start "Refactor authentication module"

# Press Ctrl+C to interrupt
^C

# Later, resume
claudetm resume
```

### Notes
- State is preserved in `.claude-task-master/`
- Resume continues from where it left off
- All context and progress is maintained

## Example 6: Clean Up After Success

### Scenario
Task completed successfully and you want to start fresh.

```bash
# Check status (should show "success")
claudetm status

# Clean up state
claudetm clean
```

### What Gets Cleaned
- `.claude-task-master/goal.txt`
- `.claude-task-master/plan.md`
- `.claude-task-master/state.json`
- `.claude-task-master/progress.md`
- `.claude-task-master/context.md`

### What's Preserved
- `.claude-task-master/logs/` (last 10 log files)

## Example 7: Force Clean

### Scenario
Task is stuck or you want to abandon it.

```bash
claudetm clean -f  # No confirmation prompt
```

## Example 8: Review Logs

### Scenario
You want to see what Claude did.

```bash
# Show last 100 lines
claudetm logs

# Show last 50 lines
claudetm logs -n 50

# View full logs
cat .claude-task-master/logs/run-*.txt
```

## Common Workflows

### Quick Task
```bash
claudetm start "Task" && claudetm status
```

### Manual Review Flow
```bash
# Start with manual review
claudetm start "Task" --no-auto-merge

# Check when PR is ready
claudetm pr-status $(gh pr list --limit 1 --json number -q '.[0].number')

# Manually merge when satisfied
gh pr merge --squash --delete-branch
```

### Limited Sessions
```bash
# Stop after 5 sessions to prevent runaway execution
claudetm start "Complex task" --max-sessions 5
```

## Tips for Beginners

1. **Start Simple**: Try a typo fix or simple function first
2. **Watch It Work**: Keep `claudetm status` running in another terminal
3. **Read the Plan**: Use `claudetm plan` to see what Claude intends to do
4. **Check Logs**: If confused, `claudetm logs` shows detailed execution
5. **Don't Worry**: You can always `claudetm clean -f` to start over
6. **Review PRs**: Even though it auto-merges, review what gets merged
7. **Use Git**: Everything is in git, you can revert if needed

## Next Steps

- [Feature Development](./02-feature-development.md) - Build complete features
- [Bug Fixing](./03-bug-fixing.md) - Debug and fix issues
- [Testing](./05-testing.md) - Add test coverage
