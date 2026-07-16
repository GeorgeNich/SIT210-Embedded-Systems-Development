# Particle Firmware - Arm and Alarm

This folder contains the Particle Argon side of the featured system.

## File

| File | Description |
|---|---|
| [`alarm_receiver.ino`](alarm_receiver.ino) | Registers the `alarm` cloud function, publishes a private event, and runs a non-blocking LED acknowledgement pattern |

## Behaviour

The cloud function accepts the argument `alert` case-insensitively. For a valid request it:

1. publishes the private event `alarm/triggered`;
2. starts an LED acknowledgement pattern;
3. returns `1` immediately.

Unsupported arguments return `-1`.

## Why the LED Pattern Is Non-Blocking

The original prototype used a sequence of delays inside the cloud function. That keeps the request handler occupied and prevents other application work. The current code stores pattern state and advances it from `loop()` using `millis()`.

## Build and Flash

1. Open `alarm_receiver.ino` in Particle Workbench or the Particle Web IDE.
2. Select the target Particle Argon and compatible Device OS version.
3. Build and flash the firmware.
4. Confirm the device is online in the Particle Console.
5. Configure the downstream event integration separately.

## Cloud Interface

- function name: `alarm`
- expected argument: `alert`
- success result: `1`
- published event: `alarm/triggered`

No access token or device identifier is stored in this folder.
