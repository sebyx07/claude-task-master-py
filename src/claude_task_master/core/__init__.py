"""Core module - exports key classes and exceptions."""

from claude_task_master.core.credentials import (
    CredentialError,
    CredentialNotFoundError,
    InvalidCredentialsError,
    CredentialPermissionError,
    TokenRefreshError,
    NetworkTimeoutError,
    NetworkConnectionError,
    TokenRefreshHTTPError,
    InvalidTokenResponseError,
    Credentials,
    CredentialManager,
)

from claude_task_master.core.agent import (
    AgentError,
    SDKImportError,
    SDKInitializationError,
    QueryExecutionError,
    APIRateLimitError,
    APIConnectionError,
    APITimeoutError,
    APIAuthenticationError,
    APIServerError,
    WorkingDirectoryError,
    ModelType,
    ToolConfig,
    AgentWrapper,
)

__all__ = [
    # Credential exceptions
    "CredentialError",
    "CredentialNotFoundError",
    "InvalidCredentialsError",
    "CredentialPermissionError",
    "TokenRefreshError",
    "NetworkTimeoutError",
    "NetworkConnectionError",
    "TokenRefreshHTTPError",
    "InvalidTokenResponseError",
    # Credential classes
    "Credentials",
    "CredentialManager",
    # Agent exceptions
    "AgentError",
    "SDKImportError",
    "SDKInitializationError",
    "QueryExecutionError",
    "APIRateLimitError",
    "APIConnectionError",
    "APITimeoutError",
    "APIAuthenticationError",
    "APIServerError",
    "WorkingDirectoryError",
    # Agent classes
    "ModelType",
    "ToolConfig",
    "AgentWrapper",
]
