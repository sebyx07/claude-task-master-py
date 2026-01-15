# Claude Task Master - Python Architecture Document (Revised)

## Overview

Claude Task Master is an autonomous task orchestration system that keeps Claude working until a goal is achieved. It uses the Claude Agent SDK with OAuth credentials from Claude Code CLI for authentication.

**Core Philosophy**: Claude is smart enough to do the work AND verify its own work. The task master just keeps the loop going and persists state between sessions.

## Authentication

Use the existing Claude Code CLI credentials stored at `~/.claude/.credentials.json`:

```
{
  "claudeAiOauth": {
    "accessToken": "sk-ant-oat01-...",
    "refreshToken": "sk-ant-ort01-...",
    "expiresAt": timestamp,
    "scopes": ["user:inference", "user:profile", "user:sessions:claude_code"],
    "subscriptionType": "max",
    "rateLimitTier": "default_claude_max_20x"
  }
}
```

**Credential Handling**:
- Read credentials from `~/.claude/.credentials.json`
- Check `expiresAt` timestamp before each session
- If expired, use `refreshToken` to obtain new `accessToken`
- Update the credentials file with new tokens after refresh
- Pass access token to Agent SDK for authentication

This means users don't need to provide an API key separately - they just need to have logged into Claude Code CLI once.

## Exit Codes and State Cleanup

**Exit Code 0 - Success**:
- All tasks completed
- Success criteria verified
- Clean up `.claude-task-master/` directory EXCEPT:
  - Keep `.claude-task-master/logs/run-{timestamp}.txt` (full session log)
- Print success summary

**Exit Code 1 - Blocked/Error**:
- Task cannot proceed (needs human intervention)
- Unrecoverable error occurred
- Max sessions reached without completion
- Keep entire `.claude-task-master/` directory intact for debugging and resume
- Print clear message about what's blocked and how to resume

**Exit Code 2 - User Interrupted** (Ctrl+C):
- User chose to pause
- Keep entire `.claude-task-master/` directory intact
- Print resume instructions

## High-Level Flow

```
User provides goal + success criteria
           ↓
    Load credentials from ~/.claude/.credentials.json
           ↓
    Planning Phase (Claude analyzes codebase, creates task list)
           ↓
    ┌──────────────────────────────────────┐
    │           WORK LOOP                  │
    │  ┌─────────────────────────────────┐ │
    │  │ Work on current task            │ │
    │  │         ↓                       │ │
    │  │ Check if task complete          │ │
    │  │         ↓                       │ │
    │  │ If PR needed: create/update PR  │ │
    │  │         ↓                       │ │
    │  │ Wait for CI + address comments  │ │
    │  │         ↓                       │ │
    │  │ Merge when ready                │ │
    │  │         ↓                       │ │
    │  │ Move to next task               │ │
    │  └─────────────────────────────────┘ │
    │  Repeat until all tasks done         │
    └──────────────────────────────────────┘
           ↓
    Verify success criteria met
           ↓
    SUCCESS: exit 0, cleanup state (keep logs)
    BLOCKED: exit 1, keep all state
```

## Architecture Components

### 1. Credential Manager

**Purpose**: Handle OAuth credential loading, validation, and refresh.

**Location**: `~/.claude/.credentials.json`

**Operations**:
- Load credentials from JSON file
- Validate credentials exist and have required fields
- Check if access token is expired (compare `expiresAt` with current time)
- Refresh access token using refresh token when expired
- Save updated credentials back to file
- Provide access token to Agent SDK

**Token Refresh**:
When `expiresAt` timestamp is in the past:
1. Call Claude OAuth refresh endpoint with `refreshToken`
2. Receive new `accessToken`, `refreshToken`, and `expiresAt`
3. Update `~/.claude/.credentials.json` with new values
4. Continue with new access token

**Error Cases**:
- Credentials file doesn't exist: Exit with message to run `claude` CLI first
- Refresh token expired/invalid: Exit with message to re-authenticate via `claude` CLI
- Network error during refresh: Retry with backoff, then fail

### 2. Entry Point and CLI Layer

**Purpose**: Handle all user interaction, argument parsing, and command dispatch.

