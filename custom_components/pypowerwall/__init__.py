"""The pypowerwall integration."""

from __future__ import annotations

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError

from pypowerwall.helpers import validate_battery_dispatch

from .const import (
    ATTR_CONFIG_ENTRY_ID,
    ATTR_DURATION_SECONDS,
    ATTR_POWER_WATTS,
    CONF_CONN_TYPE,
    CONN_TYPE_TEDAPI_V1R,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_CLOUD,
    DOMAIN,
    GRID_CONTROL_CONN_TYPES,
    SERVICE_CANCEL_MAX_BACKUP,
    SERVICE_DISPATCH_BATTERY_POWER,
    SERVICE_RESUME_BATTERY_OPERATION,
    SERVICE_SCHEDULE_MAX_BACKUP,
)
from .coordinator import PowerwallDataUpdateCoordinator, async_connect_powerwall

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SELECT,
    Platform.SWITCH,
    Platform.BUTTON,
]

type PypowerwallConfigEntry = ConfigEntry[PowerwallDataUpdateCoordinator]

SCHEDULE_MAX_BACKUP_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_DURATION_SECONDS, default=7200): vol.All(
            vol.Coerce(int), vol.Range(min=1)
        ),
    }
)


def _validate_dispatch(data: dict) -> dict:
    """Apply the library's input contract without coercing invalid values."""
    try:
        validate_battery_dispatch(data[ATTR_POWER_WATTS], data[ATTR_DURATION_SECONDS])
    except ValueError as exc:
        raise vol.Invalid(str(exc)) from exc
    return data


DISPATCH_BATTERY_POWER_SCHEMA = vol.Schema(
    vol.All(
        {
            vol.Required(ATTR_POWER_WATTS): object,
            vol.Required(ATTR_DURATION_SECONDS): object,
            vol.Optional(ATTR_CONFIG_ENTRY_ID): str,
        },
        _validate_dispatch,
    )
)
RESUME_BATTERY_OPERATION_SCHEMA = vol.Schema({vol.Optional(ATTR_CONFIG_ENTRY_ID): str})


async def async_setup_entry(hass: HomeAssistant, entry: PypowerwallConfigEntry) -> bool:
    """Set up pypowerwall from a config entry."""
    pw = await async_connect_powerwall(hass, entry.data[CONF_CONN_TYPE], entry.data)

    default_scan_interval = (
        DEFAULT_SCAN_INTERVAL_CLOUD
        if entry.data[CONF_CONN_TYPE] in GRID_CONTROL_CONN_TYPES
        else DEFAULT_SCAN_INTERVAL
    )
    scan_interval = entry.options.get("scan_interval", default_scan_interval)
    coordinator = PowerwallDataUpdateCoordinator(hass, entry, pw, scan_interval)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    entry.async_on_unload(entry.add_update_listener(_async_update_listener))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    if entry.data[CONF_CONN_TYPE] == CONN_TYPE_TEDAPI_V1R:
        _async_register_v1r_services(hass, entry)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: PypowerwallConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_update_listener(hass: HomeAssistant, entry: PypowerwallConfigEntry) -> None:
    """Reload the entry when its options change (e.g. scan interval)."""
    await hass.config_entries.async_reload(entry.entry_id)


