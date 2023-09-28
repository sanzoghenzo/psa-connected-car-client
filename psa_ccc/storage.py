"""Storage Handler."""
from __future__ import annotations

from hashlib import sha1
from pathlib import Path
from typing import Protocol


class CacheStorage(Protocol):
    """Storage cache interface."""

    def get_full_path(self, filename: str) -> Path:
        """Returns the full path of the given filename."""

    def exists(self, filename: str) -> bool:
        """Returns True if the given filename exists."""

    def read(self, filename: str) -> bytes:
        """Reads the contents of the file."""

    def get_sha(self, filename: str) -> str:
        """Returns the SHA of the given file."""

    def save(self, data: bytes, filename: str) -> None:
        """Save the data to the given file."""


class SimpleCacheStorage:
    """Simple file storage implementation."""

    def __init__(self, cache_directory: Path) -> None:
        """Sets the cache directory."""
        self.cache_directory = cache_directory

    def get_full_path(self, filename: str) -> Path:
        """Returns the full path of the given filename."""
        return self.cache_directory.joinpath(filename).resolve()

    def exists(self, filename: str) -> bool:
        """Returns True if the given filename exists."""
        return self.get_full_path(filename).exists()

    def read(self, filename: str) -> bytes:
        """Reads the contents of the file."""
        if self.exists(filename):
            return self.get_full_path(filename).read_bytes()
        raise FileNotFoundError(filename)

    def get_sha(self, filename: str) -> str:
        """Returns the SHA of the given file."""
        data = self.read(filename)
        prefix = f"blob {len(data)}\u0000"
        return sha1(prefix.encode("utf-8") + data).hexdigest()  # noqa S324

    def save(self, data: bytes, filename: str) -> None:
        """Save the data to the given file."""
        full_path = self.get_full_path(filename)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(data)
