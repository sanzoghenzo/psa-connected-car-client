"""PSAClient tests."""
from __future__ import annotations

import datetime

import pytest
from psa_ccc import models
from psa_ccc.client import ApiError


@pytest.mark.asyncio
async def test_get_user(httpx_mock, client) -> None:
    user_text = '{"email":"my@email.com","firstName":"MyName","lastName":"MyLastName","_links":{"self":{"href":"https://api.groupe-psa.com/connectedcar/v4/user"},"vehicles":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles"}},"_embedded":{"vehicles":[{"id":"myId","vin":"myVin","vehicleExtension":{"vehicleBranding":{"brand":"C", "label":"myLabel"}, "vehiclePictures":{"pictures":[]}},"_links":{"alerts":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/alerts"},"collisions":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/collisions"},"trips":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/trips"},"self":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId"},"lastPosition":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/lastPosition"},"callbacks":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/callbacks"},"remotes":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/remotes","templated":true},"telemetry":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/telemetry"},"user":{"href":"https://api.groupe-psa.com/connectedcar/v4/user"},"maintenance":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/maintenance"},"status":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/status"},"monitors":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/monitors","templated":true}}}]}}'
    httpx_mock.add_response(text=user_text)
    user = await client.get_user()
    assert user == models.User(
        email="my@email.com",
        first_name="MyName",
        last_name="MyLastName",
        embedded=models.VehicleList(
            vehicles=[
                models.VehicleSummary(
                    id="myId",
                    vin="myVin",
                    vehicle_extension=models.VehicleExtension(
                        vehicle_branding=models.VehicleBranding(
                            brand="C", label="myLabel"
                        ),
                        vehicle_pictures=models.VehiclePictures(pictures=[]),
                    ),
                )
            ]
        ),
    )


@pytest.mark.asyncio
async def test_get_user_raises_api_error(httpx_mock, client) -> None:
    error = "Something went horrendously wrong"
    httpx_mock.add_response(status_code=500, text=error)
    with pytest.raises(ApiError, match=error):
        await client.get_user()


@pytest.mark.asyncio
async def test_get_vehicles(httpx_mock, client) -> None:
    text = '{"total":1, "currentPage":1, "totalPage":1, "_embedded":{"vehicles":[{"id":"myId","vin":"myVin","vehicleExtension":{"vehicleBranding":{"brand":"C", "label":"myLabel"}, "vehiclePictures":{"pictures":[]}},"_links":{"alerts":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/alerts"},"collisions":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/collisions"},"trips":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/trips"},"self":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId"},"lastPosition":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/lastPosition"},"callbacks":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/callbacks"},"remotes":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/remotes","templated":true},"telemetry":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/telemetry"},"user":{"href":"https://api.groupe-psa.com/connectedcar/v4/user"},"maintenance":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/maintenance"},"status":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/status"},"monitors":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/monitors","templated":true}}}]}}'
    httpx_mock.add_response(text=text)
    vehicles = await client.get_vehicles()
    assert vehicles == [
        models.VehicleSummary(
            id="myId",
            vin="myVin",
            vehicle_extension=models.VehicleExtension(
                vehicle_branding=models.VehicleBranding(brand="C", label="myLabel"),
                vehicle_pictures=models.VehiclePictures(pictures=[]),
            ),
        )
    ]


@pytest.mark.asyncio
async def test_get_vehicle(httpx_mock, client) -> None:
    text = '{"id":"myId","vin":"myVin","vehicleExtension":{"vehicleBranding":{"brand":"C", "label":"myLabel"}, "vehiclePictures":{"pictures":[]}},"_links":{"alerts":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/alerts"},"collisions":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/collisions"},"trips":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/trips"},"self":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId"},"lastPosition":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/lastPosition"},"callbacks":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/callbacks"},"remotes":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/remotes","templated":true},"telemetry":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/telemetry"},"user":{"href":"https://api.groupe-psa.com/connectedcar/v4/user"},"maintenance":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/maintenance"},"status":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/status"},"monitors":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/monitors","templated":true}}}'
    httpx_mock.add_response(text=text)
    vehicle = await client.get_vehicle("myId")
    assert vehicle == models.Vehicle(
        id="myId",
        vin="myVin",
        vehicle_extension=models.VehicleExtension(
            vehicle_branding=models.VehicleBranding(brand="C", label="myLabel"),
            vehicle_pictures=models.VehiclePictures(pictures=[]),
        ),
    )


