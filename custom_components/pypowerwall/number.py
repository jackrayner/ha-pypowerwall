"""Number platform for pypowerwall."""

from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import PypowerwallConfigEntry
from .const import CONF_CONN_TYPE, CONN_TYPE_TEDAPI_V1R
from .coordinator import PowerwallDataUpdateCoordinator
from .entity import PowerwallEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: PypowerwallConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up pypowerwall number entities from a config entry."""
    coordinator = entry.runtime_data
    entities: list[NumberEntity] = [PowerwallReserveNumber(coordinator)]
    if entry.data[CONF_CONN_TYPE] == CONN_TYPE_TEDAPI_V1R:
        entities.extend(
            [
                PowerwallDispatchPowerNumber(coordinator),
                PowerwallDispatchDurationNumber(coordinator),
            ]
        )
    async_add_entities(entities)


class PowerwallReserveNumber(PowerwallEntity, NumberEntity):
    """Controls the Powerwall's backup reserve percentage."""

    _attr_translation_key = "battery_reserve"
    _attr_native_min_value = 0
    _attr_native_max_value = 100
    _attr_native_step = 1
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_mode = NumberMode.SLIDER

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_battery_reserve"

    @property
    def native_value(self) -> float | None:
        return self.coordinator.data.battery_reserve

    async def async_set_native_value(self, value: float) -> None:
        await self.hass.async_add_executor_job(self.coordinator.pw.set_reserve, value)
        await self.coordinator.async_request_refresh()


class PowerwallDispatchPowerNumber(PowerwallEntity, NumberEntity):
    """Sets the wattage the battery should dispatch during a manual event."""

    _attr_translation_key = "power_watts"
    _attr_native_min_value = -10000
    _attr_native_max_value = 10000
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "W"
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_power_watts"
        self._attr_native_value = 500

    @property
    def native_value(self) -> float | None:
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = int(value)
        self.async_write_ha_state()


class PowerwallDispatchDurationNumber(PowerwallEntity, NumberEntity):
    """Sets how long the manual battery dispatch should run."""

    _attr_translation_key = "duration_seconds"
    _attr_native_min_value = 0
    _attr_native_max_value = 86400
    _attr_native_step = 1
    _attr_native_unit_of_measurement = "s"
    _attr_mode = NumberMode.BOX

    def __init__(self, coordinator: PowerwallDataUpdateCoordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{self._din}_duration_seconds"
        self._attr_native_value = 30

    @property
    def native_value(self) -> float | None:
        return self._attr_native_value

    async def async_set_native_value(self, value: float) -> None:
        self._attr_native_value = int(value)
        self.async_write_ha_state()
