"""Android APK parser."""
from __future__ import annotations

import json
from typing import Any

import httpx
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import pkcs12
from httpx import AsyncClient
from msgspec import Struct
from msgspec.json import decode
from msgspec.json import encode
from pyaxmlparser.core import APK

from psa_ccc.brand_config import BRAND_CONFIG_MAP
from psa_ccc.github import GitHubUrlsBuilder
from psa_ccc.github import download_github_file
from psa_ccc.storage import CacheStorage

APP_VERSION = "1.33.0"
GITHUB_OWNER = "flobz"
GITHUB_REPO = "psa_apk"
PFX_PASSWORD = b"y5Y2my5B"


class ConfigInfo(Struct):
    """Information extracted from the Android app."""

    client_id: str
    client_secret: str
    site_code: str
    brand_id: str
    culture: str
    public_certificate: bytes | None
    private_key: bytes | None
    user_id: str = ""  # used for MQTT

    @property
    def access_token_url(self) -> str:
        """URL of the access token."""
        return f"{self.brand_id}/GetAccessToken"


async def download_apk(
    client: AsyncClient,
    filename: str,
    storage: CacheStorage,
) -> APK:
    """
    Returns the needed information from the APK.

    Args:
        client: async http client
        filename: name of the APK file to download
        storage: file storage handler

    Returns:
        Configuration data for the PSA client
    """
    url_builder = GitHubUrlsBuilder(GITHUB_OWNER, GITHUB_REPO, "", filename)
    await download_github_file(client, storage, url_builder)
    apk_bytes = storage.read(filename)
    return APK(apk_bytes, raw=True)


def get_config_from_apk(apk: APK, country_code: str, site_code: str) -> ConfigInfo:
    """
    Return the configuration information from an APK file.

    Args:
        apk: APK
        country_code: country code
        site_code: site code

    Returns:
        Configuration data for the PSA client.
    """
    package_name = apk.get_package()
    resources = apk.get_android_resources()
    culture = _get_cultures_code(apk.get_file("res/raw/cultures.json"), country_code)
    parameters = json.loads(apk.get_file(_get_parameters_path(culture)))

    pfx_cert = apk.get_file("assets/MWPMYMA1.pfx")
    public, private = get_keys(pfx_cert, PFX_PASSWORD)

    brand_id_url = resources.get_string(package_name, "HOST_BRANDID_PROD")[1]
    return ConfigInfo(
        client_id=parameters["cvsClientId"],
        client_secret=parameters["cvsSecret"],
        site_code=site_code,
        brand_id=brand_id_url,
        culture=culture,
        public_certificate=public,
        private_key=private,
    )


def _get_cultures_code(file: bytes, country_code: str) -> str:
    cultures = json.loads(file)
    return cultures[country_code]["languages"][0]


def _get_parameters_path(culture: str) -> str:
    language, country = culture.split("_")
    return f"res/raw-{language}-r{country}/parameters.json"


def get_keys(pfx_data: bytes, pfx_password: bytes) -> tuple[bytes | None, bytes | None]:
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
    storage: CacheStorage,
) -> ConfigInfo:
    """
    Retrieves the configuration for the API client from the Android app.

    Args:
        client: async http client
        brand: car brand
        email: user email
        password: user password
        country_code: country code
        storage: cache storage

    Returns:
        Configuration from the Android app.
    """
    config_path = "config.json"
    if storage.exists(config_path):
        return decode(storage.read(config_path), type=ConfigInfo)
    brand_config = BRAND_CONFIG_MAP[brand]
    site_code = brand_config.site_code(country_code)
    apk = await download_apk(client, brand_config.apk_name, storage)
    apk_info = get_config_from_apk(apk, country_code, site_code)
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
    if apk_info.public_certificate:
        storage.save(apk_info.public_certificate, "public.pem")
    if apk_info.private_key:
        storage.save(apk_info.private_key, "private.pem")
    return str(storage.get_full_path("public.pem")), str(
        storage.get_full_path("private.pem")
    )
