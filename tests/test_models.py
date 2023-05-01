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
  "createdAt": "2023-04-29T22:17:20Z",
  "updatedAt": "2023-04-29T22:17:20Z",
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
      "createdAt": "2023-03-10T07:45:53Z",
      "heading": 278,
      "type": "Acquire"
    }
  },
  "ignition": {
    "createdAt": "2023-04-29T22:17:20Z",
    "type": "Stop"
  },
  "battery": {
    "voltage": 82,
    "createdAt": "2023-04-29T22:17:20Z"
  },
  "privacy": {
    "createdAt": "2023-04-29T22:17:20Z",
    "state": "None"
  },
  "service": {
    "createdAt": "2022-10-20T16:55:16Z",
    "type": "Electric"
  },
  "environment": {
    "luminosity": {
      "createdAt": "2023-04-29T22:17:20Z",
      "day": false
    },
    "air": {
      "createdAt": "2023-04-29T22:17:20Z",
      "temp": 15
    }
  },
  "odometer": {
    "createdAt": "2023-04-29T22:17:20Z",
    "mileage": 14529.9
  },
  "kinetic": {
    "createdAt": "2023-04-29T22:17:20Z",
    "moving": false
  },
  "_links": {
    "self": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/19c3b0dd3b7101631b742bc69080ff24e6e2ff1fb62def3bc4f27bc87f8078936a5a148a71cadab8206f370dfc442756c41c24199d79c4fdc890ce085f839f336508b15210b14c0bc4aa7781d0f689102d5a364ff62e626f7c206bbef37d0e582/status?profile=endUser"
    },
    "vehicle": {
      "href": "https://api.groupe-psa.com/connectedcar/v4/user/vehicles/19c3b0dd3b7101631b742bc69080ff24e6e2ff1fb62def3bc4f27bc87f8078936a5a148a71cadab8206f370dfc442756c41c24199d79c4fdc890ce085f839f336508b15210b14c0bc4aa7781d0f689102d5a364ff62e626f7c206bbef37d0e582"
    }
  },
  "preconditioning": {
    "airConditioning": {
      "createdAt": "2023-04-29T22:17:20Z",
      "updatedAt": "2023-04-29T22:17:20Z",
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
  "energies": [
    {
      "createdAt": "2021-09-12T16:23:56Z",
      "type": "Fuel",
      "subType": "FossilEnergy",
      "level": 0
    },
    {
      "createdAt": "2023-04-29T22:17:20Z",
      "type": "Electric",
      "subType": "ElectricEnergy",
      "level": 43,
      "autonomy": 128,
      "extension": {
        "electric": {
          "battery": {
            "load": {
              "createdAt": "2023-04-29T22:17:20Z",
              "capacity": 33280,
              "residual": 4096
            }
          },
          "charging": {
            "plugged": false,
            "status": "Disconnected",
            "chargingRate": 0,
            "chargingMode": "No",
            "nextDelayedTime": "PT0S"
          }
        }
      }
    }
  ],
  "preconditionning": {
    "airConditioning": {
      "createdAt": "2023-04-29T22:17:20Z",
      "updatedAt": "2023-04-29T22:17:20Z",
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
      "createdAt": "2021-09-12T16:23:56Z",
      "type": "Fuel",
      "level": 0
    },
    {
      "createdAt": "2023-04-29T22:17:20Z",
      "updatedAt": "2023-04-29T22:17:20Z",
      "type": "Electric",
      "level": 43,
      "autonomy": 128,
      "charging": {
        "plugged": false,
        "status": "Disconnected",
        "chargingRate": 0,
        "chargingMode": "No",
        "nextDelayedTime": "PT0S"
      }
    }
  ]
}"""
    decoded = decode(response, type=models.VehicleStatus)
    utc = datetime.timezone.utc
    timestamp = datetime.datetime(2023, 4, 29, 22, 17, 20, tzinfo=utc)
    expected = models.VehicleStatus(
        created_at=timestamp,
        updated_at=timestamp,
        ignition=models.Ignition(created_at=timestamp, type="Stop"),
        battery=models.Battery(voltage=82, current=0, created_at=timestamp),
        energies=[
            models.Energy(
                created_at=datetime.datetime(
                    2021, 9, 12, 16, 23, 56, tzinfo=utc
                ),
                type="Fuel",
                sub_type="FossilEnergy",
                level=0,
            ),
            models.Energy(
                created_at=timestamp,
                type="Electric",
                sub_type="ElectricEnergy",
                level=43,
                autonomy=128,
                extension=models.EnergyExtension(
                    electric=models.ElectricEnergyExtension(
                        battery=models.EVBattery(
                            load=models.EVBatteryLoad(
                                created_at=timestamp,
                                capacity=33280,
                                residual=4096,
                            ),
                        ),
                        charging=models.EVBatteryCharging(
                            plugged=False,
                            status="Disconnected",
                            charging_rate=0,
                            charging_mode="No",
                            next_delayed_time="PT0S",
                        ),
                    )
                ),
            ),
        ],
        odometer=models.VehicleOdometer(created_at=timestamp, mileage=14529.9),
        kinetic=models.Kinetic(created_at=timestamp, moving=False),
        last_position=models.Position(
            geometry=models.Point(coordinates=[11.12524, 46.0059, 192]),
            properties=models.PositionProperties(
                created_at=datetime.datetime(
                    2023, 3, 10, 7, 45, 53, tzinfo=utc
                ),
                heading=278,
                type="Acquire",
            ),
        ),
        preconditioning=models.Preconditioning(
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
                created_at=timestamp,
                updated_at=timestamp,
            )
        ),
        environment=models.Environment(
            luminosity=models.EnvironmentLuminosity(
                created_at=timestamp, day=False
            ),
            air=models.EnvironmentAir(created_at=timestamp, temp=15),
        ),
        privacy=models.Privacy(created_at=timestamp, state="None"),
        service=models.ServiceType(
            type="Electric",
            created_at=datetime.datetime(2022, 10, 20, 16, 55, 16, tzinfo=utc),
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
