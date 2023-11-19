"""PSA Connected Car Client."""
from __future__ import annotations

from pathlib import Path

from httpx import AsyncClient

from psa_ccc.apk_parser import ConfigInfo
from psa_ccc.apk_parser import first_launch
from psa_ccc.auth import TokenStorage
from psa_ccc.auth import oauth_factory
from psa_ccc.brand_config import BRAND_CONFIG_MAP
from psa_ccc.client import PSAClient
from psa_ccc.memory_token_storage import MemoryTokenStorage
from psa_ccc.storage import CacheStorage
from psa_ccc.storage import SimpleCacheStorage

__version__ = "v0.1.2"


async def create_psa_client(
    brand: str,
    country_code: str,
    email: str,
    password: str,
    cache_storage: CacheStorage | None = None,
    token_storage: TokenStorage | None = None,
) -> PSAClient:
    cache_storage = cache_storage or SimpleCacheStorage(Path("."))
    token_storage = token_storage or MemoryTokenStorage()
    config = await get_config(brand, email, password, country_code, cache_storage)
    brand_config = BRAND_CONFIG_MAP[brand]
    oauth_client = await oauth_factory(
        config.client_id,
        config.client_secret,
        email,
        password,
        brand_config.access_token_url,
        brand_config.realm,
        token_storage,
    )
    return PSAClient(client=oauth_client)


async def get_config(
    brand: str, email: str, password: str, country_code: str, storage: CacheStorage
) -> ConfigInfo:
    """Retrieve the configuration for the first-time launch."""
    async with AsyncClient() as http_client:
        return await first_launch(
            http_client, brand, email, password, country_code, storage
        )
