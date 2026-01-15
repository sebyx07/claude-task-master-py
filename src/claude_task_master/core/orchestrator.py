"""Work Loop Orchestrator - Main loop driving work sessions until completion."""

from typing import Optional
from .agent import AgentWrapper
from .state import StateManager, TaskState
from .planner import Planner


class WorkLoopOrchestrator:
    """Orchestrates the main work loop."""

    def __init__(
        self,
        agent: AgentWrapper,
        state_manager: StateManager,
        planner: Planner,
    ):
        """Initialize orchestrator."""
        self.agent = agent
        self.state_manager = state_manager
        self.planner = planner

    def run(self) -> int:
        """Run the main work loop until completion or blocked."""
        state = self.state_manager.load_state()

        # Check if we've exceeded max sessions
        if state.options.max_sessions and state.session_count >= state.options.max_sessions:
            print(f"Max sessions ({state.options.max_sessions}) reached")
            return 1  # Blocked

        try:
            while not self._is_complete(state):
                # Run work session for current task
                self._run_work_session(state)

                # Check if we need to create/update PR
                # TODO: Implement PR cycle

                # Move to next task if current is complete
                # TODO: Implement task completion check

                # Increment session count
                state.session_count += 1
                self.state_manager.save_state(state)

                # Check session limit again
                if state.options.max_sessions and state.session_count >= state.options.max_sessions:
                    print(f"Max sessions ({state.options.max_sessions}) reached")
                    state.status = "blocked"
                    self.state_manager.save_state(state)
                    return 1

            # All tasks complete - verify success criteria
            if self._verify_success():
                state.status = "success"
                self.state_manager.save_state(state)
                self.state_manager.cleanup_on_success(state.run_id)
                return 0  # Success

            state.status = "blocked"
            self.state_manager.save_state(state)
            return 1  # Blocked

        except KeyboardInterrupt:
            state.status = "paused"
            self.state_manager.save_state(state)
            return 2  # User interrupted

        except Exception as e:
            print(f"Error: {e}")
            state.status = "failed"
            self.state_manager.save_state(state)
            return 1  # Error

    def _run_work_session(self, state: TaskState) -> None:
        """Run a single work session."""
        # TODO: Implement work session
        # - Get current task from plan
        # - Load context
        # - Run agent work session
        # - Log results
        # - Update progress
        pass

    def _is_complete(self, state: TaskState) -> bool:
        """Check if all tasks are complete."""
        # TODO: Parse plan.md and check if all tasks are marked as done
        return False

    def _verify_success(self) -> bool:
        """Verify success criteria are met."""
        criteria = self.state_manager.load_criteria()
        if not criteria:
            return True  # No criteria specified

        context = self.state_manager.load_context()
        result = self.agent.verify_success_criteria(criteria=criteria, context=context)

        return result.get("success", False)
