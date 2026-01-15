"""Tests for state manager."""

import pytest
from claude_task_master.core.state import StateManager, TaskState, TaskOptions


def test_state_manager_initialize(temp_dir):
    """Test state manager initialization."""
    state_manager = StateManager(temp_dir / ".claude-task-master")

    options = TaskOptions(auto_merge=True, max_sessions=10)
    state = state_manager.initialize(
        goal="Test goal",
        model="sonnet",
        options=options,
    )

    assert state.status == "planning"
    assert state.current_task_index == 0
    assert state.session_count == 0
    assert state.model == "sonnet"
    assert state.options.auto_merge is True
    assert state.options.max_sessions == 10


def test_state_manager_save_load(temp_dir):
    """Test saving and loading state."""
    state_manager = StateManager(temp_dir / ".claude-task-master")

    options = TaskOptions()
    original_state = state_manager.initialize(
        goal="Test goal",
        model="sonnet",
        options=options,
    )

    loaded_state = state_manager.load_state()

    assert loaded_state.status == original_state.status
    assert loaded_state.run_id == original_state.run_id
    assert loaded_state.model == original_state.model


def test_state_manager_goal(temp_dir):
    """Test goal persistence."""
    state_manager = StateManager(temp_dir / ".claude-task-master")
    state_manager.state_dir.mkdir(exist_ok=True)

    goal = "This is a test goal"
    state_manager.save_goal(goal)

    loaded_goal = state_manager.load_goal()
    assert loaded_goal == goal
