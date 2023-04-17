"""Models decoding tests."""
from __future__ import annotations

import datetime

from msgspec.json import decode
from psa_ccc import models


def test_user_response() -> None:
    """Get user response correctly decoded."""
    response = """{
  "_links": {
    "self": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user"
    },
    "vehicles": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles"
    }
  },
  "_embedded": {
    "vehicles": [
      {
        "id": "my_car_id",
        "vin": "MY_VIN",
        "brand": "C",
        "_links": {
          "alerts": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/alerts"
          },
          "trips": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/trips"
          },
          "self": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid"
          },
          "lastPosition": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/lastPosition"
          },
          "telemetry": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/telemetry"
          },
          "maintenance": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/maintenance"
          },
          "status": {
            "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/status"
          }
        }
      }
    ]
  }
}"""
    decoded = decode(response, type=models.UserResponse)
    expected = models.UserResponse(
        embedded=models.VehicleList(
            vehicles=[
                models.VehicleSummary(
                    id="my_car_id",
                    vin="MY_VIN",
                    brand="C",
                )
            ]
        )
    )
    assert decoded == expected


def test_vehicle_status() -> None:
    """Vehicle status response correctly decoded."""
    response = """{
  "lastPosition": {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [
        11.12524,
        46.0059,
        192
      ]
    },
    "properties": {
      "updatedAt": "2023-03-10T07:45:53Z",
      "heading": 278,
      "type": "Aquire"
    }
  },
  "preconditionning": {
    "airConditioning": {
      "updatedAt": "2023-03-24T17:24:52Z",
      "status": "Disabled",
      "programs": [
        {
          "enabled": false,
          "slot": 1,
          "recurrence": "Daily",
          "start": "PT0S"
        },
        {
          "enabled": false,
          "slot": 2,
          "recurrence": "Daily",
          "start": "PT0S"
        },
        {
          "enabled": false,
          "slot": 3,
          "recurrence": "Daily",
          "start": "PT0S"
        },
        {
          "enabled": false,
          "slot": 4,
          "recurrence": "Daily",
          "start": "PT0S"
        }
      ]
    }
  },
  "energy": [
    {
      "updatedAt": "2021-09-12T16:23:56Z",
      "type": "Fuel",
      "level": 0
    },
    {
      "updatedAt": "2023-03-25T10:14:08Z",
      "type": "Electric",
      "level": 19,
      "autonomy": 40,
      "charging": {
        "plugged": false,
        "status": "Disconnected",
        "chargingRate": 0,
        "chargingMode": "No",
        "nextDelayedTime": "PT0S"
      }
    }
  ],
  "createdAt": "2023-03-25T10:14:08Z",
  "battery": {
    "voltage": 83,
    "current": 0,
    "createdAt": "2023-03-24T17:24:52Z"
  },
  "kinetic": {
    "createdAt": "2023-03-10T07:45:53Z",
    "moving": false
  },
  "privacy": {
    "createdAt": "2023-03-25T10:14:08Z",
    "state": "None"
  },
  "service": {
    "type": "Electric",
    "updatedAt": "2022-10-20T16:55:16Z"
  },
  "_links": {
    "self": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/status"
    },
    "vehicles": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid"
    }
  },
  "timed.odometer": {
    "createdAt": null,
    "mileage": 13890.3
  },
  "updatedAt": "2023-03-25T10:14:08Z"
}
"""
    decoded = decode(response, type=models.VehicleStatus)
    utc = datetime.timezone.utc
    expected = models.VehicleStatus(
        created_at=datetime.datetime(2023, 3, 25, 10, 14, 8, tzinfo=utc),
        updated_at=datetime.datetime(2023, 3, 25, 10, 14, 8, tzinfo=utc),
        battery=models.Battery(
            voltage=83,
            current=0,
            created_at=datetime.datetime(2023, 3, 24, 17, 24, 52, tzinfo=utc),
        ),
        energy=[
            models.Energy(
                updated_at=datetime.datetime(
                    2021, 9, 12, 16, 23, 56, tzinfo=utc
                ),
                type="Fuel",
                level=0,
            ),
            models.Energy(
                updated_at=datetime.datetime(
                    2023, 3, 25, 10, 14, 8, tzinfo=utc
                ),
                type="Electric",
                level=19,
                autonomy=40,
                charging=models.EVBatteryCharging(
                    plugged=False,
                    status="Disconnected",
                    charging_rate=0,
                    charging_mode="No",
                    next_delayed_time="PT0S",
                ),
            ),
        ],
        kinetic=models.Kinetic(
            created_at=datetime.datetime(2023, 3, 10, 7, 45, 53, tzinfo=utc),
            moving=False,
        ),
        last_position=models.Position(
            geometry=models.Point(coordinates=[11.12524, 46.0059, 192]),
            properties=models.PositionProperties(
                updated_at=datetime.datetime(
                    2023, 3, 10, 7, 45, 53, tzinfo=utc
                ),
                heading=278,
                type="Aquire",
            ),
        ),
        preconditionning=models.Preconditioning(
            air_conditioning=models.AirConditioning(
                programs=[
                    models.PreconditionProgram(
                        enabled=False,
                        slot=idx,
                        start="PT0S",
                        recurrence="Daily",
                    )
                    for idx in range(1, 5)
                ],
                status="Disabled",
                updated_at=datetime.datetime(
                    2023, 3, 24, 17, 24, 52, tzinfo=utc
                ),
            )
        ),
        privacy=models.Privacy(
            created_at=datetime.datetime(2023, 3, 25, 10, 14, 8, tzinfo=utc),
            state="None",
        ),
        service=models.ServiceType(
            type="Electric",
            updated_at=datetime.datetime(2022, 10, 20, 16, 55, 16, tzinfo=utc),
        ),
    )
    assert decoded == expected


def test_maintenance_response() -> None:
    """Maintenance response correctly decoded."""
    response = """{
  "updatedAt": "2023-03-25T10:14:21Z",
  "_links": {
    "alerts": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/alerts"
    },
    "self": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid/maintenance"
    },
    "vehicles": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/vehicleid"
    }
  },
  "daysBeforeMaintenance": 610,
  "mileageBeforeMaintenance": 22920.0
}"""
    decoded = decode(response, type=models.Maintenance)
    expected = models.Maintenance(
        updated_at=datetime.datetime(
            2023, 3, 25, 10, 14, 21, tzinfo=datetime.timezone.utc
        ),
        days_before_maintenance=610,
        mileage_before_maintenance=22920,
    )
    assert decoded == expected
