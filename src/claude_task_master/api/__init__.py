"""REST API layer for Claude Task Master.

This module provides a FastAPI-based REST API that exposes claudetm functionality
as HTTP endpoints for remote task monitoring.

Currently Implemented Endpoints:
- GET /status: Get current task status
- GET /plan: Get task plan content
- GET /logs: Get log content
- GET /progress: Get progress summary
- GET /context: Get accumulated context/learnings
- GET /health: Health check endpoint

Usage:
    # Import and create the app
    from claude_task_master.api import create_app

    app = create_app()

    # Or run directly
    from claude_task_master.api import run_server

    run_server(host="0.0.0.0", port=8000)
"""

# API components - imported as they are implemented
from claude_task_master.api.models import (
    # Response models
    APIInfo,
    # Request models
    ConfigUpdateRequest,
    ContextResponse,
    ControlResponse,
    ErrorResponse,
    HealthResponse,
    # Enums
    LogFormat,
    LogLevel,
    LogsResponse,
    PauseRequest,
    PlanResponse,
    ProgressResponse,
    ResumeRequest,
    StopRequest,
    TaskDeleteResponse,
    TaskInitRequest,
    TaskInitResponse,
    TaskListItem,
    TaskListResponse,
    TaskOptionsResponse,
    TaskProgressInfo,
    TaskStatus,
    TaskStatusResponse,
    WorkflowStage,
)

# Routes
from claude_task_master.api.routes import create_info_router, register_routes

# Server components
from claude_task_master.api.server import create_app, get_app, run_server

__all__: list[str] = [
    # Server
    "create_app",
    "run_server",
    "get_app",
    # Enums
    "TaskStatus",
    "WorkflowStage",
    "LogLevel",
    "LogFormat",
    # Request models
    "PauseRequest",
    "StopRequest",
    "ResumeRequest",
    "ConfigUpdateRequest",
    "TaskInitRequest",
    # Response models
    "TaskStatusResponse",
    "TaskOptionsResponse",
    "TaskProgressInfo",
    "ControlResponse",
    "PlanResponse",
    "LogsResponse",
    "ProgressResponse",
    "ContextResponse",
    "TaskListItem",
    "TaskListResponse",
    "HealthResponse",
    "TaskInitResponse",
    "TaskDeleteResponse",
    "ErrorResponse",
    "APIInfo",
    # Routes
    "create_info_router",
    "register_routes",
]
