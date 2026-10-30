from custom_components.pypowerwall.coordinator import PowerwallData
from custom_components.pypowerwall.sensor import (
    _battery_export_power,
    _battery_import_power,
    _grid_export_power,
    _grid_import_power,
    _trapezoidal_energy_delta_kwh,
)


class TestBatteryImportExportPower:
    def test_charging_is_import_only(self):
        data = PowerwallData(battery_power=-500)
        assert _battery_import_power(data) == 500
        assert _battery_export_power(data) == 0

    def test_discharging_is_export_only(self):
        data = PowerwallData(battery_power=750)
        assert _battery_import_power(data) == 0
        assert _battery_export_power(data) == 750

    def test_idle_battery_is_zero_both_ways(self):
        data = PowerwallData(battery_power=0)
        assert _battery_import_power(data) == 0
        assert _battery_export_power(data) == 0

    def test_missing_battery_power_is_none_both_ways(self):
        data = PowerwallData(battery_power=None)
        assert _battery_import_power(data) is None
        assert _battery_export_power(data) is None


class TestGridImportExportPower:
    """Grid's sign convention is the OPPOSITE of battery's: negative grid_power
    means exporting to the grid, positive means importing -- see sensor.py's
    _grid_import_power docstring for the derivation from pypowerwall's own
    README. These cases mirror pypowerwall's example /api/meters/aggregates
    payload (site.instant_power=-23 while net-exporting), and would fail if the
    sign handling were accidentally copy-pasted from battery's convention.
    """

    def test_negative_grid_power_is_export_only(self):
        data = PowerwallData(grid_power=-23)
        assert _grid_import_power(data) == 0
        assert _grid_export_power(data) == 23

    def test_positive_grid_power_is_import_only(self):
        data = PowerwallData(grid_power=750)
        assert _grid_import_power(data) == 750
        assert _grid_export_power(data) == 0

    def test_idle_grid_is_zero_both_ways(self):
        data = PowerwallData(grid_power=0)
        assert _grid_import_power(data) == 0
        assert _grid_export_power(data) == 0

    def test_missing_grid_power_is_none_both_ways(self):
        data = PowerwallData(grid_power=None)
        assert _grid_import_power(data) is None
        assert _grid_export_power(data) is None


class TestTrapezoidalEnergyDeltaKwh:
    def test_constant_power_for_one_hour(self):
        # 1000W held constant for 3600s (1h) = 1 kWh.
        assert _trapezoidal_energy_delta_kwh(1000, 1000, 3600) == 1.0

    def test_ramping_power_averages_the_two_samples(self):
        # (0W + 2000W) / 2 = 1000W average, held for 1800s (0.5h) = 0.5 kWh.
        assert _trapezoidal_energy_delta_kwh(0, 2000, 1800) == 0.5

    def test_zero_elapsed_time_is_zero_delta(self):
        assert _trapezoidal_energy_delta_kwh(500, 1500, 0) == 0.0

    def test_short_interval_matches_hand_computed_value(self):
        # (100W + 300W) / 2 = 200W average, held for 10s -> 200 * (10/3600) / 1000 kWh.
        result = _trapezoidal_energy_delta_kwh(100, 300, 10)
        assert result == 200 * (10 / 3600) / 1000


class TestFanSensor:
    def _sensor(self, signal, fans):
        from unittest.mock import MagicMock

        from custom_components.pypowerwall.sensor import PowerwallFanSensor

        coordinator = MagicMock()
        coordinator.data = PowerwallData(din="DIN1", fans=fans)
        return PowerwallFanSensor(coordinator, "TEPINV--x", signal)

    def test_speed_is_rpm(self):
        s = self._sensor("PCH_FanSpeed_B", {"TEPINV--x": {"PCH_FanSpeed_B": 1397}})
        assert s.native_unit_of_measurement == "rpm"
        assert s.native_value == 1397
        assert s.translation_key == "fan_speed"
        assert s.translation_placeholders == {"device": "TEPINV--x", "fan": "B"}

    def test_duty_is_percent(self):
        s = self._sensor("PCH_FanDuty_A", {"TEPINV--x": {"PCH_FanDuty_A": 19.1}})
        assert s.native_unit_of_measurement == "%"
        assert s.translation_key == "fan_duty"
        assert s.native_value == 19.1

    def test_missing_device_is_none(self):
        s = self._sensor("PCH_FanDuty_A", {})
        assert s.native_value is None


