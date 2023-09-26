"""CLI app."""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

import httpx
from psa_ccc.apk_parser import ConfigInfo
from psa_ccc.apk_parser import first_launch
from psa_ccc.auth import oauth_factory
from psa_ccc.brand_config import BRAND_CONFIG_MAP
from psa_ccc.client import PSAClient
from psa_ccc.storage import CacheStorage
from psa_ccc.storage import SimpleCacheStorage

from tests.memory_token_storage import MemoryTokenStorage

# MQTT
#   ChargeControls load config
#   myp.remote_client.start()
# OTP - askCode config view
#   POST "https://api.groupe-psa.com/applications/cvs/v4/mobile/smsCode?client_id={client_id}"
#   Headers = {
#       "x-introspect-realm": realm,
#       "accept": "application/hal+json",
#       "User-Agent": "okhttp/4.8.0",
#   }
# OTP - finishOtp config view
# otp_session = new_otp_session(sms_code, code_pin, remote_client.otp)
# remote_client.otp = otp_session
# save_config()
# app.start_remote_control()


def build_parser() -> argparse.ArgumentParser:
    """Built the CLI parser."""
    parser = argparse.ArgumentParser("PSA Car Controller Client")
    parser.add_argument("brand", choices=list(BRAND_CONFIG_MAP.keys()))
    parser.add_argument("email")
    parser.add_argument("password")
    parser.add_argument("country_code")
    return parser


async def main() -> None:
    """Bootstrap the client."""
    parser = build_parser()
    args = parser.parse_args()
    storage = SimpleCacheStorage(Path(__file__).parent)
    # TODO: do this only on "config" command
    config = await get_config(args, storage)
    # TODO: make this configurable, use something permanent
    token_storage = MemoryTokenStorage()
    brand_config = BRAND_CONFIG_MAP[args.brand]
    oauth_client = await oauth_factory(
        config.client_id,
        config.client_secret,
        args.email,
        args.password,
        brand_config.access_token_url,
        brand_config.realm,
        token_storage,
    )
    api_client = PSAClient(client=oauth_client)

    user = await api_client.get_user()
    print("User:", user)
    vehicles = await api_client.get_vehicles()
    print("Vehicles:", vehicles)
    vehicle_id = vehicles[0].id
    vehicle = await api_client.get_vehicle(vehicle_id)
    print("First vehicle:", vehicle)
    alerts = await api_client.get_vehicle_alerts(vehicle_id)
    print("Vehicle alerts:", alerts)
    status = await api_client.get_vehicle_status(vehicle_id)
    print("Vehicle status:", status)
    maintenance = await api_client.get_vehicle_maintenance(vehicle_id)
    print("Vehicle maintenance:", maintenance)
    # This results in Internal server error
    # position = await api_client.get_vehicle_last_position(vehicle_id)
    # print("Vehicle position:", position)
    # but we have the info in status.last_position.geometry.coordinates
    print(
        "Vehicle position:",
        status.last_position.geometry.coordinates,
        "last updated at",
        status.last_position.properties.updated_at,
    )


async def get_config(args: argparse.Namespace, storage: CacheStorage) -> ConfigInfo:
    """Retrieve the configuration for the first-time launch."""
    async with httpx.AsyncClient() as client:
        config = await first_launch(
            client,
            args.brand,
            args.email,
            args.password,
            args.country_code,
            storage,
        )
    return config


if __name__ == "__main__":
    asyncio.run(main())
