"""Subagent Loader - Load subagents from .claude/agents/ directory.

This module loads AgentDefinition configurations from markdown files in
the project's .claude/agents/ directory, similar to how developerz.ai does it.

Agent files use YAML frontmatter format:
---
name: agent-name
description: When to use this agent...
model: opus|sonnet|haiku
---

Agent prompt content here...
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import TYPE_CHECKING, Any

from . import console

if TYPE_CHECKING:
    pass


def parse_agent_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from agent markdown file.

    Args:
        content: Full content of the markdown file.

    Returns:
        Tuple of (frontmatter_dict, prompt_content).
    """
    # Match YAML frontmatter between --- markers
    frontmatter_pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(frontmatter_pattern, content, re.DOTALL)

    if not match:
        # No frontmatter, treat entire content as prompt
        return {}, content.strip()

    frontmatter_str = match.group(1)
    prompt = match.group(2).strip()

    # Parse simple YAML (key: value pairs)
    frontmatter: dict[str, Any] = {}
    for line in frontmatter_str.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            # Handle special values
            if value.lower() in ("true", "yes"):
                value = True
            elif value.lower() in ("false", "no"):
                value = False
            elif value.startswith("[") and value.endswith("]"):
                # Simple list parsing: [item1, item2]
                value = [v.strip().strip("\"'") for v in value[1:-1].split(",")]

            frontmatter[key] = value

    return frontmatter, prompt


def load_agents_from_directory(working_dir: str) -> dict[str, Any]:
    """Load all agent definitions from .claude/agents/ directory.

    Reads markdown files from {working_dir}/.claude/agents/ and converts
    them to AgentDefinition objects.

    Args:
        working_dir: The project working directory.

    Returns:
        Dictionary of agent_name -> AgentDefinition.
    """
    try:
        from claude_agent_sdk import AgentDefinition
    except ImportError:
        console.warning("claude_agent_sdk not installed - skipping subagent loading")
        return {}

    agents_dir = Path(working_dir) / ".claude" / "agents"

    if not agents_dir.exists():
        return {}

    agents: dict[str, Any] = {}

    for agent_file in agents_dir.glob("*.md"):
        try:
            content = agent_file.read_text(encoding="utf-8")
            frontmatter, prompt = parse_agent_frontmatter(content)

            # Get agent name from frontmatter or filename
            name = frontmatter.get("name") or agent_file.stem

            # Get description (required for Claude to know when to use it)
            description = frontmatter.get("description", "")
            if not description:
                console.warning(f"Agent '{name}' has no description - skipping")
                continue

            # Get optional model override
            model = frontmatter.get("model")
            if model and model not in ("opus", "sonnet", "haiku", "inherit"):
                console.warning(f"Agent '{name}' has invalid model '{model}' - using default")
                model = None

            # Get optional tools restriction
            tools = frontmatter.get("tools")
            if tools and not isinstance(tools, list):
                tools = None

            # Create AgentDefinition
            agent_def = AgentDefinition(
                description=description,
                prompt=prompt,
                model=model,
                tools=tools,
            )

            agents[name] = agent_def

        except Exception as e:
            console.warning(f"Failed to load agent from {agent_file}: {e}")
            continue

    return agents


def detect_claude_md(working_dir: str) -> bool:
    """Detect and log if CLAUDE.md exists in the working directory.

    Args:
        working_dir: The project working directory.

    Returns:
        True if CLAUDE.md was found, False otherwise.
    """
    claude_md_path = Path(working_dir) / "CLAUDE.md"

    if claude_md_path.exists():
        console.info(f"Found project instructions: {claude_md_path}")
        return True

    # Also check for lowercase variant
    claude_md_lower = Path(working_dir) / "claude.md"
    if claude_md_lower.exists():
        console.info(f"Found project instructions: {claude_md_lower}")
        return True

    return False


def detect_project_config(working_dir: str) -> dict[str, Any]:
    """Detect all Claude project configuration in the working directory.

    Logs what was found for visibility.

    Args:
        working_dir: The project working directory.

    Returns:
        Dictionary with detected configuration info.
    """
    result: dict[str, Any] = {
        "claude_md": False,
        "agents": {},
        "skills_dir": False,
    }

    # Detect CLAUDE.md
    result["claude_md"] = detect_claude_md(working_dir)

    # Detect .claude directory
    claude_dir = Path(working_dir) / ".claude"
    if claude_dir.exists():
        # Check for agents
        agents_dir = claude_dir / "agents"
        if agents_dir.exists():
            agent_files = list(agents_dir.glob("*.md"))
            if agent_files:
                agent_names = [f.stem for f in agent_files]
                console.info(f"Found {len(agent_files)} subagent(s): {', '.join(agent_names)}")

        # Check for skills
        skills_dir = claude_dir / "skills"
        if skills_dir.exists():
            skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
            if skill_dirs:
                skill_names = [d.name for d in skill_dirs]
                console.info(f"Found {len(skill_dirs)} skill(s): {', '.join(skill_names)}")
                result["skills_dir"] = True

    return result


def get_agents_for_working_dir(working_dir: str) -> dict[str, Any]:
    """Get all available agents for a working directory.

    This is the main entry point for loading subagents.
    Also detects and logs CLAUDE.md and other project config.

    Args:
        working_dir: The project working directory.

    Returns:
        Dictionary of agent_name -> AgentDefinition.
    """
    # Detect and log project configuration
    detect_project_config(working_dir)

    # Load and return agents
    return load_agents_from_directory(working_dir)
