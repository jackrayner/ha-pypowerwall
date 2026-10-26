from datetime import timedelta
from unittest.mock import patch

import pytest
from conftest import DIN, make_fake_pw
from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.pypowerwall.const import (
    CONF_AUTHPATH,
    CONF_CONN_TYPE,
    CONF_GW_PWD,
    CONF_RSA_KEY_PATH,
    CONN_TYPE_CLOUD,
    CONN_TYPE_TEDAPI,
    CONN_TYPE_TEDAPI_V1R,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SCAN_INTERVAL_CLOUD,
    DOMAIN,
)

CONNECT_TARGET = "custom_components.pypowerwall.coordinator.pypowerwall.Powerwall"
ENTRY_DATA = {CONF_CONN_TYPE: CONN_TYPE_TEDAPI, "host": "192.168.91.1", CONF_GW_PWD: "secret"}


def _entity_state(hass: HomeAssistant, platform: str, unique_id: str):
    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id(platform, DOMAIN, f"{DIN}_{unique_id}")
    assert entity_id is not None, f"no {platform} entity registered for unique_id {unique_id}"
    return hass.states.get(entity_id)


async def test_setup_creates_entities_and_unload_removes_them(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=DIN,
        data=ENTRY_DATA,
    )
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw()):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.LOADED

    battery = _entity_state(hass, "sensor", "battery_level")
    assert float(battery.state) == 42.0

    grid_power = _entity_state(hass, "sensor", "grid_power")
    assert float(grid_power.state) == 100.0

    # conftest's default battery_power is -50.0 (charging), so import > 0, export == 0.
    battery_import_power = _entity_state(hass, "sensor", "battery_import_power")
    assert float(battery_import_power.state) == 50.0

    battery_export_power = _entity_state(hass, "sensor", "battery_export_power")
    assert float(battery_export_power.state) == 0.0

    battery_energy_imported = _entity_state(hass, "sensor", "battery_energy_imported")
    assert float(battery_energy_imported.state) == 5.0
    assert battery_energy_imported.attributes["state_class"] == "total_increasing"
    assert battery_energy_imported.attributes["device_class"] == "energy"

    battery_energy_exported = _entity_state(hass, "sensor", "battery_energy_exported")
    assert float(battery_energy_exported.state) == 3.0

    grid_connected = _entity_state(hass, "binary_sensor", "grid_connected")
    assert grid_connected.state == "on"

    temp = _entity_state(hass, "sensor", "temp_TETHC--1")
    assert float(temp.state) == 25.0

    device = dr.async_get(hass).async_get_device_by_identifier((DOMAIN, DIN), entry.entry_id)
    assert device is not None
    assert device.serial_number == DIN

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_v1r_string_sensors_discovery_updates_and_recovery(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=DIN,
        data={
            **ENTRY_DATA,
            CONF_CONN_TYPE: CONN_TYPE_TEDAPI_V1R,
            CONF_RSA_KEY_PATH: "/config/pypowerwall.pem",
        },
    )
    entry.add_to_hass(hass)
    pw = make_fake_pw()
    with patch(CONNECT_TARGET, return_value=pw):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    registry = er.async_get(hass)

    def string_entries():
        return {
            item.unique_id: item.entity_id
            for item in er.async_entries_for_config_entry(registry, entry.entry_id)
            if item.unique_id.startswith(f"{DIN}_string_")
        }

    assert string_entries() == {}
    primary = {
        f"{prefix}_{letter}": value
        for letter in "ABCDEF"
        for prefix, value in (
            ("PVAC_PVMeasuredPower", 1200),
            ("PVAC_PVCurrent", 3.0),
            ("PVAC_PVMeasuredVoltage", 400.0),
        )
    }
    pw.vitals.return_value = {"PVAC--primary": primary}
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()

    assert len(string_entries()) == 18
    for letter in "ABCDEF":
        for metric, value, unit in (
            ("power", 1200, "W"),
            ("current", 3, "A"),
            ("voltage", 400, "V"),
        ):
            state = _entity_state(hass, "sensor", f"string_PVAC--primary_{letter}_{metric}")
            assert float(state.state) == value
            assert state.attributes["device_class"] == metric
            assert state.attributes["unit_of_measurement"] == unit
            assert state.attributes["state_class"] == "measurement"

    original_entities = string_entries()
    primary["PVAC_PVMeasuredPower_A"] = 0
    primary["PVAC_PVCurrent_A"] = None
    del primary["PVAC_PVMeasuredVoltage_A"]
    pw.vitals.return_value = {
        "PVAC--secondary": {"PVAC_PVMeasuredPower_A": 600},
        "PVAC--primary": primary,
    }
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()
    assert len(string_entries()) == 19
    assert original_entities.items() <= string_entries().items()
    assert _entity_state(hass, "sensor", "string_PVAC--primary_A_power").state == "0"
    for metric in ("current", "voltage"):
        assert (
            _entity_state(hass, "sensor", f"string_PVAC--primary_A_{metric}").state == "unavailable"
        )
    assert _entity_state(hass, "sensor", "string_PVAC--secondary_A_power").state == "600"

    pw.vitals.return_value = None
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()
    assert _entity_state(hass, "sensor", "string_PVAC--primary_A_power").state == "unavailable"

    pw.vitals.return_value = {"PVAC--primary": primary}
    await entry.runtime_data.async_refresh()
    await hass.async_block_till_done()
    assert _entity_state(hass, "sensor", "string_PVAC--primary_A_power").state == "0"
    assert len(string_entries()) == 19
    assert original_entities.items() <= string_entries().items()

    assert await hass.config_entries.async_unload(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_uptime_sensor_accepts_go_duration_string(
    hass: HomeAssistant, caplog: pytest.LogCaptureFixture
) -> None:
    # pypowerwall's uptime() returns a Go-style duration string despite the
    # misleading "up_time_seconds" field name (e.g. "62h48m24.076725628s"), not
    # a numeric seconds count. Declaring a native_unit_of_measurement on this
    # sensor previously made Home Assistant expect a numeric value, which
    # raised (caught, logged as an error) on every non-numeric uptime string.
    entry = MockConfigEntry(domain=DOMAIN, unique_id=DIN, data=ENTRY_DATA)
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw(uptime="62h48m24.076725628s")):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    uptime = _entity_state(hass, "sensor", "uptime")
    assert uptime.state == "62h48m24.076725628s"
    assert "non-numeric value" not in caplog.text


