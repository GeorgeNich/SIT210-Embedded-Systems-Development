# Raspberry Pi Sensor Interfaces

Two Raspberry Pi examples covering ultrasonic ranging, PWM feedback, and I2C illuminance sensing.

## What It Demonstrates

- trigger/echo timing for an ultrasonic sensor;
- conversion of round-trip pulse duration into distance;
- bounded sensor waits to prevent permanent hangs;
- PWM output that changes with measured distance;
- I2C communication with a BH1750-compatible sensor;
- conversion of raw bytes into lux;
- complete and reusable threshold classification.

## Included Examples

### Ultrasonic Proximity Feedback

The program emits a short trigger pulse, waits for the echo signal, calculates distance, and drives a buzzer with PWM when an object is inside the configured range.

### I2C Light Sensor

The program reads two bytes from a BH1750-compatible sensor at address `0x23`, converts the raw value to lux, and classifies the result into a readable light-level category.

## Files

| File | Purpose |
|---|---|
| [`proximity_buzzer.py`](proximity_buzzer.py) | Ultrasonic distance and PWM feedback |
| [`i2c_light_sensor.py`](i2c_light_sensor.py) | BH1750 I2C light reading and classification |

## Hardware Assumptions

### Ultrasonic example - physical board numbering

| Signal | Board pin |
|---|---:|
| Trigger | 7 |
| Echo | 11 |
| Buzzer | 15 |

An HC-SR04 echo output may exceed the Raspberry Pi's 3.3 V GPIO tolerance. Use an appropriate voltage divider or level shifter.

### I2C example

- I2C bus: `1`
- default sensor address: `0x23`

Enable I2C using Raspberry Pi configuration tools and confirm the address with `i2cdetect`.

## Run

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-rpi.txt
python3 projects/05-raspberry-pi-sensors/proximity_buzzer.py
python3 projects/05-raspberry-pi-sensors/i2c_light_sensor.py
```

## Engineering Discussion

The ultrasonic implementation uses timeouts because a missing echo must not trap the process forever. Measurements can still be noisy, so a stronger system would use median filtering, sensor validity bounds, and calibrated thresholds.

The light classifier is stored in shared pure Python logic, making its boundaries explicit without mixing them into the sensor loop.

## Interview Explanation

> I worked with two different sensor interfaces: pulse timing through GPIO and address-based communication over I2C. I also considered electrical compatibility, noisy data, failure timeouts, and how to isolate conversion logic from the hardware loop.

## Historical Demonstrations

- Ultrasonic PWM: https://youtu.be/qI7bM3z5rCc
- I2C light sensor: https://youtu.be/Vd7Kszche2s
