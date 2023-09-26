"""API Client."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any
from typing import List
from typing import TypeVar

from httpx import AsyncClient
from httpx import QueryParams
from httpx import Response
from msgspec.json import decode

import psa_ccc.models as mdl


class ApiError(BaseException):
    """API response errors."""

    pass


T = TypeVar("T")


def _handle_response(response: Response, model: type[T]) -> T:
    if not 200 <= response.status_code < 300:
        raise ApiError(response.text)
    return decode(response.text, type=model)


def _query_params(other_params: dict[str, Any]) -> QueryParams | None:
    to_add = {k: v for k, v in other_params.items() if v}
    return QueryParams(to_add)


@dataclass(kw_only=True, slots=True)
class PSAClient:
    """User API."""

    client: AsyncClient

    # TODO: add a decoder cache for each schema do decode

    async def get_user(self) -> mdl.User:
        """Get user information."""
        response = await self.client.get("/user")
        return _handle_response(response, model=mdl.User)

    async def get_vehicles(
        self,
        index_range: str | None = None,
        page_size: int | None = None,
        locale: str | None = None,
        page_token: str | None = None,
    ) -> List[mdl.VehicleSummary]:
        """Get the vehicles associated with the User."""
        params = {
            "indexRange": index_range,
            "pageSize": page_size,
            "locale": locale,
            "pageToken": page_token,
        }
        response = await self.client.get("/user/vehicles", params=_query_params(params))
        return _handle_response(response, model=mdl.PaginatedVehicles).embedded.vehicles

    async def get_vehicle(self, vehicle_id: str) -> mdl.Vehicle:
        """Get the vehicles associated with the User."""
        response = await self.client.get(f"/user/vehicles/{vehicle_id}")
        return _handle_response(response, model=mdl.Vehicle)

    async def get_vehicle_alerts(
        self,
        vehicle_id: str,
        timestamps: list[datetime] | None = None,  # List[timeRange]
        index_range: str | None = None,
        page_size: int | None = None,
        locale: str | None = None,
        page_token: str | None = None,
    ) -> mdl.Alerts | None:
        """Returns the latest alert messages for a Vehicle."""
        params: dict[str, Any] = {
            "indexRange": index_range,
            "pageSize": page_size,
            "locale": locale,
            "pageToken": page_token,
            "timestamps": timestamps,
        }
        response = await self.client.get(
            f"/user/vehicles/{vehicle_id}/alerts",
            params=_query_params(params),
        )
        if response.status_code == 404:
            return None
        return _handle_response(response, model=mdl.Alerts)

    async def get_vehicle_alerts_by_id(
        self,
        vehicle_id: str,
        alert_id: str,
        locale: str | None = None,
    ) -> mdl.Alert:
        """Returns information about a specific alert message for a Vehicle."""
        response = await self.client.get(
            f"/user/vehicles/{vehicle_id}/alerts/{alert_id}",
            params=_query_params({"locale": locale}),
        )
        return _handle_response(response, model=mdl.Alert)

    async def get_vehicle_last_position(
        self,
        vehicle_id: str,
    ) -> mdl.Position:
        """Returns the latest GPS Position of the Vehicle."""
        response = await self.client.get(
            f"/user/vehicles/{vehicle_id}/lastPosition",
            headers={"Accept": "application/vnd.geo+json"},
        )
        return _handle_response(response, model=mdl.Position)

    async def get_vehicle_maintenance(
        self,
        vehicle_id: str,
    ) -> mdl.Maintenance:
        """Returns the latest GPS Position of the Vehicle."""
        response = await self.client.get(
            f"/user/vehicles/{vehicle_id}/maintenance",
        )
        return _handle_response(response, model=mdl.Maintenance)

    async def get_vehicle_status(
        self,
        vehicle_id: str,
        extension: list[str] | None = None,  # odometer | kinetic
    ) -> mdl.VehicleStatus:
        """Returns the latest vehicle status."""
        response = await self.client.get(
            f"/user/vehicles/{vehicle_id}/status",
            params=_query_params({"extension": extension}),
        )
        return _handle_response(response, model=mdl.VehicleStatus)
