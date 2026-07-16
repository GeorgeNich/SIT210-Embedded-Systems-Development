# Particle Morse Code

A Particle firmware project that translates a text message into Morse code and signals it through the onboard LED.

## What It Demonstrates

- digital output using a Particle device;
- embedded timing with dots, dashes, letter gaps, and word gaps;
- separation of data translation from hardware signalling;
- refactoring repetitive prototype code into reusable functions.

## Hardware

- Particle Argon, Photon, or another compatible Particle device;
- onboard LED on pin `D7`.

## How It Works

1. `morseFor()` maps a character to its Morse representation.
2. `signalSymbol()` converts a dot or dash into the appropriate LED-on duration.
3. `signalCharacter()` signals one encoded character and applies the letter gap.
4. `signalMessage()` iterates through the full message and applies word spacing.
5. `loop()` repeats the configured message.

## Files

| Path | Purpose |
|---|---|
| [`src/morse_encoder.ino`](src/morse_encoder.ino) | Particle firmware implementation |
| [`src/README.md`](src/README.md) | Source-level notes and configuration points |

## Build and Run

Open `src/morse_encoder.ino` in Particle Workbench or the Particle Web IDE, select the target device, build, and flash it.

Change the message here:

```cpp
constexpr const char* MESSAGE = "GEORGE";
```

## Design Discussion

The original coursework implementation manually repeated `digitalWrite()` and `delay()` calls. The portfolio version keeps the same visible behaviour but extracts reusable translation and timing functions. This reduces duplication and makes changes less error-prone.

The current implementation is deliberately simple and blocking. A more advanced version could use `millis()` and a state machine so the device remains responsive while signalling.

## Interview Explanation

> I started with a direct LED timing solution, then refactored it so character encoding, timing rules, and hardware output were separate. It is a small project, but it demonstrates how I improve a working prototype into code that is easier to modify and reason about.

## Historical Demonstration

- https://youtu.be/_Ud_MJI_hrQ
