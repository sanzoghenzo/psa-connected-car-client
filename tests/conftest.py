"""Fixtures for tests."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import httpx
import pytest
from psa_ccc import PSAClient
from psa_ccc import SimpleCacheStorage


@pytest.fixture
def client() -> PSAClient:
    http_client = httpx.AsyncClient(
        base_url="https://api.groupe-psa.com/connectedcar/v4"
    )
    yield PSAClient(client=http_client)


@pytest.fixture
def temp_storage() -> SimpleCacheStorage:
    with TemporaryDirectory() as temp_directory:
        yield SimpleCacheStorage(Path(temp_directory))
