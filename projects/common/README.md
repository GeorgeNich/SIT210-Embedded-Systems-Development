# Shared Hardware-Independent Logic

This package contains pure Python functions reused by the Raspberry Pi examples.

## Files

| File | Purpose |
|---|---|
| [`logic.py`](logic.py) | Morse encoding, light-level classification, and ultrasonic time-to-distance conversion |
| [`__init__.py`](__init__.py) | Marks the directory as a Python package |

## Why It Is Separate

Keeping conversion and classification rules separate avoids duplicating them across the Raspberry Pi examples. It also keeps the hardware-facing programs focused on GPIO, sensor communication, and user interaction.
