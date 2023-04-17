"""Models for the API responses."""
from __future__ import annotations

import datetime
from enum import StrEnum
from enum import auto
from re import sub
from typing import Any

from msgspec import Struct


def camelize(s: str) -> str:
    """Converts a string into camelCase."""
    s = sub(r"([_\-])+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def rename(name: str) -> str | None:
    """Custom function to rename the json fields."""
    return f"_{name}" if name in {"links", "embedded"} else camelize(name)


class PaginatedResponse(Struct, kw_only=True, rename=rename):
    """Generic wrapper for paginated responses."""

    # links: Any
    total: int
    current_page: int
    total_page: int


class BaseEntity(Struct, kw_only=True, rename=rename):
    """Base entity model."""

    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None


class UserResponse(Struct, kw_only=True, rename=rename):
    """Object returned by the get user response."""

    # links: Any
    embedded: VehicleList


class User(BaseEntity):
    """User information."""

    first_name: str
    last_name: str
    # email: str
    # embedded:
    # Vehicles: list[Vehicle]
    # links:
    # self: link
    # vehicles: link


class Engine(Struct, kw_only=True, rename=rename):
    """Engine of a vehicle."""

    energy: str  # "GPL" | "Gasoil" | "Petrol" | "Biologic"
    class_: str = "Thermic"  # "Electric"


class PaginatedVehicles(PaginatedResponse):
    """Paginated response of get vehicles."""

    embedded: VehicleList


class VehicleList(Struct, kw_only=True, rename=rename):
    """List of the vehicles of a user."""

    vehicles: list[VehicleSummary]


class VehicleSummary(Struct, kw_only=True, rename=rename):
    """Summary of the vehicle found in the user response."""

    brand: str
    id: str
    vin: str


class Vehicle(Struct, kw_only=True, rename=rename):
    """Vehicle information."""

    brand: str
    id: str
    vin: str
    label: str = ""
    pictures: list[str] = []  # url in realtà, min 1 max 12 items
    engine: list[Engine] = []
    # embedded: Any
    # links: Any


class VehicleOdometer(Struct, kw_only=True, rename=rename):
    """Vehicle odometer."""

    created_at: datetime.datetime
    mileage: float  # [km]


class Battery(Struct, kw_only=True, rename=rename):
    """Describe the car (with combustion engine) battery status."""

    created_at: datetime.datetime
    current: float
    voltage: float


class Opening(Struct, kw_only=True, rename=rename):
    """Opening information."""

    identifier: str  # enum
    state: str  # enum


class DoorsState(Struct, kw_only=True, rename=rename):
    """Doors state."""

    locked_state: str  # enum...
    opening: list[Opening]


class EVBatteryHealth(Struct, kw_only=True, rename=rename):
    """Battery health status."""

    capacity: int  # [%]
    resistance: int  # [%]


class EVBatteryCharging(Struct, kw_only=True, rename=rename):
    """Electric Vehicle charging information."""

    plugged: bool
    status: str  # enum
    charging_rate: int  # [0-500 km/h]
    charging_mode: str  # "No", "Slow", "Quick"
    next_delayed_time: str  # datetime.datetime  # timestamp RFC3339 - "PT05"
    # remaining_time: datetime.datetime  # ISO8601 format


class EVBattery(Struct, kw_only=True, rename=rename):
    """Battery capacity and health for electric energy type."""

    capacity: float
    health: EVBatteryHealth


class Energy(Struct, kw_only=True, rename=rename):
    """Percentage energy."""

    # battery: EVBattery
    # consumption: float
    level: float  # 0-100
    # residual: float  # [kWh]
    type: str  # "Fuel" or "Electric"
    autonomy: float = 0  # [km]
    charging: EVBatteryCharging | None = None
    updated_at: datetime.datetime | None = None


class Environment(BaseEntity):
    """Environment status."""

    air: Any  # temp: float
    luminosity: Any  # day: bool


class Ignition(Struct, kw_only=True, rename=rename):
    """Ignition."""

    updated_at: datetime.datetime
    type: str  # "Stop" | "StartUp" | "Start" | "Free"


class Kinetic(Struct, kw_only=True, rename=rename):
    """Everything related to the movement of the vehicle."""

    moving: bool
    acceleration: float = 0
    pace: float = 0
    speed: float = 0
    created_at: datetime.datetime | None = None


class Point(Struct, kw_only=True, rename=rename):
    """Point."""

    coordinates: list[float]  # min 2 elements, max 3
    type: str = "Point"


class PositionProperties(Struct, kw_only=True, rename=rename):
    """Properties of a geospatial position."""

    updated_at: datetime.datetime
    heading: float  # [0-360]
    # signal_quality: int  # [%]
    type: str  # "Estimate" | "Acquire"


class Position(Struct, kw_only=True, rename=rename):
    """Geospatial position."""

    geometry: Point
    properties: PositionProperties
    type: str = "Feature"


class ProgramOccurrence(Struct, kw_only=True, rename=rename):
    """Program occurrence."""

    day: list[str]  # Mon, Tue,Wed,Thu,Fri,Sat,Sun
    week: list[str] | None = None


class Program(Struct, kw_only=True, rename=rename):
    """Recurring action."""

    occurrence: ProgramOccurrence
    start: datetime.datetime  # ISO 8601
    recurrence: str = "Daily"  # None, Weekly


class PreconditionProgram(Struct, kw_only=True, rename=rename):
    """Precondition program."""

    enabled: bool
    slot: int
    start: str  # ISO 8601 ex. PT0S
    recurrence: str = "Daily"  # None, Weekly


class AirConditioning(Struct, kw_only=True, rename=rename):
    """Air conditioning."""

    # failure_cause: str  # enum...
    programs: list[PreconditionProgram]
    status: str  # enum
    updated_at: datetime.datetime


class Preconditioning(Struct, kw_only=True, rename=rename):
    """Preconditioning."""

    air_conditioning: AirConditioning


class Privacy(Struct, kw_only=True, rename=rename):
    """Privacy model."""

    created_at: datetime.datetime
    state: str  # enum


class Safety(Struct, kw_only=True, rename=rename):
    """Safety model."""

    created_at: datetime.datetime
    belt_warning: str  # Normal | Omission
    e_call_triggering_request: str  # AirbagUnabled | NoRequest | Requested


class ServiceType(Struct, kw_only=True, rename=rename):
    """Service type."""

    type: str  # Electric | Hybrid | Unknown
    updated_at: datetime.datetime


class Extension(Struct, kw_only=True, rename=rename):
    """Vehicle status extension."""

    kinetic: Kinetic
    odemeter: VehicleOdometer


class VehicleStatusEmbedded(Struct, kw_only=True, rename=rename):
    """Vehicle status embedded model."""

    extension: Extension


class VehicleStatus(BaseEntity):
    """Vehicle status response."""

    # links: Any  # self and vehicle
    battery: Battery
    # doors_state: DoorsState
    energy: list[Energy]
    # environment: Environment
    # ignition: Ignition
    kinetic: Kinetic
    last_position: Position
    preconditionning: Preconditioning
    privacy: Privacy
    # safety: Safety
    service: ServiceType
    # timed.odemeter {created_at, mileage}


class Alerts(PaginatedResponse):
    """Alerts container."""

    embedded: Any
    #   alerts: list[Alert]


class Maintenance(BaseEntity):
    """Next Maintenance details."""

    days_before_maintenance: int
    mileage_before_maintenance: float
    # links: Any  # alerts, self, vehicle


class AlertMsgEnum(StrEnum):
    """Alert messages."""

    alertOilPressure = auto()
    alertCoolantTemp = auto()
    chargingSystemFault = auto()
    alertBrakeFluid = auto()
    steeringFault = auto()
    alertCoolantLevel = auto()
    laneDepartureWarningSystemFault = auto()
    frontLeftDoorOpenHighSpeed = auto()
    frontRightDoorOpenHighSpeed = auto()
    rearLeftDoorOpenHighSpeed = auto()
    rearRightDoorOpenHighSpeed = auto()
    trunkOpenHighSpeed = auto()
    trunkWindowOpen = auto()
    espFault = auto()
    batteryLevelFault = auto()
    waterInGasoil = auto()
    padWearFault = auto()
    fuelLevelAlarm = auto()
    airbagOrSeatbeltFault = auto()
    engineFault = auto()
    absFault = auto()
    riskOfParticleFilterBlockage = auto()
    particleFilterAdditiveTooLow = auto()
    suspensionFault = auto()
    preaheatingDeactivatedBatteryTooLow = auto()
    preaheatingDeactivatedFuelLevelTooLow = auto()
    checkTheBrakeLamp = auto()
    retractableRoofMechanismFault = auto()
    alertSteeringLock = auto()
    electronicImmobiliserFault = auto()
    roofOperationImpossibleTemperatureTooHigh = auto()
    roofOperationImpossibleStartEngine = auto()
    roofOperationImpossibleApplyParkingBreak = auto()
    hybridSystemFault = auto()
    automaticHeadlampFault = auto()
    hybridSystemFaultRepairedTheVehicle = auto()
    washerLevelAlarm = auto()
    batteryKeyAlarm = auto()
    preaheatingDeactivatedSetTheClock = auto()
    trailerConnectionFault = auto()
    underInflationTyreFault = auto()
    limitedVisibilityAidsCamera = auto()
    electricModeNotAvailable = auto()
    wheelPressureFault = auto()
    checkSideLamps = auto()
    checkRightBrakeLamp = auto()
    checkLeftBrakeLamp = auto()
    frontFoglightFault = auto()
    rearFoglightFault = auto()
    checkDirectionIndicator = auto()
    checkReversingLamp = auto()
    parkingAssistanceFault = auto()
    adjustTyrePressure = auto()
    antipollutionFault = auto()
    placeGearBoxToP = auto()
    riskOfIce = auto()
    frontRightDoorOpen = auto()
    frontLeftDoorOpen = auto()
    rearRightDoorOpen = auto()
    rearLeftDoorOpen = auto()
    trunkOpen = auto()
    bootOpen = auto()
    rearScreenOpen = auto()
    parkingBreakFault = auto()
    activeSpoilerFault = auto()
    automaticBreakingSystemFault = auto()
    directionalHeadlampsFault = auto()
    automaticGearboxFault = auto()
    suspensionFaultLimitTo90km = auto()
    frontLeftTyreNotMonitored = auto()
    frontRightTyreNotMonitored = auto()
    rearRightTyreNotMonitored = auto()
    rearLeftTyreNotMonitored = auto()
    powerSteeringFault = auto()
    laneDepartureFault = auto()
    tyreUnderInflation = auto()
    spareWheelFittedDrivingAidsDeactivated = auto()
    automaticBreakingDeactived = auto()
    tupUpAdBlue = auto()
    longPushToUnlockTankFault = auto()


class Alert(BaseEntity):
    """Alert model."""

    id: str
    active: bool
    end_at: datetime.datetime
    start_position: Position
    started_at: datetime.datetime
    type: AlertMsgEnum
    # links: Any = None
    #   position
    #   self
    #   trip
    #   vehicle
