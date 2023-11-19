"""OAuth session factory."""
from __future__ import annotations

from typing import Any
from typing import Protocol

from authlib.common.urls import add_params_to_uri
from authlib.integrations.httpx_client import AsyncOAuth2Client
from authlib.oauth2.rfc6749 import OAuth2Token


class TokenStorage(Protocol):
    """Token storage interface."""

    async def load(
        self, access_token: str | None = None, refresh_token: str | None = None
    ) -> OAuth2Token:
        """Load the token from storage."""

    async def save(self, token: OAuth2Token) -> None:
        """Save the token."""


async def create_client(
    client_id: str,
    client_secret: str,
    token_url: str,
    realm: str,
    token_storage: TokenStorage,
) -> AsyncOAuth2Client:
    """
    Create the OAuth session handler for the API client.

    Args:
        client_id: client ID
        client_secret: client secret
        token_url: URL for token refresh
        realm: API realm
        token_storage: token storage handler

    Returns:
        OAuth session
    """

    async def update_token(
        new_token: dict[str, Any],
        refresh_token: str | None = None,
        access_token: str | None = None,
    ) -> None:
        item = await token_storage.load(
            access_token=access_token, refresh_token=refresh_token
        )
        item["access_token"] = new_token["access_token"]
        item["refresh_token"] = new_token.get("refresh_token")
        await token_storage.save(item)

    def _fix_request(
        url: str, headers: dict[str, Any], body: Any
    ) -> tuple[str, dict[str, Any], Any]:
        params = {"client_id": client_id}
        url = add_params_to_uri(url, params)
        headers["x-introspect-realm"] = realm
        if "Accept" not in headers:
            headers["Accept"] = "application/hal+json"
        return url, headers, body

    # authorize = "https://api.mpsa.com/api/connectedcar/v2/oauth/authorize"
    client = AsyncOAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        scope="openid profile",
        token_endpoint=token_url,
        update_token=update_token,
        base_url="https://api.groupe-psa.com/connectedcar/v4",
    )
    client.register_compliance_hook("protected_request", _fix_request)
    return client


async def oauth_factory(
    client_id: str,
    client_secret: str,
    username: str,
    password: str,
    token_url: str,
    realm: str,
    token_storage: TokenStorage,
) -> AsyncOAuth2Client:  # pragma: no cover
    """
    Create the OAuth session handler for the API client.

    Args:
        client_id: client ID
        client_secret: client secret
        username: username
        password: password
        token_url: URL for token refresh
        realm: API realm
        token_storage: token storage handler

    Returns:
        OAuth session
    """
    client = await create_client(
        client_id, client_secret, token_url, realm, token_storage
    )

    token = await client.fetch_token(
        token_url,
        username=username,
        password=password,
        grant_type="password",
        realm=realm,
    )
    await token_storage.save(token)
    return client