**Commands to implement**:
- `start <goal>` - Begin a new task with optional inline criteria
- `resume` - Continue previous work (also the default when no args)
- `status` - Show current state and progress
- `plan` - Display the task plan
- `logs` - View session logs with filtering options
- `context` - Show accumulated learnings
- `progress` - Show human-readable progress
- `comments [pr_number]` - View PR comments with filters for actionable/unresolved
- `pr status` - Show PR information
- `pr checks` - Show CI status
- `pr merge` - Merge current PR
- `clean` - Remove state directory and start fresh
- `doctor` - Check prerequisites (Claude Code CLI credentials, gh CLI)

**CLI Options**:
- `--model` - Specify Claude model (sonnet, opus, etc.) - default opus 4.1
- `--criteria` - Provide success criteria inline instead of prompting
- `--no-merge` - Require manual PR merges
- `--max-sessions` / `-m` - Limit total work sessions
- `--pause-on-pr` - Pause after each PR creation for manual review
- `--verbose` - Enable detailed output

Use `typer` for CLI framework (modern, type-hint based).

### 3. State Manager

**Purpose**: Handle all persistence to the `.claude-task-master/` directory.

**State Directory Structure**:
```
.claude-task-master/
├── goal.txt              # The original goal from the user
├── criteria.txt          # Success criteria
├── plan.md               # Task list with markdown checkboxes
├── state.json            # Machine-readable state
├── progress.md           # Human-readable progress summary
├── context.md            # Learnings accumulated across sessions
└── logs/
    └── run-{timestamp}.txt    # Full consolidated log (KEPT ON SUCCESS)
```

**state.json Schema**:
```
{
  "status": "planning" | "working" | "blocked" | "success" | "failed",
  "current_task_index": integer,
  "session_count": integer,
  "current_pr": integer or null,
  "created_at": ISO timestamp,
  "updated_at": ISO timestamp,
  "run_id": timestamp string (used for log filename),
  "model": string,
  "options": {
    "auto_merge": boolean,
    "max_sessions": integer or null,
    "pause_on_pr": boolean
  }
}
```

**Cleanup on Success**:
When all tasks complete and success criteria verified:
1. Copy/consolidate logs to `logs/run-{timestamp}.txt`
2. Delete `goal.txt`, `criteria.txt`, `plan.md`, `state.json`, `progress.md`, `context.md`
3. Keep only the `logs/` directory with the run log
4. Exit with code 0

**Keep Everything on Blocked/Error**:
When blocked or error:
1. Save current state
2. Keep all files for debugging and resume
3. Exit with code 1

### 4. Agent Wrapper

**Purpose**: Encapsulate all interactions with the Claude Agent SDK.

**Authentication**:
- Get access token from Credential Manager
- Pass to Agent SDK configuration
- Handle token refresh if session is long-running

**Tool Configuration**:
- Planning phase: Read, Glob, Grep (read-only analysis)
- Working phase: Read, Write, Edit, Bash, Glob, Grep
- PR phase: Same as working, plus context about PR comments

**Prompt Construction**:
Build prompts that include:
- The current goal and success criteria
- Relevant context from `context.md`
- Current task from the plan
- PR comments if in PR cycle
- Instructions appropriate to the phase

**Response Processing**:
- Extract structured information from Claude's responses
- Detect completion signals
- Detect blocked/error states
- Extract any learnings to add to context

### 5. Planner

**Purpose**: Orchestrate the initial planning phase.

**Process**:
1. Provide Claude with the goal and success criteria
2. Ask Claude to analyze the codebase structure
3. Ask Claude to create a numbered task list
4. Parse the response into structured tasks
5. Write the plan to `plan.md`

**Plan Format** (in plan.md):
```markdown
# Plan: {goal}

## Tasks

- [ ] Task 1: Description here
- [ ] Task 2: Description here
- [ ] Task 3: Description here

## Notes

Any additional context Claude wants to record.
```

### 6. Work Loop Orchestrator

**Purpose**: The main loop that drives work sessions until completion.

**Loop Logic**:
```
while not done:
    check/refresh credentials if needed
    
    if max_sessions reached:
        mark as blocked
        exit 1
    
    load current state
    determine current task
    
    run work session
    session_count += 1
    
    analyze session result:
        - task completed? mark done, move to next
        - PR created? enter PR cycle
        - blocked? exit 1 with reason
        - error? exit 1 with details
    
    save state
    
    if all tasks done:
        run success verification
        if success criteria met:
            cleanup state (keep logs)
            exit 0
        else:
            continue working or mark blocked
```

### 7. GitHub Integration Layer

