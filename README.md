# Claude Task Master

Autonomous task orchestration system that keeps Claude working until a goal is achieved.

## Overview

Claude Task Master uses the Claude Agent SDK to autonomously work on complex tasks by:

- Breaking down goals into actionable task lists
- Executing tasks using appropriate tools (Read, Write, Edit, Bash, etc.)
- Creating and managing GitHub pull requests
- Waiting for CI checks and addressing review comments
- Iterating until all tasks are complete and success criteria are met

**Core Philosophy**: Claude is smart enough to do the work AND verify its own work. The task master just keeps the loop going and persists state between sessions.

## Installation

```bash
pip install -e .
```

## Prerequisites

1. **Claude CLI credentials**: Run `claude` CLI once to authenticate and create `~/.claude/.credentials.json`
2. **GitHub CLI**: Install and authenticate with `gh auth login`
3. **Python 3.10+**

Run system checks:

```bash
claude-task-master doctor
```

## Usage

### Start a new task

```bash
claude-task-master start "Your goal here"
```

Options:
- `--model`: Choose model (sonnet, opus, haiku) - default: sonnet
- `--auto-merge/--no-auto-merge`: Auto-merge PRs when ready - default: True
- `--max-sessions`: Limit number of sessions
- `--pause-on-pr`: Pause after creating PR for manual review

### Resume a paused task

```bash
claude-task-master resume
```

### Check status

```bash
claude-task-master status    # Current status
claude-task-master plan      # View task list
claude-task-master progress  # Progress summary
claude-task-master logs      # View logs
claude-task-master context   # View accumulated learnings
```

### PR management

```bash
claude-task-master pr         # Show PR status and CI checks
claude-task-master comments   # Show review comments
```

### Cleanup

```bash
claude-task-master clean      # Clean up task state
```

## Architecture

The system follows SOLID principles with strict Single Responsibility:

- **Credential Manager**: OAuth credential loading and refresh
- **State Manager**: All persistence to `.claude-task-master/` directory
- **Agent Wrapper**: Claude Agent SDK interactions
- **Planner**: Initial planning phase with read-only tools
- **Work Loop Orchestrator**: Main execution loop
- **GitHub Integration**: PR creation, CI monitoring, comment handling
- **PR Cycle Manager**: Full PR lifecycle management
- **Logger**: Consolidated logging per run
- **Context Accumulator**: Builds learnings across sessions

## State Directory

```
.claude-task-master/
├── goal.txt              # Original user goal
├── criteria.txt          # Success criteria
├── plan.md               # Task list with checkboxes
├── state.json            # Machine-readable state
├── progress.md           # Progress summary
├── context.md            # Accumulated learnings
└── logs/
    └── run-{timestamp}.txt    # Full log (kept on success)
```

## Exit Codes

- **0 (Success)**: All tasks completed, criteria met. State cleaned up, logs preserved.
- **1 (Blocked)**: Task cannot proceed, needs human intervention or error occurred.
- **2 (Interrupted)**: User pressed Ctrl+C, state preserved for resume.

## Development

### Testing

```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest -k "test_name"     # Run specific tests
```

### Linting & Formatting

```bash
ruff check .              # Lint
ruff format .             # Format
mypy .                    # Type check
```

## License

MIT
