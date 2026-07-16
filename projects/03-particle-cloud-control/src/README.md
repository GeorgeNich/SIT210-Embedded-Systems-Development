# Particle Cloud Control Source

## Files

| File | Description |
|---|---|
| [`cloud_led_controller.ino`](cloud_led_controller.ino) | Registers `set_led` as a Particle cloud function and controls three LEDs |
| [`buddy_events.ino`](buddy_events.ino) | Subscribes to a buddy event and displays `wave` or `pat` LED patterns |

## LED Controller Commands

- `red`
- `yellow`
- `green`
- `off`

Unsupported commands return `-1`.

## Buddy Event Configuration

```cpp
constexpr char EVENT_NAME[] = "Deakin_RIOT_SIT210_Photon_Buddy";
```

Change the event name when testing in a different account or event namespace.

## Limitation

`buddy_events.ino` uses blocking delays while displaying patterns. It is retained as a clear historical example; a non-blocking state machine is preferable for firmware that must remain responsive.
