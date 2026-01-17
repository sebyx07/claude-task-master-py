"""GitHub Exception Classes - All GitHub-related exceptions."""


class GitHubError(Exception):
    """Base exception for GitHub operations."""

    def __init__(
        self, message: str, command: list[str] | None = None, exit_code: int | None = None
    ):
        super().__init__(message)
        self.message = message
        self.command = command
        self.exit_code = exit_code

    def __str__(self) -> str:
        return self.message


class GitHubTimeoutError(GitHubError):
    """Raised when a gh CLI command times out."""

    pass


class GitHubAuthError(GitHubError):
    """Raised when gh CLI is not authenticated."""

    pass


class GitHubNotFoundError(GitHubError):
    """Raised when gh CLI is not installed."""

    pass


class GitHubMergeError(GitHubError):
    """Raised when PR merge fails."""

    pass
