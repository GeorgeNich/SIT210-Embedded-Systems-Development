# Particle Morse Code Source

## Files

| File | Description |
|---|---|
| [`morse_encoder.ino`](morse_encoder.ino) | Maps letters to Morse code and signals a configured message through the Particle onboard LED |

## Main Configuration

```cpp
constexpr pin_t LED_PIN = D7;
constexpr unsigned long UNIT_MS = 250;
constexpr const char* MESSAGE = "GEORGE";
```

`UNIT_MS` controls the duration of one Morse timing unit. A dash is three units, and the code builds the remaining symbol, letter, and word spacing from that base value.

## Limitation

The signalling functions use blocking delays. That is acceptable for this isolated demonstration, but a device performing other work should use non-blocking timing or a state machine.
