"""Credential Manager - OAuth credential loading, validation, and refresh."""

from pathlib import Path
from typing import Optional
from datetime import datetime
import json
import httpx
from pydantic import BaseModel


class Credentials(BaseModel):
    """OAuth credentials model."""

    accessToken: str
    refreshToken: str
    expiresAt: str
    tokenType: str = "Bearer"


class CredentialManager:
    """Manages OAuth credentials from ~/.claude/.credentials.json."""

    CREDENTIALS_PATH = Path.home() / ".claude" / ".credentials.json"
    OAUTH_TOKEN_URL = "https://api.anthropic.com/v1/oauth/token"

    def load_credentials(self) -> Credentials:
        """Load credentials from file."""
        if not self.CREDENTIALS_PATH.exists():
            raise FileNotFoundError(
                f"Credentials not found at {self.CREDENTIALS_PATH}. "
                "Please run 'claude' CLI first to authenticate."
            )

        with open(self.CREDENTIALS_PATH) as f:
            data = json.load(f)

        return Credentials(**data)

    def is_expired(self, credentials: Credentials) -> bool:
        """Check if access token is expired."""
        expires_at = datetime.fromisoformat(credentials.expiresAt.replace("Z", "+00:00"))
        return datetime.now(expires_at.tzinfo) >= expires_at

    def refresh_access_token(self, credentials: Credentials) -> Credentials:
        """Refresh access token using refresh token."""
        response = httpx.post(
            self.OAUTH_TOKEN_URL,
            json={
                "grant_type": "refresh_token",
                "refresh_token": credentials.refreshToken,
            },
            timeout=30.0,
        )
        response.raise_for_status()

        token_data = response.json()
        new_credentials = Credentials(
            accessToken=token_data["access_token"],
            refreshToken=token_data.get("refresh_token", credentials.refreshToken),
            expiresAt=token_data["expires_at"],
            tokenType=token_data.get("token_type", "Bearer"),
        )

        self._save_credentials(new_credentials)
        return new_credentials

    def _save_credentials(self, credentials: Credentials) -> None:
        """Save updated credentials to file."""
        with open(self.CREDENTIALS_PATH, "w") as f:
            json.dump(credentials.model_dump(), f, indent=2)

    def get_valid_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        credentials = self.load_credentials()

        if self.is_expired(credentials):
            credentials = self.refresh_access_token(credentials)

        return credentials.accessToken
