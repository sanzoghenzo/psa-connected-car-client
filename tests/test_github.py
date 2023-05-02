"""GitHub related tests."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any

import pytest
from psa_ccc.github import GitHubUrlsBuilder
from psa_ccc.github import download_github_file
from psa_ccc.github import needs_download


@dataclass
class FakeCacheStorage:
    """Dictionary based cache storage."""

    files: dict[str, dict[str, str | bytes]] = field(default_factory=dict)

    def get_full_path(self, filename: str) -> Path:
        """Returns the full path of the given filename."""
        return Path(filename)

    def exists(self, filename: str) -> bool:
        """Returns True if the given filename exists."""
        return filename in self.files

    def read(self, filename: str) -> bytes:
        """Reads the contents of the file."""
        if self.exists(filename):
            return self.files[filename]["content"]
        raise FileNotFoundError(filename)

    def get_sha(self, filename: str) -> str:
        """Returns the SHA of the given file."""
        if self.exists(filename):
            return self.files[filename]["sha"]
        raise FileNotFoundError(filename)

    def save(self, data: bytes, filename: str) -> None:
        """Save the data to the given file."""
        self.files[filename] = {"content": data, "sha": "sha"}


@dataclass
class FakeResponse:
    """Fake HTTP response."""

    data: dict[str, Any] | None
    content: bytes | None

    def json(self) -> dict[str, Any]:
        """Fake response JSON data."""
        return self.data


@dataclass
class FakeClient:
    """Fake HTTP client."""

    file: str = "test.apk"

    async def get(self, url: str, **kwargs: Any) -> FakeResponse:
        """Simulates a GET request."""
        if self.file in url:
            return FakeResponse(None, b"Test content")
        return FakeResponse({"tree": [{"path": self.file, "sha": "sha"}]}, None)


@pytest.mark.asyncio
async def test_download_github_file() -> None:
    """File is downloaded if it doesn't exist yet."""
    url_builder = GitHubUrlsBuilder(
        "sanzoghenzo", "psa_connected_car_client", "", "test.apk"
    )
    storage = FakeCacheStorage()
    client = FakeClient()
    await download_github_file(client, storage, url_builder)  # type: ignore
    assert "test.apk" in storage.files
    assert storage.files["test.apk"]["content"] == b"Test content"


@pytest.mark.asyncio
async def test_download_github_file_no_need() -> None:
    """File is not downloaded if exists and matches the sha."""
    url_builder = GitHubUrlsBuilder(
        "sanzoghenzo", "psa_connected_car_client", "", "test.apk"
    )
    storage = FakeCacheStorage({"test.apk": {"content": b"Test content", "sha": "sha"}})
    client = FakeClient()
    await download_github_file(client, storage, url_builder)  # type: ignore


@pytest.mark.asyncio
async def test_needs_download_false() -> None:
    """Existing file with the right sha."""
    storage = FakeCacheStorage({"test.apk": {"content": b"Test content", "sha": "sha"}})
    client = FakeClient()
    needs = await needs_download(client, storage, "fake_url", "test.apk")  # type: ignore
    assert not needs


@pytest.mark.asyncio
async def test_needs_download_old_sha() -> None:
    """Existing file with the right sha."""
    storage = FakeCacheStorage(
        {"test.apk": {"content": b"Test content", "sha": "oldSha"}}
    )
    client = FakeClient()
    needs = await needs_download(client, storage, "fake_url", "test.apk")  # type: ignore
    assert needs


@pytest.mark.asyncio
async def test_needs_download_doesnt_exist() -> None:
    """Existing file with the right sha."""
    storage = FakeCacheStorage(
        {"missing.apk": {"content": b"Test content", "sha": "sha"}}
    )
    client = FakeClient()
    needs = await needs_download(client, storage, "fake_url", "missing.apk")  # type: ignore
    assert needs