class TestAlertAttributes:
    def _sensor(self, key, alerts):
        from unittest.mock import MagicMock

        from custom_components.pypowerwall.sensor import SENSOR_DESCRIPTIONS, PowerwallSensor

        description = next(d for d in SENSOR_DESCRIPTIONS if d.key == key)
        coordinator = MagicMock()
        coordinator.data = PowerwallData(din="DIN1", alerts=alerts)
        return PowerwallSensor(coordinator, description)

    def test_alert_names_exposed_as_attribute(self):
        s = self._sensor("alert_count", ["GridCodesWrite", "PodCommissionTime"])
        assert s.native_value == 2
        assert s.extra_state_attributes == {"alerts": ["GridCodesWrite", "PodCommissionTime"]}

    def test_no_alerts_gives_empty_list(self):
        s = self._sensor("alert_count", [])
        assert s.native_value == 0
        assert s.extra_state_attributes == {"alerts": []}

    def test_other_sensors_have_no_attributes(self):
        assert self._sensor("firmware_version", []).extra_state_attributes is None


class TestAlertBinarySensors:
    CASES = [
        ("battery_calibration", "BatteryCalibration", None),
        ("calibration_requested", "CalibrationRequested", None),
        ("battery_fault", "BatteryFault", "problem"),
        ("grid_manually_disconnected", "ScheduledIslandContactorOpen", "none"),
        ("self_consumption_reserve_limit", "SelfConsumptionReservedLimit", None),
        ("solar_charge_only_limited", "SolarChargeOnlyLimited", None),
        ("backfeed_limited", "BackfeedLimited", None),
        ("site_min_power_limited", "SiteMinPowerLimited", None),
    ]

    def _sensor(self, key, alerts):
        from unittest.mock import MagicMock

        from custom_components.pypowerwall.binary_sensor import (
            ALERT_BINARY_SENSOR_DESCRIPTIONS,
            PowerwallAlertBinarySensor,
        )

        description = next(d for d in ALERT_BINARY_SENSOR_DESCRIPTIONS if d.key == key)
        coordinator = MagicMock()
        coordinator.data = PowerwallData(din="DIN1", alerts=alerts)
        return PowerwallAlertBinarySensor(coordinator, description)

    def test_on_only_while_its_alert_is_active(self):
        for key, alert, _ in self.CASES:
            assert self._sensor(key, [alert, "GridCodesWrite"]).is_on is True
            assert self._sensor(key, ["GridCodesWrite"]).is_on is False
            assert self._sensor(key, []).is_on is False

    def test_each_sensor_ignores_the_others_alerts(self):
        others = [alert for _, alert, _ in self.CASES]
        assert (
            self._sensor("battery_fault", [a for a in others if a != "BatteryFault"]).is_on is False
        )

    def test_diagnostic_and_disabled_by_default(self):
        from homeassistant.const import EntityCategory

        for key, _, _ in self.CASES:
            sensor = self._sensor(key, [])
            assert sensor.entity_registry_enabled_default is False
            assert sensor.entity_category is EntityCategory.DIAGNOSTIC

    def test_battery_fault_is_a_problem_sensor(self):
        assert self._sensor("battery_fault", []).device_class == "problem"

    def test_unique_id_keeps_the_original_battery_calibration_suffix(self):
        assert self._sensor("battery_calibration", []).unique_id.endswith("_battery_calibration")