async def test_grid_down_marks_binary_sensor_off(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=DIN,
        data=ENTRY_DATA,
    )
    entry.add_to_hass(hass)

    pw = make_fake_pw()
    pw.grid_status.return_value = "DOWN"

    with patch(CONNECT_TARGET, return_value=pw):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    grid_connected = _entity_state(hass, "binary_sensor", "grid_connected")
    assert grid_connected.state == "off"


async def test_setup_fails_when_not_connected(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=DIN,
        data=ENTRY_DATA,
    )
    entry.add_to_hass(hass)

    pw = make_fake_pw()
    pw.is_connected.return_value = False

    with patch(CONNECT_TARGET, return_value=pw):
        assert not await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_lan_entry_defaults_to_fast_scan_interval(hass: HomeAssistant) -> None:
    entry = MockConfigEntry(domain=DOMAIN, unique_id=DIN, data=ENTRY_DATA)
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw()):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.runtime_data.update_interval == timedelta(seconds=DEFAULT_SCAN_INTERVAL)


async def test_cloud_entry_defaults_to_slow_scan_interval(hass: HomeAssistant) -> None:
    cloud_din = "CLOUD00-00-E--TG000000000000"
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=cloud_din,
        data={CONF_CONN_TYPE: CONN_TYPE_CLOUD, CONF_AUTHPATH: "/config/pypowerwall"},
    )
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw(din=cloud_din)):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.runtime_data.update_interval == timedelta(seconds=DEFAULT_SCAN_INTERVAL_CLOUD)


async def test_cloud_entry_explicit_scan_interval_overrides_cloud_default(
    hass: HomeAssistant,
) -> None:
    cloud_din = "CLOUD01-00-E--TG000000000001"
    entry = MockConfigEntry(
        domain=DOMAIN,
        unique_id=cloud_din,
        data={CONF_CONN_TYPE: CONN_TYPE_CLOUD, CONF_AUTHPATH: "/config/pypowerwall"},
        options={"scan_interval": 20},
    )
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw(din=cloud_din)):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    assert entry.runtime_data.update_interval == timedelta(seconds=20)


@pytest.mark.parametrize(
    ("key", "alert"),
    [
        ("battery_calibration", "BatteryCalibration"),
        ("battery_fault", "BatteryFault"),
        ("grid_manually_disconnected", "ScheduledIslandContactorOpen"),
        ("self_consumption_reserve_limit", "SelfConsumptionReservedLimit"),
        ("solar_charge_only_limited", "SolarChargeOnlyLimited"),
        ("backfeed_limited", "BackfeedLimited"),
        ("site_min_power_limited", "SiteMinPowerLimited"),
    ],
)
async def test_alert_binary_sensors_are_disabled_by_default(
    hass: HomeAssistant, key: str, alert: str
) -> None:
    entry = MockConfigEntry(domain=DOMAIN, unique_id=DIN, data=ENTRY_DATA)
    entry.add_to_hass(hass)

    with patch(CONNECT_TARGET, return_value=make_fake_pw(alerts=[alert])):
        assert await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()

    registry = er.async_get(hass)
    entity_id = registry.async_get_entity_id("binary_sensor", DOMAIN, f"{DIN}_{key}")
    assert entity_id is not None
    assert registry.async_get(entity_id).disabled_by is er.RegistryEntryDisabler.INTEGRATION
    assert hass.states.get(entity_id) is None
