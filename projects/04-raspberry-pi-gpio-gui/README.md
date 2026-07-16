# Raspberry Pi GPIO GUIs

Two Python/Tkinter applications that connect desktop controls to Raspberry Pi GPIO outputs.

## What It Demonstrates

- event-driven desktop interfaces;
- physical LED control through `gpiozero`;
- mapping user selections to mutually exclusive hardware states;
- separating Morse translation from hardware output;
- moving long-running output work away from the Tkinter event loop;
- cleaning up hardware resources when the window closes.

## Included Applications

### LED Status Controller

Radio buttons select a red, green, or blue LED. The program turns every output off before activating the selected LED, preventing conflicting states.

### Morse GUI

A text field accepts a short message, validates its characters, encodes it as Morse code, and signals it through an LED. The signalling task runs in a background thread so the Tkinter interface does not freeze for the full message duration.

## Files

| File | Purpose |
|---|---|
| [`led_control_gui.py`](led_control_gui.py) | Three-colour LED selection interface |
| [`morse_gui.py`](morse_gui.py) | Text-to-Morse LED interface |

## Hardware Assumptions

The examples use BCM pin numbering:

| Output | BCM pin |
|---|---:|
| Blue LED | 17 |
| Red LED | 27 |
| Green/Morse LED | 23 |

Use appropriate current-limiting resistors and verify wiring before running the programs.

## Run

From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-rpi.txt
python3 projects/04-raspberry-pi-gpio-gui/led_control_gui.py
python3 projects/04-raspberry-pi-gpio-gui/morse_gui.py
```

A graphical desktop session is required for Tkinter.

## Engineering Discussion

Tkinter owns the main event loop. Performing a long Morse sequence directly in a button callback would freeze redraws and user input. The portfolio version moves signalling to a worker thread. A more complete design would also add cancellation, progress feedback, and strict coordination around repeated button presses.

## Interview Explanation

> These programs demonstrate that embedded work is not only low-level GPIO. I connected a user-facing event-driven interface to physical outputs, handled cleanup, and separated reusable encoding logic from hardware-specific code.

## Historical Demonstrations

- LED GUI: https://www.youtube.com/watch?v=p-s5vkAsAfM
- Morse GUI: https://www.youtube.com/watch?v=vVvA213wKZs
