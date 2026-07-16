# Project Portfolio

This directory contains the technical projects selected from the original SIT210 coursework. The projects are organised by engineering concept instead of assessment number so that a reviewer can quickly understand what each one demonstrates.

## Recommended Reading Order

1. [Arm and Alarm](06-arm-and-alarm/) - the strongest end-to-end system.
2. [Raspberry Pi Sensors](05-raspberry-pi-sensors/) - sensor timing, PWM, and I2C.
3. [Particle Cloud Control](03-particle-cloud-control/) - cloud functions and events.
4. [Particle Cloud Telemetry](02-particle-cloud-telemetry/) - sensor-to-cloud data flow.
5. [Raspberry Pi GPIO GUIs](04-raspberry-pi-gpio-gui/) - user interfaces controlling hardware.
6. [Particle Morse Code](01-particle-morse-code/) - a small refactoring and timing example.

## Shared Code

The [`common`](common/) package contains hardware-independent functions used by multiple Python examples. Separating pure logic from GPIO code makes those functions easier to reuse and explain.

