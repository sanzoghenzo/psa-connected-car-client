"""OAuth2 client tests."""
from __future__ import annotations

import pytest
from httpx import URL
from psa_ccc.auth import create_client
from psa_ccc.memory_token_storage import MemoryTokenStorage


@pytest.mark.asyncio
async def test_create_client() -> None:
    """Dummy test."""
    storage = MemoryTokenStorage()
    client = await create_client("myId", "mySecret", "myTokenUrl", "myRealm", storage)
    assert client.client_id == "myId"
    assert client.client_secret == "mySecret"
    assert client.metadata["token_endpoint"] == "myTokenUrl"
    assert client.scope == "openid profile"
    assert client.base_url == URL("https://api.groupe-psa.com/connectedcar/v4/")
