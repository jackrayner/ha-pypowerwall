# Alerts

The **Active alerts** sensor reports a count, and its `alerts` attribute lists the alert names the gateway currently reports, sorted. The names are Tesla's raw identifiers, so they look like `PodCommissionTime` rather than a sentence. This page explains the ones seen so far.

> [!WARNING]
> This list is not exhaustive and the set of alerts varies by system and firmware. Most descriptions come from [pypowerwall's alert reference](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) (Tesla's Powerhub manual plus community contributions) and are best-effort, not official Tesla documentation. Rows marked "Observed" were seen on a real system but have no confirmed meaning; the sensor still reports them.

Some alerts are informational and not faults (for example `FWUpdateSucceeded`, "Firmware Upgrade Succeeded"). Names that start with a device prefix such as `POD_`, `PINV_`, `PVS_`, `SYNC_` or `THC_` are device-level codes; the pypowerwall reference also lists Tesla-manual alerts that have only a UI name and no API name, which a sensor will not show.

| Alert | Meaning | Device | Source | Upstream |
| --- | --- | --- | --- | --- |
| `BackfeedLimited` | The system is configured for inadvertent export and therefore will not further discharge to respect this limit. Also exposed as the disabled-by-default "Backfeed limited" binary sensor. | `STSTSM` | Tesla manual | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#backfeed-limited-backfeedlimited) |
| `BatteryCalibration` | Not documented upstream yet. Seen on a real system, meaning unconfirmed. Also exposed as the disabled-by-default "Battery calibration" binary sensor. | — | Observed | [not listed](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) |
| `BatteryFault` | One or more inverter blocks is in a faulted state. (Severity: Critical). Also exposed as the disabled-by-default "Battery fault" binary sensor. | `STSTSM` | Tesla manual | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#battery-fault-batteryfault) |
| `BMS_a083_Nvram_Filecache` | Not documented upstream yet. Seen on a real system, meaning unconfirmed. | — | Observed | [not listed](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) |
| `ChargeOnlyFromSolarOverride` | Not documented upstream yet. Seen on a real system, meaning unconfirmed. | — | Observed | [not listed](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) |
| `FWUpdateSucceeded` | Firmware Upgrade Succeeded | `STSTSM` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#fwupdatesucceeded) |
| `GridCodesWrite` | No description upstream. | `STSTSM` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#gridcodeswrite) |
| `PCH_a054_pwsDisabledMpptEnableLine` | Not documented upstream yet. Seen on a real system, meaning unconfirmed. | — | Observed | [not listed](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) |
| `PINV_a010_can_gtwMIA` | Indicate that gateway/sync is MIA (seen during firmware upgrade reboot) | `TEPINV` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pinv_a010_can_gtwmia) |
| `PINV_a039_can_thcMIA` | Seems to indicate that Home Controller is MIA (seen during firmware upgrade reboot) | `TEPINV` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pinv_a039_can_thcmia) |
| `PINV_a067_overvoltageNeutralChassis` | No description upstream. | `TEPINV` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pinv_a067_overvoltageneutralchassis) |
| `POD_f029_HW_CMA_OV` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_f029_hw_cma_ov) |
| `POD_w024_HW_Fault_Asserted` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w024_hw_fault_asserted) |
| `POD_w029_HW_CMA_OV` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w029_hw_cma_ov) |
| `POD_w031_SW_Brick_OV` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w031_sw_brick_ov) |
| `POD_w044_SW_Brick_UV_Warning` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w044_sw_brick_uv_warning) |
| `POD_w045_SW_Brick_OV_Warning` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w045_sw_brick_ov_warning) |
| `POD_w048_SW_Cell_Voltage_Sens` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w048_sw_cell_voltage_sens) |
| `POD_w058_SW_App_Boot` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w058_sw_app_boot) |
| `POD_w063_SW_SOC_Imbalance` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w063_sw_soc_imbalance) |
| `POD_w067_SW_Not_Enough_Energy_Precharge` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w067_sw_not_enough_energy_precharge) |
| `POD_w090_SW_SOC_Imbalance_Limit_Charge` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w090_sw_soc_imbalance_limit_charge) |
| `POD_w093_SW_Charge_Request` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w093_sw_charge_request) |
| `POD_w105_SW_EOD` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w105_sw_eod) |
| `POD_w109_SW_Self_Test_Request_Not_Serviced` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w109_sw_self_test_request_not_serviced) |
| `POD_w110_SW_EOC` | No description upstream. | `TEPOD` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pod_w110_sw_eoc) |
| `PodCommissionTime` | No description upstream. | `STSTSM` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#podcommissiontime) |
| `PVS_a018_MciString[A-D]` | This indicates a solar string (A, B, C or D) that is not connected. | `PVS` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pvs_a018_mcistringa-d) |
| `PVS_a026_Mci1PvVoltage` | No description upstream. | `PVS` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pvs_a026_mci1pvvoltage) |
| `PVS_a027_Mci2PvVoltage` | No description upstream. | `PVS` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pvs_a027_mci2pvvoltage) |
| `PVS_a031_Mci3PvVoltage` | No description upstream. | `PVS` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pvs_a031_mci3pvvoltage) |
| `PVS_a032_Mci4PvVoltage` | No description upstream. | `PVS` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#pvs_a032_mci4pvvoltage) |
| `RealPowerAvailableLimited` | The command is greater than the Available Battery Real Charge or Discharge Power | `STSTSM` | Tesla manual | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#real-power-available-limited-realpoweravailablelimited) |
| `ScheduledIslandContactorOpen` | Manually Disconnected from Grid. Also exposed as the disabled-by-default "Manually disconnected from grid" binary sensor. | `STSTSM` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#scheduledislandcontactoropen) |
| `SelfConsumptionReservedLimit` | Battery reached reserve limit during self-consumption mode and switches to grid. Also exposed as the disabled-by-default "Battery at reserve limit" binary sensor. | `STSTSM` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#selfconsumptionreservedlimit) |
| `SiteMinPowerLimited` | Cannot meet command because the Site Minimum Power Limit has been set. Also exposed as the disabled-by-default "Site minimum power limited" binary sensor. | `STSTSM` | Tesla manual | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#site-min-power-limited-siteminpowerlimited) |
| `SolarChargeOnlyLimited` | The system has been configured to only charge from solar. Solar is not available; the charge request cannot be met. Also exposed as the disabled-by-default "Solar charge only limited" binary sensor. | `STSTSM` | Tesla manual | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#solar-charge-only-limited-solarchargeonlylimited) |
| `SYNC_a001_SW_App_Boot` | No description upstream. | `TESYNC` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#sync_a001_sw_app_boot) |
| `SYNC_a038_DoOpenArguments` | No description upstream. | `TESYNC` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#sync_a038_doopenarguments) |
| `SystemConnectedToGrid` | Reported while the system is connected to the grid. pypowerwall uses this alert to derive grid status (v0.12.7 release notes). | — | pypowerwall | [release notes](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/RELEASE.md) |
| `THC_w061_CAN_TX_FIFO_Overflow` | No description upstream. | `TETHC` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#thc_w061_can_tx_fifo_overflow) |
| `THC_w155_Backup_Genealogy_Updated` | Unknown but seen during firmware upgrade. | `TETHC` | Community | [entry](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md#thc_w155_backup_genealogy_updated) |

## Using the alerts

In a template, `state_attr('sensor.<your_gateway>_active_alerts', 'alerts')` returns the list, so `'FWUpdateSucceeded' in state_attr(...)` works in automations. To report a new alert or correct a description, contribute it to [pypowerwall's reference](https://github.com/jasonacox/pypowerwall/blob/v0.23.1/docs/reference/alerts.md) so everyone benefits, then update the table here.
