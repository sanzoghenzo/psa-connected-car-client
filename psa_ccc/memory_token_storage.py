"""In-memory token storage."""
from __future__ import annotations

from authlib.oauth2.rfc6749 import OAuth2Token


class MemoryTokenStorage:
    """Store the token in memory."""

    def __init__(self) -> None:
        """Initialize the token storage."""
        self._token = None

    async def load(
        self, access_token: str | None = None, refresh_token: str | None = None
    ) -> OAuth2Token:
        """Load the token from storage."""
        return self._token

    async def save(self, token: OAuth2Token) -> None:
        """Save the token."""
        self._token = token
