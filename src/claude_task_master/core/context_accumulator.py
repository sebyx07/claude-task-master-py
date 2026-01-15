"""Context Accumulator - Builds up learnings across sessions."""

from .state import StateManager


class ContextAccumulator:
    """Accumulates context and learnings across sessions."""

    def __init__(self, state_manager: StateManager):
        """Initialize context accumulator."""
        self.state_manager = state_manager

    def add_learning(self, learning: str) -> None:
        """Add a new learning to the context."""
        current_context = self.state_manager.load_context()

        if current_context:
            updated_context = f"{current_context}\n\n## New Learning\n\n{learning}"
        else:
            updated_context = f"# Accumulated Context\n\n## Learning\n\n{learning}"

        self.state_manager.save_context(updated_context)

    def add_session_summary(self, session_number: int, summary: str) -> None:
        """Add a session summary to the context."""
        current_context = self.state_manager.load_context()

        session_entry = f"## Session {session_number}\n\n{summary}"

        if current_context:
            updated_context = f"{current_context}\n\n{session_entry}"
        else:
            updated_context = f"# Accumulated Context\n\n{session_entry}"

        self.state_manager.save_context(updated_context)

    def get_context_for_prompt(self) -> str:
        """Get formatted context for including in prompts."""
        context = self.state_manager.load_context()

        if not context:
            return ""

        return f"\n\n# Previous Context\n\n{context}"
