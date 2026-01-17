"""GitHub integration module.

This module provides a complete GitHub integration layer using the gh CLI.
The main entry point is GitHubClient which provides all GitHub operations.

Module structure:
- client.py: Main GitHubClient with initialization, merge, and mixin delegation
- client_pr.py: PR operations mixin (create, status, comments)
- client_ci.py: CI operations mixin (workflows, status, logs)
- exceptions.py: All GitHub-related exception classes
"""

from .client import DEFAULT_GH_TIMEOUT, GitHubClient, PRStatus, WorkflowRun
from .exceptions import (
    GitHubAuthError,
    GitHubError,
    GitHubMergeError,
    GitHubNotFoundError,
    GitHubTimeoutError,
)

__all__ = [
    "DEFAULT_GH_TIMEOUT",
    "GitHubAuthError",
    "GitHubClient",
    "GitHubError",
    "GitHubMergeError",
    "GitHubNotFoundError",
    "GitHubTimeoutError",
    "PRStatus",
    "WorkflowRun",
]
