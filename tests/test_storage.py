"""Simple Cache Storage tests."""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from psa_ccc.storage import SimpleCacheStorage


@pytest.fixture
def temp_storage() -> SimpleCacheStorage:
    with TemporaryDirectory() as temp_directory:
        yield SimpleCacheStorage(Path(temp_directory))


def test_file_doesnt_exist(temp_storage: SimpleCacheStorage) -> None:
    assert not temp_storage.exists("test")


def test_read_not_existing_file_raises(
    temp_storage: SimpleCacheStorage,
) -> None:
    with pytest.raises(FileNotFoundError):
        temp_storage.read("test")


def test_roundtrip(temp_storage: SimpleCacheStorage) -> None:
    data = b"test"
    filename = "test.txt"
    temp_storage.save(data, filename)
    assert temp_storage.read(filename) == data


def test_sha(temp_storage: SimpleCacheStorage) -> None:
    filename = "test.txt"
    temp_storage.save(b"test", filename)
    actual = temp_storage.get_sha(filename)
    assert actual == "30d74d258442c7c65512eafab474568dd706c430"
