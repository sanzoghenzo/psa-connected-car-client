"""CLI app."""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from psa_ccc import create_psa_client
from psa_ccc.brand_config import BRAND_CONFIG_MAP
from psa_ccc.memory_token_storage import MemoryTokenStorage
from psa_ccc.storage import SimpleCacheStorage


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
    token_storage = MemoryTokenStorage()
    api_client = await create_psa_client(
        args.brand, args.country_code, args.email, args.password, storage, token_storage
    )

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


if __name__ == "__main__":
    asyncio.run(main())
