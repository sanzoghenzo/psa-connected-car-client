"""Models for the API responses."""
from __future__ import annotations

import datetime
from enum import StrEnum
from enum import auto
from re import sub
from typing import Any
from typing import Generic
from typing import TypeVar

from msgspec import Struct


def camelize(s: str) -> str:
    """Converts a string into camelCase."""
    s = sub(r"([_\-])+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


def rename(name: str) -> str | None:
    """Custom function to rename the json fields."""
    return f"_{name}" if name in {"links", "embedded"} else camelize(name)


T = TypeVar("T")


class PaginatedResponse(Struct, Generic[T], kw_only=True, rename=rename):
    """Generic wrapper for paginated responses."""

    # links: Any
    total: int
    current_page: int
    total_page: int
    embedded: T


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


class VehicleList(Struct, kw_only=True, rename=rename):
    """List of the vehicles of a user."""

    vehicles: list[VehicleSummary]


class PaginatedVehicles(PaginatedResponse[VehicleList]):
    """Paginated response of get vehicles."""

    pass


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


class VehicleOdometer(BaseEntity, kw_only=True, rename=rename):
    """Vehicle odometer."""

    mileage: float  # [km]


class Battery(BaseEntity, kw_only=True, rename=rename):
    """Describe the car (with combustion engine) battery status."""

    current: float = 0
    voltage: float = 0


class Opening(Struct, kw_only=True, rename=rename):
    """Opening information."""

    identifier: str  # enum
    state: str  # enum


class DoorsState(Struct, kw_only=True, rename=rename):
    """Doors state."""

    locked_state: str  # enum...
    opening: list[Opening]


class EVBatteryCharging(Struct, kw_only=True, rename=rename):
    """Electric Vehicle charging information."""

    plugged: bool
    status: str  # enum
    charging_rate: int  # [0-500 km/h]
    charging_mode: str  # "No", "Slow", "Quick"
    next_delayed_time: str  # datetime.datetime  # timestamp RFC3339 - "PT05"
    # remaining_time: datetime.datetime  # ISO8601 format


class EVBatteryLoad(BaseEntity):
    """Battery capacity and health for electric energy type."""

    capacity: int = 0
    residual: int = 0


class EVBattery(Struct, kw_only=True, rename=rename):
    """Battery capacity and health for electric energy type."""

    load: EVBatteryLoad


class ElectricEnergyExtension(Struct, kw_only=True, rename=rename):
    """Electric energy extension info."""

    battery: EVBattery
    charging: EVBatteryCharging | None = None


class EnergyExtension(Struct, kw_only=True, rename=rename):
    """Vehicle status energy extension."""

    electric: ElectricEnergyExtension | None = None


class Energy(BaseEntity, kw_only=True, rename=rename):
    """Vehicle energy info."""

    type: str  # "Fuel" or "Electric"
    level: float  # 0-100
    sub_type: str = ""  # "FossilEnergy", "ElectricEnergy", ...
    autonomy: float = 0  # [km]
    extension: EnergyExtension | None = None


class EnvironmentAir(BaseEntity):
    """Environment air status."""

    temp: float


class EnvironmentLuminosity(BaseEntity):
    """Environment luminosity status."""

    day: bool


class Environment(BaseEntity):
    """Environment status."""

    air: EnvironmentAir
    luminosity: EnvironmentLuminosity


class Ignition(BaseEntity, kw_only=True, rename=rename):
    """Ignition."""

    type: str  # "Stop" | "StartUp" | "Start" | "Free"


class Kinetic(BaseEntity, kw_only=True, rename=rename):
    """Everything related to the movement of the vehicle."""

    moving: bool
    acceleration: float = 0
    pace: float = 0
    speed: float = 0


class Point(Struct, kw_only=True, rename=rename):
    """Point."""

    coordinates: list[float]  # min 2 elements, max 3
    type: str = "Point"


class PositionProperties(BaseEntity, kw_only=True, rename=rename):
    """Properties of a geospatial position."""

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


class AirConditioning(BaseEntity, kw_only=True, rename=rename):
    """Air conditioning."""

    # failure_cause: str  # enum...
    programs: list[PreconditionProgram]
    status: str  # enum


class Preconditioning(Struct, kw_only=True, rename=rename):
    """Preconditioning."""

    air_conditioning: AirConditioning


class Privacy(BaseEntity, kw_only=True, rename=rename):
    """Privacy model."""

    state: str  # enum


class Safety(BaseEntity, kw_only=True, rename=rename):
    """Safety model."""

    belt_warning: str  # Normal | Omission
    e_call_triggering_request: str  # AirbagUnabled | NoRequest | Requested


class ServiceType(BaseEntity, kw_only=True, rename=rename):
    """Service type."""

    type: str  # Electric | Hybrid | Unknown


class Extension(Struct, kw_only=True, rename=rename):
    """Vehicle status extension."""

    kinetic: Kinetic
    odemeter: VehicleOdometer


class VehicleStatusEmbedded(Struct, kw_only=True, rename=rename):
    """Vehicle status embedded model."""

    extension: Extension


class VehicleStatus(BaseEntity, kw_only=True, rename=rename):
    """Vehicle status response."""

    last_position: Position
    battery: Battery
    privacy: Privacy
    service: ServiceType
    environment: Environment
    odometer: VehicleOdometer
    kinetic: Kinetic
    preconditioning: Preconditioning
    energies: list[Energy]
    # links: Any  # self and vehicle
    # doors_state: DoorsState
    # safety: Safety
    ignition: Ignition | None = None


class Alerts(PaginatedResponse[Any]):
    """Alerts container."""

    pass


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
