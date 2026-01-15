"""Agent Wrapper - Encapsulates all Claude Agent SDK interactions."""

from typing import Any, Optional
from enum import Enum


class ModelType(Enum):
    """Available Claude models."""

    SONNET = "sonnet"
    OPUS = "opus"
    HAIKU = "haiku"


class ToolConfig(Enum):
    """Tool configurations for different phases."""

    PLANNING = ["Read", "Glob", "Grep"]
    WORKING = ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]


class AgentWrapper:
    """Wraps Claude Agent SDK for task execution."""

    def __init__(self, access_token: str, model: ModelType):
        """Initialize agent wrapper."""
        self.access_token = access_token
        self.model = model
        # TODO: Initialize Claude Agent SDK

    def run_planning_phase(
        self, goal: str, context: str = ""
    ) -> dict[str, Any]:
        """Run planning phase with read-only tools."""
        # TODO: Implement planning phase
        # - Use only read-only tools (Read, Glob, Grep)
        # - Ask Claude to analyze the goal and create a task list
        # - Return plan with tasks and success criteria
        raise NotImplementedError

    def run_work_session(
        self,
        task_description: str,
        context: str = "",
        pr_comments: Optional[str] = None,
    ) -> dict[str, Any]:
        """Run a work session with full tools."""
        # TODO: Implement work session
        # - Use all working tools (Read, Write, Edit, Bash, Glob, Grep)
        # - Include PR comments in context if provided
        # - Return session results
        raise NotImplementedError

    def verify_success_criteria(
        self, criteria: str, context: str = ""
    ) -> dict[str, Any]:
        """Verify if success criteria are met."""
        # TODO: Implement success verification
        # - Use read-only tools to check criteria
        # - Return verification result
        raise NotImplementedError

    def get_tools_for_phase(self, phase: str) -> list[str]:
        """Get appropriate tools for the given phase."""
        if phase == "planning":
            return ToolConfig.PLANNING.value
        else:
            return ToolConfig.WORKING.value