def _async_register_v1r_services(hass: HomeAssistant, entry: PypowerwallConfigEntry) -> None:
    """Register the max-backup (storm watch) and battery-dispatch actions for v1r LAN entries.

    schedule_max_backup()/cancel_max_backup() are momentary actions rather than
    persistent state, so they're exposed as Home Assistant services rather than
    entities. They require v1r LAN mode -- pypowerwall itself checks
    tedapi_mode == "v1r" and no-ops (logs an error, returns None) otherwise, and
    CONN_TYPE_TEDAPI_V1R is the only connection type that puts pypowerwall into
    that mode (see coordinator.build_powerwall_kwargs()).

    Services are domain-scoped rather than per-entry in Home Assistant. If more
    than one v1r entry is configured, the most-recently-set-up entry's
    coordinator handles max-backup actions; dispatch/resume require an explicit
    config_entry_id. To keep the services working
    for as long as *any* v1r entry is loaded, we track every currently-loaded
    v1r entry in hass.data (insertion order = setup order): unloading one entry
    re-points the services at another still-loaded v1r entry rather than
    unregistering them outright, and they're only removed once the last v1r
    entry unloads.
    """
    v1r_entries: dict[str, PypowerwallConfigEntry] = hass.data.setdefault(DOMAIN, {}).setdefault(
        "v1r_entries", {}
    )
    v1r_entries[entry.entry_id] = entry

    async def _battery_dispatch(call: ServiceCall) -> ServiceResponse:
        entry_id = call.data.get(ATTR_CONFIG_ENTRY_ID)
        if entry_id is None:
            if len(v1r_entries) != 1:
                raise ServiceValidationError(
                    translation_domain=DOMAIN,
                    translation_key="battery_dispatch_target_required",
                )
            target_entry = next(iter(v1r_entries.values()))
        elif (target_entry := v1r_entries.get(entry_id)) is None:
            raise ServiceValidationError(
                translation_domain=DOMAIN,
                translation_key="battery_dispatch_invalid_target",
            )
        coordinator = target_entry.runtime_data
        try:
            if call.service == SERVICE_DISPATCH_BATTERY_POWER:
                result = await hass.async_add_executor_job(
                    coordinator.pw.dispatch_battery_power,
                    call.data[ATTR_POWER_WATTS],
                    call.data[ATTR_DURATION_SECONDS],
                )
            else:
                result = await hass.async_add_executor_job(coordinator.pw.resume_battery_operation)
        except Exception as exc:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="battery_dispatch_failed",
            ) from exc
        if result is None:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="battery_dispatch_failed",
            )
        await coordinator.async_request_refresh()
        return result

    def _register_for(target_entry: PypowerwallConfigEntry) -> None:
        coordinator = target_entry.runtime_data

        async def _schedule_max_backup(call: ServiceCall) -> None:
            duration_seconds = call.data[ATTR_DURATION_SECONDS]
            await hass.async_add_executor_job(coordinator.pw.schedule_max_backup, duration_seconds)
            await coordinator.async_request_refresh()

        async def _cancel_max_backup(call: ServiceCall) -> None:
            await hass.async_add_executor_job(coordinator.pw.cancel_max_backup)
            await coordinator.async_request_refresh()

        hass.services.async_register(
            DOMAIN,
            SERVICE_SCHEDULE_MAX_BACKUP,
            _schedule_max_backup,
            schema=SCHEDULE_MAX_BACKUP_SCHEMA,
        )
        hass.services.async_register(DOMAIN, SERVICE_CANCEL_MAX_BACKUP, _cancel_max_backup)
        hass.services.async_register(
            DOMAIN,
            SERVICE_DISPATCH_BATTERY_POWER,
            _battery_dispatch,
            schema=DISPATCH_BATTERY_POWER_SCHEMA,
            supports_response=SupportsResponse.OPTIONAL,
        )
        hass.services.async_register(
            DOMAIN,
            SERVICE_RESUME_BATTERY_OPERATION,
            _battery_dispatch,
            schema=RESUME_BATTERY_OPERATION_SCHEMA,
            supports_response=SupportsResponse.OPTIONAL,
        )

    _register_for(entry)

    def _remove_services() -> None:
        v1r_entries.pop(entry.entry_id, None)
        if v1r_entries:
            # Another v1r entry is still loaded -- re-point the services at the
            # most-recently-set-up one still around rather than tearing them
            # down out from under it.
            _register_for(next(reversed(v1r_entries.values())))
        else:
            hass.services.async_remove(DOMAIN, SERVICE_SCHEDULE_MAX_BACKUP)
            hass.services.async_remove(DOMAIN, SERVICE_CANCEL_MAX_BACKUP)
            hass.services.async_remove(DOMAIN, SERVICE_DISPATCH_BATTERY_POWER)
            hass.services.async_remove(DOMAIN, SERVICE_RESUME_BATTERY_OPERATION)

    entry.async_on_unload(_remove_services)
