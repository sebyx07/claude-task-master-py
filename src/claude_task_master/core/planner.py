"""Planner - Orchestrates initial planning phase (read-only tools)."""

from typing import Any

from .agent import AgentWrapper
from .state import StateManager


class Planner:
    """Handles the initial planning phase."""

    def __init__(self, agent: AgentWrapper, state_manager: StateManager):
        """Initialize planner."""
        self.agent = agent
        self.state_manager = state_manager

    def create_plan(self, goal: str) -> dict[str, Any]:
        """Create initial task plan using read-only tools."""
        # Load any existing context
        context = self.state_manager.load_context()

        # Run planning phase with Claude
        result = self.agent.run_planning_phase(goal=goal, context=context)

        # Extract plan and criteria from result
        plan = result.get("plan", "")
        criteria = result.get("criteria", "")

        # Save to state
        if plan:
            self.state_manager.save_plan(plan)
        if criteria:
            self.state_manager.save_criteria(criteria)

        return result

    def update_plan_progress(self, task_index: int, completed: bool) -> None:
        """Update task completion status in plan."""
        plan = self.state_manager.load_plan()
        if not plan:
            return

        # TODO: Parse markdown checkboxes and update status
        # This will require parsing the plan.md file and toggling checkboxes

        self.state_manager.save_plan(plan)
