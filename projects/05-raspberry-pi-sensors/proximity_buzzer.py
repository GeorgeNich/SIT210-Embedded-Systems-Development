#!/usr/bin/env python3
"""Ultrasonic distance measurement with PWM buzzer feedback."""

import time
import RPi.GPIO as GPIO

TRIGGER_PIN = 7
ECHO_PIN = 11
BUZZER_PIN = 15
MAX_ALERT_DISTANCE_CM = 110.0
ECHO_TIMEOUT_SECONDS = 0.03


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


def feedback_frequency(distance: float) -> float:
    """Preserve the low-frequency relationship used in the original prototype."""
    return max(1.0, 12.0 - distance / 10.0)


def main() -> None:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)

    time.sleep(2)
    pwm = GPIO.PWM(BUZZER_PIN, 100)
    pwm.start(0)

    try:
        while True:
            try:
                distance = measure_distance_cm()
                print(f"Distance: {distance:.2f} cm")
            except TimeoutError as exc:
                pwm.ChangeDutyCycle(0)
                print(f"Sensor timeout: {exc}")
                time.sleep(0.5)
                continue

            if distance <= MAX_ALERT_DISTANCE_CM:
                pwm.ChangeFrequency(feedback_frequency(distance))
                pwm.ChangeDutyCycle(50)
            else:
                pwm.ChangeDutyCycle(0)
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()
        GPIO.cleanup()


if __name__ == "__main__":
    main()
