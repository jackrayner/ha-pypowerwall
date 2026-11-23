# Automation examples

The integration's writable entities and actions are meant to be driven by Home Assistant automations: a schedule, a price sensor or a weather warning can change how the Powerwall behaves, with no separate app or subscription. These examples cover the common cases. Each one is a complete automation you can paste into the YAML editor (Settings → Automations & scenes → Create automation → ⋮ → Edit in YAML).

The entity IDs below assume the site is called "Home", so its entities look like `number.home_battery_reserve`. Yours depend on your site's name, and recent Home Assistant versions can also put the device's area in front of it. Open the Powerwall device under Settings → Devices & services and copy the real IDs.

| Example | Uses | Connection modes |
| --- | --- | --- |
| [Charge from the grid in a cheap window](#charge-from-the-grid-in-a-cheap-window) | Grid charging switch, Battery reserve number | Cloud, FleetAPI, TEDAPI v1r LAN |
| [Stop exporting while the price is negative](#stop-exporting-while-the-price-is-negative) | Grid export select | Cloud, FleetAPI, TEDAPI v1r LAN |
| [Fill the battery before a storm](#fill-the-battery-before-a-storm) | `pypowerwall.schedule_max_backup` / `cancel_max_backup` | TEDAPI v1r LAN |
| [Get notified of a grid outage](#get-notified-of-a-grid-outage) | Grid connected binary sensor | All |

See the [Entities](../README.md#entities) table for what each mode exposes.

## Charge from the grid in a cheap window

On a time-of-use tariff, let the battery charge from the grid during the cheap hours, then go back to solar-only charging. The usual way is to allow grid charging and raise the reserve above the current charge. Whether and how fast the Powerwall then charges from the grid depends on its firmware, mode and region, so watch it once before relying on it. Set the times and the two reserve levels to match your tariff and your normal reserve.

```yaml
alias: Powerwall - charge from the grid in the cheap window
mode: single
triggers:
  - trigger: time
    at: "00:30:00"
    id: start
  - trigger: time
    at: "06:30:00"
    id: end
actions:
  - choose:
      - conditions:
          - condition: trigger
            id: start
        sequence:
          - action: switch.turn_on
            target:
              entity_id: switch.home_grid_charging
          - action: number.set_value
            target:
              entity_id: number.home_battery_reserve
            data:
              value: 80
      - conditions:
          - condition: trigger
            id: end
        sequence:
          - action: number.set_value
            target:
              entity_id: number.home_battery_reserve
            data:
              value: 20
          - action: switch.turn_off
            target:
              entity_id: switch.home_grid_charging
```

## Stop exporting while the price is negative

With a dynamic export price, stop sending energy to the grid while the price is below zero and go back to your normal export policy afterwards. `sensor.electricity_export_price` stands for whatever price sensor your energy-price integration provides; set the `option` in the second branch to the policy you normally use (`battery_ok`, `pv_only` or `never`).

```yaml
alias: Powerwall - no export at negative prices
mode: single
triggers:
  - trigger: numeric_state
    entity_id: sensor.electricity_export_price
    below: 0
    id: negative
  - trigger: numeric_state
    entity_id: sensor.electricity_export_price
    above: 0
    id: positive
actions:
  - action: select.select_option
    target:
      entity_id: select.home_grid_export
    data:
      option: "{{ 'never' if trigger.id == 'negative' else 'pv_only' }}"
```

## Fill the battery before a storm

Start a manual backup event (max backup) when a weather warning is issued for your area, and end it when the warning is lifted. `binary_sensor.weather_warning` stands for the warning entity of a weather integration such as [Meteoalarm](https://www.home-assistant.io/integrations/meteoalarm/). `duration_seconds` is a ceiling: the event ends on its own after it even if the warning never clears (at most `86400`, one day).

```yaml
alias: Powerwall - max backup during a weather warning
mode: single
triggers:
  - trigger: state
    entity_id: binary_sensor.weather_warning
    to: "on"
    id: warning
  - trigger: state
    entity_id: binary_sensor.weather_warning
    to: "off"
    id: clear
actions:
  - if:
      - condition: trigger
        id: warning
    then:
      - action: pypowerwall.schedule_max_backup
        data:
          duration_seconds: 43200
    else:
      - action: pypowerwall.cancel_max_backup
```

The two actions exist only for TEDAPI v1r LAN entries. With more than one v1r entry they act on the most recently set up one.

## Get notified of a grid outage

Send a phone notification when the home loses the grid and when it comes back, with the battery level and the backup time left. `notify.mobile_app_your_phone` is the notify action of the Home Assistant Companion app on your phone. The `for:` delays skip short blips.

```yaml
alias: Powerwall - grid outage notification
mode: single
triggers:
  - trigger: state
    entity_id: binary_sensor.home_grid_connected
    from: "on"
    to: "off"
    for: "00:00:30"
    id: outage
  - trigger: state
    entity_id: binary_sensor.home_grid_connected
    from: "off"
    to: "on"
    for: "00:01:00"
    id: restored
actions:
  - action: notify.mobile_app_your_phone
    data:
      title: >-
        {{ 'Grid outage' if trigger.id == 'outage' else 'Grid restored' }}
      message: >-
        Battery {{ states('sensor.home_battery_level') | float(0) | round(0) }}%,
        about {{ states('sensor.home_backup_time_remaining') | float(0) | round(1) }} h of backup left.
```

Notifications go through the internet, so during an outage they arrive only if your router and internet connection stay powered (for example on the Powerwall's backup circuit).