**Purpose**: All interactions with GitHub via the `gh` CLI and GitHub GraphQL API.

**Core Operations**:

**PR Discovery**:
- Find open PRs for current branch
- Get PR number, title, state, URL

**PR Creation**:
- Create PR from current branch
- Set title and body
- Return PR number

**PR Comments** (GraphQL via `gh api graphql`):
- Fetch all review comments and PR comments
- Filter by resolved/unresolved status
- Identify comment author (human vs bot)
- Get comment body, file path, line number

**CI Status** (GraphQL):
- Get all check runs for PR
- Get status (pending, success, failure) for each
- Get details URL for failed checks

**PR Merge**:
- Check if PR is mergeable
- Perform merge
- Handle merge conflicts

**GraphQL Query for PR with Comments and Checks**:
```graphql
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      id
      number
      title
      state
      mergeable
      reviewDecision
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
      comments(first: 50) {
        nodes {
          author { login }
          body
        }
      }
    }
  }
}
```

**Bot Detection**:
Any author login ending in `[bot]`:
- `coderabbitai[bot]`
- `github-actions[bot]`
- `copilot[bot]`

### 8. PR Cycle Manager

**Purpose**: Handle the create PR → wait for CI → address comments → merge cycle.

**Cycle Logic**:
```
create or update PR
while PR not merged:
    fetch CI status
    if CI pending:
        wait and poll
        continue
    
    if CI failed:
        create fix session with failure details
        continue
    
    fetch PR comments
    if unresolved comments:
        create fix session with comment details
        continue
    
    if auto_merge enabled:
        merge PR
    else:
        mark blocked (manual merge required)
        exit 1
    
move to next task
```

### 9. Logger

**Purpose**: Capture detailed logs for debugging and audit trail.

**Single Log File**: `logs/run-{timestamp}.txt`

All sessions append to this single file for the entire run. Format:

```
================================================================================
CLAUDE TASK MASTER RUN
Started: {timestamp}
Goal: {goal}
Criteria: {criteria}
================================================================================

--- SESSION 1 ---
Time: {timestamp}
Task: {current task description}
Phase: planning | working | fixing-ci | fixing-comments | verifying

Prompt:
{full prompt}

Response:
{Claude's response}

Tool Usage:
- Read: file1.py, file2.py
- Edit: file3.py
- Bash: git status, npm test

Outcome: completed | in-progress | blocked | error
Duration: {seconds}s

--- SESSION 2 ---
...

================================================================================
RUN COMPLETE
Status: SUCCESS | BLOCKED | ERROR
Duration: {total time}
Sessions: {count}
================================================================================
```

This single file is what gets kept after successful completion.

### 10. Context Accumulator

**Purpose**: Build up learnings across sessions.

**context.md Structure**:
```markdown
# Context

## Codebase Patterns
- {patterns Claude discovered}

## Decisions Made
- {architectural decisions}

## Issues Encountered
- {problems and their solutions}

## Review Feedback Patterns
- {common reviewer comments to avoid}
```

## Exit Behavior Summary

| Scenario | Exit Code | State Cleanup |
|----------|-----------|---------------|
| All tasks done, criteria met | 0 | Delete all except `logs/run-{ts}.txt` |
| Blocked (needs human help) | 1 | Keep everything |
| Max sessions reached | 1 | Keep everything |
| Unrecoverable error | 1 | Keep everything |
| User Ctrl+C | 2 | Keep everything |
| Credentials expired/invalid | 1 | Keep everything |

## Dependencies

- `claude-agent-sdk` - Core agent functionality
- `typer` - CLI framework
- `pydantic` - Data validation and serialization
- `rich` - Terminal output formatting
- `httpx` - HTTP client for token refresh

External tools (checked by doctor):
- `gh` CLI - GitHub operations
- `~/.claude/.credentials.json` - Must exist (user ran `claude` CLI)

## Success Criteria for This Implementation

The Python implementation is complete when:

1. Uses OAuth credentials from `~/.claude/.credentials.json` (no separate API key needed)
2. Handles token refresh automatically
3. All CLI commands work as specified
4. Exit code 0 on success with cleanup (keeps only log file)
5. Exit code 1 on blocked/error with full state preserved
6. Exit code 2 on user interrupt with state preserved
7. Successfully creates and merges PRs with CI checks
8. Handles review comments from humans and bots
9. Installable via pip with `claude-task-master` command available
10. Single consolidated log file per run