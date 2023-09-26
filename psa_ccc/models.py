"""Models for the API responses."""
from __future__ import annotations

import datetime
from enum import Enum
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


class User(BaseEntity):
    """User information."""

    first_name: str
    last_name: str
    email: str
    embedded: VehicleList
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


class VehicleBranding(Struct, kw_only=True, rename=rename):
    """Vehicle branding."""

    brand: str
    label: str


class VehiclePictures(Struct, kw_only=True, rename=rename):
    """Vehicle pictures."""

    pictures: list[str]


class VehicleExtension(Struct, kw_only=True, rename=rename):
    """Vehicle extension."""

    vehicle_branding: VehicleBranding
    vehicle_pictures: VehiclePictures


class VehicleSummary(Struct, kw_only=True, rename=rename):
    """Summary of the vehicle found in the user response."""

    id: str
    vin: str
    vehicle_extension: VehicleExtension


class Vehicle(Struct, kw_only=True, rename=rename):
    """Vehicle information."""

    id: str
    vin: str
    vehicle_extension: VehicleExtension
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


class AlertMsgEnum(str, Enum):
    """Alert messages."""

    ALERT_OIL_PRESSURE = "alertOilPressure"
    ALERT_COOLANT_TEMP = "alertCoolantTemp"
    CHARGING_SYSTEM_FAULT = "chargingSystemFault"
    ALERT_BRAKE_FLUID = "alertBrakeFluid"
    STEERING_FAULT = "steeringFault"
    ALERT_COOLANT_LEVEL = "alertCoolantLevel"
    LANE_DEPARTURE_WARNING_SYSTEM_FAULT = "laneDepartureWarningSystemFault"
    FRONT_LEFT_DOOR_OPEN_HIGH_SPEED = "frontLeftDoorOpenHighSpeed"
    FRONT_RIGHT_DOOR_OPEN_HIGH_SPEED = "frontRightDoorOpenHighSpeed"
    REAR_LEFT_DOOR_OPEN_HIGH_SPEED = "rearLeftDoorOpenHighSpeed"
    REAR_RIGHT_DOOR_OPEN_HIGH_SPEED = "rearRightDoorOpenHighSpeed"
    TRUNK_OPEN_HIGH_SPEED = "trunkOpenHighSpeed"
    TRUNK_WINDOW_OPEN = "trunkWindowOpen"
    ESP_FAULT = "espFault"
    BATTERY_LEVEL_FAULT = "batteryLevelFault"
    WATER_IN_GASOIL = "waterInGasoil"
    PAD_WEAR_FAULT = "padWearFault"
    FUEL_LEVEL_ALARM = "fuelLevelAlarm"
    AIRBAG_OR_SEATBELT_FAULT = "airbagOrSeatbeltFault"
    ENGINE_FAULT = "engineFault"
    ABS_FAULT = "absFault"
    RISK_OF_PARTICLE_FILTER_BLOCKAGE = "riskOfParticleFilterBlockage"
    PARTICLE_FILTER_ADDITIVE_TOO_LOW = "particleFilterAdditiveTooLow"
    SUSPENSION_FAULT = "suspensionFault"
    PREAHEATING_DEACTIVATED_BATTERY_TOO_LOW = "preaheatingDeactivatedBatteryTooLow"
    PREAHEATING_DEACTIVATED_FUEL_LEVEL_TOO_LOW = "preaheatingDeactivatedFuelLevelTooLow"
    CHECK_THE_BRAKE_LAMP = "checkTheBrakeLamp"
    RETRACTABLE_ROOF_MECHANISM_FAULT = "retractableRoofMechanismFault"
    ALERT_STEERING_LOCK = "alertSteeringLock"
    ELECTRONIC_IMMOBILISER_FAULT = "electronicImmobiliserFault"
    ROOF_OPERATION_IMPOSSIBLE_TEMPERATURE_TOO_HIGH = (
        "roofOperationImpossibleTemperatureTooHigh"
    )
    ROOF_OPERATION_IMPOSSIBLE_START_ENGINE = "roofOperationImpossibleStartEngine"
    ROOF_OPERATION_IMPOSSIBLE_APPLY_PARKING_BREAK = (
        "roofOperationImpossibleApplyParkingBreak"
    )
    HYBRID_SYSTEM_FAULT = "hybridSystemFault"
    AUTOMATIC_HEADLAMP_FAULT = "automaticHeadlampFault"
    HYBRID_SYSTEM_FAULT_REPAIRED_THE_VEHICLE = "hybridSystemFaultRepairedTheVehicle"
    WASHER_LEVEL_ALARM = "washerLevelAlarm"
    BATTERY_KEY_ALARM = "batteryKeyAlarm"
    PREAHEATING_DEACTIVATED_SET_THE_CLOCK = "preaheatingDeactivatedSetTheClock"
    TRAILER_CONNECTION_FAULT = "trailerConnectionFault"
    UNDER_INFLATION_TYRE_FAULT = "underInflationTyreFault"
    LIMITED_VISIBILITY_AIDS_CAMERA = "limitedVisibilityAidsCamera"
    ELECTRIC_MODE_NOT_AVAILABLE = "electricModeNotAvailable"
    WHEEL_PRESSURE_FAULT = "wheelPressureFault"
    CHECK_SIDE_LAMPS = "checkSideLamps"
    CHECK_RIGHT_BRAKE_LAMP = "checkRightBrakeLamp"
    CHECK_LEFT_BRAKE_LAMP = "checkLeftBrakeLamp"
    FRONT_FOGLIGHT_FAULT = "frontFoglightFault"
    REAR_FOGLIGHT_FAULT = "rearFoglightFault"
    CHECK_DIRECTION_INDICATOR = "checkDirectionIndicator"
    CHECK_REVERSING_LAMP = "checkReversingLamp"
    PARKING_ASSISTANCE_FAULT = "parkingAssistanceFault"
    ADJUST_TYRE_PRESSURE = "adjustTyrePressure"
    ANTIPOLLUTION_FAULT = "antipollutionFault"
    PLACE_GEAR_BOX_TO_P = "placeGearBoxToP"
    RISK_OF_ICE = "riskOfIce"
    FRONT_RIGHT_DOOR_OPEN = "frontRightDoorOpen"
    FRONT_LEFT_DOOR_OPEN = "frontLeftDoorOpen"
    REAR_RIGHT_DOOR_OPEN = "rearRightDoorOpen"
    REAR_LEFT_DOOR_OPEN = "rearLeftDoorOpen"
    TRUNK_OPEN = "trunkOpen"
    BOOT_OPEN = "bootOpen"
    REAR_SCREEN_OPEN = "rearScreenOpen"
    PARKING_BREAK_FAULT = "parkingBreakFault"
    ACTIVE_SPOILER_FAULT = "activeSpoilerFault"
    AUTOMATIC_BREAKING_SYSTEM_FAULT = "automaticBreakingSystemFault"
    DIRECTIONAL_HEADLAMPS_FAULT = "directionalHeadlampsFault"
    AUTOMATIC_GEARBOX_FAULT = "automaticGearboxFault"
    SUSPENSION_FAULT_LIMIT_TO90KM = "suspensionFaultLimitTo90km"
    FRONT_LEFT_TYRE_NOT_MONITORED = "frontLeftTyreNotMonitored"
    FRONT_RIGHT_TYRE_NOT_MONITORED = "frontRightTyreNotMonitored"
    REAR_RIGHT_TYRE_NOT_MONITORED = "rearRightTyreNotMonitored"
    REAR_LEFT_TYRE_NOT_MONITORED = "rearLeftTyreNotMonitored"
    POWER_STEERING_FAULT = "powerSteeringFault"
    LANE_DEPARTURE_FAULT = "laneDepartureFault"
    TYRE_UNDER_INFLATION = "tyreUnderInflation"
    SPARE_WHEEL_FITTED_DRIVING_AIDS_DEACTIVATED = (
        "spareWheelFittedDrivingAidsDeactivated"
    )
    AUTOMATIC_BREAKING_DEACTIVED = "automaticBreakingDeactived"
    TUP_UP_AD_BLUE = "tupUpAdBlue"
    LONG_PUSH_TO_UNLOCK_TANK_FAULT = "longPushToUnlockTankFault"


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
