"""Binary sensor platform for pypowerwall."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PypowerwallConfigEntry
from .const import CONF_CONN_TYPE, CONN_TYPE_TEDAPI_V1R
from .coordinator import PowerwallDataUpdateCoordinator
from .entity import PowerwallEntity


@dataclass(frozen=True, kw_only=True)
class PowerwallAlertBinarySensorDescription(BinarySensorEntityDescription):
    """Describes a binary sensor that is on while a named gateway alert is active."""

    alert: str


# All disabled by default: they only mirror whether an alert is currently reported, and
# some alert meanings are community-sourced (see docs/alerts.md).
ALERT_BINARY_SENSOR_DESCRIPTIONS: tuple[PowerwallAlertBinarySensorDescription, ...] = (
    PowerwallAlertBinarySensorDescription(
        key="battery_calibration",
        translation_key="battery_calibration",
        alert="BatteryCalibration",
    ),
    PowerwallAlertBinarySensorDescription(
        key="battery_fault",
        translation_key="battery_fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        alert="BatteryFault",
    ),
    PowerwallAlertBinarySensorDescription(
        key="grid_manually_disconnected",
        translation_key="grid_manually_disconnected",
        alert="ScheduledIslandContactorOpen",
    ),
    PowerwallAlertBinarySensorDescription(
        key="self_consumption_reserve_limit",
        translation_key="self_consumption_reserve_limit",
        alert="SelfConsumptionReservedLimit",
    ),
    PowerwallAlertBinarySensorDescription(
        key="solar_charge_only_limited",
        translation_key="solar_charge_only_limited",
        alert="SolarChargeOnlyLimited",
    ),
    PowerwallAlertBinarySensorDescription(
        key="backfeed_limited",
        translation_key="backfeed_limited",
        alert="BackfeedLimited",
    ),
    PowerwallAlertBinarySensorDescription(
        key="site_min_power_limited",
        translation_key="site_min_power_limited",
        alert="SiteMinPowerLimited",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PypowerwallConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up pypowerwall binary sensors from a config entry."""
    coordinator = entry.runtime_data
    async_add_entities(
        [
            PowerwallGridConnectedBinarySensor(coordinator),
            *(
                PowerwallAlertBinarySensor(coordinator, description)
                for description in ALERT_BINARY_SENSOR_DESCRIPTIONS
            ),
        ]
    )
    if entry.data[CONF_CONN_TYPE] == CONN_TYPE_TEDAPI_V1R:
        async_add_entities([PowerwallMaxBackupActiveBinarySensor(coordinator)])


class PowerwallGridConnectedBinarySensor(PowerwallEntity, BinarySensorEntity):
    """Whether the Powerwall gateway is currently connected to the grid."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_translation_key = "grid_connected"

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_grid_connected"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.grid_connected


class PowerwallMaxBackupActiveBinarySensor(PowerwallEntity, BinarySensorEntity):
    """Whether a manual max-backup event is active on the gateway."""

    _attr_translation_key = "max_backup_active"

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_max_backup_active"

    @property
    def is_on(self) -> bool | None:
        return self.coordinator.data.max_backup_active

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return {"backup_events": self.coordinator.data.backup_events}


class PowerwallAlertBinarySensor(PowerwallEntity, BinarySensorEntity):
    """On while the gateway reports the alert named by the description."""

    entity_description: PowerwallAlertBinarySensorDescription
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_entity_registry_enabled_default = False

    def __init__(
        self,
        coordinator: PowerwallDataUpdateCoordinator,
        description: PowerwallAlertBinarySensorDescription,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{self._din}_{description.key}"

    @property
    def is_on(self) -> bool:
        return self.entity_description.alert in self.coordinator.data.alerts
