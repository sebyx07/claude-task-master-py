# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Task Master is an autonomous task orchestration system that keeps Claude working until a goal is achieved. It uses the Claude Agent SDK with OAuth credentials from Claude Code CLI (`~/.claude/.credentials.json`) for authentication.

**Core Philosophy**: Claude is smart enough to do the work AND verify its own work. The task master just keeps the loop going and persists state between sessions.

## Development Commands

### Testing
```bash
pytest                           # Run all tests
pytest tests/test_specific.py    # Run specific test file
pytest -v                         # Verbose output
pytest -k "test_name"            # Run tests matching pattern
```

### Linting & Formatting
```bash
ruff check .                     # Lint code
ruff format .                    # Format code
mypy .                           # Type checking
```

### Installation
```bash
pip install -e .                 # Install in development mode
claude-task-master --help        # Verify installation
```

## Architecture Overview

The system follows SOLID principles with Single Responsibility Principle (SRP) strictly enforced. Each component handles one specific concern.

### Core Components

1. **Credential Manager** - OAuth credential loading, validation, and refresh from `~/.claude/.credentials.json`
2. **State Manager** - All persistence to `.claude-task-master/` directory
3. **Agent Wrapper** - Encapsulates all Claude Agent SDK interactions
4. **Planner** - Orchestrates initial planning phase (read-only tools)
5. **Work Loop Orchestrator** - Main loop driving work sessions until completion
6. **GitHub Integration Layer** - All GitHub operations via `gh` CLI and GraphQL API
7. **PR Cycle Manager** - Handles create → CI wait → address comments → merge cycle
8. **Logger** - Single consolidated log file per run: `logs/run-{timestamp}.txt`
9. **Context Accumulator** - Builds up learnings across sessions in `context.md`
10. **CLI Layer** - Uses `typer` for command parsing and dispatch

### State Directory Structure

```
.claude-task-master/
├── goal.txt              # Original user goal
├── criteria.txt          # Success criteria
├── plan.md               # Task list with markdown checkboxes
├── state.json            # Machine-readable state
├── progress.md           # Human-readable progress summary
├── context.md            # Learnings accumulated across sessions
└── logs/
    └── run-{timestamp}.txt    # Full consolidated log (KEPT ON SUCCESS)
```

### Exit Codes and Cleanup Behavior

**Exit Code 0 (Success)**:
- All tasks completed and success criteria verified
- **Cleanup**: Delete all state files EXCEPT `logs/run-{timestamp}.txt`
- Log file is kept as the audit trail

**Exit Code 1 (Blocked/Error)**:
- Task cannot proceed, needs human intervention
- Unrecoverable error or max sessions reached
- **Keep everything** for debugging and resume

**Exit Code 2 (User Interrupted)**:
- User pressed Ctrl+C to pause
- **Keep everything** for resume

### Authentication Flow

1. Read credentials from `~/.claude/.credentials.json` (created by Claude Code CLI)
2. Check if `accessToken` is expired by comparing `expiresAt` with current time
3. If expired, use `refreshToken` to get new `accessToken` from Claude OAuth endpoint
4. Update credentials file with new tokens
5. Pass access token to Agent SDK for authentication

**Error handling**: If credentials missing or refresh fails, exit with message to run `claude` CLI first.

### Work Loop Flow

```
Planning Phase (Claude analyzes, creates task list)
    ↓
┌─────────────────────────────────────┐
│          WORK LOOP                  │
│  1. Work on current task            │
│  2. Check if task complete          │
│  3. If PR needed: create/update PR  │
│  4. Wait for CI + address comments  │
│  5. Merge when ready (if auto)      │
│  6. Move to next task               │
│  Repeat until all tasks done        │
└─────────────────────────────────────┘
    ↓
Verify success criteria met
    ↓
SUCCESS: exit 0, cleanup (keep logs)
BLOCKED: exit 1, keep all state
```

### GitHub Integration

**Uses `gh` CLI** for all operations. Key GraphQL query for PR info:

```graphql
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      commits(last: 1) {
        nodes {
          commit {
            statusCheckRollup {
              state
              contexts(first: 50) {
                nodes {
                  ... on CheckRun {
                    name
                    status
                    conclusion
                    detailsUrl
                  }
                }
              }
            }
          }
        }
      }
      reviewThreads(first: 100) {
        nodes {
          isResolved
          comments(first: 10) {
            nodes {
              author { login }
              body
              path
              line
            }
          }
        }
      }
    }
  }
}
```

**Bot detection**: Any author login ending in `[bot]` (e.g., `coderabbitai[bot]`, `github-actions[bot]`)

### Tool Configuration by Phase

- **Planning phase**: Read, Glob, Grep (read-only)
- **Working phase**: Read, Write, Edit, Bash, Glob, Grep
- **PR phase**: Same as working, plus PR comment context

## Key Implementation Details

### state.json Schema

```json
{
  "status": "planning|working|blocked|success|failed",
  "current_task_index": 0,
  "session_count": 0,
  "current_pr": null,
  "created_at": "ISO timestamp",
  "updated_at": "ISO timestamp",
  "run_id": "timestamp string",
  "model": "sonnet",
  "options": {
    "auto_merge": true,
    "max_sessions": null,
    "pause_on_pr": false
  }
}
```

### Single Log File Strategy

All sessions append to one file: `logs/run-{timestamp}.txt`

Format includes session number, timestamp, phase, full prompt/response, tool usage, outcome, and duration. This file is the only thing kept after successful completion.

### PR Cycle Logic

```
create/update PR
while PR not merged:
    if CI pending: poll and wait
    if CI failed: create fix session with details
    if unresolved comments: create fix session
    if ready and auto_merge: merge
    if ready and no auto_merge: exit 1 (blocked)
move to next task
```

## Dependencies

Core:
- `claude-agent-sdk` - Agent functionality
- `typer` - CLI framework
- `pydantic` - Data validation
- `rich` - Terminal formatting
- `httpx` - Token refresh HTTP calls

External tools (checked by `doctor` command):
- `gh` CLI must be installed and authenticated
- `~/.claude/.credentials.json` must exist (user ran Claude Code CLI once)

## Success Criteria for Implementation

The implementation is complete when:
1. Uses OAuth from `~/.claude/.credentials.json` with auto-refresh
2. All CLI commands work (`start`, `resume`, `status`, `plan`, `logs`, `context`, `progress`, `comments`, `pr`, `clean`, `doctor`)
3. Exit code 0 on success with cleanup (keeps only log file)
4. Exit codes 1/2 preserve full state for resume
5. Successfully creates/merges PRs with CI checks
6. Handles review comments from humans and bots
7. Installable via pip with `claude-task-master` command
8. Single consolidated log per run
9. All code follows SOLID/SRP principles
10. All code is fully tested and linted
