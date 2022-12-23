# ChristmasTreeWatering

Small RaspberryPi project to automate the watering of a christmas-tree, by pumping water from a reservoir to the pot of the christmas-tree, when the waterlevel inside the pot is too low. The waterlevel of the reservoir and the christmass-tree are checked regularly. A buzzer is turned on, when either water-level is below the sensors.

To measure the water-level, two cables are fixated in the tank (either the water reservoir, or the pot of the christmas-tree) and connected to the RaspberryPi. By calling `check_water_level`, the RaspberryPi checks if both cables are in the water.

Calling `water_watchdog` starts an endless loop:
1. Check if Reservoir has enough water.
1.1 if not enough water, beep when it is not night (`check_off_time`). Then wait 5 seconds so that water in reservoir is in steady state.
2. Check if Christmas-Tree-Pot has enough water.
2.1 if not enough water, pump a total of `pump_duration`-seconds.
3. Wait for 20 seconds.
4. Repeat from 1.

If after 3 times of consecutive pumping the water-level of the christmas-tree is still not high enough, then turn on an a panic-alarm, regardless of day-/night-time, since there is prob. a leakage somewhere.

## GPIO Pin Configuration

- `GPIO_tree_sensor` and `GPIO_tree_ref`: Two cables used for checking water-level for the pot where the christmas-tree sits in.
- `GPIO_reservoir_sensor` and `GPIO_reservoir_ref`: Two cables used for checking water-level for the water-reservoir.
- `GPIO_alarm`: Pin to control buzzer to make beep-sound. If alarm is off, this Pin is set to `HIGH`.
- `GPIO_pump`: Pin to control pump. If pump is off, this Pin is set to `LOW`.

## Electronics

It is recommended to use an OpAmp circuit in [buffer](https://en.wikipedia.org/wiki/Buffer_amplifier)-configuration for the `GPIO_reservoir_sensor`-Pin and `GPIO_tree_sensor`-Pin, as the internal resistance of the RaspberryPi can be too small. Furthermore, a Pull-down resisitor (eg. 68kΩ) should be used for the input-pins of the OpAmp.

Sample Circuit:
| 1                   | 2                              | 3        | 4     | 5     | 6   | 7     | 8        | 9    | 10 |
|---------------------|--------------------------------|----------|-------|-------|-----|-------|----------|------|----|
| Vcc (5V)<br>(OpAmp) | Vcc (3.3V)<br>(buzzer, relais) | Sensor 1 | Alarm | Ref 1 | GND | Ref 2 | Sensor 2 | Pump | NA |

## Usage

Configure the GPIO-pins and put script into autostart of RaspberryPi.
Set up new telegram-bot using [@botfather](https://telegram.me/BotFather) and update `TOKEN` in `main.py`.
