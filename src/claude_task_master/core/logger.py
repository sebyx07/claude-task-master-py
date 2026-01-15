"""Logger - Single consolidated log file per run."""

from datetime import datetime
from pathlib import Path
from typing import Any


class TaskLogger:
    """Manages logging for task execution."""

    def __init__(self, log_file: Path):
        """Initialize logger."""
        self.log_file = log_file
        self.current_session: int | None = None
        self.session_start: datetime | None = None

    def start_session(self, session_number: int, phase: str) -> None:
        """Start logging a new session."""
        self.current_session = session_number
        self.session_start = datetime.now()

        self._write_separator()
        self._write(f"SESSION {session_number} - {phase.upper()}")
        self._write(f"Started: {self.session_start.isoformat()}")
        self._write_separator()

    def log_prompt(self, prompt: str) -> None:
        """Log the prompt sent to Claude."""
        self._write("\n=== PROMPT ===")
        self._write(prompt)
        self._write("")

    def log_response(self, response: str) -> None:
        """Log Claude's response."""
        self._write("\n=== RESPONSE ===")
        self._write(response)
        self._write("")

    def log_tool_use(self, tool_name: str, parameters: dict[str, Any]) -> None:
        """Log tool usage."""
        self._write(f"\n--- Tool: {tool_name} ---")
        self._write(str(parameters))

    def log_tool_result(self, tool_name: str, result: Any) -> None:
        """Log tool result."""
        self._write(f"\n--- Result: {tool_name} ---")
        self._write(str(result))
        self._write("")

    def end_session(self, outcome: str) -> None:
        """End the current session."""
        if self.session_start:
            duration = datetime.now() - self.session_start
            self._write(f"\nOutcome: {outcome}")
            self._write(f"Duration: {duration.total_seconds():.2f}s")
            self._write_separator()
            self._write("")

        self.current_session = None
        self.session_start = None

    def log_error(self, error: str) -> None:
        """Log an error."""
        self._write("\n!!! ERROR !!!")
        self._write(error)
        self._write("")

    def _write(self, message: str) -> None:
        """Write message to log file."""
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def _write_separator(self) -> None:
        """Write a separator line."""
        self._write("=" * 80)
