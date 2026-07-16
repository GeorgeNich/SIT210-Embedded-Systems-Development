#!/usr/bin/env python3
"""Raspberry Pi client for the Arm and Alarm prototype."""

import os
import time
from dataclasses import dataclass

import requests
import RPi.GPIO as GPIO
from dotenv import load_dotenv

TRIGGER_PIN = 7
ECHO_PIN = 11
BUZZER_PIN = 15
RED_LED_PIN = 19
ECHO_TIMEOUT_SECONDS = 0.03
REQUIRED_CONSECUTIVE_READINGS = 3
NOTIFICATION_COOLDOWN_SECONDS = 60


@dataclass(frozen=True)
class Config:
    device_id: str
    access_token: str
    function_name: str
    alarm_distance_cm: float

    @classmethod
    def from_environment(cls) -> "Config":
        load_dotenv()
        device_id = os.getenv("PARTICLE_DEVICE_ID", "").strip()
        access_token = os.getenv("PARTICLE_ACCESS_TOKEN", "").strip()
        function_name = os.getenv("PARTICLE_FUNCTION_NAME", "alarm").strip()
        alarm_distance_cm = float(os.getenv("ALARM_DISTANCE_CM", "80"))

        if not device_id or not access_token:
            raise RuntimeError(
                "Set PARTICLE_DEVICE_ID and PARTICLE_ACCESS_TOKEN in a local .env file."
            )
        return cls(device_id, access_token, function_name, alarm_distance_cm)


def wait_for_pin(pin: int, state: int, timeout: float) -> float:
    deadline = time.monotonic() + timeout
    while GPIO.input(pin) != state:
        if time.monotonic() >= deadline:
            raise TimeoutError(f"GPIO pin {pin} did not reach state {state}")
    return time.monotonic()


def measure_distance_cm() -> float:
    GPIO.output(TRIGGER_PIN, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, GPIO.LOW)

    pulse_start = wait_for_pin(ECHO_PIN, GPIO.HIGH, ECHO_TIMEOUT_SECONDS)
    pulse_end = wait_for_pin(ECHO_PIN, GPIO.LOW, ECHO_TIMEOUT_SECONDS)
    return round((pulse_end - pulse_start) * 17150, 2)


def notify_particle(config: Config, session: requests.Session) -> None:
    url = (
        f"https://api.particle.io/v1/devices/"
        f"{config.device_id}/{config.function_name}"
    )
    response = session.post(
        url,
        headers={"Authorization": f"Bearer {config.access_token}"},
        json={"arg": "Alert"},
        timeout=15,
    )
    response.raise_for_status()
    result = response.json()
    if result.get("return_value") != 1:
        raise RuntimeError(f"Particle function rejected the request: {result}")


def local_alarm(pwm: GPIO.PWM, duration_seconds: float = 2.0) -> None:
    GPIO.output(RED_LED_PIN, GPIO.HIGH)
    pwm.ChangeFrequency(8)
    pwm.ChangeDutyCycle(50)
    time.sleep(duration_seconds)
    pwm.ChangeDutyCycle(0)
    GPIO.output(RED_LED_PIN, GPIO.LOW)


def main() -> None:
    config = Config.from_environment()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RED_LED_PIN, GPIO.OUT, initial=GPIO.LOW)

    pwm = GPIO.PWM(BUZZER_PIN, 100)
    pwm.start(0)
    session = requests.Session()
    consecutive_alert_readings = 0
    next_notification_time = 0.0

    try:
        time.sleep(2)
        while True:
            try:
                distance = measure_distance_cm()
                print(f"Distance: {distance:.2f} cm")
            except TimeoutError as exc:
                consecutive_alert_readings = 0
                print(f"Sensor timeout: {exc}")
                time.sleep(0.5)
                continue

            if distance <= config.alarm_distance_cm:
                consecutive_alert_readings += 1
            else:
                consecutive_alert_readings = 0

            should_trigger = (
                consecutive_alert_readings >= REQUIRED_CONSECUTIVE_READINGS
                and time.monotonic() >= next_notification_time
            )

            if should_trigger:
                local_alarm(pwm)
                try:
                    notify_particle(config, session)
                    print("Particle alarm function called successfully.")
                except (requests.RequestException, RuntimeError, ValueError) as exc:
                    print(f"Cloud notification failed: {exc}")
                finally:
                    next_notification_time = (
                        time.monotonic() + NOTIFICATION_COOLDOWN_SECONDS
                    )
                    consecutive_alert_readings = 0

            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        session.close()
        pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
