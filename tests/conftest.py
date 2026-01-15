"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_credentials():
    """Provide mock credentials for testing."""
    return {
        "accessToken": "test-access-token",
        "refreshToken": "test-refresh-token",
        "expiresAt": "2026-12-31T23:59:59Z",
        "tokenType": "Bearer",
    }
