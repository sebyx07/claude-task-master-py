"""Tests for unified server module."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from claude_task_master.server import (
    MCP_PORT,
    MCP_TRANSPORT,
    REST_PORT,
    SERVER_HOST,
    _log_server_config,
    _run_mcp_server,
    _run_rest_server,
    _run_servers_async,
    _setup_signal_handlers,
    main,
    run_servers,
)

if TYPE_CHECKING:
    pass


class TestEnvironmentDefaults:
    """Tests for environment variable defaults."""

    def test_default_rest_port(self) -> None:
        """Test default REST port is 8000."""
        assert REST_PORT == 8000

    def test_default_mcp_port(self) -> None:
        """Test default MCP port is 8080."""
        assert MCP_PORT == 8080

    def test_default_host(self) -> None:
        """Test default host is localhost."""
        assert SERVER_HOST == "127.0.0.1"

    def test_default_mcp_transport(self) -> None:
        """Test default MCP transport is sse."""
        assert MCP_TRANSPORT == "sse"


class TestLogServerConfig:
    """Tests for server configuration logging."""

    def test_log_server_config_basic(self, caplog: pytest.LogCaptureFixture) -> None:
        """Test that server config is logged correctly."""
        import logging

        caplog.set_level(logging.INFO)

        _log_server_config(
            host="127.0.0.1",
            rest_port=8000,
            mcp_port=8080,
            mcp_transport="sse",
            auth_enabled=True,
            working_dir=Path("/tmp/test"),
        )

        assert "Claude Task Master Unified Server" in caplog.text
        assert "REST API Port: 8000" in caplog.text
        assert "MCP Server Port: 8080" in caplog.text
        assert "Password Auth: enabled" in caplog.text

    def test_log_server_config_auth_disabled_warning(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """Test warning when auth disabled on non-localhost."""
        import logging

        caplog.set_level(logging.WARNING)

        _log_server_config(
            host="0.0.0.0",
            rest_port=8000,
            mcp_port=8080,
            mcp_transport="sse",
            auth_enabled=False,
            working_dir=Path("/tmp/test"),
        )

        assert "without authentication" in caplog.text


class TestRunRestServer:
    """Tests for REST server runner."""

    @pytest.mark.asyncio
    async def test_run_rest_server_starts(self) -> None:
        """Test REST server starts correctly."""
        mock_server = AsyncMock()
        mock_server.serve = AsyncMock()

        with (
            patch("claude_task_master.api.server.create_app") as mock_create_app,
            patch("uvicorn.Config") as mock_config,
            patch("uvicorn.Server", return_value=mock_server),
        ):
            mock_create_app.return_value = MagicMock()

            await _run_rest_server(
                host="127.0.0.1",
                port=8000,
                working_dir=Path("/tmp"),
            )

            mock_create_app.assert_called_once()
            mock_config.assert_called_once()
            mock_server.serve.assert_awaited_once()


class TestRunMcpServer:
    """Tests for MCP server runner."""

    @pytest.mark.asyncio
    async def test_run_mcp_server_starts(self) -> None:
        """Test MCP server starts correctly."""
        mock_server = AsyncMock()
        mock_server.serve = AsyncMock()
        mock_mcp = MagicMock()
        mock_mcp.settings = MagicMock()

        with (
            patch(
                "claude_task_master.mcp.server.create_server", return_value=mock_mcp
            ) as mock_create,
            patch(
                "claude_task_master.mcp.server._get_authenticated_app",
                return_value=MagicMock(),
            ),
            patch("uvicorn.Config") as mock_config,
            patch("uvicorn.Server", return_value=mock_server),
        ):
            await _run_mcp_server(
                host="127.0.0.1",
                port=8080,
                working_dir=Path("/tmp"),
                transport="sse",
            )

            mock_create.assert_called_once()
            mock_config.assert_called_once()
            mock_server.serve.assert_awaited_once()


class TestSetupSignalHandlers:
    """Tests for signal handler setup."""

    def test_setup_signal_handlers(self) -> None:
        """Test signal handlers are set up correctly."""
        loop = asyncio.new_event_loop()
        try:
            # Should not raise
            _setup_signal_handlers(loop)
        finally:
            loop.close()


class TestRunServersAsync:
    """Tests for async server runner."""

    @pytest.mark.asyncio
    async def test_run_servers_async_creates_tasks(self) -> None:
        """Test that both server tasks are created."""
        # Create mock coroutines that complete immediately
        rest_called = False
        mcp_called = False

        async def mock_rest(*args: object, **kwargs: object) -> None:
            nonlocal rest_called
            rest_called = True

        async def mock_mcp(*args: object, **kwargs: object) -> None:
            nonlocal mcp_called
            mcp_called = True

        with (
            patch("claude_task_master.server._run_rest_server", side_effect=mock_rest),
            patch("claude_task_master.server._run_mcp_server", side_effect=mock_mcp),
        ):
            await _run_servers_async(
                rest_port=8000,
                mcp_port=8080,
                host="127.0.0.1",
                working_dir=Path("/tmp"),
                mcp_transport="sse",
                cors_origins=None,
                log_level="info",
            )

            assert rest_called
            assert mcp_called


class TestRunServers:
    """Tests for main run_servers function."""

    def test_run_servers_calls_event_loop(self) -> None:
        """Test that run_servers creates event loop correctly."""
        # Clean up any existing env var
        original = os.environ.pop("CLAUDETM_PASSWORD", None)

        try:
            mock_loop = MagicMock()
            mock_loop.run_until_complete = MagicMock(side_effect=KeyboardInterrupt)

            with (
                patch("claude_task_master.server.is_auth_enabled", return_value=False),
                patch("asyncio.new_event_loop", return_value=mock_loop),
                patch("asyncio.set_event_loop"),
            ):
                try:
                    run_servers(log_level="error")
                except KeyboardInterrupt:
                    pass

                mock_loop.run_until_complete.assert_called_once()
        finally:
            # Restore original value
            if original:
                os.environ["CLAUDETM_PASSWORD"] = original


class TestMainCli:
    """Tests for CLI main function."""

    def test_main_parses_args(self) -> None:
        """Test that main parses arguments correctly."""
        with (
            patch("sys.argv", ["claudetm-server", "--help"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        assert exc_info.value.code == 0

    def test_main_version(self) -> None:
        """Test --version flag."""
        with (
            patch("sys.argv", ["claudetm-server", "--version"]),
            pytest.raises(SystemExit) as exc_info,
        ):
            main()

        assert exc_info.value.code == 0

    def test_main_sets_password_env(self) -> None:
        """Test that --password sets environment variable."""
        original = os.environ.pop("CLAUDETM_PASSWORD", None)

        try:
            with (
                patch(
                    "sys.argv",
                    ["claudetm-server", "--password", "testpass", "--log-level", "error"],
                ),
                patch("claude_task_master.server.run_servers") as mock_run,
            ):
                main()

                # Check env var was set
                assert os.environ.get("CLAUDETM_PASSWORD") == "testpass"
                mock_run.assert_called_once()
        finally:
            # Restore original value
            os.environ.pop("CLAUDETM_PASSWORD", None)
            if original:
                os.environ["CLAUDETM_PASSWORD"] = original

    def test_main_parses_cors_origins(self) -> None:
        """Test that --cors-origins is parsed correctly."""
        with (
            patch(
                "sys.argv",
                [
                    "claudetm-server",
                    "--cors-origins",
                    "http://localhost:3000,http://example.com",
                ],
            ),
            patch("claude_task_master.server.run_servers") as mock_run,
        ):
            main()

            # Check cors_origins was parsed and passed
            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["cors_origins"] == [
                "http://localhost:3000",
                "http://example.com",
            ]

    def test_main_passes_all_args(self) -> None:
        """Test that all CLI args are passed to run_servers."""
        with (
            patch(
                "sys.argv",
                [
                    "claudetm-server",
                    "--host",
                    "0.0.0.0",
                    "--rest-port",
                    "9000",
                    "--mcp-port",
                    "9080",
                    "--mcp-transport",
                    "streamable-http",
                    "--working-dir",
                    "/tmp/work",
                    "--log-level",
                    "debug",
                ],
            ),
            patch("claude_task_master.server.run_servers") as mock_run,
        ):
            main()

            call_kwargs = mock_run.call_args[1]
            assert call_kwargs["host"] == "0.0.0.0"
            assert call_kwargs["rest_port"] == 9000
            assert call_kwargs["mcp_port"] == 9080
            assert call_kwargs["mcp_transport"] == "streamable-http"
            assert call_kwargs["working_dir"] == "/tmp/work"
            assert call_kwargs["log_level"] == "debug"
