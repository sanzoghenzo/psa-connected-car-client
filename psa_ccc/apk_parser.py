"""Android APK parser."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
from pyaxmlparser.core import APK
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from httpx import AsyncClient
from msgspec import Struct
from msgspec.json import decode
from msgspec.json import encode

from psa_ccc.brand_config import BRAND_CONFIG_MAP
from psa_ccc.github import CacheStorage
from psa_ccc.github import GitHubUrlsBuilder
from psa_ccc.github import download_github_file

APP_VERSION = "1.33.0"
GITHUB_OWNER = "flobz"
GITHUB_REPO = "psa_apk"


class ConfigInfo(Struct):
    """Information extracted from the Android app."""

    client_id: str
    client_secret: str
    site_code: str
    brand_id: str
    culture: str
    public_key: bytes | None
    private_key: bytes | None
    user_id: str = ""  # used for MQTT

    @property
    def access_token_url(self) -> str:
        """URL of the access token."""
        return f"{self.brand_id}/GetAccessToken"


async def get_content_from_apk(
    client: AsyncClient,
    filename: str,
    country_code: str,
    site_code: str,
    storage: CacheStorage,
) -> ConfigInfo:
    """
    Returns the needed information from the APK.

    Args:
        client: async http client
        filename: name of the APK file to download
        country_code: country code
        site_code: site code
        storage: file storage handler

    Returns:
        Configuration data for the PSA client
    """
    url_builder = GitHubUrlsBuilder(GITHUB_OWNER, GITHUB_REPO, "", filename)
    await download_github_file(client, storage, url_builder)
    apk_bytes = storage.read(filename)
    return retrieve_content_from_apk(apk_bytes, country_code, site_code)


def retrieve_content_from_apk(
    apk_bytes: bytes, country_code: str, site_code: str
) -> ConfigInfo:
    """
    Return the configuration information from an APK file.

    Args:
        apk_bytes: contents of APK file
        country_code: country code
        site_code: site code

    Returns:
        Configuration data for the PSA client.
    """
    apk = APK(apk_bytes, raw=True)
    package_name = apk.get_package()
    resources = apk.get_android_resources()
    culture = _get_cultures_code(
        apk.get_file("res/raw/cultures.json"), country_code
    )
    parameters = json.loads(apk.get_file(_get_parameters_path(culture)))

    pfx_cert = apk.get_file("assets/MWPMYMA1.pfx")
    public, private = get_keys(pfx_cert, b"y5Y2my5B")

    client_secret = parameters["cvsSecret"]
    client_id = parameters["cvsClientId"]
    brand_id_url = resources.get_string(package_name, "HOST_BRANDID_PROD")[1]
    return ConfigInfo(
        client_id=client_id,
        client_secret=client_secret,
        site_code=site_code,
        brand_id=brand_id_url,
        culture=culture,
        public_key=public,
        private_key=private,
    )


def _get_cultures_code(file: bytes, country_code: str) -> str:
    cultures = json.loads(file)
    return cultures[country_code]["languages"][0]


def _get_parameters_path(culture: str) -> str:
    language, country = culture.split("_")
    return f"res/raw-{language}-r{country}/parameters.json"


def get_keys(
    pfx_data: bytes, pfx_password: bytes
) -> tuple[bytes | None, bytes | None]:
    """
    Returns the public and private keys from a pfx certificate.

    Args:
        pfx_data: pfx certificate
        pfx_password: pfx password

    Returns:
        public and private keys
    """
    private_key, certificate = pkcs12.load_key_and_certificates(
        pfx_data, pfx_password, default_backend()
    )[:2]
    public = (
        None
        if certificate is None
        else certificate.public_bytes(encoding=serialization.Encoding.PEM)
    )
    private = (
        None
        if private_key is None
        else private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )
    return public, private


async def first_launch(
    client: AsyncClient,
    brand: str,
    email: str,
    password: str,
    country_code: str,
) -> ConfigInfo:
    """
    Retrieves the configuration for the API client from the Android app.

    Args:
        client: async http client
        brand: car brand
        email: user email
        password: user password
        country_code: country code

    Returns:
        Configuration from the Android app.
    """
    brand_config = BRAND_CONFIG_MAP[brand]
    site_code = brand_config.site_code(country_code)
    storage = CacheStorage(Path(__file__).parent)
    config_path = "config.json"
    if storage.exists(config_path):
        return decode(storage.read(config_path), type=ConfigInfo)
    apk_info = await get_content_from_apk(
        client, brand_config.apk_name, country_code, site_code, storage
    )
    token = await _get_access_token(client, apk_info, email, password)
    cert = _save_certs(apk_info, storage)
    res_dict = await _get_user(brand_config.user_url, apk_info, token, cert)
    # this is used in mqtt paths with brand code
    apk_info.user_id = res_dict["id"]
    storage.save(encode(apk_info), config_path)
    return apk_info


async def _get_access_token(
    client: AsyncClient, apk_info: ConfigInfo, email: str, password: str
) -> str:
    res = await client.post(
        apk_info.access_token_url,
        headers={
            "Connection": "Keep-Alive",
            "Content-Type": "application/json",
            "User-Agent": "okhttp/2.3.0",
        },
        params={
            "jsonRequest": json.dumps(
                {
                    "siteCode": apk_info.site_code,
                    "culture": "fr-FR",
                    "action": "authenticate",
                    "fields": {
                        "USR_EMAIL": {"value": email},
                        "USR_PASSWORD": {"value": password},
                    },
                }
            )
        },
    )
    return res.json()["accessToken"]


async def _get_user(
    user_url: str, apk_info: ConfigInfo, token: str, cert: tuple[str, str]
) -> dict[str, Any]:
    async with httpx.AsyncClient(cert=cert) as client:
        res = await client.post(
            user_url,
            params={
                "culture": apk_info.culture,
                "width": 1080,
                "version": APP_VERSION,
            },
            json={"site_code": apk_info.site_code, "ticket": token},
            headers={
                "Connection": "Keep-Alive",
                "Content-Type": "application/json;charset=UTF-8",
                "Source-Agent": "App-Android",
                "Token": token,
                "User-Agent": "okhttp/4.8.0",
                "Version": APP_VERSION,
            },
        )
        return res.json()["success"]


def _save_certs(apk_info: ConfigInfo, storage: CacheStorage) -> tuple[str, str]:
    if apk_info.public_key:
        storage.save(apk_info.public_key, "public.pem")
    if apk_info.private_key:
        storage.save(apk_info.private_key, "private.pem")
    return str(storage.get_full_path("public.pem")), str(
        storage.get_full_path("private.pem")
    )
