"""GitHub download handler."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from httpx import AsyncClient

from psa_ccc.storage import CacheStorage

logger = logging.getLogger(__name__)


@dataclass
class GitHubUrlsBuilder:
    """Builds URLs for GitHub download and SHA1 checks."""

    owner: str
    repo: str
    directory: str
    filename: str
    branch: str = "main"

    @property
    def raw_url(self) -> str:
        """URL for raw file download."""
        return f"https://github.com/{self.owner}/{self.repo}/raw/{self.branch}/{self.directory}/{self.filename}"

    @property
    def dir_sha_url(self) -> str:
        """URL  for SHA checksums of files in the directory."""
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/git/trees/{self.branch}:{self.directory}"


async def download_github_file(
    client: AsyncClient,
    storage: CacheStorage,
    url_builder: GitHubUrlsBuilder,
) -> None:
    """
    Download a file from GitHub.

    Args:
        client: async http client
        storage: storage cache for downloaded files
        url_builder: GitHubUrlsBuilder
    """
    filename = url_builder.filename
    if not await needs_download(client, storage, url_builder.dir_sha_url, filename):
        return
    response = await client.get(
        url_builder.raw_url,
        follow_redirects=True,
        headers={"Accept": "application/vnd.github.VERSION.raw"},
    )
    storage.save(response.content, filename)


async def needs_download(
    client: AsyncClient, storage: CacheStorage, sha_url: str, filename: str
) -> bool:
    """
    Returns True if the GitHub file needs to be downloaded.

    Args:
        client: async http client
        storage: storage cache for downloaded files
        sha_url: url of sha checksums for files in the parent directory
        filename: name of the file to check

    Returns:
        True if the GitHub file needs to be downloaded.
    """
    if not storage.exists(filename):
        return True
    try:
        github_sha = await _get_sha(client, sha_url, filename)
    except ValueError:
        return True
    return storage.get_sha(filename) != github_sha


async def _get_sha(client: AsyncClient, sha_url: str, filename: str) -> str:
    """
    Returns the SHA1 sum of a file on GitHub.

    Args:
        client: async http client
        sha_url: url of sha checksums for files in the parent directory
        filename: name of the file to check

    Returns:
        SHA1 sum of the file on GitHub.
    """
    res = await client.get(sha_url)
    data = res.json()
    try:
        file_info = next(
            file for file in data.get("tree", []) if file.get("path") == filename
        )
    except StopIteration as err:
        logger.error("can't get SHA for github file: %s", res)
        raise ValueError from err
    return file_info["sha"]