# Real request returns 500, skipping for now
# @pytest.mark.asyncio
# async def test_get_vehicle_alerts(httpx_mock, client) -> None:
#     text = '{"total":1, "currentPage":1, "totalPage":1, "_embedded":{"vehicles":[{"id":"myId","vin":"myVin","brand":"C","_links":{"alerts":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/alerts"},"collisions":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/collisions"},"trips":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/trips"},"self":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId"},"lastPosition":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/lastPosition"},"callbacks":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/callbacks"},"remotes":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/remotes","templated":true},"telemetry":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/telemetry"},"user":{"href":"https://api.groupe-psa.com/connectedcar/v4/user"},"maintenance":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/maintenance"},"status":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/status"},"monitors":{"href":"https://api.groupe-psa.com/connectedcar/v4/user/vehicles/myId/callbacks/{cbid}/monitors","templated":true}}}]}}'
#     httpx_mock.add_response(text=text)
#     result = await client.get_vehicle_alerts("myId")
#     assert result == models.Vehicle(brand="C", id="myId", vin="myVin")


@pytest.mark.asyncio
async def test_get_vehicle_status(httpx_mock, client) -> None:
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
    httpx_mock.add_response(text=response)
    vehicle = await client.get_vehicle_status("myId")
    utc = datetime.timezone.utc
    timestamp = datetime.datetime(2023, 4, 29, 22, 17, 20, tzinfo=utc)
    expected = models.VehicleStatus(
        created_at=timestamp,
        updated_at=timestamp,
        ignition=models.Ignition(created_at=timestamp, type="Stop"),
        battery=models.Battery(voltage=82, current=0, created_at=timestamp),
        energies=[
            models.Energy(
                created_at=datetime.datetime(2021, 9, 12, 16, 23, 56, tzinfo=utc),
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
                created_at=datetime.datetime(2023, 3, 10, 7, 45, 53, tzinfo=utc),
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
            luminosity=models.EnvironmentLuminosity(created_at=timestamp, day=False),
            air=models.EnvironmentAir(created_at=timestamp, temp=15),
        ),
        privacy=models.Privacy(created_at=timestamp, state="None"),
        service=models.ServiceType(
            type="Electric",
            created_at=datetime.datetime(2022, 10, 20, 16, 55, 16, tzinfo=utc),
        ),
    )
    assert vehicle == expected


@pytest.mark.asyncio
async def test_get_vehicle_maintenance(httpx_mock, client) -> None:
    response = """{
      "createdAt": "2023-03-25T10:14:21Z",
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
    httpx_mock.add_response(text=response)
    returned = await client.get_vehicle_maintenance("vehicleid")
    expected = models.Maintenance(
        updated_at=datetime.datetime(
            2023, 3, 25, 10, 14, 21, tzinfo=datetime.timezone.utc
        ),
        created_at=datetime.datetime(
            2023, 3, 25, 10, 14, 21, tzinfo=datetime.timezone.utc
        ),
        days_before_maintenance=610,
        mileage_before_maintenance=22920,
    )
    assert returned == expected


@pytest.mark.asyncio
async def test_get_last_position(httpx_mock, client) -> None:
    response = """{
    "type":"Feature",
    "geometry":{"type":"Point","coordinates":[11.125240,46.005900,192.000000]},
    "properties":{"createdAt":"2023-05-02T17:25:17Z","heading":278,"type":"Acquire"}
}"""
    httpx_mock.add_response(text=response)
    returned = await client.get_vehicle_last_position("vehicleid")
    expected = models.Position(
        geometry=models.Point(coordinates=[11.12524, 46.0059, 192.0], type="Point"),
        properties=models.PositionProperties(
            created_at=datetime.datetime(
                2023, 5, 2, 17, 25, 17, tzinfo=datetime.timezone.utc
            ),
            updated_at=None,
            heading=278.0,
            type="Acquire",
        ),
        type="Feature",
    )
    assert returned == expected
