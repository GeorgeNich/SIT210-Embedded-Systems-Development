# Raspberry Pi Client - Arm and Alarm

This folder contains the sensing, local-feedback, and Particle API client for the featured project.

## Files

| File | Description |
|---|---|
| [`proximity_alarm.py`](proximity_alarm.py) | Ultrasonic measurement loop, local LED/buzzer alarm, trigger filtering, cooldown, and Particle API request |
| [`.env.example`](.env.example) | Configuration names and safe placeholder values |

## Wiring Assumptions

The recovered project uses physical board numbering:

| Signal | Board pin |
|---|---:|
| Ultrasonic trigger | 7 |
| Ultrasonic echo | 11 |
| Buzzer | 15 |
| Red LED | 19 |

Check the ultrasonic sensor's echo voltage before connecting it to Raspberry Pi GPIO. Use a voltage divider or level shifter when required.

## Configuration

From this directory:

```bash
cp .env.example .env
```

Set the following values in the local `.env` file:

```dotenv
PARTICLE_DEVICE_ID=your_current_device_id
PARTICLE_ACCESS_TOKEN=your_current_access_token
PARTICLE_FUNCTION_NAME=alarm
ALARM_DISTANCE_CM=80
```

The populated `.env` is ignored by Git. Do not commit it.

## Install and Run

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-rpi.txt
python3 projects/06-arm-and-alarm/raspberry_pi/proximity_alarm.py
```

## Failure Handling

- Echo waits have a fixed timeout, preventing an infinite sensor loop.
- HTTP requests have a timeout and require a successful status code.
- The returned Particle function value is validated.
- Cloud errors are reported without skipping GPIO cleanup.
- A notification cooldown limits repeated requests while an object remains nearby.

## Safe Testing Order

1. Test the LED and buzzer independently.
2. Confirm ultrasonic readings without cloud calls.
3. Confirm `.env` values are loaded locally.
4. Test the Particle function from the Particle Console.
5. Run the integrated client with a conservative distance threshold.
6. Verify the IFTTT event workflow last.

The current portfolio code has not been physically revalidated on the original hardware, so pin assignments and thresholds should be confirmed before use.
